"""
Database Module for PolluAlert
Handles SQLite database operations for storing and retrieving pollution reports.
"""

import os
import sqlite3
import json
from datetime import datetime

# Default database path
DEFAULT_DB_PATH = os.environ.get('POLLUALERT_DB_PATH') or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'pollualert.db'
)


def get_connection(db_path=None):
    """Get a SQLite database connection."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    """
    Initialize the database and create the reports table if it doesn't exist.
    
    Schema:
        report_id       - Auto-increment primary key
        original_text   - The raw input text
        cleaned_text    - Preprocessed text
        pollution_type  - Classified pollution category
        severity        - LOW / MEDIUM / HIGH / NONE
        emergency_status - NORMAL / POLLUTION REPORT / POTENTIAL EMERGENCY
        location        - Extracted location or 'Not identified'
        keywords        - Extracted keywords (JSON list)
        entities        - Extracted entities (JSON dict)
        summary         - Generated incident summary
        confidence      - Model confidence score
        user_feedback   - User feedback (correct / incorrect / NULL)
        created_at      - Timestamp of report creation
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT NOT NULL,
            cleaned_text TEXT,
            pollution_type TEXT,
            severity TEXT,
            emergency_status TEXT,
            location TEXT,
            keywords TEXT,
            entities TEXT,
            summary TEXT,
            confidence REAL,
            user_feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {db_path or DEFAULT_DB_PATH}")


def save_report(report_data, db_path=None):
    """
    Save a pollution analysis report to the database.
    
    Parameters:
        report_data (dict): Dictionary containing report fields
        db_path (str, optional): Database file path
    
    Returns:
        int: The report_id of the saved record
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Convert lists/dicts to JSON strings
    keywords = report_data.get('keywords', [])
    if isinstance(keywords, list):
        keywords = json.dumps(keywords)
    
    entities = report_data.get('entities', {})
    if isinstance(entities, dict):
        entities = json.dumps(entities)
    
    cursor.execute('''
        INSERT INTO reports (
            original_text, cleaned_text, pollution_type, severity,
            emergency_status, location, keywords, entities, summary,
            confidence, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        report_data.get('original_text', ''),
        report_data.get('cleaned_text', ''),
        report_data.get('pollution_type', ''),
        report_data.get('severity', ''),
        report_data.get('emergency_status', ''),
        report_data.get('location', 'Not identified'),
        keywords,
        entities,
        report_data.get('summary', ''),
        report_data.get('confidence', 0.0),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return report_id


def get_all_reports(db_path=None, limit=100):
    """
    Retrieve all reports from the database.
    
    Returns:
        list of dict: List of report records
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM reports ORDER BY created_at DESC, report_id DESC LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    reports = []
    for row in rows:
        report = dict(row)
        # Parse JSON fields
        try:
            report['keywords'] = json.loads(report.get('keywords', '[]'))
        except (json.JSONDecodeError, TypeError):
            report['keywords'] = []
        try:
            report['entities'] = json.loads(report.get('entities', '{}'))
        except (json.JSONDecodeError, TypeError):
            report['entities'] = {}
        reports.append(report)
    
    return reports


def get_report_by_id(report_id, db_path=None):
    """Retrieve a single report by ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM reports WHERE report_id = ?', (report_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        report = dict(row)
        try:
            report['keywords'] = json.loads(report.get('keywords', '[]'))
        except (json.JSONDecodeError, TypeError):
            report['keywords'] = []
        try:
            report['entities'] = json.loads(report.get('entities', '{}'))
        except (json.JSONDecodeError, TypeError):
            report['entities'] = {}
        return report
    return None


def update_feedback(report_id, feedback, db_path=None):
    """
    Update user feedback for a report.
    
    Parameters:
        report_id (int): Report ID
        feedback (str): 'correct' or 'incorrect'
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE reports SET user_feedback = ? WHERE report_id = ?
    ''', (feedback, report_id))
    
    conn.commit()
    conn.close()


def get_report_stats(db_path=None):
    """
    Get aggregate statistics from the reports table.
    
    Returns:
        dict: Statistics including counts, distributions, etc.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    stats = {}
    
    # Total reports
    cursor.execute('SELECT COUNT(*) FROM reports')
    stats['total_reports'] = cursor.fetchone()[0]
    
    # Pollution type distribution
    cursor.execute('''
        SELECT pollution_type, COUNT(*) as count 
        FROM reports 
        GROUP BY pollution_type 
        ORDER BY count DESC
    ''')
    stats['pollution_type_distribution'] = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Severity distribution
    cursor.execute('''
        SELECT severity, COUNT(*) as count 
        FROM reports 
        GROUP BY severity 
        ORDER BY count DESC
    ''')
    stats['severity_distribution'] = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Emergency status distribution
    cursor.execute('''
        SELECT emergency_status, COUNT(*) as count 
        FROM reports 
        GROUP BY emergency_status 
        ORDER BY count DESC
    ''')
    stats['emergency_distribution'] = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Feedback stats
    cursor.execute('''
        SELECT user_feedback, COUNT(*) as count 
        FROM reports 
        WHERE user_feedback IS NOT NULL 
        GROUP BY user_feedback
    ''')
    stats['feedback_distribution'] = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Recent reports count (last 24 hours)
    cursor.execute('''
        SELECT COUNT(*) FROM reports 
        WHERE created_at >= datetime('now', '-1 day')
    ''')
    stats['recent_reports'] = cursor.fetchone()[0]
    
    conn.close()
    return stats


def get_report_count(db_path=None):
    """Get total number of reports."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM reports')
    count = cursor.fetchone()[0]
    conn.close()
    return count


# === Initialization ===
if __name__ == "__main__":
    init_db()
    print("\nDatabase ready.")
    
    # Test save and retrieve
    test_report = {
        'original_text': 'Test pollution report - thick smoke from factory.',
        'cleaned_text': 'test pollution report thick smoke factory',
        'pollution_type': 'Air Pollution',
        'severity': 'MEDIUM',
        'emergency_status': 'POLLUTION REPORT',
        'location': 'Not identified',
        'keywords': ['smoke', 'factory', 'thick smoke'],
        'entities': {'pollution_sources': ['factory']},
        'summary': 'Test incident summary.',
        'confidence': 0.85
    }
    
    report_id = save_report(test_report)
    print(f"Saved test report with ID: {report_id}")
    
    retrieved = get_report_by_id(report_id)
    print(f"Retrieved: {retrieved['original_text']}")
    
    stats = get_report_stats()
    print(f"Total reports: {stats['total_reports']}")
