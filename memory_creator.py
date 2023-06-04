import re

from chatbot import ChatBot

class MemoryCreator():
    def __init__(self, api_key):
        self.key = api_key
    
    def generate_observations(self, conversation):
        context = "You are a memory writer."
        prompt = f"""
This is a transcript of a conversation:
<<<
{str(conversation)}
>>>

From the perspective of the assistant (use the first person), write as many memories as you see fit. They are not reflections, but accurate retelling of the events that occurred during the conversation. Like observations.

Limit each memory to 1-3 sentences.
"""
        BOT = ChatBot(context, self.key)
        response = BOT.get_response(prompt)
        memories = self.turn_string_of_memories_into_list(response)
        return memories

    def turn_string_of_memories_into_list(input_string):
        lines = input_string.split('\n')

        memories = []

        for line in lines:
            # check if the line is not empty
            if line:
                line = line.strip()
                parts = re.split(r'^\d+\. ', line)
                if len(parts) == 2:
                    memories.append(parts[1])

        return memories