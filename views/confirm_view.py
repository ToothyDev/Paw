import discord


class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.confirmed = False
        self.disable_on_timeout = True

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, _, interaction):
        self.confirmed = True
        self.disable_all_items()
        await interaction.edit(view=self)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, _, interaction):
        self.confirmed = False
        self.disable_all_items()
        await interaction.edit(content="Cancelled", view=None)
        self.stop()
