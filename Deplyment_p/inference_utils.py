import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))

def clean_text(text):
   
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)  
    text = re.sub(r"\S+@\S+", " ", text)                   
    text = re.sub(r"[^a-zA-Z\s]", " ", text)               
    text = re.sub(r"\s+", " ", text).strip()
    text = " ".join([w for w in text.split() if w not in stop_words])  
    return text
