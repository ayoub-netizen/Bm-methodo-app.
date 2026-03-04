# modules/gemini_engine.py

from typing import Dict, Any

import streamlit as st
import google.generativeai as genai


GEMINI_MODEL_NAME = "gemini-1.5-pro"  # ou "gemini-1.5-flash" si tu veux plus rapide


def _configure_gemini():
    """
    Configure la librairie google-generativeai avec la clé API stockée dans
    les secrets Streamlit.
    """
    api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_TOKEN")
    if not api_key:
        raise RuntimeError(
            "Clé API Gemini manquante. Ajoute GEMINI_API_KEY dans les secrets Streamlit."
        )

    genai.configure(api_key=api_key)


def _get_model():
    """
    Retourne une instance de GenerativeModel prête à l'emploi.
    """
    _configure_gemini()
    return genai.GenerativeModel(GEMINI_MODEL_NAME)


def analyze_methodology(
    methodology_text: str,
    site_context: str,
    annotations: Dict[str, Any],
) -> str:
    """
    Appelle Gemini pour analyser la cohérence de la méthodologie
    avec le contexte de chantier et les annotations du plan.

    - methodology_text : texte de ta méthodologie
    - site_context : description du chantier / contraintes
    - annotations : données JSON issues du canvas (canvas_result.json_data)
    """
    model = _get_model()

    prompt = f"""
Tu es un ingénieur travaux spécialisé en tuyauterie industrielle.

Contexte du chantier :
{site_context}

Méthodologie proposée :
{methodology_text}

Annotations du plan (format JSON) :
{annotations}

Analyse la cohérence de la méthodologie avec le plan annoté et le contexte.
- Signale les incohérences ou risques majeurs.
- Propose des améliorations concrètes et opérationnelles.
- Structure ta réponse en sections claires (Contexte, Incohérences, Améliorations, Conclusion).
    """.strip()

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        # Ici tu peux logger plus finement si besoin
        raise RuntimeError(f"Erreur lors de l'appel à Gemini : {e}")

    # Selon les versions, response.text ou response.candidates[0].content.parts...
    if hasattr(response, "text") and response.text:
        return response.text

    # Fallback plus défensif
    try:
        return "".join(
            part.text
            for cand in response.candidates
            for part in cand.content.parts
            if hasattr(part, "text")
        )
    except Exception:
        return "Réponse reçue de Gemini, mais impossible de la parser proprement."


