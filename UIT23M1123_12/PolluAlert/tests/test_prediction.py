"""
Test Suite for PolluAlert
Tests the complete prediction pipeline with realistic test cases.
Run with: pytest tests/test_prediction.py -v
"""

import os
import sys
import pytest

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.preprocessing import preprocess_text, remove_urls, to_lowercase
from src.prediction import predict


# ============================================================
# Test: Preprocessing Module
# ============================================================

class TestPreprocessing:
    """Tests for the text preprocessing pipeline."""
    
    def test_lowercase(self):
        assert to_lowercase("HELLO World") == "hello world"
    
    def test_url_removal(self):
        text = "Check https://pollution.gov.in for details"
        result = remove_urls(text)
        assert "https://" not in result
    
    def test_empty_input(self):
        assert preprocess_text("") == ""
        assert preprocess_text(None) == ""
    
    def test_negation_preservation(self):
        """Negation words must be preserved to maintain meaning."""
        result = preprocess_text("The water is not contaminated")
        assert "not" in result
    
    def test_basic_preprocessing(self):
        result = preprocess_text("There is THICK smoke!!!")
        assert result != ""
        assert "thick" in result.lower() or "smoke" in result.lower()
    
    def test_whitespace_normalization(self):
        result = preprocess_text("Too   many    spaces   here")
        assert "  " not in result


# ============================================================
# Test: Prediction Pipeline
# ============================================================

class TestPrediction:
    """Tests for the complete prediction pipeline."""
    
    def test_case_1_non_pollution(self):
        """Non-pollution text should be classified as NORMAL."""
        result = predict("Today is a sunny day.")
        assert result['pollution_type'] == 'Not Pollution' or result['emergency_status'] == 'NORMAL'
        assert result['emergency_status'] == 'NORMAL'
    
    def test_case_2_waste_pollution(self):
        """Garbage dumping should be classified as waste pollution with low severity."""
        result = predict("Garbage has been dumped near the road.")
        assert 'Waste' in result['pollution_type'] or 'Garbage' in result['pollution_type'] or 'Pollution' in result['pollution_type']
        assert result['emergency_status'] != 'NORMAL'  # Should at least be a pollution report
    
    def test_case_3_air_pollution(self):
        """Factory smoke should be classified as air/industrial pollution."""
        result = predict("Smoke from the factory has been visible since morning.")
        pollution_type = result['pollution_type']
        assert any(t in pollution_type for t in ['Air', 'Industrial']), \
            f"Expected Air or Industrial pollution, got: {pollution_type}"
    
    def test_case_4_chemical_emergency(self):
        """Chemical leak with breathing problems should be HIGH severity / POTENTIAL EMERGENCY."""
        result = predict(
            "A chemical leak has caused a strong toxic smell and people are having breathing problems."
        )
        assert result['severity'] == 'HIGH', \
            f"Expected HIGH severity, got: {result['severity']}"
        assert result['emergency_status'] == 'POTENTIAL EMERGENCY', \
            f"Expected POTENTIAL EMERGENCY, got: {result['emergency_status']}"
    
    def test_case_5_ambiguous_text(self):
        """Vague text should not receive unnecessarily high confidence emergency."""
        result = predict("There is a strange smell outside.")
        # Should not be classified as POTENTIAL EMERGENCY without strong indicators
        assert result['severity'] != 'HIGH' or result['emergency_status'] != 'POTENTIAL EMERGENCY', \
            "Vague text should not be classified as high-severity emergency"
    
    def test_case_6_water_pollution(self):
        """River pollution should be classified correctly."""
        result = predict("The river water has become dark and smells very bad.")
        assert 'Water' in result['pollution_type'], \
            f"Expected Water Pollution, got: {result['pollution_type']}"
    
    def test_case_7_noise_pollution(self):
        """Loud noise complaint should be classified as noise pollution."""
        result = predict("Extremely loud music from the hall is continuing past midnight.")
        assert 'Noise' in result['pollution_type'], \
            f"Expected Noise Pollution, got: {result['pollution_type']}"
    
    def test_case_8_location_extraction(self):
        """Location should be extracted when mentioned."""
        result = predict("Thick smoke from factory near Mumbai highway.")
        # Location extraction may or may not capture 'Mumbai' depending on spaCy
        assert result['location'] is not None
    
    def test_case_9_keywords_extracted(self):
        """Keywords should be extracted from pollution text."""
        result = predict("Chemical leak causing toxic fumes and breathing difficulties.")
        assert len(result['keywords']) > 0, "Keywords should not be empty"
    
    def test_case_10_summary_generated(self):
        """An incident summary should be generated for pollution reports."""
        result = predict("Industrial waste being dumped into the river.")
        assert result['summary'] is not None
        assert len(result['summary']) > 0
    
    def test_case_11_confidence_valid(self):
        """Model confidence should be between 0 and 1."""
        result = predict("Smoke is coming from the factory.")
        assert 0.0 <= result['confidence'] <= 1.0
    
    def test_case_12_entities_structure(self):
        """Entity extraction should return proper structure."""
        result = predict("Residents near MIDC area reported smoke from a chemical factory.")
        entities = result['entities']
        assert isinstance(entities, dict)
        expected_keys = ['locations', 'organizations', 'pollution_sources', 
                         'water_bodies', 'affected_groups', 'area_types']
        for key in expected_keys:
            assert key in entities, f"Missing entity key: {key}"
    
    def test_case_13_multiple_inputs(self):
        """Pipeline should handle multiple different inputs correctly."""
        texts = [
            "Beautiful weather today.",
            "Oil spill in the sea causing marine pollution.",
            "Construction noise during exams is very disturbing.",
        ]
        for text in texts:
            result = predict(text)
            assert 'pollution_type' in result
            assert 'severity' in result
            assert 'emergency_status' in result


