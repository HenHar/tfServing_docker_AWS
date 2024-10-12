import requests
import json
import numpy as np
import tensorflow as tf
import time
import cv2
import base64


def main():
    url_aws = "http://3.120.130.54:8501/v1/models/eff_imagenet:predict"
    url_local = "http://localhost:8501/v1/models/eff_imagenet:predict"

    image = cv2.imread("dog.jpeg")
    image = cv2.resize(image, (224,244))
    #base64_serving()
    inference_array(image, url_aws)

    
def inference_array(image, url):
    start_time = time.time()
    data = json.dumps({"signature_name" : "serving_default", "instances": image.tolist()})
    headers = {"content-type": "application/json"}
    response = requests.post(url, data = data, headers= headers)
    prediction = json.loads(response.text)["predictions"]
    result = tf.keras.applications.imagenet_utils.decode_predictions(np.array(prediction))
    print(result)
    print("Time taken: ", time.time() - start_time)


def base64_serving():
    path_image = "cat.jpeg"
    image_open = open(path_image, 'rb')
    read_image_bytes = image_open.read()

    read_image = cv2.imread("cat.jpeg")
    #read_image = cv2.cvtColor(read_image, cv2.COLOR_BGR2RGB)
    read_image = cv2.imencode('.jpeg', read_image)[1]

    encoded_bytes = base64.urlsafe_b64encode(read_image)
    encoded_string = encoded_bytes.decode("utf-8")

    with open("cat_cv.txt", "w") as text_file:
        text_file.write(encoded_string)

    image_tensor = tf.io.decode_base64(encoded_string)
    image_tensor = tf.image.decode_jpeg(image_tensor, channels=3)


    url = "http://3.145.199.118:8501/v1/models/eff_imagenet:predict"

    png_base64 = base64.urlsafe_b64encode(read_image).decode("UTF-8")

    data = json.dumps({
        "signature_name": "serving_bytes",
        "instances": [
            png_base64

        ]
    })

    headers = {"content-type": "application/json"}
    response = requests.post(url, data=data, headers=headers)
    print(json.loads(response.text))
    prediction = json.loads(response.text)["predictions"]
    result = tf.keras.applications.imagenet_utils.decode_predictions(np.array(prediction))
    print(result)

if __name__ == '__main__':
    main()
    
