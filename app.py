"""
╔═══════════════════════════════════════════════════════════════╗
║       SMART CROP ADVISORY SYSTEM FOR SMALL & MARGINAL FARMERS ║
║       Built with Streamlit | AI-Powered | Voice Enabled        ║
╚═══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import json
import base64
import io
import datetime
import requests
from PIL import Image

# Plotly imports with clear error message if missing
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    st.error("❌ Missing package: plotly. Please add `plotly>=5.17.0` to your requirements.txt and redeploy.")
    st.stop()

# ─── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="🌾 Smart Crop Advisory",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── LANGUAGE TRANSLATIONS ──────────────────────────────────────
TRANSLATIONS = {
    "English": {
        "app_title": "🌾 Smart Crop Advisory System",
        "app_subtitle": "AI-Powered Farming Intelligence for Every Farmer",
        "language": "🌐 Language",
        "dashboard": "🏠 Dashboard",
        "crop_rec": "🌱 Crop Recommendation",
        "disease": "🔬 Disease Scanner",
        "weather": "🌤️ Weather Advice",
        "market": "📈 Market Prices",
        "irrigation": "💧 Irrigation Planner",
        "fertilizer": "🧪 Fertilizer Guide",
        "pest": "🐛 Pest Warning",
        "rotation": "🔄 Crop Rotation",
        "library": "📚 Crop Library",
        "chatbot": "🤖 AI Chatbot",
        "analytics": "📊 Farm Analytics",
        "satellite": "🛰️ Satellite Monitor",
        "drone": "🚁 Drone Scout",
        "tips": "💡 Daily Tips",
        "seasonal": "📅 Seasonal Guide",
        "welcome": "Welcome, Farmer!",
        "listen": "🔊 Listen",
        "submit": "Get Recommendation",
        "loading": "Analyzing...",
        "soil_type": "Soil Type",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "rainfall": "Rainfall (mm)",
        "season": "Season",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "location": "Location / District",
        "upload_image": "Upload Plant Image",
        "scan_disease": "Scan for Disease",
        "crop_name": "Crop Name",
        "best_crop": "🏆 Best Recommended Crop",
        "alt_crops": "🌿 Alternative Crops",
        "expected_yield": "📦 Expected Yield",
        "est_profit": "💰 Estimated Profit",
        "treat_advice": "💊 Treatment Advice",
        "severity": "⚠️ Severity",
        "pesticide": "🧴 Recommended Pesticide",
        "disease_name": "🦠 Disease Detected",
        "healthy": "✅ Plant is Healthy!",
        "ask_question": "Ask me anything about farming...",
        "send": "Send",
        "generating": "Generating advice...",
        "schemes": "🏛️ Govt Schemes",
        "loan": "💰 Loan & Insurance",
        "about": "👥 About / Team",
        "weather_api_key": "OpenWeatherMap API Key",
        "enter_api_key": "Enter your free API key from openweathermap.org",
    },
    "Hindi": {
        "app_title": "🌾 स्मार्ट फसल सलाहकार प्रणाली",
        "app_subtitle": "हर किसान के लिए AI-संचालित कृषि बुद्धिमत्ता",
        "language": "🌐 भाषा",
        "dashboard": "🏠 डैशबोर्ड",
        "crop_rec": "🌱 फसल अनुशंसा",
        "disease": "🔬 रोग स्कैनर",
        "weather": "🌤️ मौसम सलाह",
        "market": "📈 बाजार भाव",
        "irrigation": "💧 सिंचाई योजना",
        "fertilizer": "🧪 उर्वरक गाइड",
        "pest": "🐛 कीट चेतावनी",
        "rotation": "🔄 फसल चक्र",
        "library": "📚 फसल पुस्तकालय",
        "chatbot": "🤖 AI चैटबॉट",
        "analytics": "📊 फार्म विश्लेषण",
        "satellite": "🛰️ उपग्रह निगरानी",
        "drone": "🚁 ड्रोन स्काउट",
        "tips": "💡 दैनिक सुझाव",
        "seasonal": "📅 मौसमी गाइड",
        "welcome": "स्वागत है, किसान भाई!",
        "listen": "🔊 सुनें",
        "submit": "अनुशंसा प्राप्त करें",
        "loading": "विश्लेषण हो रहा है...",
        "soil_type": "मिट्टी का प्रकार",
        "temperature": "तापमान (°C)",
        "humidity": "आर्द्रता (%)",
        "rainfall": "वर्षा (मिमी)",
        "season": "मौसम",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फास्फोरस (P)",
        "potassium": "पोटेशियम (K)",
        "location": "स्थान / जिला",
        "upload_image": "पौधे की तस्वीर अपलोड करें",
        "scan_disease": "रोग स्कैन करें",
        "crop_name": "फसल का नाम",
        "best_crop": "🏆 सर्वश्रेष्ठ अनुशंसित फसल",
        "alt_crops": "🌿 वैकल्पिक फसलें",
        "expected_yield": "📦 अपेक्षित उपज",
        "est_profit": "💰 अनुमानित लाभ",
        "treat_advice": "💊 उपचार सलाह",
        "severity": "⚠️ गंभीरता",
        "pesticide": "🧴 अनुशंसित कीटनाशक",
        "disease_name": "🦠 पहचानी गई बीमारी",
        "healthy": "✅ पौधा स्वस्थ है!",
        "ask_question": "खेती के बारे में कुछ भी पूछें...",
        "send": "भेजें",
        "generating": "सलाह तैयार हो रही है...",
    },
    "Telugu": {
        "app_title": "🌾 స్మార్ట్ పంట సలహా వ్యవస్థ",
        "app_subtitle": "ప్రతి రైతుకు AI-ఆధారిత వ్యవసాయ మేధస్సు",
        "language": "🌐 భాష",
        "dashboard": "🏠 డాష్‌బోర్డ్",
        "crop_rec": "🌱 పంట సిఫార్సు",
        "disease": "🔬 వ్యాధి స్కానర్",
        "weather": "🌤️ వాతావరణ సలహా",
        "market": "📈 మార్కెట్ ధరలు",
        "irrigation": "💧 నీటిపారుదల ప్లానర్",
        "fertilizer": "🧪 ఎరువుల గైడ్",
        "pest": "🐛 పురుగుల హెచ్చరిక",
        "rotation": "🔄 పంట మార్పిడి",
        "library": "📚 పంట లైబ్రరీ",
        "chatbot": "🤖 AI చాట్‌బాట్",
        "analytics": "📊 వ్యవసాయ విశ్లేషణలు",
        "satellite": "🛰️ ఉపగ్రహ పర్యవేక్షణ",
        "drone": "🚁 డ్రోన్ స్కౌట్",
        "tips": "💡 రోజువారీ చిట్కాలు",
        "seasonal": "📅 సీజనల్ గైడ్",
        "welcome": "స్వాగతం, రైతు!",
        "listen": "🔊 వినండి",
        "submit": "సిఫార్సు పొందండి",
        "loading": "విశ్లేషిస్తోంది...",
        "soil_type": "నేల రకం",
        "temperature": "ఉష్ణోగ్రత (°C)",
        "humidity": "తేమ (%)",
        "rainfall": "వర్షపాతం (మిమీ)",
        "season": "సీజన్",
        "nitrogen": "నత్రజని (N)",
        "phosphorus": "భాస్వరం (P)",
        "potassium": "పొటాషియం (K)",
        "location": "స్థానం / జిల్లా",
        "upload_image": "మొక్క చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "scan_disease": "వ్యాధి స్కాన్ చేయండి",
        "crop_name": "పంట పేరు",
        "best_crop": "🏆 ఉత్తమ సిఫార్సు చేసిన పంట",
        "alt_crops": "🌿 ప్రత్యామ్నాయ పంటలు",
        "expected_yield": "📦 అంచనా దిగుబడి",
        "est_profit": "💰 అంచనా లాభం",
        "treat_advice": "💊 చికిత్స సలహా",
        "severity": "⚠️ తీవ్రత",
        "pesticide": "🧴 సిఫార్సు చేసిన పురుగుమందు",
        "disease_name": "🦠 వ్యాధి గుర్తించబడింది",
        "healthy": "✅ మొక్క ఆరోగ్యంగా ఉంది!",
        "ask_question": "వ్యవసాయం గురించి ఏదైనా అడగండి...",
        "send": "పంపండి",
        "generating": "సలహా రూపొందిస్తోంది...",
    },
    "Bengali": {
        "app_title": "🌾 স্মার্ট ফসল পরামর্শ সিস্টেম",
        "app_subtitle": "প্রতিটি কৃষকের জন্য AI-চালিত কৃষি বুদ্ধিমত্তা",
        "language": "🌐 ভাষা",
        "dashboard": "🏠 ড্যাশবোর্ড",
        "crop_rec": "🌱 ফসল সুপারিশ",
        "disease": "🔬 রোগ স্ক্যানার",
        "weather": "🌤️ আবহাওয়া পরামর্শ",
        "market": "📈 বাজার মূল্য",
        "irrigation": "💧 সেচ পরিকল্পনা",
        "fertilizer": "🧪 সার গাইড",
        "pest": "🐛 কীটপতঙ্গ সতর্কতা",
        "rotation": "🔄 ফসল আবর্তন",
        "library": "📚 ফসল লাইব্রেরি",
        "chatbot": "🤖 AI চ্যাটবট",
        "analytics": "📊 খামার বিশ্লেষণ",
        "satellite": "🛰️ স্যাটেলাইট মনিটর",
        "drone": "🚁 ড্রোন স্কাউট",
        "tips": "💡 দৈনিক টিপস",
        "seasonal": "📅 মৌসুমী গাইড",
        "welcome": "স্বাগতম, কৃষক ভাই!",
        "listen": "🔊 শুনুন",
        "submit": "সুপারিশ পান",
        "loading": "বিশ্লেষণ করা হচ্ছে...",
        "soil_type": "মাটির ধরন",
        "temperature": "তাপমাত্রা (°C)",
        "humidity": "আর্দ্রতা (%)",
        "rainfall": "বৃষ্টিপাত (মিমি)",
        "season": "ঋতু",
        "nitrogen": "নাইট্রোজেন (N)",
        "phosphorus": "ফসফরাস (P)",
        "potassium": "পটাসিয়াম (K)",
        "location": "অবস্থান / জেলা",
        "upload_image": "গাছের ছবি আপলোড করুন",
        "scan_disease": "রোগ স্ক্যান করুন",
        "crop_name": "ফসলের নাম",
        "best_crop": "🏆 সেরা সুপারিশকৃত ফসল",
        "alt_crops": "🌿 বিকল্প ফসল",
        "expected_yield": "📦 প্রত্যাশিত ফলন",
        "est_profit": "💰 আনুমানিক লাভ",
        "treat_advice": "💊 চিকিৎসা পরামর্শ",
        "severity": "⚠️ তীব্রতা",
        "pesticide": "🧴 প্রস্তাবিত কীটনাশক",
        "disease_name": "🦠 রোগ সনাক্ত হয়েছে",
        "healthy": "✅ গাছটি সুস্থ!",
        "ask_question": "চাষাবাদ সম্পর্কে যেকোনো প্রশ্ন করুন...",
        "send": "পাঠান",
        "generating": "পরামর্শ তৈরি হচ্ছে...",
    },
    "Tamil": {
        "app_title": "🌾 ஸ்மார்ட் பயிர் ஆலோசனை அமைப்பு",
        "app_subtitle": "ஒவ்வொரு விவசாயிக்கும் AI-இயக்கப்பட்ட விவசாய நுண்ணறிவு",
        "language": "🌐 மொழி",
        "dashboard": "🏠 டாஷ்போர்டு",
        "crop_rec": "🌱 பயிர் பரிந்துரை",
        "disease": "🔬 நோய் ஸ்கேனர்",
        "weather": "🌤️ வானிலை அறிவுரை",
        "market": "📈 சந்தை விலைகள்",
        "irrigation": "💧 நீர்ப்பாசன திட்டம்",
        "fertilizer": "🧪 உர வழிகாட்டி",
        "pest": "🐛 பூச்சி எச்சரிக்கை",
        "rotation": "🔄 பயிர் சுழற்சி",
        "library": "📚 பயிர் நூலகம்",
        "chatbot": "🤖 AI சாட்பாட்",
        "analytics": "📊 பண்ணை பகுப்பாய்வு",
        "satellite": "🛰️ செயற்கைக்கோள் கண்காணிப்பு",
        "drone": "🚁 ட்ரோன் ஸ்கவுட்",
        "tips": "💡 தினசரி குறிப்புகள்",
        "seasonal": "📅 பருவகால வழிகாட்டி",
        "welcome": "வரவேற்கிறோம், விவசாயி!",
        "listen": "🔊 கேளுங்கள்",
        "submit": "பரிந்துரை பெறுங்கள்",
        "loading": "பகுப்பாய்வு செய்கிறது...",
        "soil_type": "மண் வகை",
        "temperature": "வெப்பநிலை (°C)",
        "humidity": "ஈரப்பதம் (%)",
        "rainfall": "மழைப்பொழிவு (மிமீ)",
        "season": "பருவம்",
        "nitrogen": "நைட்ரஜன் (N)",
        "phosphorus": "பாஸ்பரஸ் (P)",
        "potassium": "பொட்டாசியம் (K)",
        "location": "இடம் / மாவட்டம்",
        "upload_image": "தாவர படம் பதிவேற்றவும்",
        "scan_disease": "நோய் ஸ்கேன் செய்யுங்கள்",
        "crop_name": "பயிர் பெயர்",
        "best_crop": "🏆 சிறந்த பரிந்துரைக்கப்பட்ட பயிர்",
        "alt_crops": "🌿 மாற்று பயிர்கள்",
        "expected_yield": "📦 எதிர்பார்க்கப்படும் விளைச்சல்",
        "est_profit": "💰 மதிப்பிடப்பட்ட லாபம்",
        "treat_advice": "💊 சிகிச்சை அறிவுரை",
        "severity": "⚠️ தீவிரம்",
        "pesticide": "🧴 பரிந்துரைக்கப்பட்ட பூச்சிக்கொல்லி",
        "disease_name": "🦠 கண்டறியப்பட்ட நோய்",
        "healthy": "✅ தாவரம் ஆரோக்கியமாக உள்ளது!",
        "ask_question": "விவசாயம் பற்றி எதுவும் கேளுங்கள்...",
        "send": "அனுப்பு",
        "generating": "அறிவுரை உருவாக்கப்படுகிறது...",
    },
    "Marathi": {
        "app_title": "🌾 स्मार्ट पीक सल्लागार प्रणाली",
        "app_subtitle": "प्रत्येक शेतकऱ्यासाठी AI-चालित कृषी बुद्धिमत्ता",
        "language": "🌐 भाषा",
        "dashboard": "🏠 डॅशबोर्ड",
        "crop_rec": "🌱 पीक शिफारस",
        "disease": "🔬 रोग स्कॅनर",
        "weather": "🌤️ हवामान सल्ला",
        "market": "📈 बाजार भाव",
        "irrigation": "💧 सिंचन योजना",
        "fertilizer": "🧪 खत मार्गदर्शक",
        "pest": "🐛 कीड चेतावनी",
        "rotation": "🔄 पीक फेरपालट",
        "library": "📚 पीक ग्रंथालय",
        "chatbot": "🤖 AI चॅटबॉट",
        "analytics": "📊 शेत विश्लेषण",
        "satellite": "🛰️ उपग्रह निरीक्षण",
        "drone": "🚁 ड्रोन स्काउट",
        "tips": "💡 दैनिक टिप्स",
        "seasonal": "📅 हंगामी मार्गदर्शक",
        "welcome": "स्वागत आहे, शेतकरी!",
        "listen": "🔊 ऐका",
        "submit": "शिफारस मिळवा",
        "loading": "विश्लेषण सुरू आहे...",
        "soil_type": "मातीचा प्रकार",
        "temperature": "तापमान (°C)",
        "humidity": "आर्द्रता (%)",
        "rainfall": "पाऊस (मिमी)",
        "season": "हंगाम",
        "nitrogen": "नायट्रोजन (N)",
        "phosphorus": "फॉस्फरस (P)",
        "potassium": "पोटॅशियम (K)",
        "location": "स्थान / जिल्हा",
        "upload_image": "झाडाचा फोटो अपलोड करा",
        "scan_disease": "रोग स्कॅन करा",
        "crop_name": "पिकाचे नाव",
        "best_crop": "🏆 सर्वोत्तम शिफारस केलेले पीक",
        "alt_crops": "🌿 पर्यायी पिके",
        "expected_yield": "📦 अपेक्षित उत्पादन",
        "est_profit": "💰 अंदाजे नफा",
        "treat_advice": "💊 उपचार सल्ला",
        "severity": "⚠️ तीव्रता",
        "pesticide": "🧴 शिफारस केलेले कीटकनाशक",
        "disease_name": "🦠 ओळखलेला रोग",
        "healthy": "✅ झाड निरोगी आहे!",
        "ask_question": "शेतीबद्दल काहीही विचारा...",
        "send": "पाठवा",
        "generating": "सल्ला तयार होत आहे...",
    },
    "Kannada": {
        "app_title": "🌾 ಸ್ಮಾರ್ಟ್ ಬೆಳೆ ಸಲಹಾ ವ್ಯವಸ್ಥೆ",
        "app_subtitle": "ಪ್ರತಿ ರೈತರಿಗೆ AI-ಚಾಲಿತ ಕೃಷಿ ಬುದ್ಧಿಮತ್ತೆ",
        "language": "🌐 ಭಾಷೆ",
        "dashboard": "🏠 ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "crop_rec": "🌱 ಬೆಳೆ ಶಿಫಾರಸು",
        "disease": "🔬 ರೋಗ ಸ್ಕ್ಯಾನರ್",
        "weather": "🌤️ ಹವಾಮಾನ ಸಲಹೆ",
        "market": "📈 ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು",
        "irrigation": "💧 ನೀರಾವರಿ ಯೋಜನೆ",
        "fertilizer": "🧪 ರಸಗೊಬ್ಬರ ಮಾರ್ಗದರ್ಶಿ",
        "pest": "🐛 ಕೀಟ ಎಚ್ಚರಿಕೆ",
        "rotation": "🔄 ಬೆಳೆ ಪರಿವರ್ತನೆ",
        "library": "📚 ಬೆಳೆ ಗ್ರಂಥಾಲಯ",
        "chatbot": "🤖 AI ಚಾಟ್‌ಬಾಟ್",
        "analytics": "📊 ಫಾರ್ಮ್ ವಿಶ್ಲೇಷಣೆ",
        "satellite": "🛰️ ಉಪಗ್ರಹ ಮೇಲ್ವಿಚಾರಣೆ",
        "drone": "🚁 ಡ್ರೋನ್ ಸ್ಕೌಟ್",
        "tips": "💡 ದೈನಂದಿನ ಸಲಹೆಗಳು",
        "seasonal": "📅 ಋತುಮಾನ ಮಾರ್ಗದರ್ಶಿ",
        "welcome": "ಸ್ವಾಗತ, ರೈತ!",
        "listen": "🔊 ಕೇಳಿ",
        "submit": "ಶಿಫಾರಸು ಪಡೆಯಿರಿ",
        "loading": "ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
        "soil_type": "ಮಣ್ಣಿನ ಪ್ರಕಾರ",
        "temperature": "ತಾಪಮಾನ (°C)",
        "humidity": "ತೇವಾಂಶ (%)",
        "rainfall": "ಮಳೆ (ಮಿಮೀ)",
        "season": "ಋತು",
        "nitrogen": "ನೈಟ್ರೋಜನ್ (N)",
        "phosphorus": "ಫಾಸ್ಫರಸ್ (P)",
        "potassium": "ಪೊಟ್ಯಾಸಿಯಂ (K)",
        "location": "ಸ್ಥಳ / ಜಿಲ್ಲೆ",
        "upload_image": "ಸಸ್ಯದ ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "scan_disease": "ರೋಗ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ",
        "crop_name": "ಬೆಳೆ ಹೆಸರು",
        "best_crop": "🏆 ಅತ್ಯುತ್ತಮ ಶಿಫಾರಸು ಬೆಳೆ",
        "alt_crops": "🌿 ಪರ್ಯಾಯ ಬೆಳೆಗಳು",
        "expected_yield": "📦 ನಿರೀಕ್ಷಿತ ಇಳುವರಿ",
        "est_profit": "💰 ಅಂದಾಜು ಲಾಭ",
        "treat_advice": "💊 ಚಿಕಿತ್ಸೆ ಸಲಹೆ",
        "severity": "⚠️ ತೀವ್ರತೆ",
        "pesticide": "🧴 ಶಿಫಾರಸು ಕೀಟನಾಶಕ",
        "disease_name": "🦠 ಪತ್ತೆಯಾದ ರೋಗ",
        "healthy": "✅ ಸಸ್ಯ ಆರೋಗ್ಯಕರವಾಗಿದೆ!",
        "ask_question": "ಕೃಷಿ ಬಗ್ಗೆ ಏನಾದರೂ ಕೇಳಿ...",
        "send": "ಕಳುಹಿಸಿ",
        "generating": "ಸಲಹೆ ರಚಿಸಲಾಗುತ್ತಿದೆ...",
    },
    "Gujarati": {
        "app_title": "🌾 સ્માર્ટ પાક સલાહ સિસ્ટમ",
        "app_subtitle": "દરેક ખેડૂત માટે AI-સંચાલિત કૃષિ બુદ્ધિ",
        "language": "🌐 ભાષા",
        "dashboard": "🏠 ડેશબોર્ડ",
        "crop_rec": "🌱 પાક ભલામણ",
        "disease": "🔬 રોગ સ્કેનર",
        "weather": "🌤️ હવામાન સલાહ",
        "market": "📈 બજાર ભાવ",
        "irrigation": "💧 સિંચાઈ યોજના",
        "fertilizer": "🧪 ખાતર માર્ગદર્શિકા",
        "pest": "🐛 જીવાત ચેતવણી",
        "rotation": "🔄 પાક ફેરફાર",
        "library": "📚 પાક પુસ્તકાલય",
        "chatbot": "🤖 AI ચેટબોટ",
        "analytics": "📊 ખેત વિશ્લેષણ",
        "satellite": "🛰️ ઉપગ્રહ નિગરાની",
        "drone": "🚁 ડ્રોન સ્કાઉટ",
        "tips": "💡 રોજની ટીપ્સ",
        "seasonal": "📅 મોસમી માર્ગદર્શિકા",
        "welcome": "સ્વાગત છે, ખેડૂત!",
        "listen": "🔊 સાંભળો",
        "submit": "ભલામણ મેળવો",
        "loading": "વિશ્લેષણ થઈ રહ્યું છે...",
        "soil_type": "જમીનનો પ્રકાર",
        "temperature": "તાપમાન (°C)",
        "humidity": "ભેજ (%)",
        "rainfall": "વરસાદ (mm)",
        "season": "ઋતુ",
        "nitrogen": "નાઇટ્રોજન (N)",
        "phosphorus": "ફોસ્ફરસ (P)",
        "potassium": "પોટેશિયમ (K)",
        "location": "સ્થળ / જિલ્લો",
        "upload_image": "છોડની તસ્વીર અપલોડ કરો",
        "scan_disease": "રોગ સ્કેન કરો",
        "crop_name": "પાકનું નામ",
        "best_crop": "🏆 શ્રેષ્ઠ ભલામણ કરેલ પાક",
        "alt_crops": "🌿 વૈકલ્પિક પાક",
        "expected_yield": "📦 અપેક્ષિત ઉત્પાદન",
        "est_profit": "💰 અંદાજિત નફો",
        "treat_advice": "💊 સારવાર સલાહ",
        "severity": "⚠️ ગંભીરતા",
        "pesticide": "🧴 ભલામણ કીટનાશક",
        "disease_name": "🦠 ઓળખાયેલ રોગ",
        "healthy": "✅ છોડ સ્વસ્થ છે!",
        "ask_question": "ખેતી વિશે કંઈ પણ પૂછો...",
        "send": "મોકલો",
        "generating": "સલાહ તૈયાર થઈ રહી છે...",
    },
}

# ─── CROP DATA ───────────────────────────────────────────────────
CROP_DATABASE = {
    "Rice": {
        "scientific": "Oryza sativa", "season": ["Kharif"],
        "soil": "Clay loam", "water": "High (1200–2000 mm)",
        "temp_range": "20–35°C", "duration": "90–150 days",
        "fertilizer": "NPK 120:60:40 kg/ha", "yield": "4–6 tonnes/ha",
        "market_price": 1800, "pests": ["Stem Borer", "Brown Plant Hopper"],
        "profit_range": "₹25,000–45,000/ha", "icon": "🌾"
    },
    "Wheat": {
        "scientific": "Triticum aestivum", "season": ["Rabi"],
        "soil": "Loamy", "water": "Medium (450–650 mm)",
        "temp_range": "10–25°C", "duration": "110–130 days",
        "fertilizer": "NPK 120:60:40 kg/ha", "yield": "3–5 tonnes/ha",
        "market_price": 2200, "pests": ["Aphids", "Rust"],
        "profit_range": "₹30,000–55,000/ha", "icon": "🌿"
    },
    "Maize": {
        "scientific": "Zea mays", "season": ["Kharif", "Rabi"],
        "soil": "Well-drained loamy", "water": "Medium (500–800 mm)",
        "temp_range": "18–32°C", "duration": "80–110 days",
        "fertilizer": "NPK 150:75:50 kg/ha", "yield": "5–8 tonnes/ha",
        "market_price": 1900, "pests": ["Fall Armyworm", "Stem Borer"],
        "profit_range": "₹35,000–60,000/ha", "icon": "🌽"
    },
    "Cotton": {
        "scientific": "Gossypium hirsutum", "season": ["Kharif"],
        "soil": "Black cotton soil", "water": "Medium (700–1000 mm)",
        "temp_range": "21–35°C", "duration": "150–180 days",
        "fertilizer": "NPK 100:50:50 kg/ha", "yield": "2–4 tonnes/ha",
        "market_price": 6500, "pests": ["Bollworm", "Whitefly"],
        "profit_range": "₹40,000–80,000/ha", "icon": "☁️"
    },
    "Sugarcane": {
        "scientific": "Saccharum officinarum", "season": ["Year Round"],
        "soil": "Deep loamy", "water": "High (1500–2500 mm)",
        "temp_range": "20–38°C", "duration": "300–360 days",
        "fertilizer": "NPK 250:100:100 kg/ha", "yield": "60–100 tonnes/ha",
        "market_price": 310, "pests": ["Pyrilla", "Scale Insect"],
        "profit_range": "₹60,000–1,20,000/ha", "icon": "🎋"
    },
    "Groundnut": {
        "scientific": "Arachis hypogaea", "season": ["Kharif", "Rabi"],
        "soil": "Sandy loam", "water": "Low (500–700 mm)",
        "temp_range": "20–30°C", "duration": "100–130 days",
        "fertilizer": "NPK 25:50:75 kg/ha", "yield": "1.5–3 tonnes/ha",
        "market_price": 5500, "pests": ["Leaf Miner", "Tikka Disease"],
        "profit_range": "₹30,000–55,000/ha", "icon": "🥜"
    },
    "Tomato": {
        "scientific": "Solanum lycopersicum", "season": ["Year Round"],
        "soil": "Well-drained sandy loam", "water": "Medium (600–800 mm)",
        "temp_range": "15–30°C", "duration": "60–90 days",
        "fertilizer": "NPK 120:80:60 kg/ha", "yield": "20–40 tonnes/ha",
        "market_price": 1200, "pests": ["Whitefly", "Fruit Borer"],
        "profit_range": "₹50,000–1,20,000/ha", "icon": "🍅"
    },
    "Onion": {
        "scientific": "Allium cepa", "season": ["Rabi", "Kharif"],
        "soil": "Loamy", "water": "Low-Medium (350–550 mm)",
        "temp_range": "12–24°C", "duration": "100–120 days",
        "fertilizer": "NPK 100:50:100 kg/ha", "yield": "15–25 tonnes/ha",
        "market_price": 1500, "pests": ["Thrips", "Purple Blotch"],
        "profit_range": "₹40,000–80,000/ha", "icon": "🧅"
    },
    "Soybean": {
        "scientific": "Glycine max", "season": ["Kharif"],
        "soil": "Well-drained loamy", "water": "Medium (600–900 mm)",
        "temp_range": "20–32°C", "duration": "85–110 days",
        "fertilizer": "NPK 30:80:40 kg/ha", "yield": "1.5–3 tonnes/ha",
        "market_price": 4500, "pests": ["Girdle Beetle", "Yellow Mosaic"],
        "profit_range": "₹25,000–50,000/ha", "icon": "🫘"
    },
    "Potato": {
        "scientific": "Solanum tuberosum", "season": ["Rabi"],
        "soil": "Sandy loam", "water": "Medium (500–700 mm)",
        "temp_range": "10–25°C", "duration": "75–100 days",
        "fertilizer": "NPK 180:80:100 kg/ha", "yield": "20–35 tonnes/ha",
        "market_price": 800, "pests": ["Late Blight", "Aphids"],
        "profit_range": "₹40,000–90,000/ha", "icon": "🥔"
    },
}

# ─── DISEASE DATABASE ────────────────────────────────────────────
DISEASES = {
    "Leaf Rust": {
        "severity": "High", "color": "🔴",
        "symptoms": "Orange-brown pustules on leaves",
        "treatment": "Apply Mancozeb 2.5g/L or Propiconazole 1mL/L. Remove infected leaves immediately.",
        "pesticide": "Mancozeb 75% WP @ 2.5 kg/ha",
        "prevention": "Use resistant varieties, crop rotation, avoid overhead irrigation",
        "listen_text": "Leaf Rust detected! High severity. Apply Mancozeb fungicide at 2.5 grams per litre of water. Remove all infected leaves immediately and avoid overhead irrigation."
    },
    "Bacterial Spot": {
        "severity": "Medium", "color": "🟡",
        "symptoms": "Water-soaked spots turning brown with yellow halos",
        "treatment": "Spray Copper Oxychloride 3g/L. Avoid working in wet conditions.",
        "pesticide": "Copper Oxychloride 50% WP @ 3 kg/ha",
        "prevention": "Use disease-free seeds, avoid wet field operations",
        "listen_text": "Bacterial Spot detected! Medium severity. Spray Copper Oxychloride at 3 grams per litre. Avoid working in wet field conditions."
    },
    "Powdery Mildew": {
        "severity": "Medium", "color": "🟡",
        "symptoms": "White powdery growth on leaf surfaces",
        "treatment": "Apply Sulfur 80% WP at 3g/L. Improve air circulation.",
        "pesticide": "Wettable Sulfur 80% WP @ 3 kg/ha",
        "prevention": "Adequate spacing, avoid excess nitrogen, resistant varieties",
        "listen_text": "Powdery Mildew detected! Medium severity. Apply Sulfur fungicide at 3 grams per litre of water. Ensure proper spacing for air circulation."
    },
    "Early Blight": {
        "severity": "High", "color": "🔴",
        "symptoms": "Concentric ring pattern dark spots on older leaves",
        "treatment": "Apply Chlorothalonil 2g/L or Iprodione 2mL/L every 7–10 days.",
        "pesticide": "Chlorothalonil 75% WP @ 2 kg/ha",
        "prevention": "Crop rotation, remove crop debris, avoid overhead irrigation",
        "listen_text": "Early Blight detected! High severity. Apply Chlorothalonil fungicide at 2 grams per litre every 7 to 10 days. Practice crop rotation for prevention."
    },
    "Downy Mildew": {
        "severity": "High", "color": "🔴",
        "symptoms": "Yellow patches on upper leaf surface, grey mould below",
        "treatment": "Apply Metalaxyl + Mancozeb 2.5g/L. Ensure good drainage.",
        "pesticide": "Metalaxyl 8% + Mancozeb 64% WP @ 2.5 kg/ha",
        "prevention": "Improve drainage, use resistant varieties, seed treatment",
        "listen_text": "Downy Mildew detected! High severity. Apply Metalaxyl plus Mancozeb at 2.5 grams per litre. Ensure good field drainage immediately."
    },
    "Yellow Mosaic Virus": {
        "severity": "Very High", "color": "🔴",
        "symptoms": "Yellow-green mosaic pattern on leaves, stunted growth",
        "treatment": "No chemical cure. Remove infected plants. Control whitefly vectors with Imidacloprid.",
        "pesticide": "Imidacloprid 17.8% SL @ 250 mL/ha for vector control",
        "prevention": "Use virus-free seeds, control whitefly, use reflective mulches",
        "listen_text": "Yellow Mosaic Virus detected! Very high severity. Remove infected plants immediately. Spray Imidacloprid to control whitefly which spreads the virus."
    },
    "Healthy": {
        "severity": "None", "color": "🟢",
        "symptoms": "No disease symptoms detected",
        "treatment": "No treatment required. Continue regular monitoring.",
        "pesticide": "No pesticide needed",
        "prevention": "Maintain current good farming practices",
        "listen_text": "Great news! Your plant appears healthy. No disease detected. Continue with regular monitoring and good farming practices."
    },
}

# ─── PESTS DATABASE ──────────────────────────────────────────────
PESTS = {
    "Fall Armyworm": {
        "crops": ["Maize", "Sorghum", "Rice"],
        "symptoms": "Ragged leaf edges, frass in whorl, window-pane feeding",
        "severity": "🔴 High",
        "prevention": "Early planting, push-pull technology, neem-based sprays",
        "treatment": "Emamectin benzoate 5% SG @ 200g/ha, Spinosad 45% SC @ 125mL/ha",
        "season": "Kharif"
    },
    "Brown Plant Hopper": {
        "crops": ["Rice"],
        "symptoms": "Hopper burn, circular patches of wilted plants",
        "severity": "🔴 High",
        "prevention": "Avoid excess nitrogen, use resistant varieties, alternate flooding",
        "treatment": "Buprofezin 25% SC @ 1L/ha or Imidacloprid 200SL @ 250mL/ha",
        "season": "Kharif"
    },
    "Whitefly": {
        "crops": ["Cotton", "Tomato", "Chilli"],
        "symptoms": "Yellowing leaves, honeydew secretion, sooty mould",
        "severity": "🟡 Medium",
        "prevention": "Yellow sticky traps, reflective mulches, avoid dusty conditions",
        "treatment": "Thiamethoxam 25 WG @ 100g/ha or Spiromesifen 240 SC",
        "season": "Year Round"
    },
    "Aphids": {
        "crops": ["Wheat", "Mustard", "Potato"],
        "symptoms": "Curling leaves, sticky honeydew, stunted growth",
        "severity": "🟡 Medium",
        "prevention": "Natural enemies, neem sprays, avoid late planting",
        "treatment": "Thiamethoxam 25 WG @ 100g/ha or Dimethoate 30EC @ 1L/ha",
        "season": "Rabi"
    },
    "Bollworm": {
        "crops": ["Cotton", "Tomato", "Okra"],
        "symptoms": "Bored bolls and fruits, frass visible, internal damage",
        "severity": "🔴 High",
        "prevention": "Pheromone traps, Bt cotton varieties, crop rotation",
        "treatment": "Chlorantraniliprole 18.5 SC @ 150mL/ha or Indoxacarb 14.5 SC",
        "season": "Kharif"
    },
    "Red Spider Mite": {
        "crops": ["Cotton", "Brinjal", "Beans"],
        "symptoms": "Fine webbing, yellow stippled leaves, bronzing",
        "severity": "🟡 Medium",
        "prevention": "Regular scouting, avoid dusty conditions, conserve predators",
        "treatment": "Abamectin 1.9 EC @ 750mL/ha or Spiromesifen 240 SC @ 250mL/ha",
        "season": "Summer"
    },
}

# ─── DAILY TIPS ──────────────────────────────────────────────────
DAILY_TIPS = [
    {"tip": "Test your soil pH before planting. Ideal pH is 6.0–7.5 for most crops.", "category": "Soil Health", "icon": "🌱"},
    {"tip": "Avoid spraying pesticides during rain or strong winds — it wastes chemicals and harms environment.", "category": "Pesticide Safety", "icon": "☔"},
    {"tip": "Use drip irrigation to save up to 50% water compared to flood irrigation.", "category": "Water Saving", "icon": "💧"},
    {"tip": "Apply neem cake @ 200 kg/ha to repel soil-borne pests and enrich nutrients.", "category": "Organic Farming", "icon": "🌿"},
    {"tip": "Rotate crops every season to break pest cycles and improve soil health naturally.", "category": "Crop Rotation", "icon": "🔄"},
    {"tip": "Apply lime to acidic soils (pH below 6.0) to improve nutrient availability.", "category": "Soil Management", "icon": "⚗️"},
    {"tip": "Sow seeds in lines for better sunlight, easier weeding, and higher yields.", "category": "Good Practices", "icon": "📏"},
    {"tip": "Add green manure like Dhaincha before paddy to add 80–100 kg N/ha naturally.", "category": "Organic Inputs", "icon": "♻️"},
    {"tip": "Monitor crops every 3–4 days during early growth stages to catch pest problems early.", "category": "Pest Management", "icon": "🔍"},
    {"tip": "Use certified seeds — they give 20–30% higher yield than local seeds.", "category": "Seed Quality", "icon": "🌱"},
    {"tip": "Split nitrogen fertilizer into 3 doses: basal, tillering, and panicle initiation stages.", "category": "Fertilizer Management", "icon": "🧪"},
    {"tip": "Set up light traps during night to monitor and control flying insects effectively.", "category": "Pest Monitoring", "icon": "💡"},
    {"tip": "Mulching reduces soil moisture loss by 30–40% and suppresses weed growth.", "category": "Water Management", "icon": "🍂"},
    {"tip": "Store seeds in sealed containers with dried neem leaves to prevent storage pests.", "category": "Post-Harvest", "icon": "📦"},
    {"tip": "Intercrop legumes with cereals to fix nitrogen and improve land use efficiency.", "category": "Intercropping", "icon": "🫘"},
]

# ─── CHATBOT RESPONSES ───────────────────────────────────────────
CHATBOT_KNOWLEDGE = {
    "rice": "🌾 Rice grows best in clay loam soil with pH 5.5–7.0. It needs 1200–2000mm water. Best season is Kharif (June–November). Apply NPK @ 120:60:40 kg/ha. Common pests include Stem Borer and Brown Plant Hopper.",
    "wheat": "🌿 Wheat is a Rabi crop grown November–April. Loamy soil, pH 6.0–7.5 is ideal. Needs 450–650mm water. Apply NPK @ 120:60:40 kg/ha. Watch for Rust disease and Aphids.",
    "fertilizer": "🧪 For most crops, follow the NPK ratio. Apply basal dose at sowing, top-dressing at tillering. Use organic manure (FYM @ 10 tonnes/ha) before sowing. Test soil first for best results.",
    "disease": "🔬 For plant diseases: 1) Remove infected plants immediately, 2) Apply recommended fungicide, 3) Improve drainage, 4) Avoid overhead irrigation, 5) Use disease-resistant varieties next season.",
    "irrigation": "💧 Irrigation tip: Use soil finger test — insert finger 2 inches into soil; if dry, irrigate. Critical stages needing water: germination, flowering, grain filling. Drip irrigation saves 40–50% water.",
    "pest": "🐛 For pest control: scout weekly, use yellow sticky traps, apply neem spray (5ml/L) as preventive. Use chemical pesticides only when pest crosses economic threshold. Always wear protective gear.",
    "soil": "🌱 Healthy soil needs pH 6–7.5, good organic matter (>1.5%), balanced NPK. Add FYM (Farm Yard Manure) 10 tonnes/ha annually. Avoid over-tilling. Test soil every 2 years.",
    "weather": "🌤️ Check weather before spraying pesticides — avoid rainy, windy days. Irrigate in morning or evening. During heat stress, increase irrigation frequency. Plant wind-breaks for protection.",
    "profit": "💰 To maximize profit: use certified seeds, follow IPM (Integrated Pest Management), sell at MSP or FPO level, store produce properly, consider crop insurance schemes.",
    "organic": "♻️ Organic farming: use compost, vermicompost, biofertilizers (Rhizobium, PSB), neem-based pesticides, crop rotation. Get organic certification for premium prices in market.",
    "cotton": "☁️ Cotton is a Kharif crop. Needs deep black soil, pH 6.5–8. Plant May–June. Watch for Bollworm and Whitefly. Use Bt cotton variety for bollworm resistance. Apply 100:50:50 NPK kg/ha.",
    "maize": "🌽 Maize grows in both Kharif and Rabi. Sandy loam to clay soil, pH 5.8–7.0. Very water efficient. Apply 150:75:50 NPK. Fall Armyworm is main pest — spray Emamectin benzoate.",
    "default": "🤖 Great question! As a farming assistant, I can help with: crop selection, disease identification, fertilizer doses, irrigation schedules, pest management, and market information. Please ask a specific question about any crop or farming practice!"
}

# ─── CSS STYLING ─────────────────────────────────────────────────
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: #1a1a1a;
    }

    /* ── Global text contrast fix ── */
    p, span, div, li, td, th, label {
        color: #1a1a1a;
    }
    /* Streamlit default text override */
    .stMarkdown p, .stMarkdown span, .stMarkdown li { color: #1a1a1a !important; }
    /* Ensure all custom card text is dark */
    .tip-card, .tip-card p, .tip-card span, .tip-card b, .tip-card strong,
    .alert-box, .alert-box p, .alert-box span { color: #1a1a1a !important; }

    .main { background: linear-gradient(135deg, #f0f7ee 0%, #e8f5e9 50%, #f1f8e9 100%); }

    .stApp {
        background: linear-gradient(135deg, #f0f7ee 0%, #e8f5e9 100%);
    }

    .hero-banner {
        background: linear-gradient(135deg, #1b5e20, #2e7d32, #388e3c, #43a047);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(27,94,32,0.4);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
        animation: shimmer 4s infinite;
    }
    @keyframes shimmer { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }

    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.3rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-top: 4px solid #2e7d32;
        transition: transform 0.2s;
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0,0,0,0.12); }
    .metric-number { font-size: 2rem; font-weight: 700; color: #1b5e20; }
    .metric-label { font-size: 0.85rem; color: #555; margin-top: 0.3rem; }

    .result-box {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #2e7d32;
        margin-bottom: 1rem;
    }

    .alert-box {
        background: #ffffff;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #ff6f00;
        margin-bottom: 0.8rem;
        font-size: 0.9rem;
        color: #3e2000 !important;
        box-shadow: 0 2px 8px rgba(255,111,0,0.12);
    }
    .alert-box * { color: #3e2000 !important; }

    .tip-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        border: 1.5px solid #a5d6a7;
        border-left: 5px solid #2e7d32;
        margin-bottom: 0.8rem;
        transition: all 0.2s;
        color: #1a2e1a !important;
        box-shadow: 0 2px 8px rgba(46,125,50,0.08);
    }
    .tip-card * { color: #1a2e1a !important; }
    .tip-card:hover { transform: translateX(6px); border-color: #2e7d32; box-shadow: 0 4px 16px rgba(46,125,50,0.15); }

    .section-header {
        background: linear-gradient(90deg, #2e7d32, #43a047);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .crop-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s;
        height: 100%;
        border: 2px solid transparent;
    }
    .crop-card:hover { border-color: #4caf50; transform: translateY(-5px); }
    .crop-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .crop-name { font-size: 1.1rem; font-weight: 600; color: #1b5e20 !important; }
    .crop-info { font-size: 0.8rem; color: #444 !important; margin-top: 0.3rem; font-weight: 500; }

    .disease-result {
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .disease-healthy { background: linear-gradient(135deg, #e8f5e9, #f1f8e9); border: 2px solid #4caf50; }
    .disease-warning { background: linear-gradient(135deg, #fff3e0, #fce4ec); border: 2px solid #ff5722; }

    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        max-width: 85%;
    }
    .chat-user { background: #e8f5e9; margin-left: auto; border-bottom-right-radius: 4px; }
    .chat-bot { background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-bottom-left-radius: 4px; }

    .voice-btn {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.4rem 1rem;
        cursor: pointer;
        font-size: 0.85rem;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2e7d32, #43a047) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 15px rgba(46,125,50,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(46,125,50,0.4) !important;
    }

    .stSelectbox > div > div,
    .stSlider > div { border-radius: 10px !important; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 30%, #388e3c 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stSelectbox > div > div { background: rgba(255,255,255,0.15) !important; border: 1px solid rgba(255,255,255,0.3) !important; }

    .sidebar-menu-item {
        padding: 0.7rem 1rem;
        border-radius: 10px;
        margin: 0.2rem 0;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.95rem;
    }

    .stProgress .st-bo { background: linear-gradient(90deg, #2e7d32, #81c784) !important; }

    div[data-testid="stMetric"] {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }

    .weather-card {
        background: linear-gradient(135deg, #0277bd, #0288d1, #039be5);
        color: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(2,119,189,0.3);
    }

    .market-card {
        background: white;
        border-radius: 14px;
        padding: 1rem 1.5rem;
        border-left: 4px solid #f57c00;
        box-shadow: 0 3px 15px rgba(0,0,0,0.07);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.7rem;
    }

    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# ─── TTS AUDIO GENERATOR ─────────────────────────────────────────
# Maps each language to its BCP-47 tag AND preferred voice name hints
# The JS will try to find the best matching voice installed on the device.
LANG_VOICE_MAP = {
    "English":  {"bcp": "en-IN",  "fallback": "en",   "listen_label": "🔊 Listen",       "stop_label": "⏹ Stop"},
    "Hindi":    {"bcp": "hi-IN",  "fallback": "hi",   "listen_label": "🔊 सुनें",          "stop_label": "⏹ रोकें"},
    "Telugu":   {"bcp": "te-IN",  "fallback": "te",   "listen_label": "🔊 వినండి",         "stop_label": "⏹ ఆపండి"},
    "Bengali":  {"bcp": "bn-IN",  "fallback": "bn",   "listen_label": "🔊 শুনুন",          "stop_label": "⏹ থামুন"},
    "Tamil":    {"bcp": "ta-IN",  "fallback": "ta",   "listen_label": "🔊 கேளுங்கள்",       "stop_label": "⏹ நிறுத்து"},
    "Marathi":  {"bcp": "mr-IN",  "fallback": "mr",   "listen_label": "🔊 ऐका",            "stop_label": "⏹ थांबा"},
    "Kannada":  {"bcp": "kn-IN",  "fallback": "kn",   "listen_label": "🔊 ಕೇಳಿ",           "stop_label": "⏹ ನಿಲ್ಲಿಸಿ"},
    "Gujarati": {"bcp": "gu-IN",  "fallback": "gu",   "listen_label": "🔊 સાંભળો",          "stop_label": "⏹ અટકો"},
}

def generate_tts_html(text, lang="English"):
    """
    Generates a 🔊 Listen button using the Web Speech API.
    - Tries to find the exact language voice first (e.g. te-IN for Telugu)
    - Falls back to language prefix match (e.g. 'te') if exact not found
    - Falls back to English if nothing matches
    - Button label shows in the selected language
    """
    info = LANG_VOICE_MAP.get(lang, LANG_VOICE_MAP["English"])
    bcp       = info["bcp"]
    fallback  = info["fallback"]
    listen_lbl = info["listen_label"]
    stop_lbl   = info["stop_label"]

    # Escape text safely for JS single-quoted string
    text_js = (text
               .replace("\\", "\\\\")
               .replace("'", "\\'")
               .replace("\n", " ")
               .replace("\r", "")
               .replace('"', '\\"'))

    # Unique ID per button so multiple buttons on the same page don't clash
    uid = str(abs(hash(text[:40] + lang)))[-8:]

    html = f"""
