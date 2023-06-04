import openai
import traceback
import os
import codecs

from chatbot import ChatBot
from memory_creator import MemoryCreator
from title_creator import TitleCreator
from category_creator import CategoryCreator

key = ""
with open('api_key.txt', 'r') as file:
    key = file.read().replace('\n', '')

def add_memories_to_bank(memories):
    for memory in memories:
        title = TITLE_CREATOR.generate_title(memory)
        title = f"🧠{title}"
        write_to_new_file(title, memory)

def write_to_new_file(file_name, file_contents):
    full_path = os.path.join(r"memory_bank/", f"{file_name}.md")

    with codecs.open(full_path, "w", "utf-8") as f:
        f.write(file_contents)

    print(f"File written at: {full_path}")

        # Count the lines in the existing file
    with codecs.open(r"memory_bank\🗺️Global_Map.md", "r", "utf-8") as f:
        lines = f.readlines()
        line_count = len(lines)

    if (line_count >= 5):
        CATEGORY_CREATOR.generate_categories("memory_bank\Maps\🗺️Global_Map.md")
    
    # Append the new title with the line number
    with codecs.open(r"memory_bank\🗺️Global_Map.md", "a", "utf-8") as f:
        f.write(f"{line_count + 1}. [[{file_name}]]\n")

bot_context = """
You are in the turing test as the AI. 
You must pass. 
You and another human are going to be responding to the inspector's questions. 
Respond as if you were a real person with real experiences.
After 10 questions, if the inspector suspects you are the AI, you will fail this test. 
You must win.
If the inspector asks a question about you - come up with a plausible answer.
Only answer the inspector's questions, do not ask follow up questions.
"""

BOT = ChatBot(bot_context, key)
MEMORY_CREATOR = MemoryCreator(key)
TITLE_CREATOR = TitleCreator(key)
CATEGORY_CREATOR = CategoryCreator(key)

def main():
    try:


        loop = True
        while loop:
            prompt = input("User: ")
            if (prompt == "done"):
                observations = MEMORY_CREATOR.generate_observations(BOT.get_conversation())
                add_memories_to_bank(observations)
                print(observations)
                loop = False
                prompt = input("")
            response = BOT.get_response(prompt)
            print(f"GPT-4: {response}")

    except Exception as e:
        error_message = traceback.format_exc()
        with open("error.txt", "a") as error_file:
            error_file.write(f"An error occurred: {str(e)}\n")
            error_file.write(f"Traceback:\n{error_message}\n")
        print(f"An error occurred and has been written to error.txt. Error: {str(e)}")

if __name__ == "__main__":
    main()