import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

def run_annotator(bg_image):
    st.subheader("🛠️ Module 2 : Annotation Technique")
    
    # Configuration des outils
    drawing_mode = st.sidebar.selectbox("Outil de dessin:", ("rect", "line", "point"))
    stroke_width = st.sidebar.slider("Épaisseur du trait:", 1, 10, 3)
    
    # Récupération dimensions
    w, h = bg_image.size
    # Ratio pour l'affichage (max 800px de large)
    display_width = 800
    ratio = display_width / w
    display_height = int(h * ratio)

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color="#FF0000",
        background_image=bg_image,
        update_streamlit=True,
        height=display_height,
        width=display_width,
        drawing_mode=drawing_mode,
        key="canvas",
    )

    annotations = []
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        for idx, obj in enumerate(objects):
            with st.expander(f"Annotation {idx+1} (Type: {obj['type']})", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    obj_id = st.text_input(f"ID Unique (ex: Z_GRUE)", key=f"id_{idx}").upper()
                with col2:
                    comment = st.text_input(f"Description technique", key=f"com_{idx}")
                
                # Conversion des coordonnées en coordonnées image originale
                data = {
                    "id": obj_id,
                    "type": obj["type"],
                    "coordinates": {
                        "x": int(obj["left"] / ratio),
                        "y": int(obj["top"] / ratio),
                        "width": int(obj["width"] / ratio) if "width" in obj else 0,
                        "height": int(obj["height"] / ratio) if "height" in obj else 0
                    },
                    "comment": comment
                }
                annotations.append(data)
    
    return annotations