<div style="margin:6px 0; display:inline-block;">
  <button id="btn_{uid}"
    onclick="smartSpeak_{uid}()"
    style="background:linear-gradient(135deg,#1b5e20,#2e7d32,#43a047);
           color:#fff;border:none;border-radius:25px;
           padding:9px 20px;cursor:pointer;font-size:0.88rem;
           font-family:'Poppins',sans-serif;letter-spacing:0.3px;
           box-shadow:0 3px 12px rgba(46,125,50,0.35);
           transition:all 0.2s;display:inline-flex;align-items:center;gap:7px;">
    {listen_lbl}
  </button>
  <button id="stop_{uid}"
    onclick="smartStop_{uid}()"
    style="background:linear-gradient(135deg,#b71c1c,#c62828,#d32f2f);
           color:#fff;border:none;border-radius:25px;
           padding:9px 16px;cursor:pointer;font-size:0.88rem;
           font-family:'Poppins',sans-serif;
           box-shadow:0 3px 12px rgba(183,28,28,0.35);
           display:none;align-items:center;gap:7px;margin-left:8px;">
    {stop_lbl}
  </button>
  <span id="voiceInfo_{uid}"
    style="font-size:0.72rem;color:#666;margin-left:8px;vertical-align:middle;display:none;">
  </span>
