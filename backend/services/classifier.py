SYMPTOM_LABELS = [
    "Fever", "Cough", "Headache", "Rash", "Vomiting", "Diarrhea", "Cold", "Other"
]

def classify_query(query: str) -> str:
    query_lower = query.lower()
    for label in SYMPTOM_LABELS:
        if label.lower() in query_lower:
            return label
    return "Other"

