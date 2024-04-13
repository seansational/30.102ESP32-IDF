import cv2
import streamlit as st
import numpy as np
from PIL import Image
import urllib.request
import requests
from io import BytesIO
from time import sleep

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
def brighten_image(image, amount):
    img_bright = cv2.convertScaleAbs(image, beta=amount)
    return img_bright


def blur_image(image, amount):
    blur_img = cv2.GaussianBlur(image, (11, 11), amount)
    return blur_img


def enhance_details(img):
    hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return hdr

def classify_face(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img







def main_loop():
    st.title("OpenCV Demo App")
    st.subheader("This app allows you to play with Image filters!")
    st.text("We use OpenCV and Streamlit for this demo")
    blur_rate = st.sidebar.slider("Blurring", min_value=0.5, max_value=3.5)
    brightness_amount = st.sidebar.slider("Brightness", min_value=-50, max_value=50, value=0)
    apply_enhancement_filter = st.sidebar.checkbox('Enhance Details')
    print("Hi")
    image_file = requests.get("http://192.168.189.20/frame")
    print("got image")
    original_image = Image.open(BytesIO(image_file.content))

    # original_image = Image.open(image_file.content)
    print("saving")
    original_image.save("img.jpg")
    original_image = np.array(original_image)

    st.text("Plant Stream")
    viewer = st.image([original_image])
    # time.sleep(2)

    while True:

        
        if not image_file:
            return None
        # print(type(image_file))
        image_file = requests.get("http://192.168.189.20/frame")
        original_image = Image.open(BytesIO(image_file.content))
        original_image = np.array(original_image)

        processed_image = blur_image(original_image, blur_rate)
        processed_image = brighten_image(processed_image, brightness_amount)
        face_image = classify_face(original_image)
        if apply_enhancement_filter:
            processed_image = enhance_details(processed_image)
        viewer.image([original_image,processed_image,face_image])
        sleep(1)




if __name__ == '__main__':
    main_loop()
