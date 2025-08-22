# 🍽️ Cafeteria Meal Classification with ResNet

This project trains a **ResNet-18** model using **PyTorch** to classify Indian food items (e.g., *aloo paratha, idli, vada*). It includes data preparation, training, evaluation, saving the trained model, and performing inference on unseen images.

---

## Project Structure

    .
    ├── Custom Annotated Dataset/
    │   ├── train/
    │   │   ├── aloo paratha/
    │   │   ├── chhole bhature/
    │   │   ├── idli/
    │   │   └── ...
    │   └── val/
    │       ├── aloo paratha/
    │       ├── chhole bhature/
    │       ├── idli/
    │       └── ...
    ├── foodCourtMealClassification.pth   # Saved model weights
    ├── training_notebook.py / .ipynb     # Training & inference script
    └── README.md

---


## Classes

Expected classes in the dataset:

- `aloo paratha`
- `chhole bhature`
- `idli`
- `kesari bath`
- `poori sagu`
- `set dosa`
- `vada`

Make sure these match the folder names in `dataset/train/` and `dataset/val/`.
Dataset images provided in Custom Annotated Dataset folder.

---

## Model Training

### Architecture
- **Base Model**: ResNet-18 (pretrained on ImageNet).
- **Transfer Learning Strategy**:
  - All layers frozen **except the final fully connected (fc) layer**.
  - Final layer modified to output **7 food classes**:
    - `['aloo paratha', 'chhole bhature', 'idli', 'kesari bath', 'poori sagu', 'set dosa', 'vada']`.

### Data Preparation
- **Training Transforms**:
  - RandomResizedCrop(224)
  - RandomHorizontalFlip
  - ToTensor
  - Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- **Validation Transforms**:
  - Resize(256)
  - CenterCrop(224)
  - ToTensor
  - Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- **Batch Size**: 4
- **DataLoader Workers**: 4
- **Dataset Split**: ~20 images per class moved to validation set.

### Training Setup
- **Loss Function**: CrossEntropyLoss
- **Optimizer**: SGD (lr=0.001, momentum=0.9)
- **Device**: CPU (with CUDA option available)
- **Epochs**: 10
- **Metrics**: Loss & Accuracy for both training and validation phases.

### Training Loop
- Iterates over both `train` and `val` phases per epoch.
- Performs forward pass, loss computation, and backward propagation (in train phase).
- Tracks running loss and correct predictions.
- Prints epoch-level loss and accuracy.

### Model Persistence
- Final trained weights saved to:
`foodCourtMealClassification.pth`

### Inference
- Reloads trained ResNet model.
- Applies `softmax` for probability distribution.
- Retrieves **Top-5 predicted classes** with confidence scores.
- Outputs final predicted class with label mapping.

---

## Results

- Trains a transfer-learning ResNet-18 model for food classification.
- Outputs training/validation loss and accuracy each epoch.
- Produces a saved model file (`foodCourtMealClassification.pth`) for later inference.
- Inference code returns top predictions and visualizes the result.
