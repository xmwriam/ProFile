import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from collections import Counter
from nltk.corpus import wordnet as wn
nltk.download('stopwords')
nltk.download('punkt')
file_path1 = os.path.join("data", "jobtitle", "jobss.csv")
job = pd.read_csv(file_path1)
job.drop(columns=['Job Experience Required', 'Unnamed: 1', 'Location', 'Longitude', 'Latitude', 'sal'], inplace=True)
job.dropna(inplace=True)

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)
def recommend_skills(job_title):
    processed_title = preprocess_text(job_title)
    title_vector = vectorizer.transform([processed_title])
    similarities = cosine_similarity(title_vector, tfidf_matrix)
    index = similarities.argmax()
    return job.iloc[index]['Key Skills']
def final(job_title):
    if job['Updated Job Title'].str.contains(preprocess_text(job_title)).any():
        return recommend_skills(job_title)
    else:
        return "No relevant skill suggestion found"
def number(text):
    tokens = word_tokenize(text)
    return sum(token.isdigit() for token in tokens)
def spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())
def find_misspelled_words(original_text, corrected_text):
    original_words = original_text.split()
    corrected_words = corrected_text.split()
    misspelled_words = [original for original, corrected in zip(original_words, corrected_words) if original != corrected]
    return Counter(misspelled_words)
def score(text):
    processed_text = preprocess_text(text)
    corrected = spelling(text)
    misspelled_count = sum(find_misspelled_words(text, corrected).values())
    num_count = number(text)
    final_score = -2 * misspelled_count + 7 * num_count
    return final_score if final_score > 0 else "OOPS, You need to work a little more."


text = "Ths is an exampel with som mispeled words."
print("Original Text:", text)
print("Corrected Text:", spelling(text))
print("Misspelled Words Frequency:", find_misspelled_words(text, spelling(text)))
print("Final Score:", score(text))
