"""
PolluAlert - Streamlit Web Application
NLP-Based Pollution Emergency Detection and Alert System

Pages:
    1. Home - Project overview and description
    2. Pollution Analysis - Text input and analysis results
    3. Analytics Dashboard - Report statistics and model performance
"""

import os
import sys
import json
from html import escape
import sqlite3
import streamlit as st
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.prediction import predict, load_models
from src.database import init_db, save_report, get_all_reports, get_report_stats, update_feedback
from src.preprocessing import preprocess_text
from src.entity_extraction import get_entity_extraction_mode

# Initialize database
init_db()

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="PolluAlert - Pollution Emergency Detection",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Custom CSS
# ============================================================
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a5276;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #2ecc71;
        margin-bottom: 1.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Result cards */
    .result-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border-left: 4px solid #3498db;
    }
    .result-card h4 {
        margin: 0 0 0.5rem 0;
        color: #2c3e50;
    }
    
    /* Severity badges */
    .severity-low {
        background: #d4edda;
        color: #155724;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    .severity-medium {
        background: #fff3cd;
        color: #856404;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    .severity-high {
        background: #f8d7da;
        color: #721c24;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    .severity-none {
        background: #e2e3e5;
        color: #383d41;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Emergency badges */
    .emergency-normal {
        background: #d4edda;
        color: #155724;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
    }
    .emergency-report {
        background: #fff3cd;
        color: #856404;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
    }
    .emergency-emergency {
        background: #f8d7da;
        color: #721c24;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(220, 53, 69, 0); }
        100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); }
    }
    
    /* Keyword tags */
    .keyword-tag {
        background: #e8f4fd;
        color: #1a5276;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        margin: 0.15rem;
        display: inline-block;
        font-size: 0.85rem;
        border: 1px solid #bee5eb;
    }
    
    /* Summary box */
    .summary-box {
        background: #f0f7ff;
        border: 1px solid #b8daff;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    
    /* Disclaimer */
    .disclaimer {
        background: #fff8e1;
        border: 1px solid #ffe082;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.85rem;
        color: #6d4c00;
        margin: 1rem 0;
    }
    
    /* Info box */
    .info-box {
        background: #e8f5e9;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #f0f4f8;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================================
# Sidebar Navigation
# ============================================================
with st.sidebar:
    st.markdown("## 🌍 PolluAlert")
    st.markdown("*NLP-Based Pollution Detection*")
    st.markdown("---")
    
    page = st.radio(
        "Navigate",
        ["Home", "Pollution Analysis", "Analytics Dashboard"],
        index=0,
        label_visibility="collapsed",
        key="page"
    )
    
    st.markdown("---")
    st.markdown("""
    **Technology Stack:**
    - Python + NLTK + Scikit-learn
    - TF-IDF + ML Classifiers
    - Streamlit + SQLite
    """)
    st.markdown("---")
    st.caption("Academic Mini Project | NLP")
    st.caption(f"Entity extraction: {get_entity_extraction_mode()}")


# ============================================================
# Page: Home
# ============================================================
def open_analysis():
    st.session_state['page'] = 'Pollution Analysis'


def page_home():
    st.markdown('<div class="main-header">PolluAlert</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">NLP-Based Pollution Emergency Detection and Alert System</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### About the Project")
        st.markdown("""
        **PolluAlert** is a Natural Language Processing (NLP) system that analyses textual 
        pollution complaints, incident reports, and citizen observations. The system uses 
        machine learning to identify:
        
        - **Pollution Type** (Air, Water, Soil, Noise, Industrial, Chemical, Waste, Other)
        - **Severity Level** (Low, Medium, High)
        - **Emergency Status** (Normal, Pollution Report, Potential Emergency)
        - **Location and Entities** from the text
        - **Key Indicators** that support the classification
        """)
        
        st.markdown("### How It Works")
        st.markdown("""
        1. Enter a pollution-related text description
        2. The system preprocesses and analyses the text using NLP
        3. TF-IDF features are extracted from the text
        4. Trained ML classifiers predict pollution type, severity, and emergency status
        5. Entity extraction identifies locations and relevant entities
        6. A structured incident summary is generated
        """)
    
    with col2:
        st.markdown("### Supported Pollution Categories")
        categories = {
            "Air Pollution": "Smoke, emissions, smog, exhaust fumes",
            "Water Pollution": "Contamination, sewage, chemical discharge",
            "Soil/Land Pollution": "Waste dumping, chemical seepage, contamination",
            "Noise Pollution": "Industrial noise, construction, excessive sound",
            "Industrial Pollution": "Factory emissions, industrial waste, effluent",
            "Waste/Garbage Pollution": "Illegal dumping, garbage, solid waste",
            "Chemical Pollution": "Chemical leaks, spills, toxic substances",
            "Other/Unknown": "Unidentified pollution sources",
        }
        
        for cat, desc in categories.items():
            st.markdown(f"**{cat}**: {desc}")
        
        st.markdown("### NLP Pipeline")
        st.markdown("""
        ```
        Text Input
           |-> Text Cleaning
           |-> Tokenization
           |-> Stop-word Removal (Negation-Aware)
           |-> Lemmatization
           |-> TF-IDF Feature Extraction
           |-> ML Classification
           |-> Severity / Emergency Detection
           |-> Entity & Location Extraction
           |-> Summary Generation
           |-> Database Storage
        ```
        """)
    
    st.markdown("---")
    
    st.markdown('<div class="disclaimer">'
                '<strong>Important Disclaimer:</strong> PolluAlert is a preliminary text-based '
                'screening tool developed as an academic NLP project. It does NOT replace '
                'environmental monitoring equipment, pollution sensors, medical professionals, '
                'emergency services, or government authorities. All classifications are '
                'NLP-based preliminary assessments and should be verified by appropriate authorities.'
                '</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.button("Start Analysis", type="primary", use_container_width=True,
              on_click=open_analysis)


# ============================================================
# Page: Pollution Analysis
# ============================================================
def page_analysis():
    st.markdown('<div class="main-header">Pollution Incident Analysis</div>', unsafe_allow_html=True)
    
    # Load models
    try:
        load_models()
    except FileNotFoundError:
        st.error("Models not found. Please run `python src/train_model.py` first.")
        return
    
    # Text input
    st.markdown("### Enter Pollution Incident / Report")
    
    # Example texts for quick testing
    example_texts = [
        "-- Select an example or type your own --",
        "There is thick black smoke coming from a factory near the highway.",
        "A strong chemical smell is spreading around the residential area.",
        "The river water has become dark and smells very bad.",
        "A large amount of garbage has been dumped near the school.",
        "People living near the factory are complaining about smoke.",
        "A chemical leak has caused a toxic smell and people are having breathing problems.",
        "There is a strange smell near the river.",
        "Today is a sunny day and the weather is pleasant.",
        "Extremely loud noise from the construction site at 2 AM.",
    ]
    
    def use_example():
        selected = st.session_state['example']
        st.session_state['incident_text'] = '' if selected == example_texts[0] else selected

    st.selectbox("Quick Examples:", example_texts, key="example",
                 on_change=use_example)
    input_text = st.text_area(
        "Describe the pollution incident:", key="incident_text", height=120,
        max_chars=5000,
        placeholder="Describe what happened, where it happened, and who was affected."
    )
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        analyze_btn = st.button("Analyze Incident", type="primary", use_container_width=True)
    
    if analyze_btn:
        if not input_text.strip() or not preprocess_text(input_text).strip():
            st.warning("Please enter a meaningful description, not just numbers or punctuation.")
        else:
            try:
                with st.spinner("Analysing text..."):
                    result = predict(input_text.strip())
            except ValueError as exc:
                st.warning(str(exc))
            else:
                # Save only on a new analysis, never on a feedback/download rerun.
                st.session_state['last_result'] = result
                st.session_state['last_report_id'] = None
                st.session_state['last_feedback'] = None
                try:
                    st.session_state['last_report_id'] = save_report(result)
                except sqlite3.Error:
                    st.warning("Analysis completed, but the report could not be saved. Check database access.")

    result = st.session_state.get('last_result')
    if result:
        report_id = st.session_state.get('last_report_id')
        if input_text.strip() != result['original_text']:
            st.info("Showing the previous analysis. Click Analyze Incident to analyse the edited text.")
        st.markdown("---")
        st.markdown("### Analysis Results")
        st.caption(f"Analysed text: {result['original_text']}")
        if report_id is not None:
            st.caption(f"Saved report #{report_id}")
        
        # Emergency status banner
        emergency = result['emergency_status']
        if emergency == 'POTENTIAL EMERGENCY':
            st.markdown(f'<div class="emergency-emergency">POTENTIAL EMERGENCY</div>', 
                       unsafe_allow_html=True)
        elif emergency == 'POLLUTION REPORT':
            st.markdown(f'<div class="emergency-report">POLLUTION REPORT</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="emergency-normal">NORMAL</div>', 
                       unsafe_allow_html=True)
        
        st.markdown("")
        
        # Results in columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Pollution Type
            st.markdown(f"**Pollution Type:** {result['pollution_type']}")
            
            # Severity with color
            severity = result['severity']
            severity_class = {
                'LOW': 'severity-low', 'MEDIUM': 'severity-medium',
                'HIGH': 'severity-high', 'NONE': 'severity-none'
            }.get(severity, 'severity-none')
            st.markdown(f'**Severity:** <span class="{severity_class}">{severity}</span>', 
                       unsafe_allow_html=True)
            
            # Location
            st.markdown(f"**Location:** {result['location']}")
            
            # Confidence
            confidence = result['confidence']
            st.markdown(f"**Pollution Type Confidence:** {confidence:.1%}")
            st.caption("Model score for the pollution category; not a measure of real-world danger.")
            if confidence < 0.5:
                st.info("The category score is below 50%. Review the result and add more detail if needed.")
        
        with col2:
            # Keywords
            if result['keywords']:
                keywords_html = ' '.join(
                    [f'<span class="keyword-tag">{escape(kw)}</span>' for kw in result['keywords'][:8]]
                )
                st.markdown(f"**Keywords:** {keywords_html}", unsafe_allow_html=True)
            
            # Entities
            entities = result['entities']
            entity_parts = []
            if entities.get('locations'):
                entity_parts.append(f"Locations: {', '.join(entities['locations'])}")
            if entities.get('pollution_sources'):
                entity_parts.append(f"Sources: {', '.join(entities['pollution_sources'])}")
            if entities.get('affected_groups'):
                entity_parts.append(f"Affected: {', '.join(entities['affected_groups'])}")
            if entities.get('water_bodies'):
                entity_parts.append(f"Water Bodies: {', '.join(entities['water_bodies'])}")
            if entities.get('area_types'):
                entity_parts.append(f"Area: {', '.join(entities['area_types'])}")
            
            if entity_parts:
                st.markdown("**Extracted Entities:**")
                for ep in entity_parts:
                    st.markdown(f"- {ep}")
            else:
                st.markdown("**Extracted Entities:** None identified")
        
        # Summary
        st.markdown("---")
        st.markdown("### Incident Summary")
        st.markdown(f'<div class="summary-box">{escape(result["summary"])}</div>', unsafe_allow_html=True)
        st.download_button(
            "Download Analysis (.json)",
            data=json.dumps(result, indent=2, ensure_ascii=False),
            file_name=f"pollualert-report-{report_id or 'unsaved'}.json",
            mime="application/json"
        )
        
        # Suggested Action
        st.markdown("### Suggested Action")
        if emergency == 'POTENTIAL EMERGENCY':
            st.error(result['suggested_action'])
        elif emergency == 'POLLUTION REPORT':
            st.warning(result['suggested_action'])
        else:
            st.info(result['suggested_action'])
        
        # Explanation
        with st.expander("View Classification Explanation"):
            st.markdown("**Text after preprocessing:**")
            st.code(result['cleaned_text'], language=None)
            st.markdown(f"**Severity Explanation:** {result['severity_explanation']}")
            st.markdown(f"**Emergency Explanation:** {result['emergency_explanation']}")
            if result['indicators']:
                st.markdown(f"**Emergency Indicators Found:** {', '.join(result['indicators'])}")
        
        # Human Feedback
        st.markdown("---")
        st.markdown("### Was this classification useful?")
        st.caption("Feedback is saved for later review; it does not automatically retrain the model.")
        
        col_fb1, col_fb2, col_fb3 = st.columns([1, 1, 3])
        with col_fb1:
            if st.button("Correct", type="primary", use_container_width=True, disabled=report_id is None):
                update_feedback(report_id, 'correct')
                st.session_state['last_feedback'] = 'correct'
        with col_fb2:
            if st.button("Incorrect", use_container_width=True, disabled=report_id is None):
                update_feedback(report_id, 'incorrect')
                st.session_state['last_feedback'] = 'incorrect'
        if st.session_state.get('last_feedback'):
            st.success(f"Feedback saved: {st.session_state['last_feedback']}")
        
        st.markdown('<div class="disclaimer">'
                    'Note: All classifications are NLP-based preliminary assessments. '
                    'This tool does not replace environmental monitoring equipment or professional assessment.'
                    '</div>', unsafe_allow_html=True)
    

# ============================================================
# Page: Analytics Dashboard
# ============================================================
def page_analytics():
    st.markdown('<div class="main-header">Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Load stats
    stats = get_report_stats()
    reports = get_all_reports(limit=500)
    
    if stats['total_reports'] == 0:
        st.info("No reports have been analysed yet. Go to **Pollution Analysis** to submit your first report.")
        
        # Still show model performance
        st.markdown("---")
        show_model_performance()
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reports", stats['total_reports'])
    
    with col2:
        emergency_count = stats['emergency_distribution'].get('POTENTIAL EMERGENCY', 0)
        st.metric("Emergency Reports", emergency_count)
    
    with col3:
        pollution_count = stats['emergency_distribution'].get('POLLUTION REPORT', 0)
        st.metric("Pollution Reports", pollution_count)
    
    with col4:
        normal_count = stats['emergency_distribution'].get('NORMAL', 0)
        st.metric("Normal Reports", normal_count)
    
    st.markdown("---")
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### Pollution Category Distribution")
        if stats['pollution_type_distribution']:
            df_types = pd.DataFrame(
                list(stats['pollution_type_distribution'].items()),
                columns=['Pollution Type', 'Count']
            )
            st.bar_chart(df_types.set_index('Pollution Type'))
    
    with col_chart2:
        st.markdown("#### Severity Distribution")
        if stats['severity_distribution']:
            df_sev = pd.DataFrame(
                list(stats['severity_distribution'].items()),
                columns=['Severity', 'Count']
            )
            st.bar_chart(df_sev.set_index('Severity'))
    
    # Emergency distribution
    st.markdown("#### Emergency Status Distribution")
    if stats['emergency_distribution']:
        df_em = pd.DataFrame(
            list(stats['emergency_distribution'].items()),
            columns=['Status', 'Count']
        )
        st.bar_chart(df_em.set_index('Status'))
    
    # Feedback stats
    if stats.get('feedback_distribution'):
        st.markdown("#### User Feedback")
        df_fb = pd.DataFrame(
            list(stats['feedback_distribution'].items()),
            columns=['Feedback', 'Count']
        )
        st.dataframe(df_fb, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Recent reports table
    st.markdown("#### Recent Reports")
    if reports:
        display_data = []
        for r in reports[:20]:
            display_data.append({
                'ID': r['report_id'],
                'Text': r['original_text'][:80] + '...' if len(r['original_text']) > 80 else r['original_text'],
                'Type': r['pollution_type'],
                'Severity': r['severity'],
                'Emergency': r['emergency_status'],
                'Location': r['location'],
                'Feedback': r.get('user_feedback', '-'),
                'Time': r['created_at']
            })
        df_reports = pd.DataFrame(display_data)
        st.dataframe(df_reports, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Model performance
    show_model_performance()


def show_model_performance():
    """Display model performance metrics."""
    st.markdown("#### Model Performance")
    
    eval_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'evaluation_results.json')
    if os.path.exists(eval_path):
        with open(eval_path, 'r') as f:
            eval_results = json.load(f)
        
        st.markdown(f"**Dataset:** {eval_results['dataset_info']['total_records']} records | "
                    f"**Split:** {eval_results['dataset_info']['train_test_split']} train/test")
        st.caption("Academic dataset results for the ML classifiers. Keyword rules are applied separately during analysis.")
        st.caption(eval_results['dataset_info'].get('model_selection', ''))
        
        for task_name, task_results in eval_results['results'].items():
            st.markdown(f"##### {task_name} Classification")
            
            best_model = eval_results['best_models'].get(
                {'Emergency Status': 'emergency'}.get(task_name, task_name.lower().replace(' ', '_')), 'N/A'
            )
            
            rows = []
            for model_name, metrics in task_results.items():
                is_best = " *" if model_name == best_model else ""
                rows.append({
                    'Model': model_name + is_best,
                    'Training CV F1': f"{metrics['cv_f1_score']:.4f}" if 'cv_f1_score' in metrics else 'N/A',
                    'Accuracy': f"{metrics['accuracy']:.4f}",
                    'Precision': f"{metrics['precision']:.4f}",
                    'Recall': f"{metrics['recall']:.4f}",
                    'F1-Score': f"{metrics['f1_score']:.4f}"
                })
            
            df_perf = pd.DataFrame(rows)
            st.dataframe(df_perf, use_container_width=True, hide_index=True)
            st.caption(f"* = Selected best model for {task_name}")
    else:
        st.info("Model evaluation results not available. Run training first.")


# ============================================================
# Navigation Logic
# ============================================================
if page == "Home":
    page_home()
elif page == "Pollution Analysis":
    page_analysis()
elif page == "Analytics Dashboard":
    page_analytics()
