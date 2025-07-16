from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def create_chatbot():
    """
    Creates and trains a chatbot.
    """
    chatbot = ChatBot('Hospitality Robot')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english")
    return chatbot
