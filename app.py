import streamlit as st
from modules.annotator import run_annotator
from modules.gemini_engine import analyze_methodology

st.set_page_config(
    page_title="Annotateur & Analyse IA",
    layout="wide",
)

# ---------------------------------------------------------
# SIDEBAR — UPLOAD & PARAMÈTRES
# ---------------------------------------------------------
st.sidebar.header("📁 Import du plan")
uploaded_file = st.sidebar.file_uploader(
    "Choisir un plan (PNG / JPG)", type=["png", "jpg", "jpeg"]
)

st.sidebar.header("📝 Méthodologie")
methodology_text = st.sidebar.text_area(
    "Décris ta méthodologie d’intervention",
    height=200,
)

st.sidebar.header("🏗️ Contexte du chantier")
site_context = st.sidebar.text_area(
    "Décris le contexte du chantier",
    height=150,
)

# ---------------------------------------------------------
# PAGE PRINCIPALE — ANNOTATION
# ---------------------------------------------------------
st.title("🧰 Annotateur de plans + Analyse IA Gemini")

st.markdown(
    """
    Cette application permet :
    1. D’annoter un plan de chantier (dessin libre).
    2. D’analyser la cohérence de ta méthodologie via **Gemini 1.5**.
    """
)

canvas_result = run_annotator(uploaded_file)

# ---------------------------------------------------------
# ANALYSE IA
# ---------------------------------------------------------
st.markdown("---")
st.header("🤖 Analyse IA de la méthodologie")

if st.button("Lancer l’analyse IA"):

    if uploaded_file is None:
        st.error("Tu dois d’abord importer un plan.")
    elif canvas_result is None:
        st.error("Le canvas n’a pas encore été généré.")
    elif not methodology_text.strip():
        st.error("La méthodologie est vide.")
    else:
        with st.spinner("Analyse en cours avec Gemini 1.5…"):

            annotations = canvas_result.json_data

            try:
                result = analyze_methodology(
                    methodology_text=methodology_text,
                    site_context=site_context,
                    annotations=annotations,
                )
                st.success("Analyse terminée.")
                st.markdown(result)

            except Exception as e:
                st.error(f"Erreur lors de l’appel à Gemini : {e}")
