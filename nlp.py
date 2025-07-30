#NLP Processing
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def summarize(text):
    # Basic stub summary
    sentences = text.split(".")
    return ". ".join(sentences[:3]) + "."

def extract_action_items(text):
    return re.findall(r'\b(?:will|need to|should)\b.*?\.', text, re.IGNORECASE)

def extract_dates(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == "DATE"]

def process(text):
    return {
        "summary": summarize(text),
        "actions": extract_action_items(text),
        "dates": extract_dates(text)
    }
