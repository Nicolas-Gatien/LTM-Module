import os
import re

from chatbot import ChatBot

class CategoryCreator():
    def __init__(self, api_key):
        self.key= api_key

    def get_list_of_memory_names(self, source_contents):
        lines = source_contents.split('\n')
        
        names = []
        for line in lines:
            if self.line_is_empty(line):
                #skip the rest
                continue
            
            name = line.split(' ', 1)[1]
            name = name.replace("[[", "")
            name = name.replace("]]", "")
            
            names.append(name)
        
        return names
    def line_is_empty(self, line):
        if line.strip():
            return False
        return True

    def get_contents_of_file_at(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def get_list_of_memory_paths_based_on_names(self, memories):
        paths = []
        for memory in memories:
            path = memory + ".md"
            paths.append(path)

        return paths
    def get_list_of_contents_of_all_specified_memories(self, paths):
        memories = []
        for path in paths:
            content = self.get_contents_of_file_at(path)
            memories.append(content)

        return memories

    def get_name_of_file_at(self, file_path):
        return os.path.basename(file_path)
    
    def generate_prompt(self, source_name, source_contents, memory_names, memories):
        memories_string = ""
        for i in enumerate(memory_names):
            memories_string += f"{memory_names[i]}:\n"
            memories_string += memories[i]

        f"""
        This is a file named {source_name} which contains a list of {len(memory_names)} items which are either memories or categories.
        A memory's title begins with: 🧠
        A category's title begins with: 🗺️
        <<<
        {source_contents}
        >>>

        Here is the contents of each of those memories/categories:
        <<<
        {memories_string}
        >>>

        Separate these items into as many new distinct categories as you see fit. 
        Output the new categories as seperate markdown codeblocks with the following format:
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

    def extract_code_blocks_from_response(self, response):
        # Regex pattern for code blocks
        pattern = r'```.*?```'
        
        # Use re.findall() to find all code blocks in the text
        code_blocks = re.findall(pattern, response, re.DOTALL)
        
        # Remove the backticks, 'md', and any leading or trailing newlines from each code block
        code_blocks = [block[5:-3].strip() for block in code_blocks]
        
        return code_blocks
    
    def extract_category_title_and_contents_from_code_block(self, code_block):
        # Split the text into lines
        lines = code_block.split('\n')
        
        # The title should be the first non-empty line
        category_title = None
        for line in lines:
            if line.strip():  # This line is not empty
                title = line.strip()
                break

        # Remove the hashtag and space from the title
        if category_title and category_title.startswith('# '):
            category_title = category_title[2:]

        # Remove the title from the text (with the hashtag and space)
        category_contents = code_block.replace('# ' + category_title, '').strip()

        return category_title, category_contents
    
    def get_category_titles_from_code_blocks(self, code_blocks):
        category_titles = []

        for code_block in code_blocks:
            title, content = self.extract_category_title_and_contents_from_code_block(code_block)
            category_titles.append(title)

        return category_titles            
    
    def get_category_contents_from_code_blocks(self, code_blocks):
        category_contents = []

        for code_block in code_blocks:
            title, content = self.extract_category_title_and_contents_from_code_block(code_block)
            category_contents.append(content)

        return category_contents
    
    def create_markdown_file(self, title, contents):
        directory = "memory_bank"
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        
        file_name = f"{directory}/🗺️{title}.md"
        
        # Write the content to a file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(contents)
            
        # Now, read the file and remove empty lines
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Remove empty lines
        lines = [line for line in lines if line.strip() != '']
        
        # Write the cleaned content back to the file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    def create_category_files(self, category_titles, category_contents):
        for i in enumerate(category_titles):
            self.create_markdown_file(category_titles[i], category_contents[i])

    def format_categories_for_source_file(self, category_names):
        formatted_string = ""
        for i, s in enumerate(category_names, 1):
            formatted_string += f"{i}. [[🗺️{s}]]\n"
        return formatted_string

    def override_source(self, source_path, content):
        with open(source_path, 'w') as file:
            file.write(content)

    def split_into_categories(self, source_path):
        #✅ Get Path To File In Need of Categorization

        #✅ Get contents of source
        source_content = self.get_contents_of_file_at(source_path)
        source_name = self.get_name_of_file_at(source_path)

        #✅ Extract Memory/Category Names
        memory_names = self.get_list_of_memory_names(source_content)
        memory_paths = self.get_list_of_memory_paths_based_on_names(memory_names)

        #✅ Get Memory/Category Contents
        memories = self.get_list_of_contents_of_all_specified_memories(memory_paths)

        #✅ Prompt Chatbot and Get New Categories
        prompt = self.generate_prompt(source_name, source_content, memory_names, memories)
        BOT = ChatBot("Your are a categorizer. Your job is to create relevant and cohesive categories.", self.key)
        response = BOT.get_response(prompt)

        #✅ Extract Code Bloccks from Response
        code_blocks = self.extract_code_blocks(response)

        #✅ Extract category titles
        category_titles = self.get_category_titles(code_blocks)
        category_contents = self.get_category_contents(code_blocks)

        #✅ Create category files
        self.create_category_files(category_titles, category_contents)

        #✅ Replace contents of original file
        new_source_content = self.format_categories_for_source_file(category_titles)
        self.override_source(source_path, new_source_content)