</div>
<script>
(function() {{
  var _uid    = '{uid}';
  var _text   = '{text_js}';
  var _bcp    = '{bcp}';
  var _fb     = '{fallback}';

  function getBestVoice(voices) {{
    // 1. Exact BCP-47 match (e.g. "te-IN")
    for (var i = 0; i < voices.length; i++) {{
      if (voices[i].lang === _bcp) return voices[i];
    }}
    // 2. Language prefix match (e.g. "te")
    for (var i = 0; i < voices.length; i++) {{
      if (voices[i].lang.toLowerCase().startsWith(_fb)) return voices[i];
    }}
    // 3. en-IN fallback
    for (var i = 0; i < voices.length; i++) {{
      if (voices[i].lang === 'en-IN') return voices[i];
    }}
    // 4. Any English
    for (var i = 0; i < voices.length; i++) {{
      if (voices[i].lang.startsWith('en')) return voices[i];
    }}
    return voices.length ? voices[0] : null;
  }}

  function doSpeak() {{
    var synth  = window.speechSynthesis;
    var voices = synth.getVoices();
    var voice  = getBestVoice(voices);

    synth.cancel();
    var msg = new SpeechSynthesisUtterance(_text);
    msg.lang   = voice ? voice.lang : _bcp;
    msg.rate   = 0.88;
    msg.pitch  = 1.05;
    msg.volume = 1.0;
    if (voice) msg.voice = voice;

    var infoEl = document.getElementById('voiceInfo_' + _uid);
    if (voice && infoEl) {{
      infoEl.textContent = '🎙 ' + voice.name + ' (' + voice.lang + ')';
      infoEl.style.display = 'inline';
    }}

    msg.onstart = function() {{
      document.getElementById('btn_'  + _uid).style.display = 'none';
      document.getElementById('stop_' + _uid).style.display = 'inline-flex';
    }};
    msg.onend = function() {{
      document.getElementById('btn_'  + _uid).style.display = 'inline-flex';
      document.getElementById('stop_' + _uid).style.display = 'none';
      if (infoEl) infoEl.style.display = 'none';
    }};
    msg.onerror = function() {{
      document.getElementById('btn_'  + _uid).style.display = 'inline-flex';
      document.getElementById('stop_' + _uid).style.display = 'none';
      if (infoEl) infoEl.style.display = 'none';
    }};
    synth.speak(msg);
  }}

  window['smartSpeak_' + _uid] = function() {{
    if (!('speechSynthesis' in window)) {{
      alert('Voice not supported. Please use Chrome or Edge browser.');
      return;
    }}
    var voices = window.speechSynthesis.getVoices();
    if (voices.length === 0) {{
      // Voices load async — wait for them
      window.speechSynthesis.onvoiceschanged = function() {{
        window.speechSynthesis.onvoiceschanged = null;
        doSpeak();
      }};
      // Some browsers need a nudge
      window.speechSynthesis.speak(new SpeechSynthesisUtterance(''));
      window.speechSynthesis.cancel();
    }} else {{
      doSpeak();
    }}
  }};

  window['smartStop_' + _uid] = function() {{
    window.speechSynthesis.cancel();
    document.getElementById('btn_'  + _uid).style.display = 'inline-flex';
    document.getElementById('stop_' + _uid).style.display = 'none';
    var infoEl = document.getElementById('voiceInfo_' + _uid);
    if (infoEl) infoEl.style.display = 'none';
  }};
}})();
</script>
"""
    return html

def speak(text, lang="English"):
    """Render a language-aware 🔊 Listen button in Streamlit."""
    st.components.v1.html(generate_tts_html(text, lang), height=58)

# ─── AI CROP RECOMMENDATION (rule-based ML simulation) ──────────
def recommend_crop(soil, nitrogen, phosphorus, potassium, temp, humidity, rainfall, season, location):
    scores = {}
    for crop, data in CROP_DATABASE.items():
        score = 0
        if season in data["season"] or "Year Round" in data["season"]:
            score += 30
        if "Sandy" in soil and crop in ["Groundnut", "Potato"]:
            score += 20
        elif "Clay" in soil and crop in ["Rice", "Cotton"]:
            score += 20
        elif "Loam" in soil:
            score += 15
        if nitrogen > 60 and crop in ["Rice", "Wheat", "Maize"]:
            score += 15
        elif nitrogen < 30 and crop in ["Groundnut", "Soybean"]:
            score += 15
        if temp > 25 and crop in ["Rice", "Cotton", "Sugarcane"]:
            score += 10
        elif temp < 20 and crop in ["Wheat", "Potato"]:
            score += 10
        if rainfall > 1000 and crop in ["Rice", "Sugarcane"]:
            score += 15
        elif rainfall < 600 and crop in ["Groundnut", "Wheat"]:
            score += 10
        score += random.randint(0, 10)
        scores[crop] = score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best = ranked[0][0]
    alternatives = [r[0] for r in ranked[1:4]]
    crop_data = CROP_DATABASE[best]
    yield_val = crop_data["yield"]
    price = crop_data["market_price"]

    return {
        "best_crop": best,
        "alternatives": alternatives,
        "yield": yield_val,
        "profit": crop_data["profit_range"],
        "icon": crop_data["icon"],
        "season": crop_data["season"],
        "fertilizer": crop_data["fertilizer"],
        "duration": crop_data["duration"],
    }

# ─── DISEASE DETECTION SIMULATION ───────────────────────────────
def detect_disease(image):
    diseases_list = list(DISEASES.keys())
    weights = [0.12, 0.12, 0.12, 0.12, 0.12, 0.08, 0.32]
    detected = random.choices(diseases_list, weights=weights, k=1)[0]
    confidence = random.uniform(78, 97) if detected != "Healthy" else random.uniform(88, 99)
    return detected, round(confidence, 1)

# ─── MARKET PRICE SIMULATION ─────────────────────────────────────
def get_market_prices(crop, months=12):
    base = CROP_DATABASE.get(crop, {}).get("market_price", 2000)
    prices = []
    current = base
    for _ in range(months):
        change = random.uniform(-0.08, 0.10)
        current = max(base * 0.7, min(base * 1.4, current * (1 + change)))
        prices.append(round(current))
    return prices

# ─── WEATHER SIMULATION ──────────────────────────────────────────
def get_simulated_weather(location):
    temp = random.uniform(22, 38)
    humidity = random.uniform(45, 85)
    rainfall_prob = random.uniform(0, 100)
    wind = random.uniform(5, 25)
    feels_like = temp + (humidity / 100 * 3)
    advice = []
    if rainfall_prob > 60:
        advice.append("🚫 Avoid pesticide spraying — rain likely today")
        advice.append("💧 Skip irrigation — natural rainfall expected")
    if temp > 35:
        advice.append("🌡️ Heat stress alert — increase irrigation frequency")
        advice.append("⏰ Irrigate in early morning (5–7 AM) to reduce evaporation")
    if wind > 20:
        advice.append("💨 Strong winds — postpone spraying operations")
    if humidity > 75:
        advice.append("🍄 High humidity — fungal disease risk! Inspect crops")
    if not advice:
        advice.append("✅ Good weather for farming operations today")
        advice.append("🌱 Ideal time for sowing, transplanting, or fertilizer application")
    return {
        "temp": round(temp, 1),
        "feels_like": round(feels_like, 1),
        "humidity": round(humidity, 1),
        "rainfall_prob": round(rainfall_prob, 1),
        "wind": round(wind, 1),
        "advice": advice,
        "condition": "🌧️ Rainy" if rainfall_prob > 60 else ("☀️ Sunny" if temp > 30 else "⛅ Cloudy")
    }

# ─── CHATBOT RESPONSE ────────────────────────────────────────────
def get_chatbot_response(query):
    query_lower = query.lower()
    for keyword, response in CHATBOT_KNOWLEDGE.items():
        if keyword in query_lower:
            return response
    crop_mentions = [c for c in CROP_DATABASE.keys() if c.lower() in query_lower]
    if crop_mentions:
        crop = crop_mentions[0]
        d = CROP_DATABASE[crop]
        return (f"{d['icon']} **{crop}** — Here's what you need to know:\n\n"
                f"📅 **Season:** {', '.join(d['season'])}\n"
                f"🌱 **Soil:** {d['soil']}\n"
                f"💧 **Water:** {d['water']}\n"
                f"🌡️ **Temperature:** {d['temp_range']}\n"
                f"🧪 **Fertilizer:** {d['fertilizer']}\n"
                f"📦 **Expected Yield:** {d['yield']}\n"
                f"💰 **Profit Range:** {d['profit_range']}")
    return CHATBOT_KNOWLEDGE["default"]

# ─── MODULE: DASHBOARD ───────────────────────────────────────────
def show_dashboard(T, lang):
    st.markdown(f"""
    <div class="hero-banner">
      <div class="hero-title">{T['app_title']}</div>
      <div class="hero-subtitle">{T['app_subtitle']}</div>
      <div style="margin-top:1rem;font-size:0.9rem;opacity:0.85;">
        📅 {datetime.date.today().strftime("%B %d, %Y")} &nbsp;|&nbsp; 🌡️ Season: Rabi 2025–26 &nbsp;|&nbsp; ☀️ Good Farming Day
      </div>
    </div>
    """, unsafe_allow_html=True)

    speak("Welcome to Smart Crop Advisory System! Your AI-powered farming assistant is ready to help you today.", lang)

    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        ("🌾", "10+", "Crops Covered"),
        ("🔬", "7", "Diseases Detected"),
        ("💰", "₹45K+", "Avg Profit/Ha"),
        ("🌤️", "Live", "Weather Updates"),
        ("🤖", "AI", "Powered Advisory"),
    ]
    for col, (icon, num, label) in zip([col1,col2,col3,col4,col5], metrics):
        col.markdown(f"""
        <div class="metric-card">
          <div style="font-size:1.8rem">{icon}</div>
          <div class="metric-number">{num}</div>
          <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-header">📈 Market Price Trends (Last 12 Months)</div>', unsafe_allow_html=True)
        months = ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]
        fig = go.Figure()
        colors = ["#2e7d32","#1565c0","#f57c00","#6a1b9a"]
        for i, crop in enumerate(["Rice","Wheat","Maize","Cotton"]):
            prices = get_market_prices(crop, 12)
            fig.add_trace(go.Scatter(
                x=months, y=prices, name=crop,
                line=dict(color=colors[i], width=2.5),
                mode='lines+markers',
                marker=dict(size=5)
            ))
        fig.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=20,r=20,t=20,b=20), height=280,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis_title="Price (₹/Quintal)", xaxis_title="Month",
            font=dict(family="Poppins")
        )
        st.plotly_chart(fig, use_container_width=True)

        # Crop calendar
        st.markdown('<div class="section-header">📅 Crop Calendar Overview</div>', unsafe_allow_html=True)
        calendar_data = {
            "Crop": ["Rice","Wheat","Maize","Cotton","Groundnut","Tomato","Onion","Potato"],
            "Sowing": ["Jun-Jul","Nov-Dec","Jun-Jul","Apr-May","Jun-Jul","Oct-Nov","Oct-Nov","Oct-Nov"],
            "Harvest": ["Oct-Nov","Mar-Apr","Sep-Oct","Dec-Jan","Sep-Oct","Feb-Mar","Mar-Apr","Jan-Feb"],
            "Season": ["Kharif","Rabi","Kharif","Kharif","Kharif","Rabi","Rabi","Rabi"],
            "Duration(days)":[120,120,100,160,115,85,110,90]
        }
        df_cal = pd.DataFrame(calendar_data)
        season_colors = {"Kharif":"#e8f5e9","Rabi":"#fff3e0","Year Round":"#e3f2fd"}
        def color_season(val):
            return f"background-color: {season_colors.get(val,'#f5f5f5')}"
        st.dataframe(
            df_cal.style.applymap(color_season, subset=['Season']),
            use_container_width=True, hide_index=True
        )

    with col_right:
        # Weather widget
        weather = get_simulated_weather("Your Location")
        st.markdown(f"""
        <div class="weather-card">
          <div style="font-size:3rem">{weather['condition'].split()[0]}</div>
          <div style="font-size:2.2rem;font-weight:700">{weather['temp']}°C</div>
          <div style="font-size:0.85rem;opacity:0.85">{weather['condition'].split(None,1)[1] if len(weather['condition'].split())>1 else ''} | Feels like {weather['feels_like']}°C</div>
          <div style="display:flex;justify-content:space-around;margin-top:1rem;font-size:0.85rem">
            <div>💧 {weather['humidity']}%<br><span style="opacity:0.7">Humidity</span></div>
            <div>🌧️ {weather['rainfall_prob']}%<br><span style="opacity:0.7">Rain Chance</span></div>
            <div>💨 {weather['wind']} km/h<br><span style="opacity:0.7">Wind</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        speak(f"Current weather: Temperature is {weather['temp']} degrees Celsius. Humidity is {weather['humidity']} percent. Rain probability is {weather['rainfall_prob']} percent.", lang)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">⚠️ Alerts & Advisories</div>', unsafe_allow_html=True)
        for adv in weather["advice"]:
            st.markdown(f'<div class="alert-box">{adv}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">💡 Today\'s Tips</div>', unsafe_allow_html=True)
        tips_today = random.sample(DAILY_TIPS, 3)
        for tip in tips_today:
            st.markdown(f"""
            <div class="tip-card">
              <b style="color:#1b5e20;font-size:0.95rem">{tip['icon']} {tip['category']}</b><br>
              <span style="font-size:0.88rem;color:#222;line-height:1.5">{tip['tip']}</span>
            </div>""", unsafe_allow_html=True)
        speak("Today's tip: " + tips_today[0]['tip'], lang)

    # Featured crops
    st.markdown('<div class="section-header">🌾 Featured Crops This Season</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    featured = list(CROP_DATABASE.items())[:5]
    for col, (name, data) in zip(cols, featured):
        col.markdown(f"""
        <div class="crop-card">
          <div class="crop-icon">{data['icon']}</div>
          <div class="crop-name">{name}</div>
          <div class="crop-info">💰 {data['market_price']}/quintal</div>
          <div class="crop-info">📦 {data['yield']}</div>
        </div>""", unsafe_allow_html=True)

# ─── MODULE: CROP RECOMMENDATION ────────────────────────────────
def show_crop_recommendation(T, lang):
    st.markdown(f'<div class="section-header">🌱 {T["crop_rec"]} — AI-Powered Analysis</div>', unsafe_allow_html=True)
    speak("Welcome to the AI Crop Recommendation System. Please enter your soil and climate details to get the best crop suggestion.", lang)

    col1, col2 = st.columns([1, 1])
    with col1:
        soil = st.selectbox(T["soil_type"], ["Sandy","Sandy Loam","Loam","Clay Loam","Clay","Black Cotton","Red","Alluvial"])
        nitrogen = st.slider(T["nitrogen"], 0, 150, 60, help="kg/ha")
        phosphorus = st.slider(T["phosphorus"], 0, 100, 40, help="kg/ha")
        potassium = st.slider(T["potassium"], 0, 100, 40, help="kg/ha")
        location = st.text_input(T["location"], "Hyderabad, Telangana")
    with col2:
        temp = st.slider(T["temperature"], 5, 50, 26)
        humidity = st.slider(T["humidity"], 20, 100, 65)
        rainfall = st.slider(T["rainfall"], 100, 3000, 800)
        season = st.selectbox(T["season"], ["Kharif (Rainy)","Rabi (Winter)","Summer","Year Round"])
        land_size = st.number_input("Land Size (Hectares)", 0.1, 50.0, 1.0, 0.5)

    if st.button(f"🤖 {T['submit']}", use_container_width=True):
        with st.spinner(T["loading"]):
            import time; time.sleep(1)
            season_key = season.split()[0]
            result = recommend_crop(soil, nitrogen, phosphorus, potassium, temp, humidity, rainfall, season_key, location)

        st.success("✅ Analysis Complete!")
        col_r1, col_r2 = st.columns([1.5, 1])
        with col_r1:
            st.markdown(f"""
            <div class="result-box">
              <div style="font-size:3rem;text-align:center">{result['icon']}</div>
              <h2 style="text-align:center;color:#1b5e20">{T['best_crop']}</h2>
              <h1 style="text-align:center;color:#2e7d32;font-size:2.5rem">{result['best_crop']}</h1>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem">
                <div style="background:#e8f5e9;padding:1rem;border-radius:10px;text-align:center">
                  <div style="font-weight:700;color:#1b5e20">{T['expected_yield']}</div>
                  <div style="font-size:1.1rem">{result['yield']}</div>
                </div>
                <div style="background:#e8f5e9;padding:1rem;border-radius:10px;text-align:center">
                  <div style="font-weight:700;color:#1b5e20">{T['est_profit']}</div>
                  <div style="font-size:1.1rem">{result['profit']}</div>
                </div>
                <div style="background:#e8f5e9;padding:1rem;border-radius:10px;text-align:center">
                  <div style="font-weight:700;color:#1b5e20">⏱️ Duration</div>
                  <div>{result['duration']}</div>
                </div>
                <div style="background:#e8f5e9;padding:1rem;border-radius:10px;text-align:center">
                  <div style="font-weight:700;color:#1b5e20">🧪 Fertilizer</div>
                  <div style="font-size:0.85rem">{result['fertilizer']}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

            speak(f"Best recommended crop is {result['best_crop']}. Expected yield is {result['yield']}. Estimated profit is {result['profit']}. Growing duration is {result['duration']}.", lang)

        with col_r2:
            st.markdown(f"#### {T['alt_crops']}")
            for i, alt in enumerate(result["alternatives"]):
                d = CROP_DATABASE.get(alt, {})
                st.markdown(f"""
                <div style="background:white;border-radius:12px;padding:1rem;
                            margin-bottom:0.7rem;box-shadow:0 2px 10px rgba(0,0,0,0.07);
                            border-left:4px solid {'#4caf50' if i==0 else '#81c784'}">
                  <b>{d.get('icon','🌱')} {alt}</b><br>
                  <span style="color:#666;font-size:0.85rem">
                    💰 ₹{d.get('market_price','N/A')}/quintal &nbsp; 📦 {d.get('yield','N/A')}
                  </span>
                </div>""", unsafe_allow_html=True)

            # NPK gauge
            st.markdown("#### 🧪 Soil Nutrient Status")
            fig = go.Figure()
            nutrients = ["N", "P", "K"]
            values = [nitrogen, phosphorus, potassium]
            optimal = [80, 60, 60]
            colors_bar = ["#4caf50" if v >= o*0.7 else "#ff9800" for v, o in zip(values, optimal)]
            fig.add_trace(go.Bar(x=nutrients, y=values, marker_color=colors_bar, name="Current",
                                  text=[f"{v}" for v in values], textposition='outside'))
            fig.add_trace(go.Bar(x=nutrients, y=optimal, marker_color=['rgba(100,200,100,0.3)']*3, name="Optimal"))
            fig.update_layout(barmode='overlay', height=220, margin=dict(l=10,r=10,t=30,b=10),
                              plot_bgcolor='white', paper_bgcolor='white',
                              title="NPK Levels (kg/ha)", font=dict(family="Poppins"),
                              legend=dict(orientation="h"))
            st.plotly_chart(fig, use_container_width=True)

# ─── MODULE: DISEASE SCANNER ─────────────────────────────────────
def show_disease_scanner(T, lang):
    st.markdown(f'<div class="section-header">🔬 {T["disease"]} — AI Disease Detection</div>', unsafe_allow_html=True)
    speak("Welcome to the AI Disease Scanner. Please upload a clear photo of your plant leaf to detect diseases.", lang)

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.info("📸 Upload a clear photo of the affected plant leaf for best results")
        uploaded = st.file_uploader(T["upload_image"], type=["jpg","jpeg","png","webp"])
        crop_sel = st.selectbox("Select Crop Type", list(CROP_DATABASE.keys()))

        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption="Uploaded Plant Image", use_column_width=True)
            if st.button(f"🔬 {T['scan_disease']}", use_container_width=True):
                with st.spinner("AI analyzing image..."):
                    import time; time.sleep(1.5)
                    disease, confidence = detect_disease(img)
                    st.session_state["disease_result"] = (disease, confidence, crop_sel)

    with col2:
        if "disease_result" in st.session_state:
            disease, confidence, crop = st.session_state["disease_result"]
            info = DISEASES[disease]
            is_healthy = disease == "Healthy"
            box_class = "disease-healthy" if is_healthy else "disease-warning"

            st.markdown(f"""
            <div class="disease-result {box_class}">
              <div style="font-size:2.5rem;text-align:center">{info['color']}</div>
              <h2 style="text-align:center;color:{'#1b5e20' if is_healthy else '#c62828'}">
                {T['healthy'] if is_healthy else info.get('color','')+ ' ' + disease}
              </h2>
              <div style="text-align:center;margin-bottom:1rem">
                <span style="background:{'#4caf50' if is_healthy else '#ef5350'};
                             color:white;padding:4px 16px;border-radius:20px;font-weight:600">
                  {'✅ HEALTHY' if is_healthy else '⚠️ DISEASE DETECTED'}
                </span>
              </div>
            </div>""", unsafe_allow_html=True)

            st.progress(int(confidence))
            st.caption(f"🎯 AI Confidence: **{confidence}%**")

            if not is_healthy:
                st.markdown(f"""
                <div class="result-box">
                  <b>{T['disease_name']}:</b> {disease}<br><br>
                  <b>{T['severity']}:</b> {info['severity']}<br><br>
                  <b>🔍 Symptoms:</b> {info['symptoms']}<br><br>
                  <b>{T['treat_advice']}:</b> {info['treatment']}<br><br>
                  <b>{T['pesticide']}:</b> {info['pesticide']}<br><br>
                  <b>🛡️ Prevention:</b> {info['prevention']}
                </div>""", unsafe_allow_html=True)
            else:
                st.success("Your plant is healthy! Keep following good practices.")
                st.info("**Preventive tips:** Continue regular monitoring, maintain proper spacing, and follow recommended irrigation schedule.")

            speak(info["listen_text"], lang)

            # History
            if "scan_history" not in st.session_state:
                st.session_state["scan_history"] = []
            st.session_state["scan_history"].append({
                "crop": crop, "disease": disease,
                "confidence": confidence, "time": datetime.datetime.now().strftime("%H:%M %d-%b")
            })

        else:
            st.markdown("""
            <div style="text-align:center;padding:4rem 2rem;color:#999">
              <div style="font-size:4rem">🌿</div>
              <div style="font-size:1.1rem;margin-top:1rem">Upload a plant image to detect diseases</div>
              <div style="font-size:0.85rem;margin-top:0.5rem">Supports: Rice, Wheat, Maize, Cotton, Tomato and more</div>
            </div>""", unsafe_allow_html=True)

    # Disease reference
    st.markdown('<div class="section-header">📋 Common Crop Diseases Reference</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (dname, dinfo) in enumerate(list(DISEASES.items())[:-1]):
        with cols[i % 3]:
            with st.expander(f"{dinfo['color']} {dname} — {dinfo['severity']} Risk"):
                st.markdown(f"**Symptoms:** {dinfo['symptoms']}")
                st.markdown(f"**Treatment:** {dinfo['treatment']}")
                st.markdown(f"**Pesticide:** {dinfo['pesticide']}")
                speak(dinfo["listen_text"], lang)

# ─── MODULE: MARKET PRICES ───────────────────────────────────────
def show_market_prices(T, lang):
    st.markdown(f'<div class="section-header">📈 {T["market"]} — Live Market Intelligence</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        crop_sel = st.selectbox(T["crop_name"], list(CROP_DATABASE.keys()))
        months = st.slider("History (months)", 3, 24, 12)

    with col2:
        st.markdown('<div class="section-header">Current Mandi Prices</div>', unsafe_allow_html=True)
        for crop, data in list(CROP_DATABASE.items())[:5]:
            variation = random.uniform(-0.05, 0.12)
            current_price = round(data["market_price"] * (1 + variation))
            direction = "▲" if variation > 0 else "▼"
            pct = round(abs(variation) * 100, 1)
            color = "#2e7d32" if variation > 0 else "#c62828"
            st.markdown(f"""
            <div class="market-card">
              <div><b>{data['icon']} {crop}</b><br>
                <span style="color:#666;font-size:0.82rem">₹/Quintal</span></div>
              <div style="font-size:1.3rem;font-weight:700;color:{color}">
                ₹{current_price} <span style="font-size:0.9rem">{direction}{pct}%</span>
              </div>
            </div>""", unsafe_allow_html=True)

    # Price chart
    prices = get_market_prices(crop_sel, months)
    base_price = CROP_DATABASE[crop_sel]["market_price"]
    month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    labels = (month_labels * 3)[:months]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=prices,
        fill='tozeroy',
        fillcolor='rgba(46,125,50,0.15)',
        line=dict(color='#2e7d32', width=2.5),
        mode='lines+markers',
        name=crop_sel,
        marker=dict(size=6)
    ))
    fig.add_hline(y=base_price, line_dash="dash", line_color="#f57c00",
                  annotation_text=f"MSP: ₹{base_price}", annotation_position="top right")
    fig.update_layout(
        title=f"{crop_sel} Price Trend",
        yaxis_title="Price (₹/Quintal)", xaxis_title="Month",
        plot_bgcolor='white', paper_bgcolor='white',
        height=320, margin=dict(l=20,r=20,t=50,b=20),
        font=dict(family="Poppins")
    )
    st.plotly_chart(fig, use_container_width=True)

    max_p, min_p = max(prices), min(prices)
    best_month = labels[prices.index(max_p)]
    speak(f"Market price for {crop_sel}: Current price is around {prices[-1]} rupees per quintal. Best selling time is in {best_month} at {max_p} rupees per quintal.", lang)

    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Highest Price", f"₹{max_p}/Q", f"+{round((max_p-base_price)/base_price*100,1)}%")
    col2.metric("📉 Lowest Price", f"₹{min_p}/Q", f"{round((min_p-base_price)/base_price*100,1)}%")
    col3.metric("🎯 Best Sell Month", best_month, f"₹{max_p}/Q")

