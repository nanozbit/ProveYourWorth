#!/usr/bin/env python
# _*_ coding: utf-8 -*


import requests
import json

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw

session = requests.Session()

def load_JSON():
    f = open('settings.json',)
    data = json.load(f)
    return data


def start_session():
    session.get(DATA_CONFIG['home_page_uri'])
    print('Hash:',session.cookies.get("PHPSESSID"), sep=" ")


def get_hash() ->str:
    request = session.get(DATA_CONFIG['home_page_uri'])
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup.find("input", {"name":"statefulhash"})['value']


def load_register_page():
    print("Loading information \"Activate page\" ......")
    hash = get_hash()
    request = session.get(DATA_CONFIG['activate_uri']+f'={hash}')
    print("Webside:", request.url, sep=" ")
    print("Headers:", request.headers,sep="\n")    
    print("Hash:", get_hash(), sep="")


def get_register_image() -> bytes:
    request = session.get(DATA_CONFIG["payload_uri"], stream=True)
    return request.raw


def sing_image(image: bytes) -> None:
   image = Image.open(image)
   draw = ImageDraw.Draw(image)
   draw.text((40,40), f"{DATA_CONFIG['data']['name']}. \nHash:{get_hash()} \n{DATA_CONFIG['data']['email']} \nJunior Backend Developer", fill=(227, 28, 25))   
   image.save("image.jpg", "JPEG")


def upload_information_register(payload):
    payload = session.get(payload)
    uri = f"{payload.headers['X-POST-BACK-TO']}"

    Files = {
            "code": open("code.py","rb"),
            "resume": open("CV_EN.pdf", "rb"),
            "image": open("image.jpg", "rb")
            }
    data = DATA_CONFIG["data"]
    request = session.post(uri, data=data, files=Files)
    print(request.status_code)
    

if __name__ == "__main__":
    print("Load Payload")
    DATA_CONFIG = load_JSON()
    print("Starting  ProveYourWorth session")
    start_session()
    print("Load Register page")
    load_register_page()
    print("Downloading Image")
    sing_image(get_register_image())
    print("Upload Information User")    
    upload_information_register(DATA_CONFIG["payload_uri"])
    print("Finished payload")

