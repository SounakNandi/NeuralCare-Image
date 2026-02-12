# 🚀 NeuralCare-Image

AI-powered image-based skin disease detection using Convolutional Neural Networks (CNNs).

> **⚠️ DISCLAIMER: This application is intended for research and educational purposes only. It is not a substitute for professional medical diagnosis. Please consult a dermatologist for an accurate assessment.**

## 📜 Research Paper

This project is based on my research paper, [Skin Disease Detection by Convolutional Neural Networks- An Approach](https://drive.google.com/file/d/1d4YEskGISrVcOPKPxKD1GfMgcSaGq80s/view?usp=sharing), published in [International Journal of Scientific Research and Engineering Development (IJSRED)](www.ijsred.com), Volume 8, Issue 1, Jan-Feb 2025.

## 🎥 Demo

Check out the demo to see the app in action (version 2):

<video src="https://github.com/user-attachments/assets/59b3fca6-30ac-4699-afac-3c140482fe87" width=auto height="250" controls>
</video>

<!-- <video src="https://github.com/user-attachments/assets/5b174c4a-7ee5-4871-94b3-5b7626f10d20" width=auto height="250" controls>
</video> -->

## 📌 Overview

Skin diseases are a significant global health concern, affecting millions of people. Many cases remain undiagnosed due to a lack of dermatologists, high costs, and time-consuming manual diagnoses.

This project presents an automated skin disease detection system that uses CNNs to analyze skin images and classify lesions as **Benign** or **Malignant**. The system was trained using publicly available dermatology datasets and employs image processing techniques for accurate classification.

## ✨ Key Features

- **Accurate Detection**: Classifies skin lesions as Malignant (Cancerous) or Benign (Non-Cancerous).
- **Confidence Scoring**: Provides a probability score for the prediction.

## 🛠️ Tech Stack

- **Deep Learning**: TensorFlow, Keras
- **Language**: Python 3.10+
- **GUI Frameworks**: Tkinter, CustomTkinter
- **Image Processing**: OpenCV, Pillow (PIL)
- **Data Handling**: NumPy

## 📊 Data Collection

The model is trained on the **ISIC 2019 Dataset**, a standard benchmark for skin lesion analysis.

- **Source**: [Kaggle - Skin Cancer: Malignant vs. Benign](https://www.kaggle.com/datasets/fanconic/skin-cancer-malignant-vs-benign)
- **Size**: 3,200+ labeled images.
- **Format**: High-quality RGB images.
- **Balance**: The dataset is balanced between benign and malignant classes to ensure unbiased training.

## 🔧 Installation & Usage

1️⃣ Clone the Repository

```
git clone https://github.com/SounakNandi/neuralcare-image.git
cd neuralcare-image
```

2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

3️⃣ Run the Application

**Version 1: Classic UI**

```
python ui/app1.py
```

**Version 2: Modern UI**

```
python ui/app2.py
```

## Credits

Made with ❤️ by some cool guy [SOUNAK NANDI](https://github.com/SounakNandi)
