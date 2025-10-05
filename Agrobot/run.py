from app import app, db
from app.models import User, Disease
from werkzeug.security import generate_password_hash

# disease data of image classification model
disease_data = {
    "Pepper Bell Bacterial Spot": {
        "image_class_name": "Pepper_Bell_Bacterial_Spot",
        "symptom": {
            "en": "Small, water-soaked spots on leaves and fruits, turning dark brown to black.",
            "hi": "पत्तियों और फलों पर छोटे, पानी से भरे धब्बे, जो गहरे भूरे से काले हो जाते हैं।",
            "bn": "পাতা এবং ফলের উপর ছোট, জলমগ্ন দাগ, গাঢ় বাদামি থেকে কালো হয়ে যায়।",
            "te": "ఆకులు మరియు పండ్లపై చిన్న, నీటితో నిండిన మచ్చలు, గాఢ గోధుమ రంగు నుండి నలుపు రంగుకు మారతాయి."
        },
        "prevention": {
            "en": "Use disease-free seeds, remove infected plants, apply copper-based sprays, and practice crop rotation.",
            "hi": "रोगमुक्त बीजों का उपयोग करें, संक्रमित पौधों को हटाएं, तांबे पर आधारित स्प्रे का उपयोग करें, और फसल चक्र अपनाएं।",
            "bn": "রোগমুক্ত বীজ ব্যবহার করুন, আক্রান্ত গাছ সরান, তামা-ভিত্তিক স্প্রে প্রয়োগ করুন এবং ফসল আবর্তন করুন।",
            "te": "వ్యాధి రహిత విత్తనాలను ఉపయోగించండి, సంక్రమిత మొక్కలను తొలగించండి, రాగి ఆధారిత స్ప్రేలను వాడండి మరియు పంటల మార్పిడి చేయండి."
        }
    },
    "Pepper Bell Healthy": {
        "image_class_name": "Pepper_Bell_Healthy",
        "symptom": {
            "en": "No symptoms, leaves and fruits appear green and healthy.",
            "hi": "कोई लक्षण नहीं, पत्तियां और फल हरे और स्वस्थ दिखाई देते हैं।",
            "bn": "কোনো লক্ষণ নেই, পাতা এবং ফল সবুজ এবং স্বাস্থ্যকর দেখায়।",
            "te": "ఎటువంటి లక్షణాలు లేవు, ఆకులు మరియు పండ్లు ఆకుపచ్చగా మరియు ఆరోగ్యంగా కనిపిస్తాయి."
        },
        "prevention": {
            "en": "Maintain proper irrigation, fertilization, and pest control to keep plants healthy.",
            "hi": "पौधों को स्वस्थ रखने के लिए उचित सिंचाई, उर्वरक, और कीट नियंत्रण बनाए रखें।",
            "bn": "গাছ স্বাস্থ্যকর রাখতে সঠিক সেচ, সার প্রয়োগ এবং কীটপতঙ্গ নিয়ন্ত্রণ বজায় রাখুন।",
            "te": "మొక్కలను ఆరోగ్యంగా ఉంచడానికి సరైన నీటిపారుదల, ఎరువులు మరియు కీటకాల నియంత్రణ చేయండి."
        }
    },
    "Potato Early Blight": {
        "image_class_name": "Potato_Early_Blight",
        "symptom": {
            "en": "Dark brown to black spots with concentric rings on leaves.",
            "hi": "पत्तियों पर गहरे भूरे से काले धब्बे जिनमें संकेंद्रित वलय होते हैं।",
            "bn": "পাতায় গাঢ় বাদামি থেকে কালো দাগ, যার মধ্যে কেন্দ্রীভূত বলয় থাকে।",
            "te": "ఆకులపై గాఢ గోధుమ రంగు నుండి నల్లని మచ్చలు, కేంద్రీకృత వలయాలతో."
        },
        "prevention": {
            "en": "Remove infected leaves, apply fungicides like mancozeb, practice crop rotation, and improve airflow.",
            "hi": "संक्रमित पत्तियों को हटाएं, मैनकोजेब जैसे फफूंदनाशी लागू करें, फसल चक्र अपनाएं, और हवा का संचार सुधारें।",
            "bn": "আক্রান্ত পাতা সরান, ম্যানকোজেবের মতো ছত্রাকনাশক প্রয়োগ করুন, ফসল আবর্তন করুন, এবং বায়ু চলাচল উন্নত করুন।",
            "te": "సంక్రమిత ఆకులను తొలగించండి, మాన్కోజెబ్ వంటి ఫంగిసైడ్‌లను వాడండి, పంటల మార్పిడి చేయండి మరియు గాలి ప్రవాహం మెరుగుపరచండి."
        }
    },
    "Potato Healthy": {
        "image_class_name": "Potato_Healthy",
        "symptom": {
            "en": "No symptoms, leaves and tubers appear healthy.",
            "hi": "कोई लक्षण नहीं, पत्तियां और कंद स्वस्थ दिखाई देते हैं।",
            "bn": "কোনো লক্ষণ নেই, পাতা এবং কন্দ স্বাস্থ্যকর দেখায়।",
            "te": "ఎటువంటి లక్షణాలు లేవు, ఆకులు మరియు గడ్డలు ఆరోగ్యంగా కనిపిస్తాయి."
        },
        "prevention": {
            "en": "Use proper irrigation, balanced fertilization, and monitor for pests.",
            "hi": "उचित सिंचाई, संतुलित उर्वरक का उपयोग करें, और कीटों की निगरानी करें।",
            "bn": "সঠিক সেচ, সুষম সার প্রয়োগ করুন এবং কীটপতঙ্গের জন্য নজরদারি করুন।",
            "te": "సరైన నీటిపారుదల, సమతుల్య ఎరువులు వాడండి మరియు కీటకాల కోసం పర్యవేక్షించండి."
        }
    },
    "Potato Late Blight": {
        "image_class_name": "Potato_Late_Blight",
        "symptom": {
            "en": "Dark, water-soaked lesions on leaves, often with white mold.",
            "hi": "पत्तियों पर गहरे, पानी से भरे घाव, अक्सर सफेद फफूंद के साथ।",
            "bn": "পাতায় গাঢ়, জলমগ্ন ক্ষত, প্রায়শই সাদা ছাঁচের সাথে।",
            "te": "ఆకులపై గాఢమైన, నీటితో నిండిన గాయాలు, తరచుగా తెల్లని బూజుతో."
        },
        "prevention": {
            "en": "Apply fungicides, remove infected plants, ensure good air circulation, and avoid overhead watering.",
            "hi": "फफूंदनाशी लागू करें, संक्रमित पौधों को हटाएं, अच्छा वायु संचरण सुनिश्चित करें, और ऊपर से पानी देने से बचें।",
            "bn": "ছত্রাকনাশক প্রয়োগ করুন, আক্রান্ত গাছ সরান, ভালো বায়ু চলাচল নিশ্চিত করুন, এবং উপর থেকে জল দেওয়া এড়িয়ে চলুন।",
            "te": "ఫంగిసైడ్‌లను వాడండి, సంక్రమిత మొక్కలను తొలగించండి, మంచి గాలి ప్రసరణను నిర్ధారించండి మరియు పై నుండి నీరు పోయడం నివారించండి."
        }
    },
    "Tomato Bacterial Spot": {
        "image_class_name": "Tomato_Bacterial_Spot",
        "symptom": {
            "en": "Water-soaked lesions on leaves and fruits, turning dark with yellow halos.",
            "hi": "पत्तियों और फलों पर पानी से भरे घाव, जो पीले प्रभामंडल के साथ गहरे हो जाते हैं।",
            "bn": "পাতা এবং ফলের উপর জলমগ্ন ক্ষত, হলুদ বৃত্তের সাথে গাঢ় হয়ে যায়।",
            "te": "ఆకులు మరియు పండ్లపై నీటితో నిండిన గాయాలు, పసుపు వలయాలతో గాఢంగా మారతాయి."
        },
        "prevention": {
            "en": "Use resistant varieties, copper-based sprays, remove infected plants, and crop rotation.",
            "hi": "प्रतिरोधी किस्मों का उपयोग करें, तांबे पर आधारित स्प्रे का उपयोग करें, संक्रमित पौधों को हटाएं, और फसल चक्र अपनाएं।",
            "bn": "প্রতিরোধী জাত ব্যবহার করুন, তামা-ভিত্তিক স্প্রে ব্যবহার করুন, আক্রান্ত গাছ সরান, এবং ফসল আবর্তন করুন।",
            "te": "ప్రతిఘటించే రకాలను ఉపయోగించండి, రాగి ఆధారిత స్ప్రేలను వాడండి, సంక్రమిత మొక్కలను తొలగించండి మరియు పంటల మార్పిడి చేయండి."
        }
    },
    "Tomato Early Blight": {
        "image_class_name": "Tomato_Early_Blight",
        "symptom": {
            "en": "Dark spots with concentric rings on leaves, often yellowing around spots.",
            "hi": "पत्तियों पर गहरे धब्बे जिनमें संकेंद्रित वलय होते हैं, अक्सर धब्बों के आसपास पीला पड़ना।",
            "bn": "পাতায় গাঢ় দাগ, যার মধ্যে কেন্দ্রীভূত বলয় থাকে, প্রায়শই দাগের চারপাশে হলুদ হয়ে যায়।",
            "te": "ఆకులపై గాఢమైన మచ్చలు, కేంద్రీకృత వలయాలతో, తరచుగా మచ్చల చుట్టూ పసుపు రంగు."
        },
        "prevention": {
            "en": "Remove infected leaves, apply fungicides like mancozeb, practice crop rotation, and improve airflow.",
            "hi": "संक्रमित पत्तियों को हटाएं, मैनकोजेब जैसे फफूंदनाशी लागू करें, फसल चक्र अपनाएं, और हवा का संचार सुधारें।",
            "bn": "আক্রান্ত পাতা সরান, ম্যানকোজেবের মতো ছত্রাকনাশক প্রয়োগ করুন, ফসল আবর্তন করুন, এবং বায়ু চলাচল উন্নত করুন।",
            "te": "సంక్రమిత ఆకులను తొలగించండి, మాన్కోజెబ్ వంటి ఫంగిసైడ్‌లను వాడండి, పంటల మార్పిడి చేయండి మరియు గాలి ప్రవాహం మెరుగుపరచండి."
        }
    },
    "Tomato Healthy": {
        "image_class_name": "Tomato_Healthy",
        "symptom": {
            "en": "No symptoms, leaves and fruits appear healthy.",
            "hi": "कोई लक्षण नहीं, पत्तियां और फल स्वस्थ दिखाई देते हैं।",
            "bn": "কোনো লক্ষণ নেই, পাতা এবং ফল স্বাস্থ্যকর দেখায়।",
            "te": "ఎటువంటి లక్షణాలు లేవు, ఆకులు మరియు పండ్లు ఆరోగ్యంగా కనిపిస్తాయి."
        },
        "prevention": {
            "en": "Maintain proper irrigation, fertilization, and pest control.",
            "hi": "उचित सिंचाई, उर्वरक, और कीट नियंत्रण बनाए रखें।",
            "bn": "সঠিক সেচ, সার প্রয়োগ এবং কীটপতঙ্গ নিয়ন্ত্রণ বজায় রাখুন।",
            "te": "సరైన నీటిపారుదల, ఎరువులు మరియు కీటకాల నియంత్రణ చేయండి."
        }
    },
    "Tomato Late Blight": {
        "image_class_name": "Tomato_Late_Blight",
        "symptom": {
            "en": "Dark, water-soaked lesions on leaves and fruits, often with white mold.",
            "hi": "पत्तियों और फलों पर गहरे, पानी से भरे घाव, अक्सर सफेद फफूंद के साथ।",
            "bn": "পাতা এবং ফলের উপর গাঢ়, জলমগ্ন ক্ষত, প্রায়শই সাদা ছাঁচের সাথে।",
            "te": "ఆకులు మరియు పండ్లపై గాఢమైన, నీటితో నిండిన గాయాలు, తరచుగా తెల్లని బూజుతో."
        },
        "prevention": {
            "en": "Apply fungicides, remove infected plants, ensure good air circulation, and avoid overhead watering.",
            "hi": "फफूंदनाशी लागू करें, संक्रमित पौधों को हटाएं, अच्छा वायु संचरण सुनिश्चित करें, और ऊपर से पानी देने से बचें।",
            "bn": "ছত্রাকনাশক প্রয়োগ করুন, আক্রান্ত গাছ সরান, ভালো বায়ু চলাচল নিশ্চিত করুন, এবং উপর থেকে জল দেওয়া এড়িয়ে চলুন।",
            "te": "ఫంగిసైడ్‌లను వాడండి, సంక్రమిత మొక్కలను తొలగించండి, మంచి గాలి ప్రసరణను నిర్ధారించండి మరియు పై నుండి నీరు పోయడం నివారించండి."
        }
    },
    "Tomato Yellow Leaf Curl Virus": {
        "image_class_name": "Tomato_Yellow_Leaf_Curl_Virus",
        "symptom": {
            "en": "Yellowing and curling of leaves, stunted growth, reduced fruit yield.",
            "hi": "पत्तियों का पीला पड़ना और मुड़ना, विकास रुकना, फल उत्पादन में कमी।",
            "bn": "পাতা হলুদ হওয়া এবং কুঁকড়ে যাওয়া, বৃদ্ধি বন্ধ হওয়া, ফলের উৎপাদন হ্রাস।",
            "te": "ఆకులు పసుపు రంగులోకి మారడం మరియు ముడుచుకోవడం, పెరుగుదల మందగించడం, పండ్ల దిగుబడి తగ్గడం."
        },
        "prevention": {
            "en": "Use resistant varieties, control whiteflies with insecticides, remove infected plants, and use reflective mulches.",
            "hi": "प्रतिरोधी किस्मों का उपयोग करें, कीटनाशकों से सफेद मक्खियों को नियंत्रित करें, संक्रमित पौधों को हटाएं, और परावर्तक मल्च का उपयोग करें।",
            "bn": "প্রতিরোধী জাত ব্যবহার করুন, কীটনাশক দিয়ে সাদা মাছি নিয়ন্ত্রণ করুন, আক্রান্ত গাছ সরান, এবং প্রতিফলিত মালচ ব্যবহার করুন।",
            "te": "ప్రతిఘటించే రకాలను ఉపయోగించండి, కీటనాశకాలతో తెల్ల ఈగలను నియంత్రించండి, సంక్రమిత మొక్కలను తొలగించండి మరియు ప్రతిబింబ మల్చ్‌లను వాడండి."
        }
    },
    "Powdery Mildew": {
        "symptom": {
            "en": "white powdery spots on the leaves",
            "hi": "पत्तियों पर सफेद चूर्ण जैसे धब्बे",
            "bn": "পাতায় সাদা গুঁড়ো দাগ",
            "te": "ఆకులపై తెల్లటి పొడి మచ్చలు"
        },
        "prevention": {
            "en": "Ensure proper spacing, avoid overhead watering, and use fungicide.",
            "hi": "उचित दूरी सुनिश्चित करें, ऊपर से पानी देने से बचें और फफूंदनाशी का उपयोग करें।",
            "bn": "সঠিক দূরত্ব নিশ্চিত করুন, উপরে থেকে জল দেওয়া এড়িয়ে চলুন এবং ছত্রাকনাশক ব্যবহার করুন।",
            "te": "సరైన దూరం ఉంచండి, పై నుండి నీరు పోయడం నివారించండి మరియు ఫంగిసైడ్ వాడండి."
        }
    },
    "Leaf Spot": {
        "symptom": {
            "en": "dark spots on the leaves",
            "hi": "पत्तियों पर काले धब्बे",
            "bn": "পাতায় কালো দাগ",
            "te": "ఆకులపై నల్ల మచ్చలు"
        },
        "prevention": {
            "en": "Remove infected leaves, rotate crops, and use copper-based sprays.",
            "hi": "संक्रमित पत्ते हटाएं, फसल चक्र अपनाएं और तांबे पर आधारित स्प्रे का उपयोग करें।",
            "bn": "আক্রান্ত পাতা সরান, ফসল আবর্তন করুন এবং তামা-ভিত্তিক স্প্রে ব্যবহার করুন।",
            "te": "సంక్రామిత ఆకులను తీసివేయండి, పంటల మార్పిడి చేయండి మరియు రాగి స్ప్రే వాడండి."
        }
    },
    "Rust": {
        "symptom": {
            "en": "orange pustules on the leaves",
            "hi": "पत्तियों पर नारंगी फफोले",
            "bn": "পাতায় কমলা ফোসকা",
            "te": "ఆకులపై నారింజ బుడగలు"
        },
        "prevention": {
            "en": "Use resistant varieties, remove infected leaves, and apply fungicide.",
            "hi": "प्रतिरोधी किस्मों का उपयोग करें, संक्रमित पत्तों को हटाएं और फफूंदनाशी का प्रयोग करें।",
            "bn": "প্রতিরোধী জাত ব্যবহার করুন, আক্রান্ত পাতা সরান এবং ছত্রাকনাশক প্রয়োগ করুন।",
            "te": "ప్రతిఘటించే రకాలను ఉపయోగించండి, సంక్రామిత ఆకులను తొలగించండి మరియు ఫంగిసైడ్ వాడండి."
        }
    },
    "Downy Mildew": {
        "symptom": {
            "en": "yellow angular spots on the leaves",
            "hi": "पत्तियों पर पीले कोणीय धब्बे",
            "bn": "পাতায় হলুদ কোণার দাগ",
            "te": "ఆకులపై పసుపు మచ్చలు"
        },
        "prevention": {
            "en": "Improve air circulation, avoid overhead watering, and use fungicide.",
            "hi": "हवा का संचार बढ़ाएं, ऊपर से पानी देने से बचें और फफूंदनाशी का उपयोग करें।",
            "bn": "বায়ু চলাচল বাড়ান, উপরে থেকে জল দেওয়া এড়িয়ে চলুন এবং ছত্রাকনাশক ব্যবহার করুন।",
            "te": "గాలి ప్రవాహం మెరుగుపరచండి, పై నుండి నీరు పోయడం నివారించండి మరియు ఫంగిసైడ్ వాడండి."
        }
    },
    "Fusarium Wilt": {
        "symptom": {
            "en": "yellowing and wilting of the leaves",
            "hi": "पत्तियों का पीला पड़ना और मुरझाना",
            "bn": "পাতা হলুদ হয়ে যাওয়া এবং মুরঝিয়ে যাওয়া",
            "te": "ఆకులు పసుపు రంగులోకి మారడం మరియు వాడిపోవడం"
        },
        "prevention": {
            "en": "Plant resistant varieties and practice crop rotation.",
            "hi": "प्रतिरोधी किस्मों का उपयोग करें और फसल चक्र अपनाएं।",
            "bn": "প্রতিরোধী জাত ব্যবহার করুন এবং ফসল আবর্তন করুন।",
            "te": "ప్రతిఘటించే రకాలను ఉపయోగించండి మరియు పంటల మార్పిడి చేయండి."
        }
    },
    "Bacterial Spot": {
        "symptom": {
            "en": "water-soaked lesions on the leaves",
            "hi": "पत्तियों पर पानी से भीगे हुए धब्बे",
            "bn": "পাতায় পানিতে ভেজা দাগ",
            "te": "ఆకులపై నీటితో నిండి ఉన్న మచ్చలు"
        },
        "prevention": {
            "en": "Remove infected leaves, use certified disease-free seeds, and rotate crops.",
            "hi": "संक्रमित पत्ते हटाएं, प्रमाणित रोगमुक्त बीज का उपयोग करें और फसल चक्र अपनाएं।",
            "bn": "আক্রান্ত পাতা সরান, শংসাপত্রপ্রাপ্ত রোগমুক্ত বীজ ব্যবহার করুন এবং ফসল আবর্তন করুন।",
            "te": "సంక్రామిత ఆకులను తీసివేయండి, సర్టిఫైడ్ రోగరహిత బీజాలు ఉపయోగించండి మరియు పంటల మార్పిడి చేయండి."
        }
    },
    "Leaf Curl": {
        "symptom": {
            "en": "curling of the leaves",
            "hi": "पत्तियों का मुड़ना",
            "bn": "পাতা কুঁকড়ে যাওয়া",
            "te": "ఆకులు ముడుచుకోవడం"
        },
        "prevention": {
            "en": "Avoid overhead irrigation and use resistant varieties.",
            "hi": "ऊपर से सिंचाई से बचें और प्रतिरोधी किस्मों का उपयोग करें।",
            "bn": "উপর থেকে সেচ দেওয়া এড়িয়ে চলুন এবং প্রতিরোধী জাত ব্যবহার করুন।",
            "te": "పై నుండి నీరు పోయడం నివారించండి మరియు ప్రతిఘటించే రకాలను ఉపయోగించండి."
        }
    },
    "Blossom End Rot": {
        "symptom": {
            "en": "black, sunken spots on the blossom end of fruit",
            "hi": "फलों के निचले सिरे पर काले और धंसे हुए धब्बे",
            "bn": "ফলের নিচের অংশে কালো, ধসে পড়া দাগ",
            "te": "పండ్ల చివరలో నల్లని, లోపలికి పోయిన మచ్చలు"
        },
        "prevention": {
            "en": "Ensure proper watering and calcium supplementation.",
            "hi": "सही पानी की व्यवस्था और कैल्शियम का उपयोग सुनिश्चित करें।",
            "bn": "সঠিক সেচ এবং ক্যালসিয়াম প্রদান নিশ্চিত করুন।",
            "te": "సరైన నీటిపారుదల మరియు కాల్షియం ఇచ్చే సమర్ధన చేయండి."
        }
    },
    "Verticillium Wilt": {
        "symptom": {
            "en": "stunted growth and yellowing of leaves",
            "hi": "विकास रुक जाना और पत्तों का पीला पड़ना",
            "bn": "বৃদ্ধি বন্ধ হয়ে যাওয়া এবং পাতার হলুদ হওয়া",
            "te": "పెరుగుదల మందగించడం మరియు ఆకులు పసుపు రంగులోకి మారడం"
        },
        "prevention": {
            "en": "Use resistant varieties and practice crop rotation.",
            "hi": "प्रतिरोधी किस्मों का उपयोग करें और फसल चक्र अपनाएं।",
            "bn": "প্রতিরোধী জাত ব্যবহার করুন এবং ফসল আবর্তন করুন।",
            "te": "ప్రతిఘటించే రకాలను ఉపయోగించండి మరియు పంటల మార్పిడి చేయండి."
        }
    }
}
with app.app_context():
    db.create_all()
    # Create default admin if not exists
    if User.query.filter_by(username='admin').first() is None:
        admin = User(username='admin', is_admin=True)
        admin.set_password('adminpass')  # Change this password!
        db.session.add(admin)
        db.session.commit()
    # Seed diseases if not exist
    for name, info in disease_data.items():
        if Disease.query.filter_by(name=name).first() is None:
            disease = Disease(
                name=name,
                image_class_name=info.get('image_class_name', ''),
                symptom_en=info['symptom'].get('en', ''),
                symptom_hi=info['symptom'].get('hi', ''),
                symptom_bn=info['symptom'].get('bn', ''),
                symptom_te=info['symptom'].get('te', ''),
                prevention_en=info['prevention'].get('en', ''),
                prevention_hi=info['prevention'].get('hi', ''),
                prevention_bn=info['prevention'].get('bn', ''),
                prevention_te=info['prevention'].get('te', '')
            )
            db.session.add(disease)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)