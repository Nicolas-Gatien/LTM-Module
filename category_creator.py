import re
import os

from chatbot import ChatBot

class CategoryCreator():
    def __init__(self, api_key):
        self.key = api_key


    def pull_memory_content(self, path):
        contents_list = []
        
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                # Extract file name from line
                file_name = line[line.find("[[")+2:line.find("]]")].strip()
                file_path = os.path.join(path, file_name + ".md")

                # Get the file contents using the helper function
                contents = self.get_file_contents(file_path)
                if contents is not None:
                    contents_list.append(contents)

        return contents_list
                        
    def get_file_name(self, path):
        return os.path.basename(path)
    
    def get_file_contents(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"The file at {path} does not exist.")
            return None


    def generate_categories(self, main_file_path):
        context = "You are a categorizer."
        file_title = self.get_file_name(main_file_path)
        file_contents = self.get_file_contents(main_file_path)
        memories = self.pull_memory_content(main_file_path)
        memories_string = ""
        for memory in memories:
            memories_string += memory
            memories_string += "\n"
        prompt = f"""
Here is a file {file_title} with {len(memories)} memories and/or categories:
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
        BOT = ChatBot(context, self.key)
        response = BOT.get_response(prompt)
        print(response)
        return response