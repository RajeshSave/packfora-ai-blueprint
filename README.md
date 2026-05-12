# Packfora AI Blueprint — Streamlit App

A bespoke AI Transformation Blueprint dashboard for **Packfora LLP** — the global packaging consulting firm headquartered in Mumbai.

## 🚀 Features
- **42 AI use cases** across 8 business functions, customised for Packfora's packaging consulting model
- **Interactive sidebar filters** — Function, AI Type, Priority, Operational Cost, Phase
- **4 Tabs**: Blueprint Table · Analytics · 3-Year Runway · Priority Quick Wins
- **Gantt chart** of 16 key AI initiatives across 2025–2028
- **Packfora brand colours** (orange #F05A28 on dark) with Packfora logo
- **Downloadable CSV** of filtered use cases

## 📦 Local Setup

```bash
# 1. Clone / download this folder
cd packfora_ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

App opens at `http://localhost:8501`

## ☁️ Deploy on Streamlit Community Cloud (Free)

1. Push this folder to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub → **New app**
4. Select repo, branch `main`, file `app.py`
5. Click **Deploy** — live in ~2 minutes

Your app will be at: `https://your-app-name.streamlit.app`

## 📁 File Structure

```
packfora_ai/
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
└── .streamlit/
    └── config.toml         ← Streamlit theme (Packfora orange/dark)
```

## 🏢 About Packfora

Packfora is a global packaging consulting firm headquartered in Mumbai, Maharashtra.
Founded by six technocrats with 1000+ years of collective expertise, operating across
21 countries, serving 100+ clients in food, pharma, personal care and automotive sectors.

**Services**: Design to Value · Packaging Innovation · Sustainability · Supply Chain · MaxMold · Talent Flex

Website: [packfora.com](https://packfora.com)

---
*Built for Packfora's AI Transformation Initiative · 2025–2028*
