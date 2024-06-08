import imghdr
from pathlib import Path
from better_bing_image_downloader import downloader

foodList = ['aloo paratha', 'vada', 'idli', 'rice bath',
            'kesari bath', 'poori sagu', 'chhole bhature', 'set dosa']
for food in foodList:
    downloader(food, limit=100, output_dir='dataset', adult_filter_off=True,
               force_replace=False, timeout=60, filter="", verbose=False, badsites=[], name='Image')


# data_dir = "./dataset/aloo paratha/"
# # add there all your images file extensions
# image_extensions = [".png", ".jpg", ".jpeg", ".JPG"]

# img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png", "jpg"]
# for filepath in Path(data_dir).rglob("*"):
#     if filepath.suffix.lower() in image_extensions:
#         img_type = imghdr.what(filepath)
#         if img_type is None:
#             print(f"{filepath} is not an image")
#         elif img_type not in img_type_accepted_by_tf:
#             print(f"{filepath} is a {img_type}, not accepted by TensorFlow")
