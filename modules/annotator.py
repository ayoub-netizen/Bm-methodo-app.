import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

def run_annotator(bg_image):
    st.subheader("🛠️ Module 2 : Annotation Technique")
    
    # Configuration des outils dans la barre latérale
    drawing_mode = st.sidebar.selectbox("Outil:", ("rect", "line", "point"), key="tool")
    
    # Redimensionnement propre pour l'affichage
    w, h = bg_image.size
    display_width = 700
    ratio = display_width / w
    display_height = int(h * ratio)

    # LE CANVAS (C'est ici que l'erreur se produit d'habitude)
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
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
            st.markdown(f"---")
            col1, col2 = st.columns(2)
            with col1:
                obj_id = st.text_input(f"ID Zone {idx+1}", key=f"id_{idx}", placeholder="Ex: Z_GRUE").upper()
            with col2:
                comment = st.text_input(f"Description", key=f"com_{idx}", placeholder="Action à réaliser")
            
            annotations.append({
                "id": obj_id,
                "type": obj["type"],
                "coordinates": {
                    "x": int(obj["left"] / ratio),
                    "y": int(obj["top"] / ratio),
                    "width": int(obj.get("width", 0) / ratio),
                    "height": int(obj.get("height", 0) / ratio)
                },
                "comment": comment
            })
    
    return annotations
