import pandas as pd
from bs4 import BeautifulSoup
import re

df = pd.read_csv("emails_dataset.csv")

columns_to_keep = [col for col in ["subject", "body", "gmail_labels", "from"] if col in df.columns]
df_clean = df[columns_to_keep].copy()

def extract_email(sender):
    if not isinstance(sender, str):
        return ""
    match = re.search(r'[\w\.-]+@[\w\.-]+', sender)
    return match.group(0) if match else ""

df_clean["from"] = df_clean["from"].apply(extract_email)

def deep_clean_body(text):
    if not isinstance(text, str):
        return ""
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    text = re.sub(r"\[.*?\]|\(.*?\)", " ", text)
    text = re.sub(r"=\s*\n", " ", text)
    text = re.sub(r"=\d+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s.,!?]", " ", text)
    text = text.lower()
    common_phrases = [
        "dear sir", "dear madam", "dear team", "dear all",
        "thank you", "thanks", "regards", "best regards",
        "view in browser", "unsubscribe", "click here", 
        "sent from my iphone", "confidential", "copyright", 
        "all rights reserved"
    ]
    for phrase in common_phrases:
        text = text.replace(phrase, " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

if "body" in df_clean.columns:
    df_clean["body"] = df_clean["body"].apply(deep_clean_body)

df_clean.to_csv("dataset1.csv", index=False)

print(df_clean.head(10))
print("dataset1.csv")
