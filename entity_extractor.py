import re
from typing import Dict, Any

NUMBER_REGEX = re.compile(r'\b\d+\b')
UNIT_REGEX = re.compile(r'\b(minute|second|hour|min|sec|hr)s?\b')
URL_REGEX = re.compile(r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')

def extract_entities(command: str, intent: str, action: str) -> Dict[str, Any]:
    """Applies strict bounded compilation rules to isolate variable metrics."""
    entities = {}
    
    val_match = NUMBER_REGEX.search(command)
    unit_match = UNIT_REGEX.search(command)
    url_match = URL_REGEX.search(command)
    
    if val_match:
        entities["value"] = int(val_match.group(0))
    if unit_match:
        entities["unit"] = unit_match.group(1)
    if url_match:
        entities["url"] = url_match.group(0)
        
    # Standard application parameters parsing for structural action vectors
    if action in ["open", "close"] or intent in ["open_app", "close_app"]:
        words = command.split()
        if len(words) > 1 and words[0] in ["open", "close"]:
            entities["application"] = " ".join(words[1:])
            
    return entities