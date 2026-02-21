import random

def pick_random(items):
    if not items:
        return None
    return random.choice(items)