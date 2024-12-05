from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Lade das BERT Tokenizer und Modell
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def embed_text(text):
    """Konvertiere Text in BERT-Embedding."""
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Nimm die Ausgabe des letzten Layers (Pooled Output)
    return outputs.pooler_output[0].numpy()

def get_most_similar_resume(job_posting, resumes):
    """Finde das am besten passende Resume zum Job Posting."""
    # Berechne das Embedding für das Job Posting
    job_embedding = embed_text(job_posting)
    
    # Berechne die Embeddings für alle Resumes
    resume_embeddings = [embed_text(resume) for resume in resumes]
    
    # Berechne die Kosinus-Ähnlichkeit
    similarities = cosine_similarity([job_embedding], resume_embeddings)
    
    # Finde das Resume mit der höchsten Ähnlichkeit
    best_match_index = np.argmax(similarities)
    
    # Gib den Index des besten Matches und die Ähnlichkeit zurück
    return best_match_index, similarities[0][best_match_index]

# Job Posting aus der Datei laden
with open("job_posting.txt", 'r', encoding='utf-8') as file:
    job_posting = file.read()

# Resumes aus der CSV-Datei laden (nehmen wir an, dass sie eine Spalte "Resume" enthält)
resumes = pd.read_csv("resumesamples.csv")

# Angenommen, die Spalte mit den Lebensläufen heißt 'Resume'
resume_texts = resumes['Resume'].tolist()

# Finde das passende Resume
best_match_index, similarity = get_most_similar_resume(job_posting, resume_texts)

# Hole das beste Resume basierend auf dem Index
best_resume = resumes.iloc[best_match_index]

print(f"Bestes Resume: {best_resume['Resume']}")
print(f"Ähnlichkeit: {similarity:.4f}")
