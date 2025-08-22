# Android Frontend

**Kivy-based Android application** designed to capture food images, interact with device hardware, and present results in a **clear, interactive, and user-friendly interface**.  
It acts as the bridge between the **ML backend** and the **end-user** for
- smooth camera access
- storage handling 
- API interactions
- intuitive visualization.  

---

## User Interface & Flow
- Built with **Kivy** and **ScreenManager** for multi-screen navigation.  
- UI screens include:
  - **Home Screen** → Entry point, navigation.  
  - **Camera Capture Screen** → Real-time preview & capture.  
  - **Results Screen** → Displays predictions and confidence levels.  
  - **Nutrition Screen** → Visualizes calories, macros (carbs, proteins, fats) via pie charts.  
  - **Exercise Screen** → Displays calorie burn estimations through bar graphs.  
- **Embedded Charts**:  
  - Implemented using **Matplotlib** with `FigureCanvasKivyAgg`.  
  - Customized colors, rounded charts, and responsive layouts for readability.  
- **Error Handling Screens**: User-friendly messages for:
  - Server downtime  
  - Internet errors  
  - Application errors  

---

## Android Hardware Integration
The app integrates deeply with Android hardware using `pyjnius` and helper modules.  

### 📷 Camera Access (CameraX via `camerax_provider`)
- Uses **CameraX API** through [camera4kivy](https://github.com/Android-for-Python/camera4kivy).  
- Provides:
  - Real-time camera preview inside Kivy widgets.  
  - Captures images and forwards them for ML predictions.  
  - Handles switching between device cameras.  

---

### Storage Management (`SharedStorage`)
- Interfaces with **Android MediaStore** to save/retrieve files.  
- Supports:
  - **Scoped Storage (Android ≥ 10)** and **Legacy Storage (Android < 10)**.  
  - Copying captured/private files into public storage.  
  - Importing shared files into cache for ML processing.  
  - Safe file deletion/overwriting.  

---

### Runtime Permissions (`AndroidPermissions`)
- Dynamically requests and manages runtime permissions:
  - `CAMERA` → Required for scanning meals.  
  - `RECORD_AUDIO` → Reserved for extended features.  
  - `WRITE_EXTERNAL_STORAGE` / `MANAGE_EXTERNAL_STORAGE` → For saving results & caching.  
- Provides custom dialogs when users deny permissions, ensuring the app fails gracefully.  

---

### File Chooser (`Chooser`)
- Implements **Android’s native file picker** using `Intent.ACTION_GET_CONTENT`.  
- Features:
  - Single or multiple file selection.  
  - Callback integration to retrieve file paths in Kivy.  
  - Fix for Kivy’s **black screen issue** when returning from external intents.  

---

## Visual Features
From the project report, the frontend includes:  

- **Dish Detection Screen**  
  - Displays the top prediction with % confidence.  
  - Shows top-5 predictions with confidence values.  

- **Nutrition Info Screen**  
  - Pie chart breakdown of **carbohydrates, proteins, fats**.  
  - Serving size & total calories clearly displayed.  

- **Exercise Screen**  
  - Text input for custom exercise queries.  
  - Fetches calorie-burn estimates via Nutritionix API.  
  - Animated bar charts for prediction confidence.  

---

## Frontend Workflow
1. **Permissions** → `AndroidPermissions` ensures camera & storage are accessible.  
2. **Image Capture** → `camerax_provider` launches camera preview; image captured.  
3. **Storage Handling** → `SharedStorage` saves image to cache/public storage.  
4. **Alternative Input** → `Chooser` allows gallery image selection.  
5. **Prediction Results** → ML backend results rendered in charts & text.  
6. **Nutrition & Exercise Data** → Retrieved via API and visualized.  

---

## Future Enhancements (Frontend-Specific)
- Improved **UI/UX animations** for smoother transitions.  
- Add **voice-based input** for exercise queries (leveraging `RECORD_AUDIO`).  
- Dark mode & theme customization.  

---