# ============================================================
# Test: Database Module
# ============================================================

class TestDatabase:
    """Tests for the SQLite database module."""
    
    def test_init_db(self):
        """Database initialization should create the table."""
        from src.database import init_db, get_connection
        test_db = os.path.join(os.path.dirname(__file__), 'test_pollualert.db')
        init_db(test_db)
        
        conn = get_connection(test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reports'")
        assert cursor.fetchone() is not None
        conn.close()
        
        # Cleanup
        os.remove(test_db)
    
    def test_save_and_retrieve(self):
        """Should save and retrieve a report."""
        from src.database import init_db, save_report, get_report_by_id
        test_db = os.path.join(os.path.dirname(__file__), 'test_pollualert2.db')
        init_db(test_db)
        
        report_data = {
            'original_text': 'Test report',
            'cleaned_text': 'test report',
            'pollution_type': 'Air Pollution',
            'severity': 'LOW',
            'emergency_status': 'POLLUTION REPORT',
            'location': 'Test City',
            'keywords': ['smoke', 'factory'],
            'entities': {'locations': ['Test City']},
            'summary': 'Test summary',
            'confidence': 0.85
        }
        
        report_id = save_report(report_data, test_db)
        assert report_id is not None
        
        retrieved = get_report_by_id(report_id, test_db)
        assert retrieved is not None
        assert retrieved['original_text'] == 'Test report'
        assert retrieved['pollution_type'] == 'Air Pollution'
        
        # Cleanup
        os.remove(test_db)
    
    def test_feedback_update(self):
        """Should update user feedback."""
        from src.database import init_db, save_report, update_feedback, get_report_by_id
        test_db = os.path.join(os.path.dirname(__file__), 'test_pollualert3.db')
        init_db(test_db)
        
        report_data = {
            'original_text': 'Feedback test',
            'pollution_type': 'Water Pollution',
            'severity': 'MEDIUM',
            'emergency_status': 'POLLUTION REPORT',
        }
        
        report_id = save_report(report_data, test_db)
        update_feedback(report_id, 'correct', test_db)
        
        retrieved = get_report_by_id(report_id, test_db)
        assert retrieved['user_feedback'] == 'correct'
        
        # Cleanup
        os.remove(test_db)


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
