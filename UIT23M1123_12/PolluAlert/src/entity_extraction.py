"""
Entity Extraction Module for PolluAlert
Extracts locations, organizations, and pollution-related entities.

Uses spaCy NER when available, falls back to regex-based extraction otherwise.
Also uses custom pattern matching for pollution-specific terms.
"""

import re

# Try to load spaCy - gracefully degrade if not available
_nlp = None
_spacy_available = False

def _load_spacy():
    """Attempt to load spaCy model."""
    global _nlp, _spacy_available
    try:
        import spacy
        _nlp = spacy.load("en_core_web_sm")
        _spacy_available = True
    except (ImportError, OSError, Exception):
        _nlp = None
        _spacy_available = False

_load_spacy()


def get_entity_extraction_mode():
    """Expose the actual extraction method instead of silently claiming spaCy NER."""
    return 'spaCy NER + location patterns' if _spacy_available else 'Location patterns (spaCy unavailable)'


# ============================================================
# Known location patterns (common Indian cities and areas)
# ============================================================
KNOWN_LOCATIONS = [
    # Major Indian cities
    'Mumbai', 'Delhi', 'Pune', 'Nagpur', 'Nashik', 'Kolhapur', 'Aurangabad',
    'Thane', 'Solapur', 'Ahmednagar', 'Satara', 'Sangli', 'Ratnagiri',
    'Chennai', 'Bangalore', 'Hyderabad', 'Kolkata', 'Jaipur', 'Lucknow',
    'Kanpur', 'Visakhapatnam', 'Kodaikanal', 'Mathura', 'Jamnagar',
    # Suburbs and areas
    'Andheri', 'Andheri East', 'Andheri West', 'Bhiwandi', 'Ambernath',
    'Dombivli', 'Chembur', 'Tarapur', 'Panvel', 'Badlapur',
    'Hadapsar', 'Katraj', 'Kothrud', 'Hinjewadi', 'Wagholi',
    'Bhosari', 'Chinchwad', 'Pimpri', 'Pimpri-Chinchwad', 'Kharadi',
    'Aundh', 'Baramati', 'Wai', 'Chakan', 'Shirur', 'Latur',
    'Ichalkaranji', 'Raigad', 'Manchar', 'Chandrapur', 'Raigarh',
    'Rajsamand', 'Zuarinagar', 'Mulshi', 'Mahabaleshwar', 'Viman Nagar',
    # Areas and zones
    'MIDC', 'MG Road', 'Solapur Road', 'Sinhagad Road',
    'Delhi NCR', 'Punjab', 'Haryana',
    # Ward references
    'Ward 15',
]

# Sort by length (longest first) to match multi-word locations first
KNOWN_LOCATIONS.sort(key=lambda x: len(x), reverse=True)


# Custom patterns for pollution-related entities
POLLUTION_SOURCE_PATTERNS = [
    r'\bfactor(?:y|ies)\b', r'\bplant(?:s)?\b', r'\bmill(?:s)?\b',
    r'\bkiln(?:s)?\b', r'\brefiner(?:y|ies)\b', r'\bwarehouse(?:s)?\b',
    r'\bworkshop(?:s)?\b', r'\bgodown(?:s)?\b', r'\bfoundr(?:y|ies)\b',
    r'\btanner(?:y|ies)\b', r'\bsmelter(?:s)?\b', r'\bquarr(?:y|ies)\b',
    r'\bmine(?:s)?\b', r'\bincinerator(?:s)?\b', r'\bdump\s*site(?:s)?\b',
    r'\blandfill(?:s)?\b', r'\bpower\s*plant(?:s)?\b', r'\bchemical\s*plant(?:s)?\b',
    r'\bchemical\s*factory\b', r'\bsugar\s*factory\b', r'\bcement\s*factory\b',
    r'\btextile\s*factory\b', r'\bpaint\s*factory\b', r'\bbattery\s*factory\b',
    r'\bglass\s*factory\b', r'\bplastic\s*factory\b', r'\brubber\s*factory\b',
]

WATER_BODY_PATTERNS = [
    r'\briver(?:s)?\b', r'\blake(?:s)?\b', r'\bpond(?:s)?\b',
    r'\bstream(?:s)?\b', r'\bcanal(?:s)?\b', r'\bwell(?:s)?\b',
    r'\bnullah(?:s)?\b', r'\bdrain(?:s|age)?\b', r'\bcreek(?:s)?\b',
    r'\breservoir(?:s)?\b', r'\bsea\b', r'\bocean\b', r'\bharbour\b',
    r'\bgroundwater\b', r'\bbore\s*well\b', r'\bhand\s*pump\b',
]

AFFECTED_GROUP_PATTERNS = [
    r'\bresidents?\b', r'\bpeople\b', r'\bchildren\b', r'\bworkers?\b',
    r'\bfamilies\b', r'\bstudents?\b', r'\bfarmers?\b', r'\bpatients?\b',
    r'\bvillagers?\b', r'\bcitizens?\b', r'\bneighbours?\b',
]

AREA_TYPE_PATTERNS = [
    r'\bMIDC\b', r'\bindustrial\s*(?:area|estate|zone|belt)\b',
    r'\bresidential\s*(?:area|colony|zone|neighbourhood)\b',
    r'\bcommercial\s*(?:area|zone)\b',
    r'\bschool\b', r'\bhospital\b', r'\bmarket\b', r'\bhighway\b',
    r'\bward\s*\d+\b', r'\bplayground\b', r'\bpark\b',
]


