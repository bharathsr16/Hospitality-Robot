def handle_text_input(text):
    """
    Handles text input from the user.
    """
    if "hello" in text.lower():
        return "Hello! How can I help you today?"
    else:
        return "I'm sorry, I don't understand. Please try again."
