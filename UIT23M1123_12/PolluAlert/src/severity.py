"""
Severity and Emergency Classification Module for PolluAlert
Combines ML-based classification with rule-based boosting for severity and emergency detection.

The ML classifier provides the primary prediction.
Rule-based logic provides a safety net for critical keywords that indicate danger.
"""

import re

# High-severity indicator keywords
# These terms suggest potentially serious pollution incidents
HIGH_SEVERITY_KEYWORDS = [
    'chemical leak', 'toxic', 'poisonous', 'hazardous', 'radioactive',
    'breathing problems', 'breathing difficulties', 'respiratory',
    'difficulty breathing', 'suffocating', 'suffocation',
    'hospitalized', 'hospitalised', 'hospital', 'illness', 'sick',
    'unconscious', 'collapsed', 'collapse',
    'explosion', 'exploded', 'fire', 'burning',
    'gas leak', 'gas leakage', 'chlorine', 'ammonia', 'cyanide', 'mercury',
    'contaminated water supply', 'drinking water contaminated',
    'mass evacuation', 'evacuated', 'evacuation',
    'death', 'died', 'fatal', 'killed',
    'emergency', 'urgent', 'critical', 'severe',
    'toxic fumes', 'toxic smoke', 'toxic cloud', 'toxic gas',
    'oil spill', 'acid spill', 'chemical spill',
    'skin burns', 'skin rashes', 'burns',
    'hearing loss', 'hearing damage',
    'children ill', 'children sick', 'people ill',
]

# Medium-severity indicator keywords
MEDIUM_SEVERITY_KEYWORDS = [
    'thick smoke', 'dense smoke', 'black smoke',
    'foul smell', 'strong smell', 'chemical smell', 'bad smell',
    'dead fish', 'fish dying',
    'untreated waste', 'untreated effluent',
    'illegal dumping', 'illegal dump',
    'water changed colour', 'water discoloured', 'dark water',
    'sewage', 'sewage overflow',
    'emission', 'emissions',
    'noise complaints', 'unbearable noise', 'loud noise',
    'health hazard', 'hygiene issues',
    'piling up', 'accumulating',
    'crop damage', 'crops dying',
    'visibility issues', 'smog',
]

# Emergency indicator keywords
EMERGENCY_KEYWORDS = [
    'chemical leak', 'gas leak', 'toxic', 'explosion',
    'breathing problems', 'breathing difficulties', 'difficulty breathing',
    'hospitalized', 'hospitalised', 'unconscious', 'collapsed',
    'mass evacuation', 'evacuation', 'emergency',
    'people ill', 'people sick', 'children ill', 'children sick',
    'toxic fumes', 'toxic smoke', 'toxic cloud', 'toxic gas',
    'oil spill', 'acid spill', 'chemical spill',
    'skin burns', 'burns', 'hearing loss',
    'contaminated water supply', 'contaminated drinking water',
    'fire', 'burning', 'hazardous',
    'dying', 'death', 'fatal',
    'suffocating', 'nausea', 'dizziness',
]


def matched_indicators(text, keywords):
    """Match whole phrases, excluding simple local negation (not full language understanding)."""
    text = text.lower().replace('\u2019', "'")
    matches = []
    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword).replace(r'\ ', r'\s+') + r'\b'
        for match in re.finditer(pattern, text):
            clause = re.split(r'[.!?;,]|\b(?:but|however|yet)\b', text[:match.start()])[-1]
            prefix = ' '.join(clause.split()[-5:])
            negated = re.search(r"\b(?:no|not|never|without|neither)\b|\b\w+n't\b", prefix)
            if not negated or re.search(r'\bnot only\b', prefix):
                matches.append(keyword)
                break
    return matches


def check_severity_keywords(text):
    """
    Check text for severity-indicating keywords.
    
    Returns:
        tuple: (suggested_severity, matched_keywords)
            - suggested_severity: 'HIGH', 'MEDIUM', or None
            - matched_keywords: list of matched keyword phrases
    """
    high_matches = matched_indicators(text, HIGH_SEVERITY_KEYWORDS)
    medium_matches = matched_indicators(text, MEDIUM_SEVERITY_KEYWORDS)
    
    if high_matches:
        return 'HIGH', high_matches
    elif medium_matches:
        return 'MEDIUM', medium_matches
    return None, []


