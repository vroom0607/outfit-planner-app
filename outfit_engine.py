from utils.helpers import pick_random


def generate_outfit(wardrobe, weather_data, event_type):
    """
    Selects items from wardrobe based on weather and event type.
    Returns a list of clothing items.
    """
    if not wardrobe:
        return []

    style_keywords = {
        "formal": ["formal", "office", "business"],
        "athletic": ["athletic", "gym", "workout", "sport"],
        "casual": ["casual", "weekend", "relaxed"],
    }

    desired_keywords = style_keywords.get(event_type, style_keywords["casual"])

    def matches_style(item):
        tags = (item.tags or "").lower()
        return any(keyword in tags for keyword in desired_keywords)

    preferred = [item for item in wardrobe if matches_style(item)]
    candidates = preferred if preferred else wardrobe

    top_choices = [item for item in candidates if item.category == "top"]
    bottom_choices = [item for item in candidates if item.category == "bottom"]
    shoe_choices = [item for item in candidates if item.category == "shoes"]
    outerwear_choices = [item for item in candidates if item.category == "outerwear"]
    accessory_choices = [item for item in candidates if item.category == "accessory"]

    outfit = []
    for choice in [pick_random(top_choices), pick_random(bottom_choices), pick_random(shoe_choices)]:
        if choice:
            outfit.append(choice)

    temp = weather_data.get("temp", 70)
    raining = weather_data.get("rain", False)

    if temp < 60:
        outerwear = pick_random(outerwear_choices)
        if outerwear:
            outfit.append(outerwear)

    if raining:
        rain_ready = [item for item in outerwear_choices if "rain" in (item.tags or "").lower()]
        rain_item = pick_random(rain_ready) or pick_random(outerwear_choices)
        if rain_item and rain_item not in outfit:
            outfit.append(rain_item)

    accessory = pick_random(accessory_choices)
    if accessory:
        outfit.append(accessory)

    return outfit


def map_event_to_style(event_title):
    """
    Converts event title string to outfit type: formal, casual, athletic, etc.
    """
    title = (event_title or "").lower()

    formal_keywords = ["meeting", "interview", "presentation", "office", "conference"]
    athletic_keywords = ["gym", "workout", "run", "training", "yoga", "sports"]

    if any(keyword in title for keyword in formal_keywords):
        return "formal"
    if any(keyword in title for keyword in athletic_keywords):
        return "athletic"
    return "casual"
