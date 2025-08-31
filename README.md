# 📧 Email Classification Problem



A machine learning project that classifies Gmail emails into meaningful categories such as Academic, Bills & Finance, News & Updates, Personal, and Official.
This project integrates data collection (from Gmail API), data cleaning, preprocessing, model development, and deployment via Streamlit wrapped in an Electron desktop app.

🚀 Features

Fetch emails directly from Gmail using the Gmail API

Data cleaning pipelines (basic and deep cleaning)

Preprocessing with TF-IDF vectorization

Multiple ML models: Logistic Regression, Naive Bayes, Random Forest, SVM

Streamlit web app for interactive classification

Electron wrapper for cross-platform desktop application

Ability to mark emails as read directly from the app

📂 Project Structure

Email-Classification-Problem/
│── data/
│   ├── emails_dataset.csv          # Raw emails dataset
│   ├── emails_dataset_clean.csv    # Cleaned dataset
│   ├── dataset1.csv                # Deep cleaned dataset
│   ├── emails_cleaned.csv          # Preprocessed dataset
│
│── read.py                         # Fetch emails from Gmail API
│── clean.py                        # Basic cleaning of emails
│── deepclean.py                    # Deep cleaning of emails
│── preprocessing.py                 # Text preprocessing + TF-IDF
│── model_dev.py (notebook/script)  # Model development & evaluation
│
│── app.py                          # Streamlit app for deployment
│── connection.py                   # Gmail connection & helpers
│── inference_utils.py              # Inference-time cleaning
│
│── electron/                       # Electron desktop wrapper
│   ├── main.js                     # Electron entry point
│   ├── package.json                # Electron build config
│   └── assets/                     # App icons & resources
│
│── requirements.txt                # Python dependencies
│── README.md                       # Documentation

🔑 Setup Instructions
1. Clone the Repository

git clone https://github.com/yourusername/Email-Classification-Problem.git
cd Email-Classification-Problem

2. Set up Gmail API

-Go to Google Cloud Console
-Enable Gmail API
-Create OAuth client credentials → download credentials.json
-Place credentials.json in the project root

On first run, you’ll authenticate and generate a token.json for reuse.

3. Python Environment

Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt

4. Data Collection

Fetch emails from Gmail and save to CSV:
python read.py

Clean them:
python clean.py
python deepclean.py

Preprocess and vectorize:
python preprocessing.py

5. Model Training

Run your training script or notebook to train and evaluate models.
Best model can be saved as .pkl:
import joblib
joblib.dump(best_model, "email_sorting_model.pkl")

6. Run Streamlit App
streamlit run app.py

7. Run Desktop App (Electron)

Install Node.js dependencies:
cd electron
npm install
npm start

To build the desktop app:
npm run build

🧪 Models Used

-Logistic Regression
-Naive Bayes
-Random Forest
-Support Vector Machine (SVM)

Evaluation metrics include:

-Accuracy
-Precision
-Recall
-F1-Score
-Confusion Matrix

📊 Example Categories

-Academic → university notices, research updates
-Bills & Finance → bank statements, invoices
-News & Updates → newsletters, subscriptions
-Personal → personal conversations
-Official → workplace / corporate emails

🖼️ Screenshots
![Streamlit App - Screenshot](https://github.com/user-attachments/assets/42489995-cdf8-453b-8873-8dd75b30e719)


🛠️ Tech Stack

-Python (Pandas, Scikit-learn, NLTK, BeautifulSoup, Joblib)
-Streamlit (UI)
-Electron.js (Desktop wrapper)
-Gmail API (Email data source)

📜 License
No License
