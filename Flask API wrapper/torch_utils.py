import torch
from torchvision import models, transforms
import torch.nn as nn
from torchvision import transforms, models


# Load the saved model
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
# Adjust to match the original model's output units
model.fc = nn.Linear(model.fc.in_features, 1000)
model.load_state_dict(torch.load('app/foodCourtMealClassification.pth'))
model.eval()

# Create a new model with the correct final layer
new_model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
# Adjust to match the desired output units
new_model.fc = nn.Linear(new_model.fc.in_features, 7)

# Copy the weights and biases from the loaded model to the new model
# Copy only the first 2 output units
new_model.fc.weight.data = model.fc.weight.data[0:2]
new_model.fc.bias.data = model.fc.bias.data[0:2]


# image -> tensor
def transform_image(image_bytes):
    # Load and preprocess the unseen image
    # image_path = 'test.jpg'  # Replace with the path to your image
    # image = Image.open(image_path)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    input_tensor = preprocess(image_bytes)
    input_batch = input_tensor.unsqueeze(0)  # Add a batch dimension
    return input_batch


# predict
def get_prediction(image_tensor):
    class_labels = ['aloo paratha', 'chhole bhature', 'idli', 'kesari bath', 'poori sagu',
                    'set dosa', 'vada']  # Make sure these class names match your training data
    # Perform inference
    with torch.no_grad():
        output = model(image_tensor)
        probs = nn.functional.softmax(output, dim=1)
        _, indices = torch.topk(probs, k=5)
        # Assuming 'class_labels' is a list of class labels
        top_classes = [class_labels[i] for i in indices[0]]
        top_confidences = [probs[0, i].item() for i in indices[0]]

    zippedPairs = dict(zip(top_classes, top_confidences))

    # Get the predicted class
    _, predicted_class = output.max(1)

    # Map the predicted class to the class name
    predicted_class_name = class_labels[predicted_class.item()]

    print(f'The predicted class is: {predicted_class_name}')

    return {"top-5": zippedPairs, "top-prediction": predicted_class_name}
