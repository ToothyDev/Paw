import discord


class ReRunView(discord.ui.View):
    """ Provides functionality to rerun any command using a cv2 view. Currently breaks at attempt 2
        :param ctx: The context of the command
        :param command_options: All options the command takes in the right order
        :param args: Any other args for the view
        :param kwargs: Any other kwargs for the view
    """

    def __init__(self, ctx: discord.ApplicationContext, command_options: list, *args, **kwargs):
        redo_button = discord.ui.Button(label="Run again", emoji="<:retry:1405584711979499560>",
                                        style=discord.ButtonStyle.secondary)

        redo_button.callback = self.redo
        self.ctx = ctx
        self.ctx_command = ctx.command
        self.command_args = command_options
        self.view_args = list(args) + [redo_button]

        super().__init__(timeout=600, *self.view_args, **kwargs)
        self.disable_on_timeout = True

    async def redo(self, interaction: discord.Interaction):
        self.disable_all_items()
        await self.message.edit(view=self)

        self.ctx.interaction = interaction
        self.ctx.command = self.ctx_command
        await self.ctx.invoke(self.ctx_command, *self.command_args)
