import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import streamlit.components.v1 as components


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

    w, h = img.size

    html = f"""
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.2.4/fabric.min.js"></script>
    </head>
    <body>
        <canvas id="c" width="{w}" height="{h}" style="border:1px solid #ccc"></canvas>

        <script>
            const canvas = new fabric.Canvas('c');

            fabric.Image.fromURL("data:image/png;base64,{img_b64}", function(img) {{
                canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
            }});

            canvas.isDrawingMode = true;
            canvas.freeDrawingBrush.width = 3;
            canvas.freeDrawingBrush.color = "red";

            function sendData() {{
                const json = JSON.stringify(canvas.toJSON());
                window.parent.postMessage({{type: "canvas_json", data: json}}, "*");
            }}

            setInterval(sendData, 800);
        </script>
    </body>
    </html>
    """

    components.html(html, height=h + 20)

    # On stocke le JSON dans la session
    if "canvas_json" not in st.session_state:
        st.session_state["canvas_json"] = None

    return type("CanvasResult", (), {"json_data": st.session_state["canvas_json"]})
