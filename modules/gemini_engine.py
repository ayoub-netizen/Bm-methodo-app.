import streamlit as st
import google.generativeai as genai

MODEL_NAME = "gemini-1.5-pro-latest"

def _configure():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY manquante dans les secrets Streamlit.")
    genai.configure(api_key=api_key)

def analyze_methodology(methodology_text, site_context, annotations):
    _configure()
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
Tu es ingénieur travaux en tuyauterie industrielle.

Contexte du chantier :
{site_context}

Méthodologie :
{methodology_text}

Annotations du plan (JSON) :
{annotations}

Analyse la cohérence, signale les incohérences, propose des améliorations.
Structure la réponse en sections claires.
"""

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        raise RuntimeError(f"Erreur Gemini : {e}")

    if hasattr(response, "text"):
        return response.text

    return "Réponse reçue mais illisible."
