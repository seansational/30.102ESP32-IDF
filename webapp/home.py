import cv2
import streamlit as st
import numpy as np
from PIL import Image
import urllib.request
import requests
from io import BytesIO
from time import sleep,time
from datetime import datetime
import plotly.express as px  # interactive charts
import plotly
import pandas as pd
from random import randrange
import boto3
from functools import reduce   # Only in Python 3, omit this in Python 2.x
from ultralyticsplus import YOLO, render_result

plotly.io.json.config.default_engine = 'orjson'

#Webapp setup in class
class Web_App:
    def __init__(self) -> None:
        #initalise class variables with placeholders and initalisation time for variables that call time()
        self.plant_val = 98
        self.image_save = time()
        self.stat_save = time()
        self.assess_cv = time()
        self.image_last = None
        self.img_path = "img.jpg"

        #initalise YOLO model for CV
        self.model = YOLO('foduucom/plant-leaf-detection-and-classification')
        # set model parameters
        self.model.overrides['conf'] = 0.25  # NMS confidence threshold
        self.model.overrides['iou'] = 0.45  # NMS IoU threshold
        self.model.overrides['agnostic_nms'] = False  # NMS class-agnostic
        self.model.overrides['max_det'] = 1000  # maximum number of detections per image
        self.model.model.names = {0: 'ginger | Health', 1: 'banana | Health', 2: 'tobacco | Health', 3: 'ornamaental | Health', 4: 'rose | Health', 5: 'soyabean | Health', 6: 'papaya | Health', 7: 'garlic | Health', 8: 'raspberry | Health', 9: 'mango | Health', 10: 'cotton | Health', 11: 'corn | Health', 12: 'pomgernate | Health', 13: 'strawberry | Health', 14: 'Blueberry | Health', 15: 'brinjal | Health', 16: 'potato | Health', 17: 'wheat | Health', 18: 'olive | Health', 19: 'rice | Health', 20: 'lemon | Health', 21: 'cabbage | Health', 22: 'gauava | Health', 23: 'chilli | Health', 24: 'capcicum | Health', 25: 'sunflower | Health', 26: 'cherry | Health', 27: 'cassava | Health', 28: 'apple | Health', 29: 'tea | Health', 30: 'sugarcane | Health', 31: 'groundnut | Health', 32: 'weed | Health', 33: 'peach | Health', 34: 'coffee | Health', 35: 'cauliflower | Health', 36: 'tomato | Health', 37: 'onion | Health', 38: 'gram | Health', 39: 'chiku | Health', 40: 'jamun | Health', 41: 'castor | Health', 42: 'pea | Health', 43: 'cucumber | Health', 44: 'grape | Health', 45: 'cardamom | Health'}
        
        #run page setup
        self.setup()

    #Function for classifying plant health (plant classification model used as a placeholder)
    def classify_plant(self,img):

        #runs cv model based on frequency set by user
        # if time() > self.assess_cv + self.cv_rate*60*60 or self.image_last == None :

        #Running cv model inference on image
        results = self.model.predict(img)
        boxes = results[0].boxes
        # print("BOX",boxes.conf)
        # object_predictions = []

        #if plant found update metrics on streamlit
        if boxes is not None and boxes.conf.shape[0] >0 :
            plant_conf = round(float(boxes.conf[0].item()) *100,1)
            self.plant_health_metric_new.metric(
            label="Plant Health ❤️",
            value=f"{plant_conf}% ",
            delta=plant_conf-self.plant_val ,

            )
            self.plant_val =  plant_conf

            # #saving image and plant health to database
            # if time() > self.stat_save + self.stat_freq*60*60:
            #     self.table.put_item(
            #             Item={
            #                     'image': img,
            #                     'time': time(),
            #                     'boundingbox': boxes,
            #                 }
            #             )

        #adding cv results and bounding box to images
        render = render_result(model=self.model, image=img, result=results[0])
        # self.image_last = render
        # else:
        #     return self.image_last
        return render

    #function to read database
    def read_database(self):
        #initalise dictionary for saving database entries
        pump_activation = {}
        humidity_levels = {}

        #setup database access
        ddb = boto3.resource('dynamodb')
        table = ddb.Table('esp32c6_data')
        
        #accessing table contents
        self.table = table
        response = table.scan(
            AttributesToGet=[
                'data',
            ],
            # Limit=2,
        )

        #reading table contents in to preinitalised variables
        for iter, result in enumerate(response['Items']):
            pump_activation[iter] = reduce(lambda rst, x: rst * 10 + x, result['data']['pump_activated'].as_tuple().digits)
            humidity_levels[iter] = reduce(lambda rst, x: rst * 10 + x, result['data']['humidity'].as_tuple().digits)
        
        #loading into dataframe for easy reading
        pump_pd = pd.DataFrame(list(pump_activation.items()), columns=['iteration', 'pump activated'])
        humidity_pd = pd.DataFrame(list(humidity_levels.items()), columns=['iteration', 'humidity'])
        pump_pd.sort_values(by='date', ascending=True,inplace=True)
        humidity_pd.sort_values(by='date', ascending=True,inplace=True)

        return float(humidity_pd["humidity"].iloc[-1]),float(pump_pd["iteration"].iloc[-1]),float(humidity_pd["humidity"].iloc[-1]- humidity_pd["humidity"].iloc[-2])



    #Function to setup Streamlit webapp home page layout
    def setup(self):
        #streamlit page config setup
        st.set_page_config(
        page_title="Plant Monitoring App",
        page_icon="☘️",
        layout="wide",
        )

        st.title("Plant Monitoring App ☘️")


        #setup of settings bar
        st.sidebar.title("Settings")
        self.save_img_freq = st.sidebar.slider("Saving Image Frequency (Timelapse)/hours", min_value=1, max_value=100,step=1,value=1)
        self.stat_freq = st.sidebar.slider("Saving Statistics Frequency/hours", min_value=0.1, max_value=10.0,step=0.1,value=1.0)
        self.cv_rate = st.sidebar.slider("Plant Health CV/hours", min_value=-0.1, max_value=5.0, value=1.0,step=0.1)
        self.water_thresh = st.sidebar.slider("Watering Threshold (Humidity)", min_value=1, max_value=100,step=1,value=1)

        self.stream_freq = st.sidebar.slider("Image Streaming Frequency/img per seconds", min_value=-0.1, max_value=5.0, value=1.0,step=0.1)
        self.run_cv = st.sidebar.checkbox('Run CV for Plant Health')
        
        #setup of metrics display
        self.kpi1, self.kpi2, self.kpi3 = st.columns(3)

        #reading metrics from database
        hum,lastwatered, hdelta = self.read_database()
        update_time = datetime.now().strftime("%H:%M:%S")



        # fill in those three columns with respective metrics or KPIs
        self.kpi1.metric(
            label="Soil Humidity 🌱",
            value=hum,
            delta= hdelta,
        )
        

        self.plant_health_metric_new = self.kpi2.metric(
            label="Plant Health ❤️",
            value=f"{98}% ",
            delta=0,
        )


        self.kpi3.metric(
            label="Last Watered 💧",
            value=f"{lastwatered} hours ago ",
        )
        
        self.last_updated = st.write(f"*Last Updated at {update_time}*")
        self.col1,self.col2 = st.columns(2)
        
        #Setup camera layout 
        st.write("### Plant Cam 📸")
        self.pic_col1,self.pic_col2 = st.columns(2)
        with self.pic_col1:
            st.text("Live Stream")
            self.view1 = st.image([],use_column_width=True)
        with self.pic_col2:
            st.text("With Plant Health CV")
            self.view2 = st.image([],use_column_width=True)

    def main_loop(self):

        while True:
            #read http get request from ESP - CAM
            image_file = requests.get("http://192.168.189.20/frame")
            original_image = Image.open(BytesIO(image_file.content))

            #saving image
            # if time() > self.image_save + self.save_img_freq*60*60:
            #     original_image.save(self.img_path)
                # self.image_save = time()

            #reformat image
            original_image = np.array(original_image)
            original_image = cv2.flip(original_image,0)

            #run cv model if option enabled and update image in streamlit
            if self.run_cv:
                face_image = self.classify_plant(original_image)
                self.view1.image(original_image)
                self.view2.image(face_image)
            else:
                self.view1.image(original_image)


            #set rate of update for image stream
            sleep(1/self.stream_freq)




if __name__ == '__main__':
    #initalise webapp and run
    webapp = Web_App()
    webapp.main_loop()