# ─── MODULE: IRRIGATION PLANNER ──────────────────────────────────
def show_irrigation(T, lang):
    st.markdown(f'<div class="section-header">💧 {T["irrigation"]} — Smart Water Management</div>', unsafe_allow_html=True)
    speak("Welcome to the Smart Irrigation Planner. Enter your crop and soil details to get a personalized irrigation schedule.", lang)

    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox(T["crop_name"], list(CROP_DATABASE.keys()))
        soil = st.selectbox(T["soil_type"], ["Sandy","Sandy Loam","Loam","Clay Loam","Clay","Black Cotton"])
        area = st.number_input("Field Area (Acres)", 0.1, 100.0, 1.0)
    with col2:
        rainfall_mm = st.slider("Recent Rainfall (mm)", 0, 200, 20)
        stage = st.selectbox("Crop Growth Stage", ["Germination","Seedling","Vegetative","Flowering","Grain Filling","Maturity"])
        irrigation_method = st.selectbox("Irrigation Method", ["Flood","Furrow","Sprinkler","Drip","Pitcher"])

    if st.button("💧 Generate Irrigation Schedule", use_container_width=True):
        water_needs = {"Sandy":35,"Sandy Loam":28,"Loam":22,"Clay Loam":18,"Clay":15,"Black Cotton":20}
        stage_factor = {"Germination":0.5,"Seedling":0.7,"Vegetative":1.0,"Flowering":1.3,"Grain Filling":1.1,"Maturity":0.4}
        method_eff = {"Flood":0.55,"Furrow":0.65,"Sprinkler":0.80,"Drip":0.92,"Pitcher":0.85}

        base_water = water_needs.get(soil, 25)
        stage_adj = stage_factor.get(stage, 1.0)
        eff = method_eff.get(irrigation_method, 0.7)
        rain_adj = max(0, 1 - rainfall_mm/150)
        daily_mm = round(base_water * stage_adj * rain_adj / eff, 1)
        daily_litres = round(daily_mm * area * 4046.86 / 1000)
        frequency_days = 2 if soil == "Sandy" else (3 if "Loam" in soil else 5)

        speak(f"Irrigation recommendation: Apply {daily_mm} millimeters of water daily. Total {daily_litres} litres per day for your {area} acre field. Irrigate every {frequency_days} days using {irrigation_method} method.", lang)

        st.success(f"✅ Irrigation Plan Generated for {crop} at {stage} stage")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💧 Daily Water", f"{daily_mm} mm")
        c2.metric("🪣 Total Volume", f"{daily_litres:,} L/day")
        c3.metric("📅 Frequency", f"Every {frequency_days} days")
        c4.metric("⚡ Efficiency", f"{int(eff*100)}%")

        # Weekly schedule
        st.markdown('<div class="section-header">📅 Weekly Irrigation Schedule</div>', unsafe_allow_html=True)
        week_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        irrigate = [True if i % frequency_days == 0 else False for i in range(7)]
        for d, irr in zip(week_days, irrigate):
            color = "#e8f5e9" if irr else "#f5f5f5"
            status = f"💧 Irrigate — {daily_mm}mm ({daily_litres:,} litres)" if irr else "✅ Rest Day — Monitor soil moisture"
            border = "4px solid #4caf50" if irr else "4px solid #e0e0e0"
            st.markdown(f"""
            <div style="background:{color};padding:0.8rem 1.2rem;border-radius:10px;
                        margin-bottom:0.5rem;border-left:{border};
                        display:flex;justify-content:space-between;align-items:center">
              <b>{d}</b> <span style="color:#555">{status}</span>
            </div>""", unsafe_allow_html=True)

        # Water saving tips
        st.markdown('<div class="section-header">💡 Water Saving Strategies</div>', unsafe_allow_html=True)
        tips_col1, tips_col2 = st.columns(2)
        tips_irr = [
            ("🌅", "Irrigate early morning (5–7 AM) to reduce evaporation losses by 30%"),
            ("🍂", "Apply mulch to reduce soil water evaporation by 25–40%"),
            ("📏", "Level the field properly for uniform water distribution"),
            ("🔄", "Alternate wet-dry irrigation for rice saves 25% water"),
        ]
        for i, (icon, tip) in enumerate(tips_irr):
            col = tips_col1 if i % 2 == 0 else tips_col2
            col.markdown(f'<div class="tip-card">{icon} {tip}</div>', unsafe_allow_html=True)

