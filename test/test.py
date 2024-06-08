import requests
from PIL import Image

# https://your-heroku-app-name.herokuapp.com/predict
# http://localhost:5000/predict
url = 'https://c8.alamy.com/comp/2ME3G5A/a-plate-of-pongal-and-vada-with-chutney-and-sambar-in-disposable-environment-friendly-plate-2ME3G5A.jpg'
im = Image.open(requests.get(url, stream=True).raw)
im.save('testimage.jpg')
resp = requests.post("https://foodcourt-classification.onrender.com/predict",
                     files={'file': open('testimage.jpg', 'rb')})

print(resp.text)
