import os

from interactions import Client, Intents, listen, slash_command, SlashContext, slash_option, OptionType, Attachment, File, AutocompleteContext
from dotenv import load_dotenv
from datetime import date
import aiohttp
import io

load_dotenv()  # load the .env file

bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

@listen()  # this decorator tells interactions.py that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@slash_command(description="displays the current date")
async def currentdate(ctx: SlashContext):
    today = date.today()
    await ctx.send(today.strftime('%m/%d/%Y'))


@slash_command(description="sends \"Pong!\"")  # this decorator tells interactions.py to make a slash command with the corresponding name
async def ping(ctx: SlashContext):
    # slash commands are always passed a SlashContext object, used to actually respond to the command
    await ctx.send("Pong!", tts=True)  # send a message to the channel the command was used in

@slash_command(description="hehehehehehe")
async def funny(ctx: SlashContext):

    await ctx.send(file="noBitches.jpg")

@slash_command(description="displays the color palette of the image sent")
@slash_option(
    name="attachment_option",
    description="file to be displayed",
    required=True,
    opt_type=OptionType.ATTACHMENT
)
async def display_color_pallet(ctx: SlashContext, attachment_option: Attachment):
    async with aiohttp.ClientSession() as session:
        async with session.get(attachment_option.url) as resp:
            hello = await resp.read()
        data = aiohttp.FormData()
        data.add_field("file", io.BytesIO(hello), filename="uwu", content_type=attachment_option.content_type)
        async with session.post("https://uf-api-group.pythiauf.repl.co/color-palette", data=data) as resp:
            hello = await resp.read()
            # hello still needs to be transformed from raw data into a file object
            hello2 = io.BytesIO(hello)
            hello_file = File(hello2, "hello.jpeg")
    await ctx.send(file=hello_file)
    
@slash_command(description="displays the status of the chosen gym building")
@slash_option(
    name="integer_option",
    description="uwu",
    required=True,
    opt_type=OptionType.INTEGER,
    autocomplete=True
)
async def report_gym_stats(ctx: SlashContext, integer_option: int):
    await ctx.send("\n" + f"You input {integer_option}")

@report_gym_stats.autocomplete("integer_option")
async def autocomplete(ctx: AutocompleteContext):
    # learn how runtime functions work (eventually (not now (good moringn)))
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uf-api-group.pythiauf.repl.co/gymstats") as resp:
            hello = await resp.json()
        hello2 = []
        for index, i in enumerate(hello):
            stringe = f"Building {index+1}: {i['name']}"
            hello2.append({"name": stringe, "value": index})
    integer_option_input = ctx.input_text
    await ctx.send(choices=hello2)

    




bot.start(os.environ["BOT_TOKEN"])