# ─── MODULE: FERTILIZER ──────────────────────────────────────────
def show_fertilizer(T, lang):
    st.markdown(f'<div class="section-header">🧪 {T["fertilizer"]} — Precision Nutrition Planning</div>', unsafe_allow_html=True)
    speak("Welcome to the Smart Fertilizer Recommendation System. Enter soil nutrient levels and crop details for a personalized fertilizer plan.", lang)

    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox(T["crop_name"], list(CROP_DATABASE.keys()))
        area = st.number_input("Area (Hectares)", 0.1, 50.0, 1.0)
        soil_ph = st.slider("Soil pH", 4.0, 9.0, 6.5, 0.1)
        organic_matter = st.slider("Organic Matter (%)", 0.1, 5.0, 1.2, 0.1)
    with col2:
        current_n = st.slider(f"Current {T['nitrogen']}", 0, 120, 40)
        current_p = st.slider(f"Current {T['phosphorus']}", 0, 80, 25)
        current_k = st.slider(f"Current {T['potassium']}", 0, 100, 30)
        soil_type_f = st.selectbox("Soil Type", ["Sandy","Loamy","Clay","Black Cotton"])

    if st.button("🧪 Generate Fertilizer Plan", use_container_width=True):
        crop_data = CROP_DATABASE[crop]
        rec_parts = crop_data["fertilizer"].split(":")
        try:
            req_n = int(rec_parts[0].split()[-1])
            req_p = int(rec_parts[1])
            req_k = int(rec_parts[2].split()[0])
        except:
            req_n, req_p, req_k = 100, 50, 50

        deficit_n = max(0, req_n - current_n)
        deficit_p = max(0, req_p - current_p)
        deficit_k = max(0, req_k - current_k)

        # Organic adjustment
        if organic_matter > 2.5:
            deficit_n = round(deficit_n * 0.7)

        # Fertilizer quantities
        urea_kg = round((deficit_n / 0.46) * area)
        dap_kg = round((deficit_p / 0.46) * area)
        mop_kg = round((deficit_k / 0.60) * area)
        fym_tonnes = round(5 * area, 1)

        speak(f"Fertilizer plan for {crop}: Apply {urea_kg} kilograms of Urea, {dap_kg} kilograms of DAP, and {mop_kg} kilograms of MOP per {area} hectare. Also add {fym_tonnes} tonnes of organic manure.", lang)

        st.success("✅ Fertilizer Plan Ready!")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌿 Urea (N)", f"{urea_kg} kg", f"₹{urea_kg*6}")
        c2.metric("🔵 DAP (P)", f"{dap_kg} kg", f"₹{dap_kg*26}")
        c3.metric("🟡 MOP (K)", f"{mop_kg} kg", f"₹{mop_kg*17}")
        c4.metric("🌱 FYM", f"{fym_tonnes} t", "Organic")

        # Application schedule
        st.markdown('<div class="section-header">📅 Application Schedule</div>', unsafe_allow_html=True)
        schedule = [
            {"stage": "Land Preparation (Before Sowing)", "npk": f"FYM {fym_tonnes}t + DAP {round(dap_kg*0.5)}kg + MOP {round(mop_kg*0.5)}kg",
             "note": "Mix thoroughly into soil before final ploughing"},
            {"stage": "Basal Dose (At Sowing)", "npk": f"Urea {round(urea_kg*0.33)}kg + DAP {round(dap_kg*0.5)}kg + MOP {round(mop_kg*0.5)}kg",
             "note": "Apply in furrows, do not place directly on seeds"},
            {"stage": "Top Dressing 1 (Tillering/30 days)", "npk": f"Urea {round(urea_kg*0.33)}kg",
             "note": "Apply when soil is moist, avoid application before rain"},
            {"stage": "Top Dressing 2 (Flowering/60 days)", "npk": f"Urea {round(urea_kg*0.34)}kg",
             "note": "Critical stage — do not skip this application"},
        ]
        for s in schedule:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:1rem;
                        margin-bottom:0.7rem;box-shadow:0 2px 10px rgba(0,0,0,0.07);
                        border-left:4px solid #4caf50">
              <b>📅 {s['stage']}</b><br>
              <span style="color:#2e7d32;font-weight:600">🧪 {s['npk']}</span><br>
              <span style="color:#666;font-size:0.85rem">💡 {s['note']}</span>
            </div>""", unsafe_allow_html=True)

# ─── MODULE: PEST WARNING ─────────────────────────────────────────
def show_pest_warning(T, lang):
    st.markdown(f'<div class="section-header">🐛 {T["pest"]} — Integrated Pest Management</div>', unsafe_allow_html=True)
    speak("Pest Warning System! Stay ahead of crop pests with early identification and treatment advice.", lang)

    # Pest alerts
    st.markdown("### ⚠️ Current Season Pest Alerts")
    active_pests = random.sample(list(PESTS.keys()), 3)
    for pest_name in active_pests:
        pest = PESTS[pest_name]
        severity_color = "#ffebee" if "High" in pest["severity"] else "#fff3e0"
        st.markdown(f"""
        <div style="background:{severity_color};border-radius:14px;padding:1.2rem;
                    margin-bottom:1rem;border-left:5px solid {'#c62828' if 'High' in pest['severity'] else '#f57c00'}">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <h3 style="margin:0">🐛 {pest_name}</h3>
            <span style="font-weight:600">{pest['severity']}</span>
          </div>
          <p style="margin:0.5rem 0;color:#555">
            <b>Crops at Risk:</b> {', '.join(pest['crops'])}<br>
            <b>Symptoms:</b> {pest['symptoms']}<br>
            <b>Treatment:</b> {pest['treatment']}
          </p>
          <small style="color:#777">🛡️ Prevention: {pest['prevention']}</small>
        </div>""", unsafe_allow_html=True)
        speak(f"Pest Alert: {pest_name}. {pest['severity']} severity. Crops affected: {', '.join(pest['crops'])}. {pest['treatment']}", lang)

    # IPM strategies
    st.markdown('<div class="section-header">🌿 Integrated Pest Management (IPM) Strategies</div>', unsafe_allow_html=True)
    ipm_tabs = st.tabs(["🌱 Cultural", "🔬 Biological", "⚗️ Chemical", "🪤 Mechanical"])
    with ipm_tabs[0]:
        cultural = ["Crop rotation to break pest cycles","Use of certified disease-free seeds","Deep summer ploughing to expose pupae","Adjust sowing time to avoid peak pest seasons","Maintain proper plant spacing for air circulation","Remove crop debris after harvest"]
        for c in cultural:
            st.markdown(f"✅ {c}")
    with ipm_tabs[1]:
        biological = ["Release Trichogramma cards for stem borer control","Use Beauveria bassiana for soil-borne pests","Apply NPV (Nuclear Polyhedrosis Virus) for caterpillars","Conserve natural enemies: ladybird, spider, parasitic wasps","Use neem-based formulations (5% NSKE)","Trichoderma for soil-borne fungal pathogens"]
        for b in biological:
            st.markdown(f"🌿 {b}")
    with ipm_tabs[2]:
        chemical = ["Use pesticides only when Economic Threshold Level (ETL) is crossed","Rotate pesticide groups to prevent resistance","Prefer selective over broad-spectrum pesticides","Follow correct dose and timing as per label","Wear protective equipment during spraying","Observe waiting period before harvest"]
        for c in chemical:
            st.markdown(f"⚗️ {c}")
    with ipm_tabs[3]:
        mechanical = ["Install pheromone traps @ 5–8 per acre for monitoring","Use yellow/blue sticky traps for flying insects","Light traps for nocturnal insects during night","Hand picking of egg masses and larvae","Bird perches for insectivorous birds","Sticky barriers on tree trunks against crawling pests"]
        for m in mechanical:
            st.markdown(f"🪤 {m}")

# ─── MODULE: CROP ROTATION ───────────────────────────────────────
def show_crop_rotation(T, lang):
    st.markdown(f'<div class="section-header">🔄 {T["rotation"]} — Sustainable Soil Management</div>', unsafe_allow_html=True)
    speak("Crop Rotation Advisor. Rotating crops improves soil health, breaks pest cycles, and increases long-term yield.", lang)

    current_crop = st.selectbox("Current / Previous Crop", list(CROP_DATABASE.keys()))

    rotation_plans = {
        "Rice": {"next": ["Wheat","Mustard","Potato","Pulses"], "reason": "Rice exhausts soil N & P. Wheat uses different nutrients. Adding pulses after rice fixes nitrogen naturally."},
        "Wheat": {"next": ["Paddy","Maize","Sunflower","Groundnut"], "reason": "After wheat, grow pulse/oilseed to restore N. Prevents cereal diseases from building up."},
        "Maize": {"next": ["Soybean","Wheat","Potato","Vegetables"], "reason": "Maize depletes N heavily. Soybean rotation adds 80–120 kg N/ha. Breaks Fall Armyworm cycle."},
        "Cotton": {"next": ["Wheat","Sorghum","Groundnut","Soybean"], "reason": "Cotton is a heavy feeder. Cereals & legumes help restore soil structure and organic matter."},
        "Sugarcane": {"next": ["Wheat","Onion","Garlic","Pulses"], "reason": "After sugarcane, grow short-duration crops. Restores soil aeration after heavy root extraction."},
        "Groundnut": {"next": ["Maize","Rice","Cotton","Vegetables"], "reason": "Groundnut fixes nitrogen. Follow with heavy feeders like maize or cotton to utilize the N benefit."},
        "Tomato": {"next": ["Rice","Maize","Onion","Wheat"], "reason": "Avoid repeating solanaceous crops. Helps break Early Blight and Fusarium wilt cycles."},
        "Onion": {"next": ["Tomato","Maize","Paddy","Pulses"], "reason": "After onion, grow cereals or legumes. Avoid garlic/onion rotation which spreads purple blotch."},
        "Soybean": {"next": ["Wheat","Maize","Sorghum","Vegetables"], "reason": "Soybean fixes N (100–200 kg/ha). Ideal pre-crop for wheat. Breaks yellow mosaic virus cycle."},
        "Potato": {"next": ["Wheat","Maize","Onion","Pulses"], "reason": "After potato, avoid other tubers. Wheat breaks Late Blight cycle. Legumes restore soil."},
    }

    plan = rotation_plans.get(current_crop, {"next": ["Wheat","Maize","Pulses","Vegetables"], "reason": "General rotation: alternate between cereals, legumes and vegetables."})

    st.markdown(f"""
    <div class="result-box">
      <h3>🔄 Recommended Rotation After {current_crop}</h3>
      <p><b>Why rotate?</b> {plan['reason']}</p>
    </div>""", unsafe_allow_html=True)

    speak(f"For {current_crop}, recommended next crops are: {', '.join(plan['next'])}. {plan['reason']}", lang)

    st.markdown("### 🌱 Recommended Next Crops")
    cols = st.columns(len(plan["next"]))
    for col, next_crop in zip(cols, plan["next"]):
        d = CROP_DATABASE.get(next_crop, {})
        col.markdown(f"""
        <div class="crop-card">
          <div class="crop-icon">{d.get('icon','🌿')}</div>
          <div class="crop-name">{next_crop}</div>
          <div class="crop-info">{d.get('season', ['Year Round'])[0] if d.get('season') else 'Year Round'}</div>
          <div class="crop-info">📦 {d.get('yield','N/A')}</div>
        </div>""", unsafe_allow_html=True)

    # 3-year plan
    st.markdown('<div class="section-header">📅 3-Year Crop Rotation Plan</div>', unsafe_allow_html=True)
    years = ["Year 1","Year 2","Year 3"]
    kharif = [current_crop, plan["next"][0], plan["next"][1] if len(plan["next"]) > 1 else "Pulses"]
    rabi = ["Wheat","Mustard","Potato"]
    rotation_df = pd.DataFrame({"Year": years, "Kharif Season": kharif, "Rabi Season": rabi})
    st.dataframe(rotation_df, use_container_width=True, hide_index=True)

    # Benefits
    benefits = ["💰 Increases overall farm income by 20–40%","🌱 Improves soil organic matter and structure","🐛 Breaks pest and disease cycles","💧 Reduces water usage through efficient root systems","🧪 Reduces chemical inputs by 30–50%","🌍 Reduces greenhouse gas emissions from farmland"]
    cols2 = st.columns(2)
    st.markdown("### ✅ Benefits of Crop Rotation")
    for i, b in enumerate(benefits):
        (cols2[0] if i % 2 == 0 else cols2[1]).markdown(f'<div class="tip-card">{b}</div>', unsafe_allow_html=True)

# ─── MODULE: CROP LIBRARY ────────────────────────────────────────
def show_crop_library(T, lang):
    st.markdown(f'<div class="section-header">📚 {T["library"]} — Complete Crop Encyclopedia</div>', unsafe_allow_html=True)
    search = st.text_input("🔍 Search crop...", "")
    filtered = {k: v for k, v in CROP_DATABASE.items() if search.lower() in k.lower()} if search else CROP_DATABASE

    for crop_name, data in filtered.items():
        with st.expander(f"{data['icon']} {crop_name} — {data['scientific']}"):
            col1, col2, col3 = st.columns(3)
            details = [
                (col1, [("🌱 Scientific Name", data['scientific']),("📅 Season", ', '.join(data['season'])),
                        ("⏱️ Duration", data['duration']),("📦 Yield", data['yield'])]),
                (col2, [("🪱 Soil Type", data['soil']),("🌡️ Temperature", data['temp_range']),
                        ("💧 Water Needs", data['water']),("🧪 Fertilizer", data['fertilizer'])]),
                (col3, [("💰 Market Price", f"₹{data['market_price']}/Quintal"),("💵 Profit", data['profit_range']),
                        ("🐛 Major Pests", ', '.join(data['pests'])),("📊 Demand", "High" if data['market_price'] > 3000 else "Medium")]),
            ]
            for col, items in details:
                with col:
                    for label, val in items:
                        st.markdown(f"**{label}:** {val}")
            speak_lib = f"{crop_name}. Scientific name: {data['scientific']}. Best season: {', '.join(data['season'])}. Soil: {data['soil']}. Water: {data['water']}. Expected yield: {data['yield']}. Market price: {data['market_price']} rupees per quintal."
            speak(speak_lib, lang)

# ─── MODULE: AI CHATBOT ──────────────────────────────────────────
def show_chatbot(T, lang):
    st.markdown(f'<div class="section-header">🤖 {T["chatbot"]} — Your AI Farming Assistant</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "text": f"🌾 Namaste! I'm your Smart Farming Assistant. I can help you with:\n\n• 🌱 Crop selection & planning\n• 🔬 Disease identification\n• 🧪 Fertilizer recommendations\n• 💧 Irrigation advice\n• 📈 Market price information\n• 🐛 Pest management\n\nAsk me anything about farming!"}
        ]

    # Display chat
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-message chat-user">👨‍🌾 <b>You:</b> {msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message chat-bot">🤖 <b>Assistant:</b><br>{msg["text"]}</div>', unsafe_allow_html=True)
                speak(msg["text"].replace("**","").replace("*",""), lang)

    # Quick questions
    st.markdown("**💡 Quick Questions:**")
    quick_qs = ["Best crop for black soil?","How to treat rice disease?","Best fertilizer for wheat?","Water requirement of cotton?","What is crop rotation?"]
    cols = st.columns(len(quick_qs))
    for col, q in zip(cols, quick_qs):
        if col.button(q, use_container_width=True, key=f"quick_{q}"):
            st.session_state.chat_history.append({"role": "user", "text": q})
            response = get_chatbot_response(q)
            st.session_state.chat_history.append({"role": "bot", "text": response})
            st.rerun()

    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(T["ask_question"], key="chat_input", label_visibility="collapsed")
    with col_send:
        if st.button(f"📤 {T['send']}", use_container_width=True):
            if user_input.strip():
                st.session_state.chat_history.append({"role": "user", "text": user_input})
                with st.spinner(T["generating"]):
                    import time; time.sleep(0.5)
                    response = get_chatbot_response(user_input)
                st.session_state.chat_history.append({"role": "bot", "text": response})
                st.rerun()

    if st.button("🗑️ Clear Chat", use_container_width=False):
        st.session_state.chat_history = []
        st.rerun()

# ─── MODULE: ANALYTICS ───────────────────────────────────────────
def show_analytics(T, lang):
    st.markdown(f'<div class="section-header">📊 {T["analytics"]} — Smart Farm Intelligence</div>', unsafe_allow_html=True)
    speak("Farm Analytics Dashboard. Here's a complete overview of your farming performance and insights.", lang)

    months = ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]

    # Production trend
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📈 Monthly Yield Trends")
        yield_data = {"Rice": [round(random.uniform(3.5,6.0),2) for _ in range(12)],
                      "Wheat": [round(random.uniform(2.8,5.0),2) for _ in range(12)],
                      "Maize": [round(random.uniform(4.0,7.5),2) for _ in range(12)]}
        fig = go.Figure()
        for crop, ydata in yield_data.items():
            fig.add_trace(go.Bar(name=crop, x=months, y=ydata))
        fig.update_layout(barmode='group', height=280, plot_bgcolor='white', paper_bgcolor='white',
                          margin=dict(l=10,r=10,t=10,b=10), font=dict(family="Poppins"),
                          yaxis_title="Yield (tonnes/ha)", legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🥧 Disease Distribution")
        disease_counts = {d: random.randint(2,25) for d in list(DISEASES.keys())[:-1]}
        fig2 = px.pie(values=list(disease_counts.values()), names=list(disease_counts.keys()),
                      color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4)
        fig2.update_layout(height=280, margin=dict(l=10,r=10,t=10,b=10), font=dict(family="Poppins"))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 💰 Crop Profitability Comparison")
        crops = list(CROP_DATABASE.keys())[:8]
        profits = [int(CROP_DATABASE[c]["profit_range"].split("–")[0].replace("₹","").replace(",","").replace("k","000")) // 1000 for c in crops]
        fig3 = go.Figure(go.Bar(x=crops, y=profits,
                                marker_color=['#2e7d32','#4caf50','#81c784','#a5d6a7','#c8e6c9','#1b5e20','#388e3c','#66bb6a'],
                                text=[f"₹{p}K" for p in profits], textposition='outside'))
        fig3.update_layout(height=260, plot_bgcolor='white', paper_bgcolor='white',
                           margin=dict(l=10,r=10,t=10,b=50), font=dict(family="Poppins"),
                           yaxis_title="Min Profit (₹K/ha)", xaxis_tickangle=-30)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### 🌡️ Soil Health Radar")
        categories = ['Nitrogen','Phosphorus','Potassium','pH Score','Organic Matter','Moisture']
        values = [random.randint(50,95) for _ in range(6)]
        fig4 = go.Figure(go.Scatterpolar(r=values+[values[0]], theta=categories+[categories[0]],
                                          fill='toself', fillcolor='rgba(46,125,50,0.25)',
                                          line=dict(color='#2e7d32', width=2)))
        fig4.update_layout(polar=dict(radialaxis=dict(range=[0,100])),
                           height=260, margin=dict(l=20,r=20,t=20,b=20),
                           font=dict(family="Poppins"), showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    # KPI cards
    st.markdown('<div class="section-header">📊 Season Performance Summary</div>', unsafe_allow_html=True)
    kpis = [
        ("🌾 Total Crops Planted", "8", "+2 vs last season"),
        ("📦 Avg Yield", "4.8 t/ha", "+12% improvement"),
        ("💰 Total Revenue", "₹3.2L", "+₹45K vs last year"),
        ("🔬 Diseases Detected", "3", "Early detection saved ₹18K"),
        ("💧 Water Saved", "35%", "Using drip irrigation"),
        ("🌱 Soil Health Score", "78/100", "Good — maintain practices"),
    ]
    cols = st.columns(3)
    for i, (label, value, delta) in enumerate(kpis):
        with cols[i % 3]:
            st.metric(label, value, delta)

# ─── MODULE: SATELLITE MONITOR ───────────────────────────────────
def show_satellite(T, lang):
    st.markdown(f'<div class="section-header">🛰️ {T["satellite"]} — NDVI Crop Health Mapping</div>', unsafe_allow_html=True)
    speak("Satellite Crop Monitoring System. This shows simulated vegetation health data for your field.", lang)

    st.info("🛰️ This module simulates satellite-based NDVI monitoring. In production, connect to Sentinel-2 or Landsat API.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### 🗺️ Field NDVI Heat Map (Simulated)")
        ndvi_data = np.random.uniform(0.2, 0.9, (20, 30))
        ndvi_data[5:8, 10:14] = np.random.uniform(0.1, 0.3, (3, 4))  # stress zone
        fig = px.imshow(ndvi_data, color_continuous_scale="RdYlGn",
                        labels=dict(color="NDVI"), zmin=0, zmax=1,
                        title="NDVI Vegetation Index Map")
        fig.add_annotation(x=12, y=6, text="⚠️ Stress Zone", showarrow=True,
                           arrowcolor="red", font=dict(color="red", size=12))
        fig.update_layout(height=380, margin=dict(l=10,r=10,t=40,b=10), font=dict(family="Poppins"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Field Health Summary")
        zones = {"🟢 Healthy (NDVI > 0.6)": 65, "🟡 Moderate (0.4–0.6)": 22, "🔴 Stressed (< 0.4)": 13}
        for zone, pct in zones.items():
            st.markdown(f"**{zone}:** {pct}%")
            st.progress(pct)

        st.markdown("#### 📅 NDVI History")
        weeks = [f"W{i+1}" for i in range(8)]
        ndvi_hist = [round(random.uniform(0.4, 0.8), 2) for _ in range(8)]
        fig2 = go.Figure(go.Scatter(x=weeks, y=ndvi_hist, fill='tozeroy',
                                    fillcolor='rgba(46,125,50,0.2)',
                                    line=dict(color='#2e7d32', width=2),
                                    mode='lines+markers'))
        fig2.update_layout(height=200, margin=dict(l=5,r=5,t=10,b=10),
                           plot_bgcolor='white', paper_bgcolor='white',
                           yaxis=dict(range=[0,1], title="NDVI"),
                           font=dict(family="Poppins"))
        st.plotly_chart(fig2, use_container_width=True)
        speak("Field health analysis: 65 percent of your field is healthy with good vegetation. 22 percent shows moderate stress. 13 percent needs immediate attention.", lang)

# ─── MODULE: DRONE SCOUT ─────────────────────────────────────────
def show_drone(T, lang):
    st.markdown(f'<div class="section-header">🚁 {T["drone"]} — AI Drone Field Inspection</div>', unsafe_allow_html=True)
    speak("Drone Field Scout. Simulate aerial inspection of your field for pests, diseases and crop health monitoring.", lang)

    st.info("🚁 This simulates AI drone-based field scouting. Integrates with DJI, Parrot, or AgEagle drone systems.")

    col1, col2, col3 = st.columns(3)
    drone_metrics = [
        ("✈️ Flight Coverage", "2.5 ha/flight", "Full field mapped"),
        ("🎯 Detection Accuracy", "94.2%", "AI model v3.1"),
        ("⚡ Battery Life", "28 min", "Per charge"),
    ]
    for col, (label, val, note) in zip([col1,col2,col3], drone_metrics):
        col.markdown(f"""
        <div class="metric-card">
          <div style="font-size:1.8rem">{label.split()[0]}</div>
          <div class="metric-number" style="font-size:1.5rem">{val}</div>
          <div class="metric-label">{note}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_map, col_stats = st.columns([2, 1])
    with col_map:
        st.markdown("#### 🗺️ Drone Scan Results Map")
        n_points = 50
        lats = np.random.uniform(17.30, 17.40, n_points)
        lons = np.random.uniform(78.40, 78.50, n_points)
        types = np.random.choice(["Healthy","Pest","Disease","Nutrient Deficiency"], n_points, p=[0.6,0.2,0.12,0.08])
        color_map = {"Healthy":"green","Pest":"red","Disease":"orange","Nutrient Deficiency":"blue"}
        fig = go.Figure()
        for t, color in color_map.items():
            mask = types == t
            fig.add_trace(go.Scatter(
                x=lons[mask], y=lats[mask], mode='markers',
                marker=dict(color=color, size=10, opacity=0.7),
                name=t
            ))
        fig.update_layout(
            xaxis_title="Longitude", yaxis_title="Latitude",
            height=360, margin=dict(l=10,r=10,t=10,b=10),
            plot_bgcolor='#e8f5e9', paper_bgcolor='white',
            font=dict(family="Poppins"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_stats:
        st.markdown("#### 📋 Scan Summary")
        scan_results = {"Healthy Plants": 60, "Pest Hotspots": 20, "Disease Zones": 12, "Nutrient Deficiency": 8}
        for result, pct in scan_results.items():
            emoji = {"Healthy Plants":"🟢","Pest Hotspots":"🔴","Disease Zones":"🟡","Nutrient Deficiency":"🔵"}[result]
            st.markdown(f"{emoji} **{result}:** {pct}%")
            st.progress(pct)
        speak("Drone scan results: 60 percent healthy plants. 20 percent pest hotspot areas detected. 12 percent disease zones. 8 percent nutrient deficiency zones. Immediate action recommended for affected areas.", lang)

        st.markdown("#### 🚨 Priority Actions")
        actions = ["🔴 Spray pesticide in NE quadrant (Pest)", "🟡 Apply fungicide in central area", "🔵 Top-dress fertilizer NW corner"]
        for a in actions:
            st.markdown(f'<div class="alert-box">{a}</div>', unsafe_allow_html=True)

# ─── MODULE: DAILY TIPS ──────────────────────────────────────────
def show_daily_tips(T, lang):
    st.markdown(f'<div class="section-header">💡 {T["tips"]} — Smart Farming Knowledge</div>', unsafe_allow_html=True)

    today_tip = DAILY_TIPS[datetime.date.today().day % len(DAILY_TIPS)]
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1b5e20,#2e7d32,#43a047);
                color:white;border-radius:20px;padding:2rem;text-align:center;margin-bottom:1.5rem">
      <div style="font-size:3rem">{today_tip['icon']}</div>
      <h2 style="font-family:'Playfair Display',serif">💡 Tip of the Day</h2>
      <p style="font-size:1.1rem;line-height:1.6;max-width:600px;margin:0 auto">{today_tip['tip']}</p>
      <span style="background:rgba(255,255,255,0.2);padding:4px 12px;border-radius:12px;font-size:0.85rem">
        📂 {today_tip['category']}
      </span>
    </div>""", unsafe_allow_html=True)
    speak("Tip of the day: " + today_tip["tip"], lang)

    # Category filter
    categories = list(set([t["category"] for t in DAILY_TIPS]))
    selected_cat = st.multiselect("Filter by Category", categories, default=categories[:3])
    filtered_tips = [t for t in DAILY_TIPS if t["category"] in selected_cat] if selected_cat else DAILY_TIPS

    cols = st.columns(2)
    for i, tip in enumerate(filtered_tips):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="tip-card">
              <div style="font-size:1.5rem">{tip['icon']}</div>
              <div style="font-weight:700;color:#1b5e20 !important;margin:0.4rem 0;font-size:0.95rem">{tip['category']}</div>
              <div style="font-size:0.9rem;color:#1a1a1a !important;line-height:1.6;font-weight:400">{tip['tip']}</div>
            </div>""", unsafe_allow_html=True)
            speak(tip["tip"], lang)

# ─── MODULE: SEASONAL GUIDE ──────────────────────────────────────
def show_seasonal_guide(T, lang):
    st.markdown(f'<div class="section-header">📅 {T["seasonal"]} — Season-Wise Crop Planning</div>', unsafe_allow_html=True)

    season_sel = st.radio("Select Season", ["🌧️ Kharif (June–Oct)", "❄️ Rabi (Nov–Mar)", "☀️ Summer (Mar–Jun)"], horizontal=True)

    seasons_data = {
        "🌧️ Kharif (June–Oct)": {
            "crops": ["Rice","Maize","Cotton","Groundnut","Soybean","Bajra","Jowar","Arhar"],
            "tip": "Kharif crops depend on monsoon rainfall. Sow after first good rain. Ensure proper drainage.",
            "key_tasks": ["Land preparation by May end","Seed treatment with fungicide before sowing","Apply basal fertilizer at sowing","Monitor for Kharif pests — Stem Borer, BPH","Harvest before winter rains begin"],
            "ideal_conditions": {"Rainfall": "600–2000 mm", "Temperature": "22–35°C", "Humidity": "65–90%"}
        },
        "❄️ Rabi (Nov–Mar)": {
            "crops": ["Wheat","Mustard","Potato","Onion","Chickpea","Lentil","Barley","Peas"],
            "tip": "Rabi crops grow in cool winter conditions. Timely irrigation is critical during dry spells.",
            "key_tasks": ["Pre-sowing irrigation before planting","Use certified seeds for higher yield","Apply full dose of P and K at sowing","Irrigation at critical stages: CRI, tillering, flowering","Watch for aphids and Powdery Mildew"],
            "ideal_conditions": {"Rainfall": "200–500 mm", "Temperature": "10–25°C", "Humidity": "40–70%"}
        },
        "☀️ Summer (Mar–Jun)": {
            "crops": ["Tomato","Cucumber","Bitter Gourd","Groundnut","Sunflower","Moong","Watermelon"],
            "tip": "Summer crops need frequent irrigation. Mulching is highly recommended to conserve soil moisture.",
            "key_tasks": ["Apply mulch to conserve moisture","Irrigate every 3–5 days","Evening irrigation preferred to reduce evaporation","Shade nets for sensitive crops","Harvest early morning for better quality"],
            "ideal_conditions": {"Rainfall": "0–200 mm", "Temperature": "28–42°C", "Humidity": "30–55%"}
        }
    }

    data = seasons_data[season_sel]
    speak(f"Season guide for {season_sel.split()[1]} season. {data['tip']}", lang)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"#### 🌱 Recommended Crops for {season_sel.split()[1]}")
        crop_cols = st.columns(4)
        for i, crop_name in enumerate(data["crops"]):
            crop_info = CROP_DATABASE.get(crop_name, {})
            with crop_cols[i % 4]:
                st.markdown(f"""
                <div class="crop-card">
                  <div class="crop-icon">{crop_info.get('icon','🌿')}</div>
                  <div class="crop-name" style="font-size:0.95rem">{crop_name}</div>
                  <div class="crop-info">{crop_info.get('duration','60–120 days')}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown(f"#### 📝 Key Tasks")
        for task in data["key_tasks"]:
            st.markdown(f"✅ {task}")

    with col2:
        st.markdown("#### 🌡️ Ideal Conditions")
        for key, val in data["ideal_conditions"].items():
            st.markdown(f"**{key}:** {val}")

        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:1.2rem;margin-top:1rem;
                    border-left:5px solid #2e7d32;border:1.5px solid #a5d6a7;
                    box-shadow:0 2px 8px rgba(46,125,50,0.10)">
          <b style="color:#1b5e20">💡 Season Tip:</b><br>
          <span style="font-size:0.9rem;color:#222">{data['tip']}</span>
        </div>""", unsafe_allow_html=True)

