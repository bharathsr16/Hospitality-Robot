from hospitality_robot.chatbot import create_chatbot
from chatterbot.corpus import download_corpus

if __name__ == "__main__":
    download_corpus()
    create_chatbot()
