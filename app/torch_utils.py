import torch
from torchvision import models, transforms
import torch.nn as nn
from torchvision import transforms, models

# load model
# Load the saved model
model = models.resnet18(pretrained=True)
# Adjust to match the original model's output units
model.fc = nn.Linear(model.fc.in_features, 1000)
model.load_state_dict(torch.load('app/foodCourtMealClassification.pth'))
model.eval()

# Create a new model with the correct final layer
new_model = models.resnet18(pretrained=True)
# Adjust to match the desired output units
new_model.fc = nn.Linear(new_model.fc.in_features, 2)

# Copy the weights and biases from the loaded model to the new model
# Copy only the first 2 output units
new_model.fc.weight.data = model.fc.weight.data[0:2]
new_model.fc.bias.data = model.fc.bias.data[0:2]


# image -> tensor


def transform_image(image_bytes):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    input_tensor = preprocess(image_bytes)
    input_batch = input_tensor.unsqueeze(0)
    return input_batch


# predict


def get_prediction(image_tensor):

    # Perform inference
    with torch.no_grad():
        output = model(image_tensor)

    # Get the predicted class
    _, predicted_class = output.max(1)

    class_names = ['set dosa', 'vada']
    predicted_class_name = class_names[predicted_class.item()]
    return predicted_class_name
    # # Map the predicted class to the class name
    # # Make sure these class names match your training data
    # class_names = ['aloo paratha', 'vada', 'idli', 'rice bath',
    #                'kesari bath', 'poori sagu', 'chhole bhature', 'set dosa']
    # predicted_class_name = class_names[predicted_class.item()]

    # print(f'The predicted class is: {predicted_class_name}')