# ─── MODULE: REAL WEATHER API ────────────────────────────────────
def show_weather(T, lang):
    st.markdown(f'<div class="section-header">🌤️ {T["weather"]} — Live Weather + Farming Advisory</div>', unsafe_allow_html=True)

    # API Key input
    with st.expander("🔑 OpenWeatherMap API Setup (Free)", expanded=False):
        st.markdown("""
        1. Go to **[openweathermap.org](https://openweathermap.org/api)** → Sign up free
        2. Copy your API key from **My API Keys**
        3. Paste it below — it's saved for this session
        """)
        api_key_input = st.text_input(
            "API Key", 
            value=st.session_state.get("owm_api_key", ""),
            type="password",
            placeholder="e.g. a1b2c3d4e5f6..."
        )
        if api_key_input:
            st.session_state["owm_api_key"] = api_key_input
            st.success("✅ API key saved!")

    col1, col2 = st.columns([3, 1])
    with col1:
        location = st.text_input("📍 Enter City / District", "Hyderabad")
    with col2:
        unit = st.selectbox("🌡️ Unit", ["Celsius (°C)", "Fahrenheit (°F)"])

    units_param = "metric" if "Celsius" in unit else "imperial"
    unit_sym = "°C" if "Celsius" in unit else "°F"

    if st.button("🔄 Get Live Weather", use_container_width=True):
        api_key = st.session_state.get("owm_api_key", "")
        
        if api_key:
            # ── Live API call ──────────────────────────────────────
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={location},IN&appid={api_key}&units={units_param}"
                resp = requests.get(url, timeout=8)
                if resp.status_code == 200:
                    data = resp.json()
                    temp        = round(data["main"]["temp"], 1)
                    feels_like  = round(data["main"]["feels_like"], 1)
                    humidity    = data["main"]["humidity"]
                    wind        = round(data["wind"]["speed"] * 3.6, 1)   # m/s → km/h
                    description = data["weather"][0]["description"].title()
                    rain_1h     = data.get("rain", {}).get("1h", 0)
                    pressure    = data["main"]["pressure"]
                    visibility  = round(data.get("visibility", 10000) / 1000, 1)
                    clouds      = data["clouds"]["all"]
                    icon_code   = data["weather"][0]["icon"]

                    # Weather emoji
                    cond_id = data["weather"][0]["id"]
                    if cond_id < 300:   w_emoji = "⛈️"
                    elif cond_id < 500: w_emoji = "🌦️"
                    elif cond_id < 600: w_emoji = "🌧️"
                    elif cond_id < 700: w_emoji = "🌨️"
                    elif cond_id < 800: w_emoji = "🌫️"
                    elif cond_id == 800: w_emoji = "☀️"
                    else:               w_emoji = "⛅"

                    rainfall_prob = min(100, clouds + (rain_1h * 20))

                else:
                    st.error(f"❌ City not found or invalid API key. Status: {resp.status_code}")
                    return
            except requests.exceptions.ConnectionError:
                st.warning("⚠️ No internet — showing simulated weather data.")
                weather_sim = get_simulated_weather(location)
                temp, feels_like   = weather_sim["temp"], weather_sim["feels_like"]
                humidity, wind     = weather_sim["humidity"], weather_sim["wind"]
                rainfall_prob      = weather_sim["rainfall_prob"]
                description        = weather_sim["condition"]
                w_emoji            = "🌤️"
                pressure           = 1013
                visibility         = 10.0
                clouds             = int(humidity * 0.6)
            except Exception as e:
                st.error(f"❌ Error: {e}")
                return
        else:
            # ── Simulated fallback (no API key) ────────────────────
            st.info("💡 No API key entered — showing simulated weather. Add a free key above for live data.")
            weather_sim = get_simulated_weather(location)
            temp, feels_like   = weather_sim["temp"], weather_sim["feels_like"]
            humidity, wind     = weather_sim["humidity"], weather_sim["wind"]
            rainfall_prob      = weather_sim["rainfall_prob"]
            description        = weather_sim["condition"]
            w_emoji            = "🌤️"
            pressure           = 1013
            visibility         = 10.0
            clouds             = int(humidity * 0.6)

        # ── Display weather cards ──────────────────────────────────
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0277bd,#0288d1,#039be5);
                    color:white;border-radius:20px;padding:2rem;text-align:center;
                    margin-bottom:1.5rem;box-shadow:0 8px 30px rgba(2,119,189,0.3)">
          <div style="font-size:4rem">{w_emoji}</div>
          <div style="font-size:2.5rem;font-weight:700">{temp}{unit_sym}</div>
          <div style="font-size:1rem;opacity:0.9">{description} · {location}</div>
          <div style="font-size:0.85rem;opacity:0.8;margin-top:0.3rem">Feels like {feels_like}{unit_sym}</div>
          <div style="display:flex;justify-content:space-around;margin-top:1.5rem;font-size:0.9rem">
            <div>💧 {humidity}%<br><small>Humidity</small></div>
            <div>💨 {wind} km/h<br><small>Wind</small></div>
            <div>🌧️ {rainfall_prob:.0f}%<br><small>Rain Chance</small></div>
            <div>🌡️ {pressure} hPa<br><small>Pressure</small></div>
            <div>👁️ {visibility} km<br><small>Visibility</small></div>
          </div>
        </div>""", unsafe_allow_html=True)

        speak(f"Live weather for {location}. Temperature is {temp} degrees. {description}. Humidity {humidity} percent. Wind speed {wind} kilometres per hour.", lang)

        # ── Farming advisories based on conditions ─────────────────
        st.markdown('<div class="section-header">🌾 AI Farming Advisories</div>', unsafe_allow_html=True)
        advisories = []
        if rainfall_prob > 60:
            advisories += ["🚫 **Avoid pesticide/fertilizer spraying** — rain likely, chemicals will wash off",
                           "💧 **Skip irrigation today** — natural rainfall expected",
                           "🌱 **Good time for transplanting** seedlings after rain"]
        if temp > 38:
            advisories += [f"🌡️ **Extreme heat alert ({temp}{unit_sym})** — irrigate at 5–7 AM only",
                           "🍂 **Apply mulch** to reduce soil temperature by 5–8°C",
                           "🚜 **Avoid field work** between 11 AM – 4 PM"]
        if humidity > 80:
            advisories += ["🍄 **High fungal disease risk!** Inspect crops for Powdery Mildew, Blight",
                           "💊 **Apply preventive fungicide** (Mancozeb 2.5g/L) as precaution"]
        if wind > 25:
            advisories += ["💨 **Strong winds — postpone all spraying** operations",
                           "🌿 **Check for lodging** in tall crops like maize, sugarcane"]
        if temp < 12:
            advisories += [f"❄️ **Cold stress alert ({temp}{unit_sym})** — protect young seedlings",
                           "🌾 **Delay irrigation** — cold water can shock root systems"]
        if not advisories:
            advisories = ["✅ **Good weather for all farming operations today!**",
                          "🌱 **Ideal for:** sowing, spraying, fertilizer application",
                          "🔍 **Good visibility** for pest scouting"]

        for adv in advisories:
            st.markdown(f'<div class="alert-box">{adv}</div>', unsafe_allow_html=True)

        speak("Farming advisory: " + " ".join([a.replace("**","").replace("🚫","").replace("💧","").replace("🌡️","").replace("✅","") for a in advisories[:2]]), lang)

        # ── 7-day simulated forecast ───────────────────────────────
        st.markdown('<div class="section-header">📅 7-Day Forecast (Simulated Trend)</div>', unsafe_allow_html=True)
        days = ["Today","Tomorrow","Wed","Thu","Fri","Sat","Sun"]
        emojis = [w_emoji, "⛅","🌧️","🌦️","☀️","⛅","☀️"]
        temps_7 = [round(temp + random.uniform(-4, 4)) for _ in range(7)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=temps_7, mode='lines+markers+text',
                                  text=[f"{t}{unit_sym}" for t in temps_7],
                                  textposition='top center',
                                  line=dict(color='#f57c00', width=2.5),
                                  marker=dict(size=9, color='#f57c00')))
        for i, (d, e) in enumerate(zip(days, emojis)):
            fig.add_annotation(x=d, y=min(temps_7)-4, text=e, showarrow=False, font=dict(size=18))
        fig.update_layout(height=240, margin=dict(l=10,r=10,t=20,b=50),
                          plot_bgcolor='white', paper_bgcolor='white',
                          font=dict(family="Poppins"), yaxis_title=f"Temp ({unit_sym})",
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ─── MODULE: GOVERNMENT SCHEMES ──────────────────────────────────
GOVT_SCHEMES = [
    {
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "icon": "🏛️",
        "benefit": "₹6,000/year direct income support in 3 instalments of ₹2,000",
        "eligibility": "All small & marginal farmers with cultivable land",
        "documents": ["Aadhaar Card", "Land Records (Khasra/Khatauni)", "Bank Account linked to Aadhaar"],
        "apply": "pmkisan.gov.in or nearest CSC centre",
        "deadline": "Ongoing — apply anytime",
        "category": "Income Support",
        "states": "All India",
        "color": "#e8f5e9"
    },
    {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "icon": "🛡️",
        "benefit": "Crop insurance at 2% premium for Kharif, 1.5% for Rabi, 5% for horticulture",
        "eligibility": "All farmers growing notified crops in notified areas",
        "documents": ["Aadhaar Card", "Bank Passbook", "Land Records", "Sowing Certificate"],
        "apply": "Nearest bank branch or insurance company before cut-off date",
        "deadline": "Before sowing cut-off date of each season",
        "category": "Crop Insurance",
        "states": "All India",
        "color": "#e3f2fd"
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "icon": "💳",
        "benefit": "Crop loans up to ₹3 lakh at 4% interest rate (after 3% subvention)",
        "eligibility": "All farmers, tenant farmers, share croppers, SHGs",
        "documents": ["Aadhaar Card", "Land Records", "Passport Photo", "Bank Account"],
        "apply": "Any nationalized bank, cooperative bank, or RRB",
        "deadline": "Ongoing — apply anytime",
        "category": "Credit / Loan",
        "states": "All India",
        "color": "#fff3e0"
    },
    {
        "name": "Soil Health Card Scheme",
        "icon": "🌱",
        "benefit": "Free soil testing + personalized nutrient recommendations card",
        "eligibility": "All farmers — free of cost",
        "documents": ["Aadhaar Card", "Land location details"],
        "apply": "Nearest Krishi Vigyan Kendra (KVK) or Agriculture Department",
        "deadline": "Ongoing",
        "category": "Soil & Inputs",
        "states": "All India",
        "color": "#f3e5f5"
    },
    {
        "name": "PM Krishi Sinchai Yojana (PMKSY)",
        "icon": "💧",
        "benefit": "Subsidy up to 90% on drip/sprinkler irrigation systems",
        "eligibility": "Small & marginal farmers (higher subsidy), all farmers eligible",
        "documents": ["Aadhaar Card", "Land Records", "Bank Account", "Quotation from supplier"],
        "apply": "State Agriculture Department or Horticulture Department",
        "deadline": "Annual — check state agriculture portal",
        "category": "Irrigation",
        "states": "All India",
        "color": "#e0f7fa"
    },
    {
        "name": "National Food Security Mission (NFSM)",
        "icon": "🌾",
        "benefit": "Subsidized seeds, fertilizers, farm machinery, and training",
        "eligibility": "Farmers in identified low-productivity districts",
        "documents": ["Aadhaar Card", "Land Records"],
        "apply": "District Agriculture Officer",
        "deadline": "Before season — check with district office",
        "category": "Seeds & Inputs",
        "states": "Selected districts",
        "color": "#f1f8e9"
    },
    {
        "name": "eNAM — National Agriculture Market",
        "icon": "📈",
        "benefit": "Online trading platform — sell crops at best price across India",
        "eligibility": "All farmers",
        "documents": ["Aadhaar Card", "Bank Account", "Mobile Number"],
        "apply": "enam.gov.in or nearest APMC mandi",
        "deadline": "Ongoing",
        "category": "Market Access",
        "states": "All India",
        "color": "#fff8e1"
    },
    {
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "icon": "♻️",
        "benefit": "₹50,000/ha for 3 years for organic farming cluster development",
        "eligibility": "Farmers willing to adopt organic farming in clusters of 50 acres",
        "documents": ["Aadhaar Card", "Land Records", "Group formation documents"],
        "apply": "State Organic Certification Agency or Agriculture Department",
        "deadline": "Annual — check state portal",
        "category": "Organic Farming",
        "states": "All India",
        "color": "#e8f5e9"
    },
]

def show_govt_schemes(T, lang):
    st.markdown(f'<div class="section-header">🏛️ {T.get("schemes","Government Schemes")} — Benefits for Farmers</div>', unsafe_allow_html=True)
    speak("Government Schemes for Farmers. Discover benefits, eligibility, and how to apply for PM-KISAN, crop insurance, Kisan Credit Card, and more.", lang)

    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("🏛️", "8+", "Active Schemes"),
        ("💰", "₹6,000", "PM-KISAN/Year"),
        ("🛡️", "2%", "Min Insurance Premium"),
        ("💳", "4%", "KCC Interest Rate"),
    ]
    for col, (icon, val, label) in zip([col1,col2,col3,col4], stats):
        col.markdown(f"""
        <div class="metric-card">
          <div style="font-size:1.8rem">{icon}</div>
          <div class="metric-number" style="font-size:1.4rem">{val}</div>
          <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter by category
    categories = ["All"] + list(set([s["category"] for s in GOVT_SCHEMES]))
    cat_filter = st.selectbox("🔍 Filter by Category", categories)
    filtered = GOVT_SCHEMES if cat_filter == "All" else [s for s in GOVT_SCHEMES if s["category"] == cat_filter]

    for scheme in filtered:
        with st.expander(f"{scheme['icon']} {scheme['name']} — {scheme['category']}"):
            col_a, col_b = st.columns([3, 2])
            with col_a:
                st.markdown(f"""
                <div style="background:{scheme['color']};border-radius:12px;padding:1.2rem;
                            border-left:5px solid #2e7d32;margin-bottom:0.8rem">
                  <div style="font-size:1.1rem;font-weight:700;color:#1b5e20">{scheme['icon']} {scheme['name']}</div>
                  <div style="margin-top:0.5rem;color:#222">
                    <b>💰 Benefit:</b> {scheme['benefit']}<br><br>
                    <b>✅ Eligibility:</b> {scheme['eligibility']}<br><br>
                    <b>📅 Deadline:</b> {scheme['deadline']}<br><br>
                    <b>🌍 Coverage:</b> {scheme['states']}
                  </div>
                </div>""", unsafe_allow_html=True)
            with col_b:
                st.markdown("**📋 Documents Required:**")
                for doc in scheme["documents"]:
                    st.markdown(f"✅ {doc}")
                st.markdown(f"**🖥️ How to Apply:**")
                st.markdown(f"👉 {scheme['apply']}")
                speak(f"{scheme['name']}. Benefit: {scheme['benefit']}. Eligibility: {scheme['eligibility']}. Apply at: {scheme['apply']}", lang)

    # Helpline numbers
    st.markdown('<div class="section-header">📞 Important Helplines</div>', unsafe_allow_html=True)
    helplines = [
        ("🌾 Kisan Call Centre", "1800-180-1551", "Free • 24/7 • All languages"),
        ("🏛️ PM-KISAN Helpline", "155261 / 011-24300606", "Mon–Fri 9AM–6PM"),
        ("🛡️ PMFBY Helpline", "1800-200-7710", "Free • For crop insurance queries"),
        ("💧 Water/Irrigation", "1800-180-1551", "Ministry of Jal Shakti"),
        ("🌱 Soil Health Card", "1800-180-1551", "Agriculture extension"),
        ("📈 eNAM Support", "1800-270-0224", "Online market queries"),
    ]
    cols = st.columns(3)
    for i, (name, number, note) in enumerate(helplines):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:1rem;
                        box-shadow:0 2px 10px rgba(0,0,0,0.07);margin-bottom:0.8rem;
                        border-top:3px solid #2e7d32;text-align:center">
              <div style="font-weight:700;color:#1b5e20">{name}</div>
              <div style="font-size:1.3rem;font-weight:700;color:#1565c0;margin:0.3rem 0">📞 {number}</div>
              <div style="font-size:0.78rem;color:#555">{note}</div>
            </div>""", unsafe_allow_html=True)


# ─── MODULE: LOAN & INSURANCE CALCULATOR ─────────────────────────
def show_loan_calculator(T, lang):
    st.markdown(f'<div class="section-header">💰 {T.get("loan","Loan & Insurance Calculator")}</div>', unsafe_allow_html=True)
    speak("Loan and Insurance Calculator. Calculate your Kisan Credit Card loan eligibility and crop insurance premium.", lang)

    tab1, tab2, tab3 = st.tabs(["💳 Kisan Credit Card", "🛡️ Crop Insurance (PMFBY)", "📊 Loan Comparison"])

    # ── Tab 1: KCC ─────────────────────────────────────────────────
    with tab1:
        st.markdown("#### 💳 Kisan Credit Card Loan Calculator")
        col1, col2 = st.columns(2)
        with col1:
            land_area   = st.number_input("Land Area (Acres)", 0.1, 50.0, 2.0, 0.5)
            crop_kcc    = st.selectbox("Crop", list(CROP_DATABASE.keys()), key="kcc_crop")
            season_kcc  = st.selectbox("Season", ["Kharif","Rabi","Summer"], key="kcc_season")
            bank_type   = st.selectbox("Bank Type", ["Nationalized Bank","Cooperative Bank","RRB","Private Bank"])
        with col2:
            existing_loan = st.number_input("Existing Loan (₹)", 0, 500000, 0, 5000)
            land_value    = st.number_input("Land Value (₹/Acre)", 50000, 2000000, 200000, 10000)
            credit_score  = st.select_slider("Credit Score", ["Poor","Fair","Good","Very Good","Excellent"], value="Good")

        if st.button("💳 Calculate KCC Eligibility", use_container_width=True, key="kcc_calc"):
            # Calculate scale of finance
            crop_d        = CROP_DATABASE[crop_kcc]
            base_price    = crop_d["market_price"]
            scale_finance = round(land_area * 15000 * (1.2 if season_kcc == "Kharif" else 1.0))
            credit_mult   = {"Poor": 0.5, "Fair": 0.7, "Good": 1.0, "Very Good": 1.2, "Excellent": 1.3}[credit_score]
            max_loan      = round(min(scale_finance * credit_mult, land_value * land_area * 0.5) - existing_loan)
            interest_rate = {"Nationalized Bank": 7.0, "Cooperative Bank": 6.5, "RRB": 7.0, "Private Bank": 9.5}[bank_type]
            effective_rate = max(4.0, interest_rate - 3.0)  # 3% govt subvention
            annual_int    = round(max_loan * effective_rate / 100)
            emi           = round(max_loan / 12)

            speak(f"KCC Loan eligibility: Maximum loan amount is {max_loan} rupees. Effective interest rate is {effective_rate} percent per year. Annual interest payable is {annual_int} rupees.", lang)

            st.success("✅ KCC Loan Eligibility Calculated!")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💰 Max Loan Amount", f"₹{max_loan:,}")
            c2.metric("📊 Effective Rate", f"{effective_rate}% p.a.")
            c3.metric("💸 Annual Interest", f"₹{annual_int:,}")
            c4.metric("📅 Monthly Repay", f"₹{emi:,}")

            st.markdown(f"""
            <div class="result-box">
              <b>📋 Loan Details Summary</b><br><br>
              <b>Scale of Finance:</b> ₹{scale_finance:,} for {land_area} acres of {crop_kcc}<br>
              <b>Bank Interest Rate:</b> {interest_rate}% → After 3% Govt Subvention = <b>{effective_rate}%</b><br>
              <b>Repayment Period:</b> 12 months (crop cycle based)<br>
              <b>Collateral Required:</b> {'None (< ₹1.6L)' if max_loan < 160000 else 'Land mortgage may be required'}<br><br>
              <b>💡 Tip:</b> Repay within 1 year to avail 3% interest subvention — effective rate becomes just 4%!
            </div>""", unsafe_allow_html=True)

            # Amortization chart
            months = list(range(1, 13))
            outstanding = [round(max_loan * (1 - i/12)) for i in range(12)]
            int_paid    = [round(max_loan * effective_rate / 100 * i / 12) for i in range(1,13)]
            fig = go.Figure()
            fig.add_trace(go.Bar(x=months, y=outstanding, name="Outstanding Loan", marker_color="#ef5350"))
            fig.add_trace(go.Scatter(x=months, y=int_paid, name="Interest Paid", line=dict(color="#2e7d32", width=2), mode='lines+markers'))
            fig.update_layout(title="Loan Repayment Schedule", height=280,
                              plot_bgcolor='white', paper_bgcolor='white',
                              font=dict(family="Poppins"), xaxis_title="Month",
                              yaxis_title="Amount (₹)", barmode='overlay',
                              legend=dict(orientation="h"))
            st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2: PMFBY Insurance ─────────────────────────────────────
    with tab2:
        st.markdown("#### 🛡️ PMFBY Crop Insurance Premium Calculator")
        col1, col2 = st.columns(2)
        with col1:
            crop_ins    = st.selectbox("Crop", list(CROP_DATABASE.keys()), key="ins_crop")
            season_ins  = st.selectbox("Season", ["Kharif (2%)","Rabi (1.5%)","Horticulture (5%)"], key="ins_season")
            area_ins    = st.number_input("Area (Hectares)", 0.1, 50.0, 1.0, 0.5, key="ins_area")
        with col2:
            sum_insured = st.number_input("Sum Insured (₹/Ha)", 10000, 200000, 50000, 5000)
            state_ins   = st.selectbox("State", ["Andhra Pradesh","Telangana","Maharashtra","Karnataka","Tamil Nadu","Rajasthan","Madhya Pradesh","Uttar Pradesh","Punjab","Haryana","Bihar","West Bengal"])

        if st.button("🛡️ Calculate Insurance Premium", use_container_width=True, key="ins_calc"):
            prem_rates  = {"Kharif (2%)": 0.02, "Rabi (1.5%)": 0.015, "Horticulture (5%)": 0.05}
            farmer_rate = prem_rates[season_ins]
            total_sum   = sum_insured * area_ins
            farmer_prem = round(total_sum * farmer_rate)
            actuarial   = round(total_sum * 0.12)   # Typical actuarial rate
            govt_share  = actuarial - farmer_prem
            max_claim   = total_sum

            speak(f"Crop insurance premium for {crop_ins}: You pay {farmer_prem} rupees. Maximum claim amount is {max_claim} rupees. Government subsidy covers {govt_share} rupees of the premium.", lang)

            st.success("✅ Insurance Premium Calculated!")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💰 You Pay", f"₹{farmer_prem:,}", f"{int(farmer_rate*100)}% of sum insured")
            c2.metric("🏛️ Govt Pays", f"₹{govt_share:,}", "Subsidy")
            c3.metric("📋 Total Premium", f"₹{actuarial:,}", "Actuarial rate")
            c4.metric("🛡️ Max Claim", f"₹{max_claim:,}", "If 100% crop loss")

            # Risk coverage chart
            categories_ins = ["Drought", "Flood", "Cyclone", "Pest/Disease", "Hailstorm", "Landslide"]
            coverage       = [95, 90, 85, 80, 88, 75]
            fig2 = go.Figure(go.Bar(x=categories_ins, y=coverage,
                                    marker_color='#2e7d32',
                                    text=[f"{c}%" for c in coverage],
                                    textposition='outside'))
            fig2.update_layout(title="Coverage % by Risk Type", height=260,
                               plot_bgcolor='white', paper_bgcolor='white',
                               font=dict(family="Poppins"), yaxis=dict(range=[0,110]),
                               yaxis_title="Coverage (%)")
            st.plotly_chart(fig2, use_container_width=True)

            st.info(f"📞 To claim: Call 14447 or contact your nearest insurance company. Submit claim within 72 hours of crop damage.")

    # ── Tab 3: Loan Comparison ─────────────────────────────────────
    with tab3:
        st.markdown("#### 📊 Bank Loan Comparison")
        loan_amt = st.slider("Loan Amount (₹)", 10000, 300000, 100000, 5000)
        banks = {
            "State Bank of India": {"rate": 7.0, "processing": 0.5, "max_tenure": 12},
            "NABARD (via RRB)":    {"rate": 6.5, "processing": 0.0, "max_tenure": 12},
            "Cooperative Bank":    {"rate": 6.0, "processing": 0.0, "max_tenure": 12},
            "Punjab National Bank":{"rate": 7.0, "processing": 0.5, "max_tenure": 12},
            "HDFC Bank":           {"rate": 9.5, "processing": 1.0, "max_tenure": 12},
            "Axis Bank":           {"rate": 9.0, "processing": 1.0, "max_tenure": 12},
        }
        rows = []
        for bank, info in banks.items():
            eff  = max(4.0, info["rate"] - 3.0)
            ann_int = round(loan_amt * eff / 100)
            proc_fee = round(loan_amt * info["processing"] / 100)
            total_cost = ann_int + proc_fee
            rows.append({"Bank": bank, "Rate": f"{info['rate']}%",
                         "After Subsidy": f"{eff}%",
                         "Annual Interest": f"₹{ann_int:,}",
                         "Processing Fee": f"₹{proc_fee:,}",
                         "Total Cost": f"₹{total_cost:,}"})
        df_banks = pd.DataFrame(rows)
        st.dataframe(df_banks, use_container_width=True, hide_index=True)
        st.caption("💡 Cooperative banks & NABARD have lowest rates. Always compare before applying.")


# ─── MODULE: ABOUT / TEAM ─────────────────────────────────────────
def show_about(T, lang):
    st.markdown('<div class="section-header">👥 About — Smart Crop Advisory System</div>', unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1b5e20,#2e7d32,#43a047);
                color:white;border-radius:20px;padding:2.5rem;text-align:center;
                margin-bottom:2rem;box-shadow:0 10px 40px rgba(27,94,32,0.4)">
      <div style="font-size:4rem">🌾</div>
      <h1 style="font-family:'Playfair Display',serif;margin:0.5rem 0">Smart Crop Advisory System</h1>
      <p style="font-size:1rem;opacity:0.9;max-width:600px;margin:0.5rem auto">
        An AI-powered agricultural decision support system built to empower India's
        140 million small and marginal farmers with data-driven farming intelligence.
      </p>
      <div style="margin-top:1rem">
        <span style="background:rgba(255,255,255,0.2);padding:5px 14px;border-radius:12px;margin:4px;display:inline-block;font-size:0.85rem">🤖 AI-Powered</span>
        <span style="background:rgba(255,255,255,0.2);padding:5px 14px;border-radius:12px;margin:4px;display:inline-block;font-size:0.85rem">🔊 Voice Enabled</span>
        <span style="background:rgba(255,255,255,0.2);padding:5px 14px;border-radius:12px;margin:4px;display:inline-block;font-size:0.85rem">🌐 8 Languages</span>
        <span style="background:rgba(255,255,255,0.2);padding:5px 14px;border-radius:12px;margin:4px;display:inline-block;font-size:0.85rem">📱 Mobile Friendly</span>
        <span style="background:rgba(255,255,255,0.2);padding:5px 14px;border-radius:12px;margin:4px;display:inline-block;font-size:0.85rem">☁️ Streamlit Cloud</span>
      </div>
    </div>""", unsafe_allow_html=True)

    speak("Smart Crop Advisory System. An AI-powered platform built to help small and marginal farmers of India with crop planning, disease detection, weather advice, government schemes, and more.", lang)

    # Team section — editable
    st.markdown('<div class="section-header">👨‍💻 Team Members</div>', unsafe_allow_html=True)
    st.info("✏️ Edit the team details below in app.py → `TEAM_MEMBERS` list to match your actual team!")

    TEAM_MEMBERS = [
        {"name": "Your Name Here",    "role": "Team Lead & Full Stack Developer", "icon": "👨‍💻", "skills": "Python, Streamlit, AI/ML"},
        {"name": "Member 2 Name",     "role": "Data Scientist & ML Engineer",     "icon": "🧠", "skills": "Scikit-learn, TensorFlow, Data Analysis"},
        {"name": "Member 3 Name",     "role": "UI/UX Designer",                   "icon": "🎨", "skills": "Figma, CSS, User Research"},
        {"name": "Member 4 Name",     "role": "Domain Expert (Agriculture)",      "icon": "🌾", "skills": "Agronomy, Soil Science, Crop Management"},
    ]

    cols = st.columns(len(TEAM_MEMBERS))
    for col, member in zip(cols, TEAM_MEMBERS):
        col.markdown(f"""
        <div style="background:white;border-radius:16px;padding:1.5rem;text-align:center;
                    box-shadow:0 4px 20px rgba(0,0,0,0.08);border-top:4px solid #2e7d32;
                    height:100%">
          <div style="font-size:3rem">{member['icon']}</div>
          <div style="font-weight:700;color:#1b5e20;margin:0.5rem 0;font-size:1rem">{member['name']}</div>
          <div style="color:#555;font-size:0.85rem;font-weight:600">{member['role']}</div>
          <div style="color:#777;font-size:0.78rem;margin-top:0.5rem">{member['skills']}</div>
        </div>""", unsafe_allow_html=True)

    # Project details
    st.markdown('<div class="section-header">📋 Project Details</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
        <div class="result-box">
          <b>🏆 Project Information</b><br><br>
          <b>📌 Event/Hackathon:</b> Add your event name here<br>
          <b>🏫 Institution:</b> Add your college/university<br>
          <b>📅 Year:</b> 2026<br>
          <b>🏷️ Category:</b> Agriculture Tech / AI for Social Good<br>
          <b>🌐 Live Demo:</b> your-app.streamlit.app<br>
          <b>📂 GitHub:</b> github.com/yourusername/smart-crop-advisory
        </div>""", unsafe_allow_html=True)
    with col_r:
        st.markdown("""
        <div class="result-box">
          <b>🛠️ Tech Stack</b><br><br>
          <b>Frontend & Backend:</b> Python + Streamlit<br>
          <b>Data Processing:</b> Pandas, NumPy<br>
          <b>Visualizations:</b> Plotly<br>
          <b>Image Processing:</b> Pillow (PIL)<br>
          <b>Weather API:</b> OpenWeatherMap<br>
          <b>Voice (TTS):</b> Web Speech API (browser-native)<br>
          <b>Deployment:</b> Streamlit Cloud (Free)
        </div>""", unsafe_allow_html=True)

    # Features summary
    st.markdown('<div class="section-header">✨ Features Built</div>', unsafe_allow_html=True)
    features = [
        ("🏠","Dashboard","Live weather, market trends, crop calendar, alerts"),
        ("🌱","Crop Recommendation","AI-powered crop selection based on soil & climate"),
        ("🔬","Disease Scanner","Upload plant image → detect disease + treatment"),
        ("🌤️","Weather (Live API)","Real-time weather from OpenWeatherMap"),
        ("📈","Market Prices","Live mandi prices + 12-month price trends"),
        ("💧","Irrigation Planner","Personalized weekly irrigation schedule"),
        ("🧪","Fertilizer Guide","Precision NPK recommendation with schedule"),
        ("🐛","Pest Warning","Seasonal alerts + IPM strategies"),
        ("🔄","Crop Rotation","3-year rotation planner for soil health"),
        ("📚","Crop Library","Encyclopedia for 10+ crops"),
        ("🤖","AI Chatbot","Natural language farming assistant"),
        ("📊","Farm Analytics","Yield trends, disease charts, profitability"),
        ("🛰️","Satellite Monitor","NDVI crop health mapping simulation"),
        ("🚁","Drone Scout","AI drone field inspection simulation"),
        ("💡","Daily Tips","Curated farming tips by category"),
        ("📅","Seasonal Guide","Season-wise crop planning"),
        ("🏛️","Govt Schemes","PM-KISAN, PMFBY, KCC and 8 more schemes"),
        ("💰","Loan Calculator","KCC loan + PMFBY insurance calculator"),
    ]
    cols_f = st.columns(3)
    for i, (icon, name, desc) in enumerate(features):
        with cols_f[i % 3]:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:0.8rem;
                        margin-bottom:0.6rem;box-shadow:0 2px 8px rgba(0,0,0,0.06);
                        border-left:3px solid #4caf50">
              <b style="color:#1b5e20">{icon} {name}</b><br>
              <span style="font-size:0.8rem;color:#444">{desc}</span>
            </div>""", unsafe_allow_html=True)

