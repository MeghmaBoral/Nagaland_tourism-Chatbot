import pandas as pd
import requests
import re

# =========================
# LOAD DATASET
# =========================

data = pd.read_csv("data.csv")

# =========================
# HELPER FUNCTIONS
# =========================

def extract_number(query, default=5):
    numbers = re.findall(r'\d+', query)
    if numbers:
        return int(numbers[0])
    return default


def get_unique_values(column):
    return list(data[column].dropna().unique())


def format_list(title, items):
    response = f"\n✨ {title}:\n"
    for i, item in enumerate(items, 1):
        response += f"{i}. {item}\n"
    return response


def contains_keywords(query, keywords):
    return any(word in query for word in keywords)


# =========================
# INTENT KEYWORDS
# =========================

food_keywords = [
    "food","eat","dish","restaurant","cafe","cuisine",
    "meal","local food","street food","what should i eat",
    "best food","naga food","famous food"
]

place_keywords = [
    "place","visit","tourist","attraction","spot",
    "location","sightseeing","must visit","travel spots"
]

hotel_keywords = [
    "hotel","stay","accommodation","resort","guest house",
    "hostel","lodging","places to stay"
]

transport_keywords = [
    "transport","travel","reach","how to reach",
    "flight","airport","railway","train","bus",
    "taxi","directions"
]

activity_keywords = [
    "activity","things to do","adventure",
    "trek","trekking","festival","experience"
]

itinerary_keywords = [
    "itinerary","plan","trip","schedule","tour plan"
]

greeting_keywords = [
    "hi","hello","hey","good morning","good evening"
]

# =========================
# OLLAMA AI FUNCTION
# =========================

def ollama_ai_reply(user_query):

    prompt = f"""
You are a Nagaland tourism assistant.

Rules:
- Only answer about Nagaland tourism.
- Give short helpful answers.
- Prefer bullet points.
- If itinerary requested, provide day-wise suggestions.

User Question: {user_query}

Answer:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()
        return result["response"].strip()

    except:
        return "⚠️ AI model not running. Start Ollama using: ollama run tinyllama"


# =========================
# MAIN CHATBOT FUNCTION
# =========================

def chatbot_response(user_input):

    query = user_input.lower()

    # =========================
    # GREETING
    # =========================

    if contains_keywords(query, greeting_keywords):
        return (
            "👋 Hello! I'm your Nagaland Travel Assistant.\n\n"
            "I can help you with:\n"
            "• Best places to visit\n"
            "• Hotels & stays\n"
            "• Food to try\n"
            "• Activities & adventures\n"
            "• Travel itinerary\n"
            "• Transport guide\n\n"
            "👉 Ask me anything about Nagaland! 😊"
        )

    # =========================
    # FOOD
    # =========================

    if contains_keywords(query, food_keywords):

        limit = extract_number(query, 5)
        foods = get_unique_values("Food_and_Famous_Dishes")[:limit]

        return format_list(f"Top {limit} Foods to Try in Nagaland", foods)

    # =========================
    # BEST PLACES
    # =========================

    if contains_keywords(query, place_keywords):

        limit = extract_number(query, 5)
        places = get_unique_values("Location")[:limit]

        return format_list(f"Top {limit} Places to Visit in Nagaland", places)

    # =========================
    # HOTELS
    # =========================

    if contains_keywords(query, hotel_keywords):

        limit = extract_number(query, 5)
        hotels = get_unique_values("Recommended_Hotels_with_Rating_and_PriceRange")[:limit]

        return format_list(f"Top {limit} Hotels in Nagaland", hotels)

    # =========================
    # ACTIVITIES
    # =========================

    if contains_keywords(query, activity_keywords):

        limit = extract_number(query, 5)
        activities = get_unique_values("Activities")[:limit]

        return format_list(f"Top {limit} Activities in Nagaland", activities)

    # =========================
    # ITINERARY
    # =========================

    if contains_keywords(query, itinerary_keywords):

        days = extract_number(query, 3)

        response = f"\n🗺️ {days}-Day Nagaland Travel Itinerary\n\n"

        total_rows = len(data)

        for i in range(days):

            row = data.iloc[i % total_rows]

            response += f"📅 Day {i+1}\n"
            response += f"📍 Location: {row['Location']}\n"
            response += f"🎯 Activities: {row['Activities']}\n"
            response += f"🍜 Food: {row['Food_and_Famous_Dishes']}\n"
            response += f"🏨 Stay: {row['Recommended_Hotels_with_Rating_and_PriceRange']}\n\n"

        return response

    # =========================
    # TRANSPORT
    # =========================

    if contains_keywords(query, transport_keywords):

        return (
            "🚗 Transport Guide for Nagaland:\n\n"
            "✈️ Nearest Airport: Dimapur Airport\n"
            "🚆 Nearest Railway Station: Dimapur\n"
            "🚌 Buses & taxis available to Kohima and nearby towns\n"
            "🚖 Shared taxis are common for intercity travel\n"
            "🏍️ Local taxis available for sightseeing\n"
        )

    # =========================
    # AI FALLBACK (OLLAMA)
    # =========================

    return ollama_ai_reply(user_input)
