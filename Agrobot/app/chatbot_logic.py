from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from indictrans2 import IndicTranslator
from langdetect import detect
import numpy as np
from app import db, tf_model
from app.models import Disease
from PIL import Image
import os

translator = IndicTranslator()

def detect_language(text):
    try:
        lang_code = detect(text)
        if lang_code.startswith('hi'):
            return 'hi'
        elif lang_code.startswith('bn'):
            return 'bn'
        elif lang_code.startswith('te'):
            return 'te'
        elif lang_code.startswith('en'):
            return 'en'
        else:
            return 'en'  # fallback
    except:
        return 'en'

def translate_text(text, src_lang, tgt_lang):
    if src_lang == tgt_lang:
        return text
    try:
        translated = translator.translate(text, source_lang=src_lang, target_lang=tgt_lang)
        if isinstance(translated, list):
            return translated[0]
        else:
            return translated
    except Exception:
        return text

# Global variables for text prediction
symptom_en_texts = None
vectorizer_en = None
X_en = None
all_symptoms = []
symptom_to_disease = {}
symptom_langs = []

def init_chatbot():
    global symptom_en_texts, vectorizer_en, X_en, all_symptoms, symptom_to_disease, symptom_langs
    all_symptoms = []
    symptom_to_disease = {}
    symptom_langs = []
    for d in Disease.query.all():
        symptoms = {
            'en': d.symptom_en,
            'hi': d.symptom_hi,
            'bn': d.symptom_bn,
            'te': d.symptom_te
        }
        for lang, text in symptoms.items():
            if text:
                all_symptoms.append(text)
                symptom_to_disease[text] = d.name
                symptom_langs.append(lang)
    symptom_en_texts = [translate_text(s, lang, 'en') for s, lang in zip(all_symptoms, symptom_langs)]
    vectorizer_en = TfidfVectorizer()
    X_en = vectorizer_en.fit_transform(symptom_en_texts)

def predict_disease_text(symptom_input, preferred_lang):
    global symptom_en_texts, vectorizer_en, X_en
    if symptom_en_texts is None:
        init_chatbot()
    user_lang = detect_language(symptom_input)
    symptom_en = translate_text(symptom_input, user_lang, 'en')
    input_vec_en = vectorizer_en.transform([symptom_en])
    sim = cosine_similarity(input_vec_en, X_en)[0]
    idx = np.argmax(sim)
    confidence = sim[idx]
    matched_symptom_orig = all_symptoms[idx]
    matched_disease = symptom_to_disease[matched_symptom_orig]
    disease_local = translate_text(matched_disease, 'en', preferred_lang)
    disease_obj = Disease.query.filter_by(name=matched_disease).first()
    preventions = {
        'en': disease_obj.prevention_en,
        'hi': disease_obj.prevention_hi,
        'bn': disease_obj.prevention_bn,
        'te': disease_obj.prevention_te
    }
    prevention = preventions.get(preferred_lang)
    if prevention is None or not prevention:
        prevention = preventions.get('en', 'No prevention info available.')
        if preferred_lang != 'en':
            prevention = translate_text(prevention, 'en', preferred_lang)
    return disease_local, prevention, confidence

# Image prediction
image_size = (128, 128)
class_names = [
    'Pepper_Bell_Bacterial_Spot', 'Pepper_Bell_Healthy',
    'Potato_Early_Blight', 'Potato_Healthy', 'Potato_Late_Blight',
    'Tomato_Bacterial_Spot', 'Tomato_Early_Blight', 'Tomato_Healthy',
    'Tomato_Late_Blight', 'Tomato_Yellow_Leaf_Curl_Virus'
]

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize(image_size)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_disease_image(image_path, preferred_lang):
    if tf_model is None:
        return "Model not loaded", "Run train_model.py to generate model.h5", 0.0
    img_array = preprocess_image(image_path)
    pred_probs = tf_model.predict(img_array)[0]
    pred_class_idx = np.argmax(pred_probs)
    pred_class = class_names[pred_class_idx]
    pred_conf = pred_probs[pred_class_idx]
    
    disease_obj = Disease.query.filter_by(image_class_name=pred_class).first()
    if not disease_obj:
        disease_obj = Disease.query.filter_by(name=pred_class.replace('_', ' ')).first()
    if not disease_obj:
        return pred_class, "No treatment info available", pred_conf
    
    disease_local = translate_text(disease_obj.name, 'en', preferred_lang)
    preventions = {
        'en': disease_obj.prevention_en,
        'hi': disease_obj.prevention_hi,
        'bn': disease_obj.prevention_bn,
        'te': disease_obj.prevention_te
    }
    prevention = preventions.get(preferred_lang)
    if prevention is None or not prevention:
        prevention = preventions.get('en', 'No treatment info available.')
        if preferred_lang != 'en':
            prevention = translate_text(prevention, 'en', preferred_lang)
    return disease_local, prevention, pred_conf

# Output labels
output_labels = {
    'en': {
        'disease': 'Disease:',
        'prevention': 'Prevention/Treatment:',
        'confidence': 'Confidence:'
    },
    'hi': {
        'disease': 'रोग:',
        'prevention': 'रोकथाम/उपचार:',
        'confidence': 'विश्वास:'
    },
    'bn': {
        'disease': 'রোগ:',
        'prevention': 'প্রতিরোধ/চিকিৎসা:',
        'confidence': 'আত্মবিশ্বাস:'
    },
    'te': {
        'disease': 'రోగం:',
        'prevention': 'నివారణ/చికిత్స:',
        'confidence': 'నమ్మకం:'
    }
}