# ─── MODULE: WEATHER (original simulated — kept as fallback) ──────
# The original show_weather is now replaced above with the API version.
# get_simulated_weather is still used as fallback inside the new show_weather.

# ─── SIDEBAR ─────────────────────────────────────────────────────
def setup_sidebar():
    with st.sidebar:
        # Language selector
        lang = st.selectbox(
            "🌐 Language / भाषा",
            list(TRANSLATIONS.keys()),
            key="language_select"
        )
        T = TRANSLATIONS[lang]

        st.markdown("---")
        st.markdown(f"<h2 style='color:white;text-align:center;font-size:1.1rem'>🌾 Smart Crop Advisory</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:rgba(255,255,255,0.8);text-align:center;font-size:0.8rem'>AI-Powered Farming Platform</p>", unsafe_allow_html=True)
        st.markdown("---")

        menu_items = [
            ("dashboard", "🏠 Dashboard"),
            ("crop_rec",  "🌱 Crop Recommendation"),
            ("disease",   "🔬 Disease Scanner"),
            ("weather",   "🌤️ Weather (Live API)"),
            ("market",    "📈 Market Prices"),
            ("irrigation","💧 Irrigation Planner"),
            ("fertilizer","🧪 Fertilizer Guide"),
            ("pest",      "🐛 Pest Warning"),
            ("rotation",  "🔄 Crop Rotation"),
            ("library",   "📚 Crop Library"),
            ("chatbot",   "🤖 AI Chatbot"),
            ("analytics", "📊 Farm Analytics"),
            ("schemes",   "🏛️ Govt Schemes"),
            ("loan",      "💰 Loan & Insurance"),
            ("satellite", "🛰️ Satellite Monitor"),
            ("drone",     "🚁 Drone Scout"),
            ("tips",      "💡 Daily Tips"),
            ("seasonal",  "📅 Seasonal Guide"),
            ("about",     "👥 About / Team"),
        ]

        if "active_page" not in st.session_state:
            st.session_state.active_page = "dashboard"

        for key, label in menu_items:
            btn_style = "background:rgba(255,255,255,0.25)" if st.session_state.active_page == key else "background:rgba(255,255,255,0.08)"
            if st.button(T.get(key, label), key=f"nav_{key}", use_container_width=True):
                st.session_state.active_page = key
                st.rerun()

        st.markdown("---")
        st.markdown("""
        <div style="text-align:center;color:rgba(255,255,255,0.7);font-size:0.75rem;padding:0.5rem">
          🌾 Smart Crop Advisory v3.0<br>
          Built for Indian Farmers 🇮🇳<br>
          🤖 AI | 🔊 Voice | 🌐 8 Languages<br>
          🌤️ Live Weather | 🏛️ Govt Schemes
        </div>""", unsafe_allow_html=True)

    return T, lang

