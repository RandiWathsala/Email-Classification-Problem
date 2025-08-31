import streamlit as st
import joblib
import pandas as pd
from collections import defaultdict
from connection import (
    gmail_connect,
    get_inbox_emails,
    get_sent_emails,
    get_spam_emails,
    get_trash_emails,
    mark_as_read,
)
from inference_utils import clean_text

# Load Model 
loaded_model = joblib.load("email_sorting_model.pkl")

# Label mapping
label_map = {
    0: "Academic",
    1: "Bills & Finance",
    2: "News & Updates",
    3: "Personal",
    4: "Official",
}

# Streamlit Page Setup
st.set_page_config(page_title="Email Classifier", layout="wide")
st.title("📧 Email Classifier")


# Refresh Button
col1, col2 = st.columns([0.85, 0.15])
with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

# Sidebar Styling
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #202124;
        padding-top: 20px;
    }
    div.stButton > button {
        display: block;
        width: 100% !important;
        margin: 0 !important;
        padding: 12px 20px;
        border: none !important;
        border-radius: 0 !important;
        background: none !important;
        color: #e8eaed !important;
        text-align: left;
        font-size: 15px;
        font-weight: 500;
    }
    div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    div.stButton > button.active {
        background-color: rgba(138, 180, 248, 0.3) !important;
        font-weight: 600 !important;
        color: white !important;
    }
    div[data-baseweb="tab-list"] {
        gap: 10px;
    }
    button[data-baseweb="tab"] {
        min-width: 180px !important;
        padding: 12px 20px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }
    button[data-baseweb="tab"]:hover {
        background-color: rgba(138, 180, 248, 0.15) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: rgba(138, 180, 248, 0.3) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# count unread messages
def count_unread(emails):
    return sum(1 for e in emails if "UNREAD" in e.get("labels", []))


# Sidebar Logic (Folders with counts)
if "menu" not in st.session_state:
    st.session_state.menu = "Inbox"

service = gmail_connect()

folder_fetchers = {
    "Inbox": get_inbox_emails,
    "Sent": get_sent_emails,
    "Spam": get_spam_emails,
    "Trash": get_trash_emails,
}

st.sidebar.markdown("### 📂 E-Mails")
for folder, fetcher in folder_fetchers.items():
    try:
        fetched_emails = fetcher(service, max_results=50)
    except Exception:
        fetched_emails = []
    count = count_unread(fetched_emails)
    label = f"{folder} ({count})" if count else folder
    if st.sidebar.button(label, key=folder):
        st.session_state.menu = folder

menu = st.session_state.menu

# Fetch emails for current folder
if menu == "Inbox":
    st.subheader("📥 Gmail Inbox")
    emails = get_inbox_emails(service, max_results=50)

elif menu == "Sent":
    st.subheader("📤 Gmail Sent")
    emails = get_sent_emails(service, max_results=50)

elif menu == "Spam":
    st.subheader("🚫 Gmail Spam")
    emails = get_spam_emails(service, max_results=50)

elif menu == "Trash":
    st.subheader("🗑️ Gmail Trash")
    emails = get_trash_emails(service, max_results=50)

else:
    emails = []

# Classification 
unread_by_category = defaultdict(int)

for email in emails:
    sender = email.get("from", "unknown")
    combined_text = f"{email.get('subject','')} {email.get('snippet','')}"
    cleaned = clean_text(combined_text)

    email_record = {
        "clean_text": cleaned,
        "from": sender,
        "gmail_labels": str(email.get("labels", [])),
    }
    X_new = pd.DataFrame([email_record], columns=["clean_text", "from", "gmail_labels"])
    pred = loaded_model.predict(X_new)[0]
    email["predicted_label"] = label_map[pred]

    if "UNREAD" in email.get("labels", []):
        unread_by_category[label_map[pred]] += 1

# Top Tabs 
tabs = st.tabs([
    f"📘 Academic ({unread_by_category['Academic']})",
    f"💰 Bills & Finance ({unread_by_category['Bills & Finance']})",
    f"📰 News & Updates ({unread_by_category['News & Updates']})",
    f"👤 Personal ({unread_by_category['Personal']})",
    f"🏢 Official ({unread_by_category['Official']})",
])
categories = ["Academic", "Bills & Finance", "News & Updates", "Personal", "Official"]

# Display emails under tabs
for i, category in enumerate(categories):
    with tabs[i]:
        st.subheader(f"{category} - {menu}")

        filtered_emails = [e for e in emails if e.get("predicted_label") == category]

        if not filtered_emails:
            st.info("No emails in this category.")
        for email in filtered_emails:
            is_unread = "UNREAD" in email.get("labels", [])
            expander_label = f"📌 {email['subject']}  ({email.get('from','')})"

            # Unread
            if is_unread:
                expander_label = f"🟢 {expander_label}"
                expander_style = "background-color: rgba(138,180,248,0.15);"
            else:
                expander_style = "background-color: rgba(255,255,255,0.05);"

            with st.expander(expander_label):
                st.markdown(
                    f"<div style='{expander_style} padding:10px;'>{email['snippet']}</div>",
                    unsafe_allow_html=True,
                )

                # Read button
                unique_key = f"{email['id']}_{category}_{menu}"
                if "UNREAD" in email.get("labels", []):
                    if st.button("✅ Mark as Read", key=unique_key):
                        mark_as_read(service, email['id'])
                        st.success("Email marked as read! Please refresh to see changes.")
