# Hyperbolic Chatbot By JuniorEfik

# About
- Allows you to autochat with Hyperbolic AI models (generated images aren't shown for now)
- Random generated questions
- Can't handle errors could your credit be used up. Best would be to recharge your credits and then restart the bot

# Gettting your bearer token (Hyperbolic API key)
- Go-to [Hyperbolic API key](https://app.hyperbolic.xyz/settings) 
- You'll be needing the obtained key..... Keep it safe and ready

# Setup
1 **Install packages**
``` bash 
    sudo apt update && sudo apt upgrade -y
    sudo apt install git screen python3 python3-pip python3-venv -y
```
2 **Clone Repo**
```
    git clone https://github.com/JuniorEfik/Hyperbolic.git
    cd Hyperbolic
```
3 **Input your hyperbolic API into the quotes then hit Ctrl+X then Y to save**
```
    nano .env
```
4 **Install Dependencies**
```
    python3 -m venv .venv
```
5 **Open a new screen and start the text bot (Paste each lines one-by-one)**
```
    screen -S hyperText
    source .venv/bin/activate
    pip3 install dotenv colored requests
    python3 hyper_text.py
```
Ctrl+A+D to minimize screen
6 **Open a new screen and start the image bot (Paste each lines one-by-one)**
```
    screen -S hyperImage
    source .venv/bin/activate
    python3 hyper_image.py
```
Ctrl+A+D to minimize screen

# Usage
* The bot will keep running unless the screen is force-killed or you hit Ctrl+C
* The bot will keep retrying whenever there's an error until its get it right
* The bot will fail to work properly if the API keys is non-existent under .env file
