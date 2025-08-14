import random

import discord


class InteractionsView(discord.ui.View):
    def __init__(self, ctx: discord.ApplicationContext, members: list[discord.Member], action: str, button_label: str,
                 giflist: list[str], action_error: str = None):
        self.ctx = ctx
        self.members = members
        self.action = action
        self.giflist = giflist
        self.action_error = action_error
        self.disable_on_timeout = True
        self.original_allowed_mentions = discord.AllowedMentions(users=members)

        self.interact_button = discord.ui.Button(label=f"{button_label} back!", style=discord.ButtonStyle.primary)
        self.interact_button.callback = self.button_callback

        memberlist = [member.mention for member in members]
        if len(members) >= 3:
            memberlist.append(f"**and **{memberlist.pop()}")
        if len(members) == 2:
            memberlist = f"{memberlist[0]}** and **{memberlist[1]}"
        else:
            memberlist = ', '.join(memberlist)

        components = [
            discord.ui.Container(
                discord.ui.TextDisplay(f"**{ctx.author.mention}** {action} **" + memberlist + "**"),
                discord.ui.MediaGallery(discord.MediaGalleryItem(url=random.choice(giflist))),
                self.interact_button,
                color=discord.Color.blue()
            )
        ]

        super().__init__(timeout=600, *components)

    async def button_callback(self, interaction: discord.Interaction):
        if interaction.user not in self.members:
            if not self.action_error:
                await interaction.respond(f"You weren't {self.action}!", ephemeral=True)
                return
            await interaction.respond(f"You weren't {self.action_error}!", ephemeral=True)
            return
        self.members.remove(interaction.user)
        if len(self.members) == 0:
            self.disable_all_items()
            await interaction.message.edit(view=self, allowed_mentions=self.original_allowed_mentions)

        components = [
            discord.ui.Container(
                discord.ui.TextDisplay(
                    f"**{interaction.user.mention}** {self.action} **" + self.ctx.author.mention + "** back!"),
                discord.ui.MediaGallery(discord.MediaGalleryItem(url=random.choice(self.giflist))),
                color=discord.Color.blue()
            )
        ]
        view = discord.ui.View(*components)
        await interaction.respond(view=view, allowed_mentions=discord.AllowedMentions(users=[self.ctx.author]))
