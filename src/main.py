import os
import subprocess
import discord
<<<<<<< Updated upstream
from dotenv import load_dotenv
=======
from discord.ext import commands
>>>>>>> Stashed changes

from rich import print
from rich.traceback import install

# from DiscordClass import MyClient
# from textsCogs import TextsCog
from config import load_discord_bot_config

install(show_locals=True)
# POTENTIAL NAME: Coriakin because this character matches a lot of my plans and past fails with this bot

cogs_list = ["textsCogs", "ownerCogs"]
discord_bot_config = load_discord_bot_config()
intents = discord.Intents.default()
intents.message_content = True


# async def load_extensions():
#     # Iterate through files and load extensions asynchronously
#     for filename in cogs_list:
#         await coriakin.load_extension(f"{filename}")


# TODO: add print statements to a log file instead of the console
coriakin = commands.Bot(command_prefix="!", intents=intents)


def main():
    print("Running Discord bot...")
<<<<<<< Updated upstream
    client.run(client.TOKEN)
=======
    coriakin.run(token=discord_bot_config.bot_token)
>>>>>>> Stashed changes


@coriakin.event
async def on_ready():
    try:
        for cog in os.listdir("./"):
            if cog.endswith("Cogs.py"):
                print(f"Cog loading: {cog[:-3]}")
                await coriakin.load_extension(f"{cog[:-3]}")

    except Exception as e:
        print(f"Failed to load cog {cog[:-3]}: {e}")
    # try:
    #     synced = await coriakin.tree.sync()
    #     print(f"Synced {len(synced)} command(s)")
    # except Exception as e:
    #     print(f"Failed to sync commands: {e}")

if __name__ == "__main__":
    main()
