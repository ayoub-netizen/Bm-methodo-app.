import streamlit as st
import google.generativeai as genai

# 🔥 Modèle compatible API actuelle
MODEL_NAME = "models/gemini-1.5-pro"   # ou "models/gemini-1.5-flash"


def _configure():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY manquante dans les secrets Streamlit.")

    # ❗️ NE PAS mettre api_version ici
    genai.configure(api_key=api_key)


def analyze_methodology(methodology_text, site_context, annotations):
    _configure()

    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config={
            "temperature": 0.4,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
    )

    prompt = f"""
Tu es ingénieur travaux spécialisé en tuyauterie industrielle.

Contexte du chantier :
{site_context}

Méthodologie proposée :
{methodology_text}

Annotations du plan (JSON) :
{annotations}

Analyse la cohérence technique, les risques, les incohérences, et propose des améliorations.
Structure ta réponse en sections claires.
"""

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        raise RuntimeError(f"Erreur Gemini : {e}")

    if hasattr(response, "text"):
        return response.text

    return "Réponse reçue mais illisible."
