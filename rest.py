from time import sleep
from random import randint

def rest():
    random_minutes = randint(1,3)
    print(f"Waiting for {random_minutes} minute{"s" if random_minutes > 1 else ""} before sending next question...\n")
    sleep(random_minutes * 60)
    