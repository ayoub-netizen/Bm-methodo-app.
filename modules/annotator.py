from io import BytesIO
from typing import Optional

import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas


def _load_image(uploaded_file) -> Optional[Image.Image]:
    if uploaded_file is None:
        return None

    try:
        data = uploaded_file.read()
        img = Image.open(BytesIO(data))
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        return img
    except Exception as e:
        st.error(f"Erreur chargement image : {e}")
        return None


def run_annotator(uploaded_file, key="annotator_canvas"):
    st.subheader("Annotation du plan")

    img = _load_image(uploaded_file)

    if img is None:
        st.info("Importe un plan pour commencer.")
        return None

    canvas_width = min(1200, img.width)
    ratio = img.height / img.width
    canvas_height = int(canvas_width * ratio)

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=2,
        stroke_color="#ff0000",
        background_color=None,
        background_image=img,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="freedraw",
        key=key,
    )

    return canvas_result
