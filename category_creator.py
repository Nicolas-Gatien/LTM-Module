import os
from chatbot import ChatBot
import traceback

class FileHandler():
    MEMORY_DIR = "memory_bank/Memories/"
    MAPS_DIR = "memory_bank/Maps/"

    def read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
            return None

    def extract_file_name_from_line(self, line):
        try:
            return line[line.find("[[")+2:line.find("]]")].strip()
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
            return None

    def write_body_to_file(self, title, body):
        try:
            filename = os.path.join(self.MAPS_DIR, title + ".md")
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(body)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")

    def write_headers_to_file(self, headers):
        try:
            file_path = os.path.join(self.MAPS_DIR, "headers.txt")
            with open(file_path, 'w', encoding='utf-8') as file:
                for i, header in enumerate(headers, start=1):
                    file.write(f"{i}. [[🗺️{header}]]\n")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")



class ChatbotManager():
    def __init__(self, api_key):
        try:
            self.key = api_key
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")

    def get_chatbot_response(self, prompt):
        try:
            bot = ChatBot("You are a categorizer", self.key)
            return bot.get_response(prompt)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
            return None

    def extract_code_blocks(self, response):
        try:
            code_blocks = response.split("```md")
            return [block for block in code_blocks if block.strip() != '']
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
            return None

    def process_code_blocks(self, code_blocks):
        headers = []
        try:
            for block in code_blocks:
                block = self.remove_trailing_code_block(block)
                title, body = self.split_block_into_title_and_body(block)
                headers.append(title)
            return headers
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
            return None

    def remove_trailing_code_block(self, block):
        try:
            return block.replace("```", "")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
            return None

    def split_block_into_title_and_body(self, block):
        try:
            split_block = block.split('\n', 1)
            title = split_block[0].strip('# ')
            body = split_block[1] if len(split_block) > 1 else ""
            return title, body
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
            return None, None


class CategoryCreator():
    def __init__(self, api_key):
        try:
            self.file_handler = FileHandler()
            self.chatbot_manager = ChatbotManager(api_key)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")

    def pull_memories(self, main_file_path):
        memories_list = []
        try:
            main_file_contents = self.file_handler.read_file(main_file_path)

            for line in main_file_contents.split('\n'):
                file_name = self.file_handler.extract_file_name_from_line(line)
                memory_path = os.path.join(FileHandler.MEMORY_DIR, file_name + ".md")
                memory_contents = self.file_handler.read_file(memory_path)
                if memory_contents is not None:
                    memories_list.append(memory_contents)

        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
        
        return memories_list

    def generate_prompt(self, file_title, file_contents, memories):
        try:
            memories_string = "\n".join(memories)
            num_memories = len(memories)
            return f"""
Here is a file {file_title} with {num_memories} memories and/or categories:
<<<
{file_contents}
>>>

Here are those memories and/or categories:
<<<
{memories_string}
>>>

Separate these memories and/or categories into as many new distinct categories as you see fit. 
Output the new categories as three markdown codeblocks with the following format:

```md
# Title
1. [[memory 1]]
2. [[Memory 2]]
```

Here is an example response:
```md
# Nature Experiences
1. [[🧠 First Glimpse of Grand Canyon]]
2. [[🧠 Witnessing My First Snowfall]]
3. [[🧠 First Solo Drive Along the Coastline]]
```
```md
# Personal Milestones
1. [[🧠 Completing My First Marathon]]
2. [[🧠 First Solo Drive Along the Coastline]]
```
```md
# Solo Travels
1. [[🧠 Solo Journey Through Japan]]
2. [[🧠 First Solo Drive Along the Coastline]]
```
"""
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
            return None

    def parse_categories_from_response(self, response):
        try:
            code_blocks = self.chatbot_manager.extract_code_blocks(response)
            headers = self.chatbot_manager.process_code_blocks(code_blocks)
            return headers
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
            return None

    def generate_categories(self, main_file_path):
        try:
            file_title = os.path.basename(main_file_path)
            file_contents = self.file_handler.read_file(main_file_path)
            memories = self.pull_memories(main_file_path)
            prompt = self.generate_prompt(file_title, file_contents, memories)
            chatbot_response = self.chatbot_manager.get_chatbot_response(prompt)
            categories = self.parse_categories_from_response(chatbot_response)

            for title, body in categories.items():
                self.file_handler.write_body_to_file(title, body)

            self.file_handler.write_headers_to_file(categories)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\033[91mError: {str(e)}\nAt: {tb}\033[0m")
        

