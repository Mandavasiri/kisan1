# 🤝 Contributing to Smart Crop Advisory System

Thank you for your interest in contributing! This project helps Indian farmers with AI-powered farming advice.

---

## 🚀 How to Contribute

### 1. Fork & Clone
```bash
git fork https://github.com/yourusername/smart-crop-advisory
git clone https://github.com/YOUR_USERNAME/smart-crop-advisory
cd smart-crop-advisory
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

### 3. Run Locally
```bash
streamlit run app.py
```

### 4. Make Changes & Test
- Make your changes in `app.py`
- Test all modules that you changed
- Ensure the app runs without errors

### 5. Submit Pull Request
```bash
git add .
git commit -m "feat: add [your feature name]"
git push origin main
```
Then open a Pull Request on GitHub.

---

## 💡 Ways to Contribute

| Type | Examples |
|------|---------|
| 🐛 Bug Fix | Fix errors, crashes, broken features |
| ✨ New Feature | Add new crop, disease, scheme, language |
| 🌐 Translation | Add/improve language translations |
| 📊 Data | Add more crop data, disease info |
| 🎨 UI/UX | Improve mobile layout, accessibility |
| 📝 Docs | Improve README, add comments |

---

## 📋 Code Style Guidelines

- Add comments for all new functions
- Follow existing naming conventions
- Test on both desktop and mobile
- Keep single-file structure (`app.py`)
- Add new translations to ALL 8 languages

---

## 🌐 Adding a New Language

1. Add language to `TRANSLATIONS` dict in `app.py`
2. Add language to `LANG_VOICE_MAP` for voice support
3. Test all UI labels display correctly
4. Submit PR with language name in title

---

## 🐛 Reporting Bugs

Open a GitHub Issue with:
- Module where bug occurs
- Steps to reproduce
- Expected vs actual behavior
- Screenshot if possible

---

## 📞 Contact

Open a GitHub Discussion for questions or feature ideas.

**Together, let's help every farmer in India! 🌾**
