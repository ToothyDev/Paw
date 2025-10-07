import discord


class ConfirmView(discord.ui.DesignerView):
    def __init__(self, prompt: str):
        super().__init__(timeout=120)
        self.confirmed = False
        self.disable_on_timeout = True

        confirm_button = discord.ui.Button(label="Confirm", style=discord.ButtonStyle.green)
        confirm_button.callback = self.confirm_callback

        cancel_button = discord.ui.Button(label="Cancel", style=discord.ButtonStyle.red)
        cancel_button.callback = self.cancel_callback

        self.add_item(discord.ui.TextDisplay(prompt))
        self.add_item(discord.ui.ActionRow(
            confirm_button,
            cancel_button
        ))

    async def confirm_callback(self, interaction):
        self.confirmed = True
        self.disable_all_items()
        await interaction.edit(view=self)
        self.stop()

    async def cancel_callback(self, interaction):
        self.confirmed = False
        self.disable_all_items()
        await interaction.edit(view=discord.ui.DesignerView(discord.ui.TextDisplay("Cancelled")))
        self.stop()
