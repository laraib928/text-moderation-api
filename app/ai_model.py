from transformers import pipeline
import logging


logger = logging.getLogger(__name__)


try:
    classifier = pipeline(
        task="text-classification",
        model="unitary/toxic-bert",
        top_k=None,
        framework="pt"
    )
    logger.info("Toxicity model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise

def analyze_text(text: str):
    """Analyze text for toxic content with proper error handling"""
    if not text.strip():
        return "approved", 0.0, "Empty text input"
    
    try:
        results = classifier(text)
        if not results or not results[0]:
            return "approved", 0.0, "No toxicity detected"
        
        toxic_scores = [
            {"label": entry['label'], "score": entry['score']}
            for entry in results[0]
            if entry['label'] != 'non-toxic'
        ]
        
        if not toxic_scores:
            return "approved", 0.0, "Non-toxic content"
        
        max_toxic = max(toxic_scores, key=lambda x: x['score'])
        
        # Convert label to more readable format
        label = max_toxic['label'].replace('_', ' ').title()
        
        if max_toxic['score'] > 0.8:
            return "rejected", max_toxic['score'], f"{label} content detected"
        elif max_toxic['score'] > 0.6:
            return "flagged", max_toxic['score'], f"Potential {label}"
        else:
            return "approved", max_toxic['score'], "Content appears safe"
            
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return "error", 0.0, "Analysis failed"
