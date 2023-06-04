import re

from chatbot import ChatBot

class TitleCreator():
    def __init__(self, api_key):
        self.key = api_key
    
    def generate_title(self, memory):
        context = "You are a summarizer"
        prompt = f"Summarize this in 3-8 words: {memory}"
        BOT = ChatBot(context, self.key, model="gpt-3.5-turbo")
        title = BOT.get_response(prompt)
        title = self.remove_unwanted_chars(title)
        return title
    
    def remove_unwanted_chars(self, s):
        unwanted_chars = "*\"\\/<>:|?."
        table = str.maketrans('', '', unwanted_chars)
        return s.translate(table)