def check_emergency_keywords(text):
    """
    Check text for emergency-indicating keywords.
    
    Returns:
        tuple: (is_potential_emergency, matched_keywords)
    """
    matches = matched_indicators(text, EMERGENCY_KEYWORDS)
    
    # Need at least one strong emergency indicator
    is_emergency = len(matches) >= 1
    
    return is_emergency, matches


def adjust_severity(ml_severity, text):
    """
    Adjust ML-predicted severity using rule-based keyword checking.
    
    Logic:
    - If ML says LOW but keywords suggest HIGH → escalate to MEDIUM
    - If ML says LOW but keywords suggest MEDIUM → escalate to MEDIUM
    - If ML says MEDIUM but strong HIGH keywords present → escalate to HIGH
    - Otherwise, trust ML prediction
    
    Parameters:
        ml_severity (str): ML-predicted severity ('LOW', 'MEDIUM', 'HIGH', 'NONE')
        text (str): Original text
    
    Returns:
        tuple: (final_severity, explanation)
    """
    if ml_severity == 'NONE':
        return 'NONE', 'Text classified as non-pollution related.'
    
    keyword_severity, matched = check_severity_keywords(text)
    
    explanation_parts = []
    final_severity = ml_severity
    
    if keyword_severity == 'HIGH' and ml_severity == 'LOW':
        final_severity = 'MEDIUM'
        explanation_parts.append(
            f"ML predicted LOW severity, but high-risk keywords detected: {', '.join(matched[:3])}. "
            f"Severity escalated to MEDIUM for safety."
        )
    elif keyword_severity == 'HIGH' and ml_severity == 'MEDIUM':
        final_severity = 'HIGH'
        explanation_parts.append(
            f"ML predicted MEDIUM severity. High-risk keywords confirmed: {', '.join(matched[:3])}. "
            f"Severity escalated to HIGH."
        )
    elif keyword_severity == 'MEDIUM' and ml_severity == 'LOW':
        final_severity = 'MEDIUM'
        explanation_parts.append(
            f"ML predicted LOW severity, but notable keywords detected: {', '.join(matched[:3])}. "
            f"Severity adjusted to MEDIUM."
        )
    elif keyword_severity and ml_severity == keyword_severity:
        explanation_parts.append(
            f"ML prediction ({ml_severity}) confirmed by keyword analysis: {', '.join(matched[:3])}."
        )
    else:
        explanation_parts.append(
            f"Severity based on ML classification: {ml_severity}."
        )
    
    if not explanation_parts:
        explanation_parts.append(f"Severity classified as {final_severity} by ML model.")
    
    return final_severity, ' '.join(explanation_parts)


def adjust_emergency(ml_emergency, text, final_severity):
    """
    Adjust ML-predicted emergency status using keywords and severity.
    
    Logic:
    - If severity is HIGH and emergency keywords present → POTENTIAL EMERGENCY
    - If ML says NORMAL but text has pollution keywords → POLLUTION REPORT
    - Trust ML for other cases
    
    Parameters:
        ml_emergency (str): ML-predicted emergency status
        text (str): Original text
        final_severity (str): Final (adjusted) severity
    
    Returns:
        tuple: (final_emergency, explanation, indicators)
    """
    is_emergency, emergency_matches = check_emergency_keywords(text)
    
    indicators = emergency_matches
    final_emergency = ml_emergency
    explanation_parts = []
    
    if final_severity == 'NONE':
        return 'NORMAL', 'Text classified as non-pollution related.', []
    
    if is_emergency and final_severity == 'HIGH':
        final_emergency = 'POTENTIAL EMERGENCY'
        explanation_parts.append(
            f"HIGH severity with emergency indicators detected: {', '.join(emergency_matches[:3])}. "
            f"Classified as POTENTIAL EMERGENCY."
        )
    elif is_emergency and final_severity == 'MEDIUM' and ml_emergency != 'POTENTIAL EMERGENCY':
        # Don't escalate to emergency for medium severity unless ML also agrees
        final_emergency = 'POLLUTION REPORT'
        explanation_parts.append(
            f"Emergency keywords detected ({', '.join(emergency_matches[:2])}), "
            f"but severity is MEDIUM. Classified as POLLUTION REPORT."
        )
    elif ml_emergency == 'NORMAL' and final_severity in ('LOW', 'MEDIUM', 'HIGH'):
        final_emergency = 'POLLUTION REPORT'
        explanation_parts.append(
            f"Pollution indicators present. Classified as POLLUTION REPORT."
        )
    else:
        explanation_parts.append(
            f"Emergency status: {final_emergency}."
        )
    
    if not explanation_parts:
        explanation_parts.append(f"Emergency status classified as {final_emergency}.")
    
    return final_emergency, ' '.join(explanation_parts), indicators


