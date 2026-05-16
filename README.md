# MediGuide AI 🏥
**Smart Medical Tourism & Healthcare Cost Intelligence Platform**

MediGuide AI is a complete, production-ready healthcare startup platform that provides AI-powered medical tourism cost estimates, hospital recommendations, intelligent symptom checking, and OCR-based medical document scanning.

## 🚀 Features
- **AI Cost Predictor**: Predicts full medical budgets using Machine Learning (`XGBoost`, `RandomForest`).
- **Hospital & Doctor Recommender**: Intelligent AI matching based on patient budget and conditions.
- **Medical Report OCR**: Built-in support for uploading and scanning reports (PDF/JPG) or capturing them live via webcam.
- **Voice-Enabled AI Chatbot**: Chat with an AI assistant via text or microphone.
- **Interactive Analytics**: Country-wise cost metrics, disease trends via `Plotly`.
- **Premium UI**: Glassmorphism cards, Lottie animations, custom sidebar, responsive layouts.
- **Security**: Full user authentication (SQLite), admin panel, secure environment variable support.

## 📦 Project Structure
```
medical_cost-main/
├── app.py                      # Thin entry point (page config + routing)
├── train.py                    # CLI to regenerate dataset + retrain pipelines
├── config.py                   # Centralized paths and constants
├── core/                       # Cross-cutting: CSS, session state, auth UI
│   ├── styling.py
│   ├── session.py
│   └── auth_ui.py
├── repositories/               # Data access layer (SQLite)
│   ├── db.py
│   ├── users.py
│   └── predictions.py
├── services/                   # Domain logic (no Streamlit imports)
│   ├── chatbot.py
│   ├── symptom_analyzer.py
│   ├── ocr.py
│   ├── recommendation.py
│   ├── currency.py
│   └── pdf_report.py
├── ml/                         # ML training + inference
│   ├── data_generator.py
│   ├── trainer.py
│   └── inference.py            # Single source of joblib.load
├── ui/
│   ├── components.py           # Reusable glass-card, metric-card, plotly theme, nav
│   └── pages/                  # One module per page
│       ├── dashboard.py
│       ├── prediction.py
│       ├── analytics.py
│       ├── recommendation.py
│       ├── ocr_page.py
│       ├── chatbot_page.py
│       └── packages.py
├── models/                     # Saved scikit-learn pipelines + categories.pkl
├── dataset.csv                 # Generated training data
├── mediguide.db                # SQLite database (users, predictions)
├── .streamlit/config.toml      # Theme + upload-size config
├── requirements.txt
├── packages.txt                # Apt-get packages (tesseract, poppler)
├── Dockerfile
└── render.yaml
```

## 🌐 How to Deploy on Streamlit Cloud
This repository is pre-configured and optimized for 1-click deployment on Streamlit Cloud.

### Step 1: Upload to GitHub
1. Initialize Git in this project folder: `git init`
2. Add all files: `git add .`
3. Commit the code: `git commit -m "Prepare for deployment"`
4. Push to your GitHub repository.

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Connect your GitHub account.
3. Select your repository and set the **Main file path** to `app.py`.
4. Click **Deploy!**

### Streamlit Cloud Settings & Permissions:
- Streamlit Cloud will automatically read `packages.txt` to install `tesseract-ocr` and `poppler-utils` required for the OCR functionality.
- It will read `requirements.txt` to install all Python packages.
- `.streamlit/config.toml` automatically applies the UI theme and increases the max file upload size.
- **Browser Permissions**: When users interact with the app, their browser will automatically prompt for **Camera** (for live prescription capture) and **Microphone** (for the AI Chatbot voice input). Ensure users grant these permissions.

## 💻 Local Setup
If you want to run this locally:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---
*Note: This is an AI-simulated platform. Not a replacement for real medical guidance.*