def extract_entities_spacy(text):
    """
    Extract named entities using spaCy NER.
    Falls back to empty results if spaCy is not available.
    """
    result = {
        'locations': [],
        'organizations': [],
        'facilities': [],
        'persons': [],
        'other_entities': []
    }
    
    if not _spacy_available or _nlp is None:
        return result
    
    doc = _nlp(text)
    
    for ent in doc.ents:
        entity_info = {'text': ent.text, 'label': ent.label_}
        
        if ent.label_ in ('GPE', 'LOC'):
            if ent.text not in [e['text'] for e in result['locations']]:
                result['locations'].append(entity_info)
        elif ent.label_ == 'ORG':
            if ent.text not in [e['text'] for e in result['organizations']]:
                result['organizations'].append(entity_info)
        elif ent.label_ == 'FAC':
            if ent.text not in [e['text'] for e in result['facilities']]:
                result['facilities'].append(entity_info)
        elif ent.label_ == 'PERSON':
            if ent.text not in [e['text'] for e in result['persons']]:
                result['persons'].append(entity_info)
        else:
            result['other_entities'].append(entity_info)
    
    return result


def extract_location_regex(text):
    """
    Extract location from text using known location patterns.
    This works as a fallback when spaCy is not available.
    """
    for location in KNOWN_LOCATIONS:
        # Case-insensitive search for the known location
        pattern = r'\b' + re.escape(location) + r'\b'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None


def extract_custom_entities(text):
    """
    Extract pollution-specific entities using custom regex patterns.
    """
    text_lower = text.lower()
    
    result = {
        'pollution_sources': [],
        'water_bodies': [],
        'affected_groups': [],
        'area_types': []
    }
    
    for pattern in POLLUTION_SOURCE_PATTERNS:
        matches = re.findall(pattern, text_lower)
        result['pollution_sources'].extend(matches)
    
    for pattern in WATER_BODY_PATTERNS:
        matches = re.findall(pattern, text_lower)
        result['water_bodies'].extend(matches)
    
    for pattern in AFFECTED_GROUP_PATTERNS:
        matches = re.findall(pattern, text_lower)
        result['affected_groups'].extend(matches)
    
    for pattern in AREA_TYPE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        result['area_types'].extend(matches)
    
    # Remove duplicates
    for key in result:
        result[key] = list(set(result[key]))
    
    return result


def extract_location(text):
    """
    Extract the primary location from text.
    Combines spaCy NER and regex-based extraction.
    
    Returns:
        str: Extracted location or "Not identified"
    """
    # Try spaCy first
    if _spacy_available:
        spacy_entities = extract_entities_spacy(text)
        locations = [loc['text'] for loc in spacy_entities['locations']]
        if locations:
            return locations[0]
    
    # Fallback to regex-based location extraction
    regex_location = extract_location_regex(text)
    if regex_location:
        return regex_location
    
    # Check area type patterns
    custom = extract_custom_entities(text)
    if custom['area_types']:
        return custom['area_types'][0]
    
    return "Not identified"


def extract_all_entities(text):
    """
    Combine spaCy NER and custom pattern matching for comprehensive entity extraction.
    
    Parameters:
        text (str): Original (unprocessed) text
    
    Returns:
        dict: Combined entity extraction results
    """
    spacy_entities = extract_entities_spacy(text)
    custom_entities = extract_custom_entities(text)
    location = extract_location(text)
    
    # Combine spaCy locations with regex locations
    all_locations = [e['text'] for e in spacy_entities['locations']]
    regex_loc = extract_location_regex(text)
    if regex_loc and regex_loc not in all_locations:
        all_locations.append(regex_loc)
    
    return {
        'location': location,
        'spacy_entities': spacy_entities,
        'custom_entities': custom_entities,
        'all_locations': all_locations,
        'organizations': [e['text'] for e in spacy_entities['organizations']],
        'pollution_sources': custom_entities['pollution_sources'],
        'water_bodies': custom_entities['water_bodies'],
        'affected_groups': custom_entities['affected_groups'],
        'area_types': custom_entities['area_types'],
        'spacy_available': _spacy_available
    }


# === Demonstration ===
if __name__ == "__main__":
    test_texts = [
        "Residents near MIDC Ahmednagar reported thick smoke from a chemical factory.",
        "A chemical leak has caused a toxic smell and breathing problems.",
        "The river water near Kolhapur has turned dark brown.",
        "Today is a sunny day.",
        "Toxic gas leak from the pesticide factory has caused breathing emergencies in Thane.",
        "Dense smoke from factory near Andheri East affecting residential area.",
    ]
    
    print("=" * 60)
    print(f"Entity Extraction Demo (spaCy available: {_spacy_available})")
    print("=" * 60)
    
    for text in test_texts:
        print(f"\nInput: {text}")
        entities = extract_all_entities(text)
        print(f"  Location: {entities['location']}")
        print(f"  All Locations: {entities['all_locations']}")
        print(f"  Organizations: {entities['organizations']}")
        print(f"  Pollution Sources: {entities['pollution_sources']}")
        print(f"  Water Bodies: {entities['water_bodies']}")
        print(f"  Affected Groups: {entities['affected_groups']}")
        print(f"  Area Types: {entities['area_types']}")
        print("-" * 60)
