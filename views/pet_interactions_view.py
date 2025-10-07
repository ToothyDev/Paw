import io

import aiohttp
import discord
from discord import File


class PetInteractionView(discord.ui.DesignerView):
    def __init__(self, ctx: discord.ApplicationContext, member: discord.Member, gif: File, action_error: str = None):
        self.ctx = ctx
        self.member = member
        self.gif = gif
        self.action_error = action_error
        self.disable_on_timeout = True
        self.original_allowed_mentions = discord.AllowedMentions(users=[member])

        self.interact_button = discord.ui.Button(label="Pet back!", style=discord.ButtonStyle.primary)
        self.interact_button.callback = self.button_callback

        components = [
            discord.ui.Container(
                discord.ui.TextDisplay(f"**{ctx.author.mention}** petted **" + member.mention + "**"),
                discord.ui.MediaGallery(discord.MediaGalleryItem(url="attachment://petpet.gif")),
                discord.ui.ActionRow(self.interact_button),
                color=discord.Color.blue()
            )
        ]

        super().__init__(timeout=600, *components)

    async def button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.member:
            await interaction.respond("You weren't petted!", ephemeral=True)
            return

        self.disable_all_items()
        await interaction.message.edit(view=self, allowed_mentions=self.original_allowed_mentions)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.some-random-api.com/premium/petpet?avatar={self.ctx.author.display_avatar.with_format('png').with_size(256).url}") as resp:
                gif_file = discord.File(io.BytesIO(await resp.read()), filename="petpet.gif")

        components = [
            discord.ui.Container(
                discord.ui.TextDisplay(f"**{self.member.mention}** pet **{self.ctx.author.mention}** back!!"),
                discord.ui.MediaGallery(
                    discord.MediaGalleryItem(
                        url="attachment://petpet.gif")
                ),
                color=discord.Color.blue()
            )
        ]

        view = discord.ui.DesignerView(*components)
        await interaction.respond(view=view, allowed_mentions=discord.AllowedMentions(users=[self.ctx.author]),
                                  file=gif_file)
