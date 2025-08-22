# 🍴 Food-Court Meal Classifier App  

An **Android application** powered by a **PyTorch-based image classification model** hosted on Heroku.  
The app detects Indian cafeteria meals from photos, retrieves **nutritional information** using the **Nutritionix API**, and even estimates **calorie burn from exercises**.  

---

## Introduction
In today’s fast-paced world, making informed food choices is crucial for maintaining a healthy lifestyle.  
This project bridges the gap between **cafeteria dining** and **nutritional awareness** by enabling users to:  

- 📷 Detect meals using a **PyTorch image classification model**  
- 🥗 Retrieve calorie and nutrient information via the **Nutritionix API**  
- 🏃 Estimate calorie burn from exercises  
- 📱 Access results through an **Android app**  

Whether you’re a student, fitness enthusiast, or simply curious about your meal’s impact, this app empowers you to make smarter lifestyle choices.  

---

## Problem Definition
The project addresses the following challenges:  

- **Dish Detection** → Identify cafeteria meals using the phone camera.  
- **Hosting the ML Model** → Deployed on Heroku, predictions returned via API.  
- **Nutritional Information Retrieval** → Integrated with Nutritionix API to fetch calorie and macro data.  
- **Exercise Calorie Burn** → Calculate calories burned by activities to promote balanced choices.  
- **User-Friendly Interface** → Android frontend built with Kivy.  

---

## Overview
The solution consists of three major components:  

1. **ML Backend (PyTorch Model)**  
   - Trained on Indian meal images (Aloo Paratha, Set Dosa, Chhole Bhature, Idli, Vada, Poori Sagu, Kesari Bhath).  
   - Hosted on **Heroku** to provide predictions via REST API.  

2. **Nutrition API Integration**  
   - **Nutritionix API** used to retrieve calories and macros for detected meals.  
   - Also used to estimate **exercise-related calorie burn**.  

3. **Android Frontend (Kivy App)**  
   - Captures images, sends them to backend, and displays results.  
   - Provides pie charts (carbs, protein, fats) and bar charts (prediction confidence).  
   - Handles Android hardware integration: Camera, Storage, Permissions, File Chooser.  

---

## 🍛 Supported Meals
The model currently recognizes the following Indian dishes:  
- Aloo Paratha  
- Set Dosa  
- Chhole Bhature  
- Idli  
- Vada  
- Poori Sagu  
- Kesari Bhath  

The dataset can be easily extended to include more meals.  

---

## 🧪 Challenges and Research
During the development of this project, several challenges were encountered, leading to valuable research and learning:  

### 🔹 Dataset Creation
- **Challenge**: No publicly available dataset for Indian cafeteria meals.  
- **Solution**: Built a custom dataset using `bing-image-downloader` - a custom python script to scrape images. Each food class had ~100 images. Filtered out the remo
- **Learning**: Dataset quality and diversity are critical for ML performance. Future improvements could include crowdsourced images or curated datasets.  

### 🔹 ML Model Hosting
- **Challenge**: Deploying PyTorch models with limited resources.  
- **Solution**: Used **Heroku** with free credits from GitHub Student Developer Pack.  
- **Learning**: Model optimization and efficient request handling were essential to reduce response times.  

### 🔹 API Integration
- **Challenge**: Using Nutritionix API with authentication (App ID, API key) and handling request limits.  
- **Solution**: Integrated robust error handling for API calls (timeouts, invalid input, server-side errors).  
- **Learning**: Secure key management and API rate-limit handling are crucial for production apps.  

### 🔹 Asynchronous UI
- **Challenge**: Fetching API and ML results caused UI freezes in Kivy.  
- **Solution**: Implemented **multithreading** and Kivy’s `@mainthread` decorators to keep UI responsive.  
- **Learning**: Concurrency in Python-Kivy apps requires careful thread-safe updates to UI components.  

### 🔹 Android Hardware Access
- **Challenge**: Kivy does not natively support advanced Android features like CameraX, scoped storage, and runtime permissions.  
- **Solution**: Integrated custom Python-Java bridges using `pyjnius`:
  - `camerax_provider` for CameraX API  
  - `SharedStorage` for MediaStore integration  
  - `AndroidPermissions` for runtime permission handling  
  - `Chooser` for gallery image selection  
- **Learning**: Deep understanding of Android APIs was needed to bridge Python with native functionality.  

---

## 🛠️ Tech Stack
- **Frontend**: Python (Kivy, Matplotlib)  
- **Backend**: PyTorch, Flask (Heroku)  
- **APIs**: Nutritionix API  
- **Dataset**: Collected via `bing-image-downloader`  

---

## 🖼️ App Screenshots

| Loading Screen | Camera Screen | Prediction Screen |
|----------------|---------------|-------------------|
| <img width="191" height="398" alt="LoadingScreen" src="https://github.com/user-attachments/assets/336df945-955c-4b05-b32f-59c711164ed8" />
 |<img width="199" height="398" alt="cameraScreen" src="https://github.com/user-attachments/assets/755a9245-5155-4174-ba1a-44966bc79fb4" />
  | <img width="191" height="398" alt="PredictionScreen" src="https://github.com/user-attachments/assets/71cb0fa6-1f54-45a2-9c99-f06faee25b74" />
  |

| Nutrition Info Screen | Internet Error Screen | Server Error Screen |
|------------------------|-----------------------|---------------------|
| <img width="200" height="398" alt="nutritionalInfoScreen" src="https://github.com/user-attachments/assets/78b7fb5e-3e27-4d5e-bf4c-b88127e8ecfc" />
 | <img width="195" height="398" alt="internetErrorScreen" src="https://github.com/user-attachments/assets/c421c071-ce48-4c44-b501-02efca721fe7" />
 |  <img width="192" height="398" alt="serverErrorScreen" src="https://github.com/user-attachments/assets/2cb5110c-da51-4550-a28d-8fac1fc15f93" />
|

---

## Future Enhancements
- Dish recommendations (suggest healthier alternatives).  
- Personalization (diet & fitness goals).  
- Social sharing of meals & workout results.  
- Support for restaurant menus, home-cooked meals, food delivery apps.  

---

