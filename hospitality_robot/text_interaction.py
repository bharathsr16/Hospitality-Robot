import nltk

def get_intent(text):
    """
    Gets the user's intent from the text.
    """
    # Tokenize the text
    tokens = nltk.word_tokenize(text.lower())

    # Check if the user is asking for a location
    if "where" in tokens and "is" in tokens:
        # Find the noun phrase after "is"
        for i in range(len(tokens)):
            if tokens[i] == "is" and i + 1 < len(tokens):
                return "find_location", tokens[i+1]

    return "unknown", None


def handle_text_input(text):
    """
    Handles text input from the user.
    """
    intent, data = get_intent(text)

    if intent == "find_location":
        return f"I will find {data} for you."
    elif "hello" in text.lower():
        return "Hello! How can I help you today?"
    else:
        return "I'm sorry, I don't understand. Please try again."
