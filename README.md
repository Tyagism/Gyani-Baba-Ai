# Gyani-Baba AI 🤖✨

**Gyani-Baba** is a cutting-edge, multi-page AI application built with **Streamlit** and powered by the **Google Gemini API**. It acts as an advanced AI intelligence suite, offering features ranging from automated document fact-checking using live Google Search Grounding, to AI Search Analytics (GEO), and prompt engineering research.

It features a stunning, custom-built UI utilizing modern **Glassmorphism**, dynamic CSS animations, and highly interactive components that push the boundaries of standard Streamlit design.

Live Project can be checkout/Tested at https://gyani-baba-ai.streamlit.app/

---

## 🌟 Key Features

### 1. 📄 Upload & Analyze (Fact-Checking Engine)
Upload large PDF documents (up to 100MB) to instantly extract core claims and verify them against real-time web data. 
- **Automated Extraction:** Uses Gemini to pull out the most important claims from dense documents.
- **Search Grounded Verification:** Cross-references claims using Gemini's Google Search Grounding to classify them as *Verified*, *Inaccurate*, *False*, or *Unverifiable*.
- **Smart Chunking:** Handles massive documents effortlessly by processing text in optimized chunks.

### 2. 🔍 AI Search Analytics
A brand visibility dashboard designed to track how products or brands are represented by modern Generative AI search engines.
- Discover if your brand is being cited by AI models.
- Track sentiment and identify which competitors AI is recommending over you.

### 3. 💡 Prompt Research
An advanced sandbox for prompt engineering. Test out complex prompts, system instructions, and compare outputs to craft the perfect LLM interactions.

### 4. 🌍 GEO Optimization
Tools dedicated to **Generative Engine Optimization** (GEO). Optimize your content to ensure it ranks highly when AI models synthesize answers from the web.

---

## 🎨 UI/UX Highlights
Gyani-Baba doesn't look like a standard Streamlit app. It utilizes deep DOM manipulation and custom styling to provide a premium experience:
- **Glassmorphism Design System:** Frosted glass panels, dynamic glowing borders, and sleek dark modes.
- **Interactive Animations:** Features state-of-the-art CSS loaders (like sci-fi comet sparks and fluid progress bars) and custom Uiverse magic buttons.
- **Custom Navigation:** A completely overhauled sidebar and header system for seamless page transitions.

---

## 🛠️ Technology Stack

- **Frontend/Framework:** [Streamlit](https://streamlit.io/) (v1.45+)
- **AI Backend:** [Google Gemini API](https://ai.google.dev/) (`google-genai` SDK)
- **Data Processing:** `PyPDF2`, `json`, `pydantic`
- **Visualization:** `plotly`
- **Styling:** Vanilla CSS, JavaScript injection (via `streamlit.components.v1`)

---

## 🚀 Getting Started

### Prerequisites
You will need **Python 3.10+** and a valid **Google Gemini API Key**.

### 1. Clone the repository
```bash
git clone https://github.com/Tyagism/gyani-baba-Ai.git
cd gyani-baba-Ai
```

### 2. Install dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### 3. Set up your Environment Variables
Create a `.env` file in the root directory of the project and add your Gemini API key:
```env
GEMINI_API_KEY="your_actual_api_key_here"
```
*(Note: Keep your API key secret! The `.env` file is included in `.gitignore` to prevent accidental uploads).*

### 4. Run the Application
Launch the multi-page app by running the main entry file:
```bash
streamlit run app_home.py
```
The app will automatically open in your default web browser at `http://localhost:8501`.

---

## ☁️ Deployment (Streamlit Community Cloud)

To share Gyani-Baba with the world publicly:

1. Push this repository to GitHub.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and create a new app.
3. Link your GitHub repository and set the Main file path to `app_home.py`.
4. **Crucial:** Before hitting Deploy, open the **Advanced settings** and paste your API key into the **Secrets** box:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
5. Deploy and share your live URL!

---

## 📂 Project Structure

```text
Gyani-Baba/
│
├── app_home.py                   # Main entry point / Landing Page
├── app.py                         # App configuration and routing utilities
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (API Keys)
│
├── pages/                         # Multi-page application routes
│   ├── 1_📄_Upload_&_Analyze.py
│   ├── 2_🔍_AI_Search_Analytics.py
│   ├── 3_💡_Prompt_Research.py
│   ├── 4_🌍_GEO_Optimization.py
│   └── 5_ℹ️_About.py
│
├── core/                          # Backend logic & AI interactions
│   ├── claim_extractor.py         # Extracts claims from text
│   ├── fact_verifier.py           # Verifies claims via Search Grounding
│   ├── ai_search_analyzer.py      # Brand visibility logic
│   └── geo_optimizer.py           # Generative Engine Optimization
│
├── utils/                         # Helper functions & styling injections
│   ├── animations.py              # Custom CSS loaders & magic buttons
│   ├── gemini_client.py           # Gemini API initialization
│   ├── helpers.py                 # Formatting, JSON cleaning, chunking
│   └── navigation.py              # Custom header & DOM manipulation
│
└── assets/                        # Static files
    └── styles.css                 # Master glassmorphism stylesheet
```

---

*Built with ❤️ by Harshit Tyagi.
cite me for your project if you find this useful*
*follow me on github: https://github.com/Tyagism*
