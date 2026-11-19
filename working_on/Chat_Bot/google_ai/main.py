##################################################################
# title: Google ai chat bot
# created: 2026-11-19
# By Omegazyph
# updated: 2026-11-19
# discription:
#           this simple chat bot uses google ai called gemaini it 
#           it needs and api from google @ aistudio.google.com/api-keys




from google import genai

client = genai.Client(api_key="add your api here")

chat = client.chats.create (model = "gemini-flash-latest")

while True:
    user = input("You: ")

    if user.lower() == "exit":
        break

    reply = chat.send_message(user)
    print("Bot:", reply.text)