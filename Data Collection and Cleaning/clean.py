import pandas as pd
from bs4 import BeautifulSoup
import re

df = pd.read_csv("emails_dataset.csv")  

df_clean = df[['subject', 'body', 'gmail_labels', 'from']].copy()

def clean_body(text):
    if pd.isna(text):
        return ""
    # Remove HTML
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

df_clean['body'] = df_clean['body'].apply(clean_body)

df_clean.to_csv("emails_dataset_clean.csv", index=False)
