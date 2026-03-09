import pandas as pd
import requests
import re
import random

# Load dataset
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


# =========================
# CHATBOT RESPONSE
# =========================

def chatbot_response(user_input):

    query = user_input.lower()

    # =========================
    # GREETING
    # =========================

    if query in ["hi", "hello", "hey"]:
        return (
            "👋 Hello! I'm your Nagaland Travel Assistant.\n\n"
            "I can help you with:\n"
            "• Best places to visit\n"
            "• Hotels & stays\n"
            "• Food to try\n"
            "• Travel itinerary\n"
            "• Transport guide\n\n"
            "👉 Ask me anything about Nagaland! 😊"
        )

    # =========================
    # BEST PLACES
    # =========================

    if "place" in query or "visit" in query:

        limit = extract_number(query, 5)

        places = get_unique_values("Location")

        places = places[:limit]

        return format_list(f"Top {limit} Places to Visit in Nagaland", places)

    # =========================
    # FOOD
    # =========================

    if "food" in query or "eat" in query or "dish" in query:

        limit = extract_number(query, 5)

        foods = get_unique_values("Food_and_Famous_Dishes")[:limit]

        return format_list(f"Top {limit} Foods to Try in Nagaland", foods)

    # =========================
    # HOTELS
    # =========================

    if "hotel" in query or "stay" in query or "accommodation" in query:

        limit = extract_number(query, 5)

        hotels = get_unique_values("Recommended_Hotels_with_Rating_and_PriceRange")[:limit]

        return format_list(f"Top {limit} Hotels in Nagaland", hotels)

    # =========================
    # ACTIVITIES
    # =========================

    if "activity" in query or "things to do" in query or "adventure" in query:

        limit = extract_number(query, 5)

        activities = get_unique_values("Activities")[:limit]

        return format_list(f"Top {limit} Activities in Nagaland", activities)

    # =========================
    # ITINERARY
    # =========================

    if "itinerary" in query or "plan" in query or "trip" in query:

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

    if "transport" in query or "travel" in query or "reach" in query:

        return (
            "🚗 Transport Guide for Nagaland:\n\n"
            "✈️ Nearest Airport: Dimapur Airport\n"
            "🚆 Nearest Railway Station: Dimapur\n"
            "🚌 Buses & taxis available to Kohima and other cities\n"
            "🚖 Local taxis are common for sightseeing\n"
        )

    # =========================
    # DEFAULT RESPONSE
    # =========================

    return (
        "🤖 Sorry, I didn't understand that.\n"
        "Try asking:\n"
        "• Top 10 places in Nagaland\n"
        "• 7 day itinerary\n"
        "• Famous food in Nagaland\n"
        "• Best hotels in Nagaland"
    )
