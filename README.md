# Agrobot — AI-Powered Farmer Assistant 🌱

![MIT License](https://img.shields.io/badge/license-MIT-green)  
![Python](https://img.shields.io/badge/python-3.8%2B-blue)  
![Framework](https://img.shields.io/badge/framework-Flask-orange)  
![Model](https://img.shields.io/badge/model-CNN-informational)  

---

## 🌟 Introduction
Welcome to *Agrobot*, your AI-driven farming buddy! 🚜  
Agrobot empowers farmers with *AI-based plant disease detection* and *multilingual chatbot support*.  
Built with Flask, TensorFlow, and trained on the PlantVillage dataset, it identifies diseases (like Tomato Bacterial Spot or Potato Late Blight) and provides *prevention tips* in *English, Hindi, Bengali, and Telugu*.  

Farmers can *upload leaf images 📸* or *describe symptoms 💬*, and Agrobot will guide them toward better crop health. 🌍  

---

## ✨ Features
- 🌐 *Multilingual Magic* — English, Hindi, Bengali, Telugu  
- 📷 *Image Detection* — Upload plant pics for instant AI diagnosis  
- 💬 *Symptom Chatbot* — Text-based disease detection & advice  
- 👨‍💻 *Admin Dashboard* — Manage diseases & users  
- 🔒 *Secure Login* — Role-based authentication for admins & farmers  

---

## 🛠 Prerequisites
- 🐍 Python *3.8+*  
- 📥 Git (for cloning the repo)  
- 🌐 Internet connection (for installing dependencies)  

---

## ⚙ Setup Instructions

# Clone the repository
git clone https://github.com/anika0520/agrobot.git

cd agrobot

# Create & activate a virtual environment
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Prepare the dataset (example for Windows PowerShell)
Expand-Archive -Path dataset/photos.zip -DestinationPath dataset

# Train the model (takes 5-10 mins ⏳)
python app/train_model.py
# Output: app/static/models/model.h5

# Run the application
python run.py
``
👉 Access at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🎮 Usage

* 🖼 *Upload Images* — Detect diseases from plant leaf pictures.
* 💬 *Chatbot Mode* — Enter symptoms in your language.(Hindi, English, Bengali, Telugu)
* 👩‍💼 *Admin Mode* — Add/edit disease records via the dashboard.
* 🔑 *Login Required* — Farmers & admins have separate access levels.

---

## 🤝 Contributing

We ❤ contributions!

* Fork the repo 🌴
* Create a new feature branch
* Submit *Pull Requests* for improvements
* Open *Issues* for bugs or new ideas (languages, accuracy, optimizations)

---

## 📜 License

This project is licensed under the *MIT License*.
See the [LICENSE](LICENSE) file for details.

---

##  Acknowledgments

* 🌾 *PlantVillage Dataset* contributors on Kaggle
* 👨‍🏫 Mentor: *Eldhose Mathew* (Infosys Springboard 6.0)
* ⚙ Built with Flask, TensorFlow & the xAI community
* 💼 Connect with me on [LinkedIn](https://linkedin.com/in/anika0520)

---

### 👩‍💻 Developed with ❤ by [Anika](https://github.com/anika0520)

```
```
