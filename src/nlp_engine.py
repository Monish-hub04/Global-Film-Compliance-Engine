import spacy
import spacy.cli
from spacy.pipeline import EntityRuler

def load_nlp_pipeline():
    # Load the small english model
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        # Fallback if not downloaded properly
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    # Add EntityRuler
    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    else:
        ruler = nlp.get_pipe("entity_ruler")

    # Define patterns for our compliance categories
    patterns = [
        # PROFANITY (Sample terms - kept mild for illustrative purposes in this generic script)
        {"label": "PROFANITY", "pattern": [{"LOWER": "fuck"}]},
        {"label": "PROFANITY", "pattern": [{"LOWER": "shit"}]},
        {"label": "PROFANITY", "pattern": [{"LOWER": "bitch"}]},
        {"label": "PROFANITY", "pattern": [{"LOWER": "asshole"}]},
        {"label": "PROFANITY", "pattern": [{"LOWER": "crap"}]},
        {"label": "PROFANITY", "pattern": [{"LOWER": "damn"}]},
        {"label": "PROFANITY", "pattern": [{"LOWER": "bastard"}]},

        # VIOLENCE
        {"label": "VIOLENCE", "pattern": [{"LEMMA": "kill"}]},
        {"label": "VIOLENCE", "pattern": [{"LEMMA": "murder"}]},
        {"label": "VIOLENCE", "pattern": [{"LEMMA": "shoot"}]},
        {"label": "VIOLENCE", "pattern": [{"LEMMA": "stab"}]},
        {"label": "VIOLENCE", "pattern": [{"LEMMA": "punch"}]},
        {"label": "VIOLENCE", "pattern": [{"LEMMA": "attack"}]},
        {"label": "VIOLENCE", "pattern": [{"LEMMA": "destroy"}]},

        # GORE
        {"label": "GORE", "pattern": [{"LOWER": "blood"}]},
        {"label": "GORE", "pattern": [{"LOWER": "guts"}]},
        {"label": "GORE", "pattern": [{"LOWER": "dismember"}]},
        {"label": "GORE", "pattern": [{"LOWER": "decapitate"}]},
        {"label": "GORE", "pattern": [{"LOWER": "gore"}]},

        # SUBSTANCE ABUSE
        {"label": "DRUGS", "pattern": [{"LOWER": "cocaine"}]},
        {"label": "DRUGS", "pattern": [{"LOWER": "heroin"}]},
        {"label": "DRUGS", "pattern": [{"LOWER": "meth"}]},
        {"label": "DRUGS", "pattern": [{"LOWER": "weed"}]},
        {"label": "DRUGS", "pattern": [{"LOWER": "marijuana"}]},
        {"label": "DRUGS", "pattern": [{"LEMMA": "smoke"}]},
        {"label": "DRUGS", "pattern": [{"LOWER": "drunk"}]},
        {"label": "DRUGS", "pattern": [{"LOWER": "vodka"}]},
        {"label": "DRUGS", "pattern": [{"LOWER": "beer"}]},

        # NUDITY_SEX
        {"label": "NUDITY_SEX", "pattern": [{"LOWER": "sex"}]},
        {"label": "NUDITY_SEX", "pattern": [{"LOWER": "naked"}]},
        {"label": "NUDITY_SEX", "pattern": [{"LOWER": "nude"}]},
        {"label": "NUDITY_SEX", "pattern": [{"LOWER": "fuck"}]}, # overlapping meaning, but commonly a severe flag
    ]

    ruler.add_patterns(patterns)
    return nlp

def extract_compliance_entities(text):
    nlp = load_nlp_pipeline()
    doc = nlp(text)
    
    entities_found = {"PROFANITY": 0, "VIOLENCE": 0, "GORE": 0, "DRUGS": 0, "NUDITY_SEX": 0}
    highlights = []
    
    last_idx = 0
    
    # We will track all found rule-based entities
    for ent in doc.ents:
        if ent.label_ in entities_found:
            entities_found[ent.label_] += 1
            if len(highlights) < 50:
                sentence = ent.sent.text.strip().replace('\n', ' ').replace('\r', '')
                highlights.append({
                    "entity": ent.text,
                    "label": ent.label_,
                    "context": sentence
                })
            
    return doc, entities_found, highlights

