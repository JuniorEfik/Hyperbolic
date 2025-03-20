import requests
from random import randint
import base64
from io import BytesIO

models = [
    "FLUX.1-dev",
    "SDXL1.0-base",
    "SD1.5",
    "SSD"
]

url = "https://api.hyperbolic.xyz/v1/image/generation"

head = {
    "Content-Type": "application/json"
}

images = [
    "A serene forest with a waterfall cascading into a crystal-clear lake, surrounded by vibrant autumn foliage.",
    "A futuristic city built on floating islands in the clouds, illuminated by neon lights.",
    "A desert landscape with a lone cactus under a starry night sky and the Milky Way clearly visible.",
    "A tropical beach at sunset with turquoise waters, palm trees, and colorful parrots flying overhead.",
    "A magical fairy tale land with a glowing castle surrounded by enchanted trees and sparkling fireflies.",
    "A cyberpunk cityscape at night, filled with holograms, neon signs, and flying cars.",
    "A dragon perched on top of a snowy mountain, breathing blue flames into the sky.",
    "An alien planet with three suns, purple vegetation, and floating rock formations.",
    "An oil painting of a thunderstorm over a bustling cityscape with dramatic lighting.",
    "A minimalist black-and-white sketch of a lone tree on a hill under a crescent moon.",
    "A 3D rendering of an Art Nouveau-inspired train station with intricate floral patterns.",
    "An impressionist painting of a river winding through a meadow with soft pastel tones.",
    "An ancient Roman marketplace bustling with people wearing traditional togas and sandals.",
    "A Japanese garden during cherry blossom season, complete with koi ponds and stone lanterns.",
    "An Egyptian pharaoh seated on a golden throne inside a grand pyramid chamber lit by torches.",
    "A medieval knight standing in front of a castle gate under stormy skies.",
    "An explosion of colors representing human emotions in an abstract art style.",
    "A surreal depiction of time as melting clocks floating in space among stars.",
    "An infinite staircase spiraling into the sky, surrounded by clouds and glowing light.",
    "A kaleidoscope of geometric shapes forming an optical illusion in vibrant hues.",
    "A majestic Bengal tiger prowling through a lush rainforest with sunlight filtering through the trees.",
    "A flock of birds flying over a calm river at sunrise, painted in watercolor style.",
    "A surreal image of two robotic dogs playing fetch in a futuristic park.",
    "An owl perched on a tree branch under moonlight, its feathers glowing faintly.",
    "A vintage red convertible driving along a coastal road at sunset, with waves crashing against cliffs.",
    "A cozy café on a rainy day, with steaming coffee cups on wooden tables and people reading books.",
    "A bustling farmers' market filled with colorful fruits, vegetables, and flowers under bright sunlight.",
    "A black-and-white photograph of an old man walking in the rain with an umbrella."
]

data = {
    "model_name": "SSD",
    "prompt": "",
    "steps": 30,
    "cfg_scale": 5,
    "enable_refiner": False,
    "height": 1024,
    "width": 1024,
    "backend": "auto"
}

def random_image():
    ques = images[randint(0,len(images)-1)]
    return ques

def base64_to_image(base64_string):
    try:
        img_data = base64.b64decode(base64_string)
        return BytesIO(img_data) 
    except Exception as e:
        print(f"Decoding Error: {e}")
        return None

def generate_image(model, token):
    headers = {**head, **{"Authorization": token}}
    prompt = random_image()
    response = requests.post(url, headers=headers, json={**data, **{
        "model_name":models[model], 
        "prompt": prompt
    }})
    return [prompt, base64_to_image(response.json()['images'][0]['image'])]