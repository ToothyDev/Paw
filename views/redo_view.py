import discord


class RedoView(discord.ui.View):
    def __init__(self, ctx: discord.ApplicationContext, command_args: list, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.ctx = ctx
        self.ctx_command = ctx.command
        self.command_args = command_args

        redo_button = discord.ui.Button(label="Redo", style=discord.ButtonStyle.secondary)
        redo_button.callback = self.redo

        args = list(args) + [redo_button]
        super().__init__(*args, **kwargs)

    async def redo(self, interaction: discord.Interaction):
        self.ctx.interaction = interaction
        await self.ctx.invoke(self.ctx_command, *self.command_args)
