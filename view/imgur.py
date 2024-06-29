from imgurpython import ImgurClient
from datetime import datetime


def upload(client_data, name ):
    config = {
        'name': name,
    }

    image = client_data.upload_from_path('FCertificate.png', config=config, anon=False)
    return image


# if __name__ == "__main__":
#     client_id ='6cca211229bdb72'
#     client_secret = '71a4af51db0c990c99fb3950c8f6760967df12c1'
#     access_token = "711b91f3df509af23502dad9bc3386687c513c93"
#     refresh_token = "755d5b499edf523d0a9e1f57ea9a6629702280d8"
#     local_img_file = "good1.jpg"

#     client = ImgurClient(client_id, client_secret, access_token, refresh_token)
#     image = upload(client, local_img_file)
#     print(f"圖片網址: {image['link']}")