def generate_suggested_action(severity, emergency_status):
    """
    Generate a suggested action based on severity and emergency status.
    
    Returns:
        str: Suggested course of action
    """
    if emergency_status == 'NORMAL':
        return "No immediate action required. This text does not appear to describe a pollution incident."
    
    if emergency_status == 'POTENTIAL EMERGENCY':
        return (
            "URGENT: This report contains indicators of a potentially serious pollution incident. "
            "Immediate verification by local authorities or environmental agencies is recommended. "
            "If people are experiencing health problems, contact emergency medical services."
        )
    
    # POLLUTION REPORT
    if severity == 'HIGH':
        return (
            "This report indicates a significant pollution concern. "
            "Prompt investigation by environmental authorities is recommended. "
            "Monitor the situation and escalate if conditions worsen."
        )
    elif severity == 'MEDIUM':
        return (
            "This report describes a notable pollution incident. "
            "It is recommended to notify the local pollution control board or municipal authority for investigation."
        )
    else:  # LOW
        return (
            "This report describes a minor pollution observation. "
            "It may be logged for record-keeping and addressed during routine environmental monitoring."
        )


def generate_incident_summary(pollution_type, severity, emergency_status, location, keywords):
    """
    Generate a structured incident summary.
    
    Returns:
        str: Formatted incident summary
    """
    summary_parts = []
    
    # Incident type
    if pollution_type == 'Not Pollution':
        return "No pollution incident detected in the provided text."
    
    summary_parts.append(f"Incident: Possible {pollution_type.lower()} incident detected.")
    summary_parts.append(f"Location: {location}")
    summary_parts.append(f"Severity: {severity} (NLP-based preliminary classification)")
    summary_parts.append(f"Emergency Status: {emergency_status}")
    
    if keywords:
        summary_parts.append(f"Detected Indicators: {', '.join(keywords[:5])}")
    
    summary_parts.append(f"Suggested Action: {generate_suggested_action(severity, emergency_status)}")
    
    return '\n'.join(summary_parts)


# === Demonstration ===
if __name__ == "__main__":
    test_cases = [
        ("A chemical leak has caused a toxic smell and breathing problems.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT"),
        ("Garbage has been dumped near the road.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT"),
        ("Today is a sunny day.", "Not Pollution", "NONE", "NORMAL"),
        ("Thick smoke from the factory visible since morning.", "Air Pollution", "MEDIUM", "POLLUTION REPORT"),
    ]
    
    print("=" * 60)
    print("Severity & Emergency Adjustment Demo")
    print("=" * 60)
    
    for text, ptype, ml_sev, ml_em in test_cases:
        print(f"\nInput: {text}")
        print(f"ML Predictions: Type={ptype}, Severity={ml_sev}, Emergency={ml_em}")
        
        final_sev, sev_explanation = adjust_severity(ml_sev, text)
        final_em, em_explanation, indicators = adjust_emergency(ml_em, text, final_sev)
        
        print(f"Final Severity: {final_sev}")
        print(f"  Explanation: {sev_explanation}")
        print(f"Final Emergency: {final_em}")
        print(f"  Explanation: {em_explanation}")
        if indicators:
            print(f"  Indicators: {indicators}")
        print(f"Suggested Action: {generate_suggested_action(final_sev, final_em)}")
        print("-" * 60)
