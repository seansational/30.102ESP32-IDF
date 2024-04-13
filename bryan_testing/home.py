import cv2
import streamlit as st
import numpy as np
from PIL import Image
import urllib.request
import requests
from io import BytesIO
from time import sleep
import plotly.express as px  # interactive charts
import plotly
import pandas as pd
from random import randrange

from ultralyticsplus import YOLO, render_result

plotly.io.json.config.default_engine = 'orjson'
# face_classifier = cv2.dnn.readNet('yolov4-obj_best.weights', 'yolov4-obj.cfg')

# def brighten_image(image, amount):
#     img_bright = cv2.convertScaleAbs(image, beta=amount)
#     return img_bright


# def blur_image(image, amount):
#     blur_img = cv2.GaussianBlur(image, (11, 11), amount)
#     return blur_img


# def enhance_details(img):
#     hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
#     return hdr


class Web_App:
    def __init__(self) -> None:
        # self.face_classifier = cv2.CascadeClassifier(
        # cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        # )
        self.model = YOLO('foduucom/plant-leaf-detection-and-classification')
        # set model parameters
        self.model.overrides['conf'] = 0.25  # NMS confidence threshold
        self.model.overrides['iou'] = 0.45  # NMS IoU threshold
        self.model.overrides['agnostic_nms'] = False  # NMS class-agnostic
        self.model.overrides['max_det'] = 1000  # maximum number of detections per image
        self.model.model.names = {0: 'ginger | Health', 1: 'banana | Health', 2: 'tobacco | Health', 3: 'ornamaental | Health', 4: 'rose | Health', 5: 'soyabean | Health', 6: 'papaya | Health', 7: 'garlic | Health', 8: 'raspberry | Health', 9: 'mango | Health', 10: 'cotton | Health', 11: 'corn | Health', 12: 'pomgernate | Health', 13: 'strawberry | Health', 14: 'Blueberry | Health', 15: 'brinjal | Health', 16: 'potato | Health', 17: 'wheat | Health', 18: 'olive | Health', 19: 'rice | Health', 20: 'lemon | Health', 21: 'cabbage | Health', 22: 'gauava | Health', 23: 'chilli | Health', 24: 'capcicum | Health', 25: 'sunflower | Health', 26: 'cherry | Health', 27: 'cassava | Health', 28: 'apple | Health', 29: 'tea | Health', 30: 'sugarcane | Health', 31: 'groundnut | Health', 32: 'weed | Health', 33: 'peach | Health', 34: 'coffee | Health', 35: 'cauliflower | Health', 36: 'tomato | Health', 37: 'onion | Health', 38: 'gram | Health', 39: 'chiku | Health', 40: 'jamun | Health', 41: 'castor | Health', 42: 'pea | Health', 43: 'cucumber | Health', 44: 'grape | Health', 45: 'cardamom | Health'}
        self.setup()

    def classify_face(self,img):
        # gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # face = face_classifier.forward(
        #     img
        # )
        results = self.model.predict(img)
        boxes = results[0].boxes
        print("BOX",boxes.cls)
        # object_predictions = []
        # if boxes is not None:
        #     for xyxy, conf, cls in zip(boxes.xyxy, boxes.conf, boxes.cls):
        #         print(xyxy,conf,cls)

        render = render_result(model=self.model, image=img, result=results[0])
        


        # for (x, y, w, h) in face:
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)

        # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return render



    def setup(self):
        st.set_page_config(
        page_title="Plant Monitoring App",
        page_icon="🪴",
        layout="wide",
        )

        st.title("Plant Monitoring App")
        # st.subheader("This app allows you to play with Image filters!")
        # st.text("We use OpenCV and Streamlit for this demo")

        st.sidebar.title("Settings")
        self.save_img_freq = st.sidebar.slider("Saving Image Frequency (Timelapse)/hours", min_value=1, max_value=100,step=1,value=1)
        self.stream_freq = st.sidebar.slider("Image Streaming Frequency/img per seconds", min_value=-0.1, max_value=5.0, value=1.0,step=0.1)
        self.save_img_freq = st.sidebar.slider("Saving Statistics Frequency/hours", min_value=0.1, max_value=10.0,step=0.1,value=1.0)
        self.stream_freq = st.sidebar.slider("Plant Health CV", min_value=-0.1, max_value=5.0, value=1.0,step=0.1)
        self.run_cv = st.sidebar.checkbox('Run CV for Plant Health')
        
        # create three columns
        self.kpi1, self.kpi2, self.kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        self.kpi1.metric(
            label="Soil Humitity 🌱",
            value=0.3,
            delta=- 0.1,
        )
        
        self.kpi2.metric(
            label="Last Watered 💧",
            value=f"{98} hours ago ",
            delta=10
        )
        
        self.kpi3.metric(
            label="Plant Health ❤️",
            value=f"{98}% ",
            delta=0,
        )
        self.last_updated = st.write("*Last Updated 2 hours ago*")
        self.col1,self.col2 = st.columns(2)
        
        df = pd.DataFrame(dict(
            x = [i for i in range(0,50)],
            y = [randrange(60,100) for i in range(0,50)]
        ))


        with self.col1:
            st.markdown("### Soil Humitity Chart")
            fig = px.line(
                data_frame=df, y="y", x="x"
            )
            st.plotly_chart(fig,use_container_width=True)


        with self.col2:
            st.markdown("### Plant Health Chart")
            fig = px.line(
                data_frame=df, y="y", x="x"
            )
            st.plotly_chart(fig,use_container_width=True)
        st.write("### Plant Cam 📸")
        self.pic_col1,self.pic_col2 = st.columns(2)
        with self.pic_col1:
            st.text("Live Stream")
            self.view1 = st.image([],use_column_width=True)
        with self.pic_col2:
            st.text("With Plant Health CV")
            self.view2 = st.image([],use_column_width=True)




    # apply_enhancement_filter = st.sidebar.checkbox('Enhance Details')





    def main_loop(self):

        while True:
            # try:
            image_file = requests.get("http://192.168.0.20/frame")
            original_image = Image.open(BytesIO(image_file.content))
            # original_image = Image.open("img.jpg")

            original_image = np.array(original_image)
            # viewer.image(original_image)
            # viewer.caption("Live Stream")
            if self.run_cv:
                face_image = self.classify_face(original_image)
                self.view1.image(original_image)
                # self.view1.caption("Live Stream")
                self.view2.image(face_image)
                # self.view2.caption("With Plant Health CV")
            else:
                self.view1.image(original_image)
                # self.view1.caption("Live Stream")
            # except:
            #     print("connection timeout")

            sleep(1/self.stream_freq)




if __name__ == '__main__':
    webapp = Web_App()
    webapp.main_loop()
