import requests
from random import randint
from pprint import pprint
from dotenv import load_dotenv
from os import getenv
from colorist import red, blue
from rest import rest

load_dotenv()

BEARER = getenv("BEARER") 

questions = [
    "What do you wear on your head when riding a bike?",
    "Which is the smallest country in the world by land area?",
    "What is the chemical symbol for gold?",
    "Who was the first President of the United States?",
    "Which planet has the most moons in our solar system?",
    "What is the hardest natural substance on Earth?",
    "Which ocean is the largest by surface area?",
    "Who wrote the play Romeo and Juliet?",
    "What is the national currency of the United Kingdom?",
    "Which element is necessary for breathing and survival?",
    "What is the tallest mountain in the world?",
    "Which is the largest desert in the world?",
    "Who painted the famous artwork Mona Lisa?",
    "What is the capital of Australia?",
    "Which gas is most abundant in Earth's atmosphere?",
    "Who discovered penicillin?",
    "Which continent has the most countries?",
    "What is the national flower of India?",
    "How many bones are there in the adult human body?",
    "Which bird is known for its ability to mimic human speech?",
    "What is the currency of Japan?",
    "Which is the longest wall in the world?",
    "What is the main ingredient in traditional Japanese miso soup?",
    "Which is the only planet that rotates on its side?",
    "What is the name of the fairy tale character who leaves a glass slipper behind at a royal ball?",
    "Who invented the light bulb?",
    "Which country is famous for the Great Pyramids of Giza?",
    "What is the chemical formula of water?",
    "What is the fastest land animal in the world?",
    "Who is known as the 'Father of Computers'?",
    "Which two colors are on the flag of Canada?",
    "Which planet is the hottest in the solar system?",
    "Who wrote the famous book The Origin of Species?",
    "What is the main language spoken in Brazil?",
    "Which country is known as the Land of the Rising Sun?",
    "What is the longest railway in the world?",
    "Which element is represented by the symbol 'O' on the periodic table?",
    "Which organ in the human body produces insulin?",
    "What is the deepest ocean in the world?",
    "Who was the first woman to win a Nobel Prize?",
    "Which sport is played at Wimbledon?",
    "Why do leaves change color in autumn?",
    "What is the greenhouse effect and why is it important?",
    "How do airplanes stay in the air despite their weight?",
    "Why do we have different time zones around the world?",
    "What causes tides in the ocean?",
    "How does a rainbow form in the sky?",
    "What is the purpose of the United Nations?",
    "How does a compass work to show direction?"
]

url = "https://api.hyperbolic.xyz/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": BEARER
}

models = {
    "coder": {
        "model": "Qwen/QwQ-32B",
        "max_tokens": 1024,
        "temperature": 0.6,
        "top_p": 0.95
    },
    "llama":{
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "max_tokens": 512,
        "temperature": 0.1,
        "top_p": 0.9
    }
}

def random_question():
    ques = questions[randint(0,len(questions)-1)]
    print(f"Question: {ques}\n")
    return ques

def get_data(arg):
    data = {
        "messages": [
            {
                "role": "user",
                "content": random_question()
            }
        ]
    }
    return {**data, **(models["coder"])} if arg == 1 else {**data, **(models["llama"])}

choice = int(input("Which model do you want to run? \n1. Coder \n2. llama\n\n..."))

if choice != 1 and choice != 2:
    print("Wrong input.....exiting program now!")
    exit(1)

while True:
    response = requests.post(url, headers=headers, json=get_data(choice))
    if response.status_code >= 400:
        red(f"Error: {response.status_code}. Try checking if you have enough credits!\n")
    else:
        blue(f"Answer: {response.json()["choices"][0]["message"]["content"]}\n\n")
    rest()