# 🍽️ Food Court Meal Classification with ResNet

This project trains a **ResNet-18** model using **PyTorch** to classify Indian food items (e.g., *aloo paratha, idli, vada*). It includes data preparation, training, evaluation, saving the trained model, and performing inference on unseen images.

---

## Project Structure

    .
    ├── dataset/
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

## Requirements

Install the required Python packages:

    pip install torch torchvision matplotlib pillow

---

## Dataset Preparation

1. Place your dataset inside the `dataset/` folder with subdirectories for each class:

    dataset/train/<class_name>/
    dataset/val/<class_name>/

2. The notebook includes helper code to:
   - Remove Jupyter `.ipynb_checkpoints/` directories.
   - Move a subset of images from `train/` to `val/` for validation (example script included in the notebook).

---

## Training the Model

- **Model:** ResNet-18 (pretrained on ImageNet)  
- **Transfer learning:** Only the final fully-connected layer is trained (other layers frozen).  
- **Optimizer:** SGD (lr=0.001, momentum=0.9)  
- **Loss:** CrossEntropyLoss  
- **Epochs:** 10 (adjustable)

Run the notebook/script:

    python training_notebook.py

During training you will see printed loss and accuracy for both the `train` and `val` phases.

---

## Saving the Model

After training, the model weights are saved as:

    foodCourtMealClassification.pth

---

## Inference on Unseen Images

To classify a new image:

1. Load the trained model.
2. Apply the same preprocessing transforms used during training.
3. Run inference and interpret the outputs.

**Example inference code (conceptual):**

    from PIL import Image
    import requests
    import torch
    from torchvision import transforms
    import torch.nn as nn

    # Load image
    url = "https://example.com/food.jpg"
    im = Image.open(requests.get(url, stream=True).raw)

    # Preprocess
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
    input_tensor = preprocess(im).unsqueeze(0)

    # Predict
    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
        probs = nn.functional.softmax(output, dim=1)
        _, pred = torch.max(probs, 1)

    predicted_class = class_names[pred.item()]
    print(f"Predicted class: {predicted_class}")

---

## Visualization

Display the image with the predicted label (example):

    import matplotlib.pyplot as plt
    plt.imshow(im)
    plt.title(f"Predicted: {predicted_class}")
    plt.axis("off")
    plt.show()

---

## Classes

Expected classes in the dataset (example):

- `aloo paratha`
- `chhole bhature`
- `idli`
- `kesari bath`
- `poori sagu`
- `set dosa`
- `vada`

Make sure these match the folder names in `dataset/train/` and `dataset/val/`.

---

## Results

- Trains a transfer-learning ResNet-18 model for food classification.
- Outputs training/validation loss and accuracy each epoch.
- Produces a saved model file (`foodCourtMealClassification.pth`) for later inference.
- Inference code returns top predictions and visualizes the result.
