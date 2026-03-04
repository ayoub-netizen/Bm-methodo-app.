# modules/annotator.py

from io import BytesIO
from typing import Optional

import streamlit as st
from PIL import Image
from streamlit_drawable_canvas_fix import st_canvas  # si tu utilises le fork
# Si tu restes sur le package original :
# from streamlit_drawable_canvas import st_canvas


def _load_image_from_upload(uploaded_file) -> Optional[Image.Image]:
    """
    Charge l'image uploadée en mémoire (PIL.Image) pour éviter tout accès par URL
    et donc toute contrainte CORS côté navigateur/Fabric.js.
    """
    if uploaded_file is None:
        return None

    try:
        bytes_data = uploaded_file.read()
        img = Image.open(BytesIO(bytes_data))
        # On force un mode standard pour éviter certains soucis d'affichage
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        return img
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image : {e}")
        return None


def run_annotator(uploaded_file, key: str = "annotator_canvas"):
    """
    Affiche un canvas annotable avec l'image uploadée en fond.
    Retourne l'objet canvas (données de dessin + image).
    """
    st.subheader("Annotation du plan")

    img = _load_image_from_upload(uploaded_file)

    if img is None:
        st.info("Uploade un plan (PNG/JPEG) pour commencer l’annotation.")
        return None

    # Affichage de contrôle (debug visuel)
    with st.expander("Aperçu brut de l'image de fond"):
        st.image(img, caption="Image de fond utilisée pour le canvas", use_container_width=True)

    # Paramètres du canvas
    canvas_width = min(1200, img.width)
    # On garde le ratio de l'image
    ratio = img.height / img.width
    canvas_height = int(canvas_width * ratio)

    st.write("Tu peux dessiner directement sur le plan ci-dessous :")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=2,
        stroke_color="#ff0000",
        background_color=None,          # important : pas de couleur qui masque l'image
        background_image=img,           # image en mémoire → pas de CORS
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="freedraw",
        point_display_radius=0,
        key=key,
    )

    # canvas_result contient :
    # - image_data (numpy array)
    # - json_data (objets dessinés)
    return canvas_result
