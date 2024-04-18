# 30.102ESP32-IDF

## Project Goal
To simplify the necessary steps required to get into urban farming using AI LLM models such as ChatGPT for AIOT, and in doing so, creating a larger community of urban farmers for sustainability.

## Components
### Direct-to-plant System
This system uses a sensor and sends the packet of information via MQTT to AWS IoT Core using TLS.

### Backend
This backend processes the information and routes the message to our DynamoDB Database.

### Plant Surveillance
This system utilises ESPCAM, sending the data to our frontend.

### Webapp
The webapp has a landing page showcasing live data, as well as the images and a model loaded to tell plant health.

## Requirements
The ESP AWS IOT SDK is required by our example, and you can check it out here at https://github.com/espressif/esp-aws-iot, and install the SDK by cloning it into this main folder as well.