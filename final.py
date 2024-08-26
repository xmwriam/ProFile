# %%


# %% [markdown]
# data
# 

# %%
import pandas as pd
import numpy as np
import os
import seaborn as sns
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
nltk.download('universal_tagset')
from textblob import TextBlob
from collections import Counter
from nltk.corpus import wordnet as wn

# %%
file_path1 = os.path.join("data","jobtitle", "jobss.csv")
job = pd.read_csv(file_path1)

# %%
job.drop(columns=['Job Experience Required', 'Unnamed: 1','Location','Longitude','Latitude','sal'],inplace=True)

# %%
job.dropna(inplace=True)

# %%

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)
job['Updated Job Title'] = job['Job Title'].apply(preprocess_text)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(job['Updated Job Title'])
def recommend_skills(job_title):
    processed_title = preprocess_text(job_title)
    title_vector = vectorizer.transform([processed_title])
    similarities = cosine_similarity(title_vector, tfidf_matrix)
    index = similarities.argmax()
    return job.iloc[index]['Key Skills']

# %% [markdown]
# 

# %%
def final(job_title): #single input milega
    found = 0
    job_title = job_title.lower()

    if job['Updated Job Title'].str.contains(job_title).any():
            found = 1
            
    if found==1:
        recommended_skills = recommend_skills(job_title)
        result = f"{recommended_skills}"
    else:
        reuslt = "No relevant skill suggestion found"
    return result
ans = final(job_title)
print(ans)

# %%
def finalnum(job_title):  
    y = final(job_title)
    if y == "No relevant skill suggestion found":
        relskill = 0 
    else:
        keys = y.split("|")
        relskill = len(keys)

    return relskill
d = finalnum('sales')
print(d)

# %%
text = "time management"
words = word_tokenize(text)
all_synonyms = set()
for word in words:
    synsets = wn.synsets(word, pos=wn.VERB) 
    for synset in synsets:
        for lemma in synset.lemmas():
            all_synonyms.add(lemma.name())

print("Synonyms found:")
print(all_synonyms)

# %%
file_path2 = os.path.join("data","skill", "skills_index_final.csv")
skill = pd.read_csv(file_path2)

# %%

# %%
def synonym(soft_skill):
    words = word_tokenize(soft_skill)
    all_synonyms = []
    for word in words:
        synsets = wn.synsets(word, pos=wn.VERB) 
        for synset in synsets:
            for lemma in synset.lemmas():
                all_synonyms.append(lemma.name())

    
    return all_synonyms
    
    
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)
skill['Updated Skill'] = skill['Skill'].apply(preprocess_text)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(skill['Updated Skill'])
for j in skill['Updated Skill']:
    
    soft_skill = j.lower()
    list = synonym(soft_skill)
    for i in range(len(list)):
        if skill['Updated Skill'].str.contains(list[i]).any() :
            print(j , ": buzzword")
    if skill['Updated Skill'].str.contains(soft_skill).any():
        print(j)        
    
    

  
 

# %%

def synonym(word):
    synsets = wn.synsets(word, pos=wn.ADJ)
    all_synonyms = set()  
    for synset in synsets:
        for lemma in synset.lemmas():
            all_synonyms.add(lemma.name().replace('_', ' '))
    return all_synonyms

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)


# Apply preprocessing to 'Skill' column
skill['Updated Skill'] = skill['Skill'].apply(preprocess_text)

# Vectorization (not used in this snippet but set up for potential future use)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(skill['Updated Skill'])

# Process each skill
for soft_skill in skill['Updated Skill']:
    soft_skill_processed = preprocess_text(soft_skill.lower())
    synonyms_list = synonym(soft_skill_processed)  # Get synonyms for the soft skill
    
    # Check if the soft skill or any of its synonyms are in the 'Updated Skill' column
    if skill['Updated Skill'].str.contains(soft_skill_processed).any():
        print(soft_skill, ": buzzword")
    else:
        for synonym_word in synonyms_list:
            if skill['Updated Skill'].str.contains(synonym_word).any():
                print(soft_skill, ": buzzword")
                break  

# %%
def preprocess_text(text):
    
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return tokens
    
    
    
newtext = preprocess_text(text)
list = text.split(" ")
for i in list:
    print(i)
count = 0 
for i in list:
    try:
        num = int(i)
        count = count + 1
    except ValueError:
        pass
print(newtext)   

# %%
def number(text):
    list = text.split(" ")
    for i in list:
        print(i)
    count = 0 
    for i in list:
        try:
            num = int(i)
            count = count + 1
        except ValueError:
            pass
    print(count)

# %%
from textblob import TextBlob

def spelling(text):
    blob = TextBlob(text)
    corrected_text = blob.correct()
    return str(corrected_text)
corrected_text = spelling(text)
    
print("Original:", text)
print("Corrected:", corrected_text)

# %%
from textblob import TextBlob
from collections import Counter

def spelling(text):
    blob = TextBlob(text)
    corrected_text = blob.correct()
    return str(corrected_text)

def find_misspelled_words(original_text, corrected_text):
    original_words = original_text.split()
    corrected_words = corrected_text.split()
    
    misspelled_words = []
    
    for original, corrected in zip(original_words, corrected_words):
        if original != corrected:
            misspelled_words.append(original)
    
    word_frequency = Counter(misspelled_words)
    
    return word_frequency

text = "Ths is an exampel with som mispeled words."

corrected_text = spelling(text)

misspelled_word_frequency = find_misspelled_words(text, corrected_text)

print("Original Text:", text)
print("Corrected Text:", corrected_text)
print("Misspelled Words Frequency:", misspelled_word_frequency)


# %%
def score(text):
    processed_text = preprocess_text(text)    
    corrected = spelling(text)
    x = find_misspelled_words(text,corrected)
    total_misspelled = sum(x.values())
    num = number(text)
   
    final_score  = -20*total_misspelled + 5*num 
    return final_score

# %%
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter


def spelling(text):
    blob = TextBlob(text)
    corrected_text = blob.correct()
    return str(corrected_text)


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)


def find_misspelled_words(original_text, corrected_text):
    original_words = original_text.split()
    corrected_words = corrected_text.split()
    
    misspelled_words = []
    
    for original, corrected in zip(original_words, corrected_words):
        if original != corrected:
            misspelled_words.append(original)
    
    word_frequency = Counter(misspelled_words)
    return word_frequency


def number(text):
    tokens = word_tokenize(text)
    count = 0
    for token in tokens:
        try:
            int(token)
            count += 1
        except ValueError:
            continue
    return count


def score(text):
    processed_text = preprocess_text(text)    
    corrected = spelling(text)
    x = find_misspelled_words(text, corrected)
    total_misspelled = sum(x.values())
    num = number(text)
   
    final_score = -2* total_misspelled + 7 * num 
    if final_score>0:
        
        return final_score
    else:
        return "OOPS , You need to work a little more."

    


final_score = score(text)
print("Final Score:", final_score)



