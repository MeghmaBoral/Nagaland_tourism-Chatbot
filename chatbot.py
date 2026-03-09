import pandas as pd
import requests

# Load dataset
data = pd.read_csv("data.csv")


# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

def format_list(title, items):
    response = f"✨ {title}:\n"
    for i, item in enumerate(items, 1):
        response += f"{i}. {item}\n"
    return response


def get_unique_values(column):
    values = data[column].dropna().unique()
    return [str(v) for v in values]


# ---------------------------
# MAIN CHAT FUNCTION
# ---------------------------

def chatbot_response(user_query):
    query = user_query.lower().strip()

    # ============================
    # GREETING
    # ============================
    if query in ["hi", "hello", "hey", "hii", "helo"]:
        return """👋 Hello! I'm your Nagaland Travel Assistant.

I can help you with:
• Best places to visit
• Hotels & stays
• Food to try
• Travel itinerary
• Transport guide

👉 Ask me anything about Nagaland! 😊"""

    # ============================
    # THANK YOU
    # ============================
    if "thank" in query:
        return "😊 You're welcome! Have a great trip to Nagaland!"

    # ============================
    # BYE
    # ============================
    if "bye" in query:
        return "👋 Goodbye! Enjoy your Nagaland trip!"

    # ============================
    # BEST PLACES
    # ============================
    if "place" in query or "visit" in query:
        places = get_unique_values("Location")[:5]
        return format_list("Top Places to Visit in Nagaland", places)

    # ============================
    # FOOD
    # ============================
    if "food" in query or "eat" in query:
        foods = get_unique_values("Food_and_Famous_Dishes")[:5]
        return format_list("Must Try Foods", foods)

    # ============================
    # HOTELS
    # ============================
    if "hotel" in query or "stay" in query:
        hotels = get_unique_values("Recommended_Hotels_with_Rating_and_PriceRange")[:5]
        return format_list("Best Places to Stay", hotels)

    # ============================
    # ADVENTURE
    # ============================
    if "adventure" in query or "trek" in query:
        adv = get_unique_values("Adventure_Activities")[:5]
        return format_list("Adventure Activities", adv)

    # ============================
    # TRANSPORT
    # ============================
    if "reach" in query or "transport" in query:
        ways = get_unique_values("How_to_go")[:5]
        return format_list("How to Reach Nagaland", ways)

    # ============================
    # MARKETS
    # ============================
    if "market" in query or "shopping" in query:
        markets = get_unique_values("Markets")[:5]
        return format_list("Shopping Places", markets)

    # ============================
    # TRIBES
    # ============================
    if "tribe" in query or "culture" in query:
        tribes = get_unique_values("Tribes_Info")[:5]
        return format_list("Tribal Culture Info", tribes)

    # ============================
    # ITINERARY
    # ============================
    if "itinerary" in query or "plan" in query or "days" in query:
        response = "🗺️ Suggested Nagaland Itinerary:\n\n"

        grouped = data.groupby("Day")

        for day, group in grouped:
            row = group.iloc[0]

            response += f"📅 Day {day}:\n"
            response += f"📍 Location: {row['Location']}\n"
            response += f"👉 Activities: {row['Activities']}\n"
            response += f"🍜 Food: {row['Food_and_Famous_Dishes']}\n\n"

        return response

    # ============================
    # BEST TIME
    # ============================
    if "best time" in query or "season" in query:
        notes = get_unique_values("Notes")[:5]
        return format_list("Best Time & Travel Tips", notes)

    # ============================
    # AI FALLBACK (CONTROLLED)
    # ============================
    try:
        prompt = f"""
You are a Nagaland tourism chatbot.

STRICT RULES:
- Answer ONLY about Nagaland
- No examples
- No explanation
- No long paragraph
- Max 5 bullet points

FORMATS:
- Places → Top 5 places
- Food → 5 dishes
- Hotels → 3-5 options
- Itinerary → Day-wise

User Question: {user_query}

Answer:
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )

        answer = response.json()["response"]

        # Clean unwanted text
        bad_words = ["Question:", "Answer:", "Example"]
        for word in bad_words:
            answer = answer.replace(word, "")

        # Filter wrong states
        if any(x in answer.lower() for x in ["meghalaya", "assam", "manipur"]):
            return "⚠️ Sorry, I only provide information about Nagaland."

        return answer.strip()

    except:
        return "⚠️ AI not running. Please start Ollama using: ollama run tinyllama"