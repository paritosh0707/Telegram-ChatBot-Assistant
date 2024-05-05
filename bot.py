from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import openai
import google.generativeai as genai

load_dotenv()
TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Connect with OpenAI
openai.api_key = OPENAI_API_KEY

# print("Ok")

MODEL_NAME = "gpt-3.5-turbo"

#Initialize bot 
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class Reference:
    def __init__(self) -> None:
        self.response = ""


reference = Reference()


def clear_past():
    reference.response = ""




@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")




@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """This handler receives messages with `/start` or  `/help `command

    Args:
        message (types.Message): _description_
    """
    await message.reply("Hi\nI am a Chat Bot! Created by Paritosh. How can i assist you?")




@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Paritosh! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)




@dispatcher.message_handler()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")

    # response = openai.ChatCompletion.create(
    #     model = MODEL_NAME,
    #     messages = [
    #         {"role": "assistant", "content": reference.response}, # role assistant
    #         {"role": "user", "content": message.text} #our query 
    #     ]
    # )
    # reference.response = response['choices'][0]['message']['content']
    reference.response = get_response_from_gemini(message.text)
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]").replace("(", "\\(").replace(")", "\\)"),parse_mode=types.ParseMode.MARKDOWN)
    
    


def get_response_from_gemini(prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+"\nNote: Provide me the result in the amrkdown format")
    return response.text


# def generate_gemini_response(assistant_response, user_query, session_id):
#     # Create a client for the Gemina API
#     client = gemina_v1beta1.GeminaClient()

#     # Define the assistant's message
#     assistant_message = {
#         "role": gemina_v1beta1.ParticipantRole.ASSISTANT,
#         "content": assistant_response
#     }

#     # Define the user's message
#     user_message = {
#         "role": gemina_v1beta1.ParticipantRole.USER,
#         "content": user_query
#     }

#     # Send messages to Gemina and receive the response
#     response = client.converse(
#         session=session_id,
#         participant="USER",
#         messages=[assistant_message, user_message],
#         language_code="en"  # Assuming English language
#     )

#     # Access the assistant's response from the Gemina API response
#     gemina_response = response.messages[0].content

#     return gemina_response

# # Example usage:
# MODEL_NAME = "gemini-pro"
# # session_id = "your-session-id"
# reference_response = "Hello, how can I assist you?"
# user_query = "What's the weather today?"
# reference_response = generate_gemini_response(reference_response, user_query, session_id)



if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)