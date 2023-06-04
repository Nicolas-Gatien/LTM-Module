import os

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
    
    def generate_prompt(self, source_name, source_contents, memory_names, memories)

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

        #Prompt Chatbot and Get New Categories
        #Extract Code Bloccks from Response
        #Extract category titles
        #Create category files
        #Replace contents of original file