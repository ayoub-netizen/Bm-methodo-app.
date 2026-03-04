import streamlit as st
from PIL import Image
from io import BytesIO
import base64


def run_annotator(uploaded_file, key="annotator_canvas"):
    st.subheader("Annotation du plan")

    if uploaded_file is None:
        st.info("Importe un plan pour commencer.")
        return None

    # Charger l'image
    img = Image.open(uploaded_file)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode()

    # Canvas HTML + Fabric.js
    st.markdown(
        f"""
        <canvas id="c" width="{img.width}" height="{img.height}" 
                style="border:1px solid #ccc"></canvas>

        <script>
        const canvas = new fabric.Canvas('c');
        fabric.Image.fromURL("data:image/png;base64,{img_b64}", function(img) {{
            canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
        }});

        canvas.isDrawingMode = true;
        canvas.freeDrawingBrush.width = 3;
        canvas.freeDrawingBrush.color = "red";

        function exportCanvas() {{
            const json = canvas.toJSON();
            const py = window.parent.streamlitPython;
            py.sendJson(json);
        }}

        setInterval(exportCanvas, 1000);
        </script>
        """,
        unsafe_allow_html=True,
    )

    # Récupération JSON envoyée par JS
    annotations = st.session_state.get("canvas_json", None)
    return type("CanvasResult", (), {"json_data": annotations})
