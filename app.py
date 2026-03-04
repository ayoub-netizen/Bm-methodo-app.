import streamlit as st
from PIL import Image
from modules.annotator import run_annotator
from modules.gemini_engine import analyze_methodology
from modules.generator import generate_sequence

st.set_page_config(page_title="BIM-Methodo Architect", layout="wide")

# --- CSS Custom ---
st.markdown("""<style>.stAlert {border: 2px solid #ff4b4b;}</style>""", unsafe_allow_html=True)

# --- Sidebar : Configuration ---
with st.sidebar:
    st.title("⚙️ Paramètres")
    api_key = st.text_input("Clé API Gemini", type="password")
    uploaded_file = st.file_uploader("Import Support (Plan/Photo)", type=['png', 'jpg', 'jpeg'])

# --- Session State ---
if 'analysis' not in st.session_state:
    st.session_state.analysis = None

# --- Main App Flow ---
if uploaded_file:
    image = Image.open(uploaded_file)
    
    tab1, tab2, tab3 = st.tabs(["1. Annotation", "2. Méthodologie & Cohérence", "3. Génération Séquencée"])

    with tab1:
        st.info("Dessinez les zones sur le plan et nommez-les avec des ID uniques.")
        current_annotations = run_annotator(image)
        st.session_state.annotations = current_annotations

    with tab2:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.subheader("Rédaction Méthodologique")
            methodo_text = st.text_area("Saisissez votre texte (Citez les ID entre crochets ou directement)", height=300)
        
        with col_m2:
            st.subheader("Validation Technique")
            if st.button("🔍 Analyser la Cohérence", use_container_width=True):
                if not api_key:
                    st.error("Veuillez saisir votre clé API.")
                else:
                    with st.spinner("Analyse sémantique en cours..."):
                        report = analyze_methodology(api_key, st.session_state.annotations, methodo_text)
                        st.session_state.analysis = report
                        
                        if report["coherence"]:
                            st.success("✅ Cohérence validée : Méthodologie conforme aux annotations.")
                        else:
                            st.error("❌ Incohérences détectées :")
                            for err in report["erreurs"]:
                                st.write(f"- {err}")

    with tab3:
        if st.session_state.analysis and st.session_state.analysis["coherence"]:
            st.subheader("Rendu de la Séquence")
            if st.button("🚀 Générer la Séquence Image par Image"):
                steps = st.session_state.analysis["etapes_identifiees"]
                images = generate_sequence(image, st.session_state.annotations, steps)
                
                for idx, img in enumerate(images):
                    st.write(f"Étape {idx+1} : {steps[idx]}")
                    st.image(img, use_column_width=True)
        else:
            st.warning("Veuillez d'abord valider la cohérence en Tab 2.")

else:
    st.title("🏗️ BIM-Methodo Architect")
    st.write("Veuillez uploader un plan ou une photo pour commencer.")
