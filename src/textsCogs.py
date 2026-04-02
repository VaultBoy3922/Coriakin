import time

import discord
from discord import ui
from discord import app_commands
from discord.ext import commands
from typing import List

from rich import print
from rich.traceback import install

import TwilioClass
import NocoClass
from config import load_discord_bot_config, load_text_update_groups


install(show_locals=True)
# NocoClass = NocoClass.NocoClass()
config_data = load_discord_bot_config()
update_groups = load_text_update_groups()


class TextMessageUI(ui.Modal, title="Send Text Message Notification"):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.noco_class = NocoClass.NocoClass()
        self.twilio_class = TwilioClass.TwilioClient()

    group_options = []

    for group in update_groups.text_update_groups.keys():
        group_options += [
            discord.SelectOption(
                label=f"{group}", description=f"Send message to {group} subscribers"
            )
        ]

    groupName = ui.Label(
        text="Group Selection",
        description="Please Select the Notification Group",
        component=ui.Select(placeholder="Choose group...", options=group_options),
    )

    message = ui.TextInput(
        label="Text Notification Message",
        style=discord.TextStyle.paragraph,
        placeholder="Enter the message to send to subscribers",
        required=True,
        max_length=1500,
    )

    fileUpload = ui.Label(
        text="File Upload (Optional)",
        description="Upload a file to send with the message",
        component=ui.FileUpload(required=False),
    )

    # TODO: add file upload functionality, add error handling for file upload, add check for if file is too large for twilio, add check for if file type is supported by twilio, add functionality to send file with message in twilio, add functionality to send file with message in discord webhook, add functionality to send message in correct announcement channel in discord based on group selection
    # TODO: add logging instead of print statements, make sure Sending Message message sends only if twilio sucessfully send message and add error message in discord to show why it failed
    async def on_submit(self, interaction: discord.Interaction):
        self.noco_class.authorize()
        for i in self.noco_class.subscriber_list:
            if (
                self.groupName.component.values[0]
                in i[f"{self.noco_class.subscriber_type_column}"].lower()
            ):
                print(
                    f"{i['PhoneNumber']} is subscribed to {self.groupName.component.values[0]} updates"
                )
                if self.fileUpload.component.values:
                    print(
                        f"File uploaded: {self.fileUpload.component.values[0].url}, sending with message"
                    )
                    self.twilio_class.send_message(
                        body=self.message.value,
                        to=f"+{i['PhoneNumber']}",
                        media_url=self.fileUpload.component.values[0].url,
                    )
                else:
                    print("No file uploaded")
                    self.twilio_class.send_message(
                        body=self.message.value, to=f"+{i['PhoneNumber']}"
                    )
            else:
                print(
                    f"{i['PhoneNumber']} not subscribed to {self.groupName.component.values[0]} updates"
                )
            # time.sleep(1)

        await interaction.response.send_message(
            f"Sending message to: {self.groupName.component.values[0]}, subscribers: {self.message.value}, with file: {self.fileUpload.component.values[0].url if self.fileUpload.component.values else 'No file uploaded'}",
            ephemeral=True,
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(
            f"An error occurred while processing your request: {str(error)}",
            ephemeral=True,
        )


class TextsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: add error handling, rewite to be more efficient with new command structure, report success/failure, have message from bot only sender can see to walk through process, send webhook message in correct announcmenet channel from sender
    @app_commands.command(
        name="send_text", description="Send a text message to subscribers."
    )
    # TODO: make the role configurable in the config file instead of hardcoding it here
    # TODO: make error handling for if user does not have the role
    # TODO: hide command from users who do not have the role
    @app_commands.checks.has_role("text-updates")
    async def send_text(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TextMessageUI())


async def setup(bot):
    await bot.add_cog(TextsCog(bot))
