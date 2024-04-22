#!/usr/bin/env python
# coding: utf-8

# In[1]:


from docx import Document
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
nltk.download('punkt')


# In[2]:


def read_doc(file_path, patent_start=r'^\s*US[0-9A-Z]*$'):
    doc = Document(file_path)
    labels = []
    patents = []
    current_patent_text = []
    
    for i, paragraph in enumerate(doc.paragraphs):
        if re.search(patent_start, paragraph.text):
            labels.append(paragraph.text)
            if current_patent_text:
                patents.append('\n'.join(current_patent_text))
            current_patent_text = []
        else:
            # If not a patent start, add the paragraph text to the current patent text
            current_patent_text.append(paragraph.text)
            
    # Add the last patent text
    if current_patent_text:
        patents.append('\n'.join(current_patent_text))

    return patents, labels


# In[3]:


def preprocess_text(text):
    stop_words = stopwords.words('english')
    stop_words.append('may')
    stop_words = set(stop_words)
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