# ─── MAIN APP ────────────────────────────────────────────────────
def main():
    load_css()
    T, lang = setup_sidebar()
    page = st.session_state.get("active_page", "dashboard")

    routes = {
        "dashboard":  show_dashboard,
        "crop_rec":   show_crop_recommendation,
        "disease":    show_disease_scanner,
        "weather":    show_weather,
        "market":     show_market_prices,
        "irrigation": show_irrigation,
        "fertilizer": show_fertilizer,
        "pest":       show_pest_warning,
        "rotation":   show_crop_rotation,
        "library":    show_crop_library,
        "chatbot":    show_chatbot,
        "analytics":  show_analytics,
        "schemes":    show_govt_schemes,
        "loan":       show_loan_calculator,
        "satellite":  show_satellite,
        "drone":      show_drone,
        "tips":       show_daily_tips,
        "seasonal":   show_seasonal_guide,
        "about":      show_about,
    }

    if page in routes:
        routes[page](T, lang)
    else:
        show_dashboard(T, lang)

    # Footer
    st.markdown("""
    <div class="footer">
      🌾 Smart Crop Advisory System v3.0 | Built for Indian Farmers 🇮🇳 | AI-Powered 🤖 | Voice Enabled 🔊<br>
      🌐 8 Languages | 🌤️ Live Weather API | 🏛️ Govt Schemes | 💰 Loan Calculator | 19 Modules<br>
      <small>⚠️ Recommendations are advisory. Consult local agricultural extension officers for verified advice.</small>
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
