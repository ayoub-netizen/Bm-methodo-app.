from PIL import Image, ImageDraw

def generate_sequence(bg_image, annotations, steps):
    output_images = []
    
    for i, step in enumerate(steps):
        # Créer une copie de l'image originale
        img_step = bg_image.copy()
        draw = ImageDraw.Draw(img_step)
        
        # Filtrer les annotations mentionnées dans cette étape (simplifié par ID)
        for ann in annotations:
            if ann["id"] in step:
                coord = ann["coordinates"]
                # Dessiner le rectangle de focus
                shape = [coord["x"], coord["y"], coord["x"] + coord["width"], coord["y"] + coord["height"]]
                draw.rectangle(shape, outline="red", width=10)
                draw.text((coord["x"], coord["y"]-20), ann["id"], fill="red")
        
        output_images.append(img_step)
        
    return output_images
