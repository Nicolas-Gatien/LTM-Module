import openai
import traceback
from chatbot import ChatBot

key = ""
with open('api_key.txt', 'r') as file:
    key = file.read().replace('\n', '')

def main():
    try:
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
        
        while True:
            prompt = input("User: ")
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