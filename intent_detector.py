import difflib
from enum import Enum

# 6. Confidence Thresholds (Enums for routing logic)
class Route(Enum):
    EXECUTE = 0.95       # Immediate Plugin Execution
    CONFIDENT = 0.80     # Plugin Execution
    CLARIFY = 0.60       # Ask User ("Did you mean...")
    LLM_FALLBACK = 0.00  # Send to Llama

def _fuzzy_match(word1: str, word2: str) -> float:
    return difflib.SequenceMatcher(None, word1, word2).ratio()

def detect_intent(command: str, precompiled_registry: dict) -> tuple:
    """
    3 & 4. Weighted Confidence Scoring with Fuzzy Fallback.
    """
    best_intent = "unknown"
    best_action = None
    best_confidence = 0.0
    
    for intent_name, plugin_data in precompiled_registry.items():
        # 2. Action detection mapped directly from Plugin metadata
        for action_name, compiled_triggers in plugin_data.get("actions", {}).items():
            for trigger in compiled_triggers:
                
                # Weighted Scoring
                if command == trigger:
                    confidence = 1.0  # Exact
                elif command.startswith(trigger):
                    confidence = 0.95 # Prefix
                elif trigger in command:
                    confidence = 0.80 # Contains
                else:
                    # Fuzzy match fallback (e.g., "open chrom" vs "open chrome")
                    confidence = _fuzzy_match(command, trigger) * 0.70 
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_intent = intent_name
                    best_action = action_name
                    
    return best_intent, best_action, best_confidence