from modules.annotator import run_annotator

uploaded_file = st.file_uploader("Plan de chantier", type=["png", "jpg", "jpeg"])
canvas_result = run_annotator(uploaded_file)
