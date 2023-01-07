# This bot will use open ai to generate a response scolding or praising a user for their participation in the last 10 messages

import discord
import openai

# grab the OpenAI API key from the OpenAI API key file
with open("OpenAiKey", "r") as f:
    #openai.api_key = f.read()
    

# grab the discord bot token from the discord bot token file
with open("BotToken", "r") as f:
    #token = f.read()
    

# create the prompt for the open ai api
def create_prompt(user, tone, style, messages):
    # parse the messages into a string
    message_string = ""

    for message in messages:
        message_string += message.author.display_name + ": " + message.content + "\n"

    # create the prompt
    return f"{tone} {user} in the style of {style} for his/her participation in the following chat:\n {message_string}"

# create the discord client
class MyClient(discord.Client):
    # startup

    async def on_ready(self):
        print('Logged on as', self.user)

    # when a message is sent, check if it is a command
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        # if the message is a command, do the command
        if message.content.startswith('!!'):
            await self.do_command(message)
    
    # do the command
    async def do_command(self, message):
        # get the command
        command = message.content[2:]

        # get the user
        user = message.mentions[0]

        # get the tone
        tone = command.split(" ")[0]

        # get the style
        style = command.split(" ")[1]

        # get the last 10 messages sent by users other than the bot
        messages = []
        async for message in message.channel.history(limit=10):
            if message.author != self.user:
                messages.append(message)

        # create the prompt
        prompt = create_prompt(user, tone, style, messages)

        # get the response
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop="\n"
        )

        # send the response
        await message.channel.send(response.choices[0].text)
    
# create the client and run the bot
client = MyClient()
client.run(token)
