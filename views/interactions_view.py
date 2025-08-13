import random

import discord


class InteractionsView(discord.ui.View):
    def __init__(self, ctx, members, action, button_label, giflist, action_error=None):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.members = members
        self.action = action
        self.giflist = giflist
        self.action_error = action_error
        self.button_callback.label = f"{button_label} back!"
        self.disable_on_timeout = True

    @discord.ui.button(style=discord.ButtonStyle.primary)
    async def button_callback(self, _, interaction: discord.Interaction):
        if interaction.user not in self.members:
            if not self.action_error:
                await interaction.respond(f"You weren't {self.action}!", ephemeral=True)
                return
            await interaction.respond(f"You weren't {self.action_error}!", ephemeral=True)
            return
        self.members.remove(interaction.user)
        if len(self.members) == 0:
            self.disable_all_items()
            await interaction.message.edit(view=self)
        image = random.choice(self.giflist)
        embed = discord.Embed(
            description=f"**{interaction.user.display_name}** {self.action} **" + self.ctx.author.display_name + "** back!",
            color=discord.Color.blue())
        embed.set_image(url=image)
        await interaction.respond(embed=embed)
