##################################################################
# Title: Google AI Chat Bot
# Created: 2026-11-19
# By: Omegazyph
# Updated: 2026-11-19
# Description:
#     This simple command-line chat bot uses Google Gemini via the
#     google-genai SDK and loads the API key from a local .env file.
#     Get an API key at: https://aistudio.google.com/api-keys
##################################################################

import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load environment variables from a local .env file if one exists
load_dotenv()

# Retrieve the API key from the environment variables
gemini_api_key = os.environ.get("GEMINI_API_KEY")

# Stop early with a clear message if the key is missing
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Add GEMINI_API_KEY=your_key to your .env file."
    )

# Initialize the Google GenAI client with the key from the environment
client = genai.Client(api_key=gemini_api_key)

# Start a multi-turn chat session with the model
chat = client.chats.create(model="gemini-flash-latest")

print("Chat bot started. Type 'exit' to quit.")

while True:
    # Read input from the user
    user_message = input("You: ").strip()

    # Skip empty lines so we do not waste API calls
    if not user_message:
        continue

    # Allow the user to exit the conversation cleanly
    if user_message.lower() == "exit":
        print("Exiting chat bot. Goodbye!")
        break

    # Send the message and print the model reply, handling errors gracefully
    try:
        reply = chat.send_message(user_message)
        print("Bot:", reply.text)
    except errors.APIError as api_error:
        print("Gemini API error", api_error)
    except OSError as network_error:
        print("Network or connection error:", network_error)