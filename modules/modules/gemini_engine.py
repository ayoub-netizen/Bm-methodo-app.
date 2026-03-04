import google.generativeai as genai
import json

def analyze_methodology(api_key, annotations, text_methodo):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    En tant qu'expert en ingénierie BTP, analyse la cohérence entre les annotations JSON et la méthodologie rédigée.
    
    ANNOTATIONS (JSON):
    {json.dumps(annotations)}
    
    MÉTHODOLOGIE:
    {text_methodo}
    
    RÈGLES CRITIQUES:
    1. Chaque ID cité dans le texte DOIT exister dans le JSON.
    2. Chaque ID du JSON DOIT être utilisé au moins une fois dans le texte.
    3. L'ordre des étapes doit respecter la logique de sécurité (ex: pas de grue avant fondation).
    4. Répondre STRICTEMENT au format JSON : 
    {{"coherence": bool, "erreurs": [], "etapes_identifiees": []}}
    """
    
    response = model.generate_content(prompt)
    try:
        # Nettoyage de la réponse si Gemini ajoute des backticks
        clean_res = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_res)
    except:
        return {"coherence": False, "erreurs": ["Erreur de parsing IA"], "etapes_identifiees": []}
