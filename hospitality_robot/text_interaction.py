def get_intent(text):
    """
    Gets the user's intent from the text.
    """
    # Tokenize the text
    import nltk
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
    rules = {
        "hello": "Hello! How can I help you today?",
        "how are you": "I'm doing great, thanks for asking!",
        "what is your name": "My name is Hospitality Robot.",
        "bye": "Goodbye! Have a great day."
    }

    for rule, response in rules.items():
        if rule in text.lower():
            return response

    return "I'm sorry, I don't understand. Please try again."
