# Outfit Planner Hackathon Project

## Project Overview

**Outfit Planner** is a Python/FastAPI web application that helps users plan outfits based on their wardrobe, upcoming calendar events, and weather conditions. The app allows users to:

- Upload clothes and accessories with categories, colors, and images.
- Generate outfit suggestions based on event type and current weather.
- Get explanations for why an outfit was recommended.
- View uploaded wardrobe and past outfit choices.

This project was built for a hackathon with the theme **"Reinventing the Wheel"**, demonstrating a new way to combine AI, weather, and personal wardrobe planning.

---

## Features

- **Upload Wardrobe**: Users can upload clothing items with images, names, categories, and tags.
- **Outfit Generator**: Automatically generates an outfit based on weather data, calendar events, and color harmony.
- **Weather Integration**: Fetches real-time weather data using the OpenWeather API.
- **Calendar Integration**: Connects with Google Calendar to suggest outfits appropriate for upcoming events.
- **AI Explanations**: Provides natural-language explanations for outfit choices (using OpenAI API or mock logic for hackathon demo).
- **Responsive Web Interface**: Minimalistic UI built with Tailwind CSS and Jinja2 templates.

---

## Folder Structure
.
├── ai_explainer.py
├── calendar_service.py
├── credentials.json
├── database.py
├── main.py
├── models.py
├── outfit_engine.py
├── README.md
├── requirements.txt
├── static
│   ├── styles.css
│   └── uploads
├── templates
│   ├── base.html
│   ├── index.html
│   ├── outfit.html
│   ├── upload.html
│   └── wardrobe.html
├── token.json
├── utils
│   ├── color_match.py
│   └── helpers.py
└── weather.py

