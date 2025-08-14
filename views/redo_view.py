import discord


class ReRunView(discord.ui.View):
    """ Provides functionality to rerun any command using a cv2 view. Currently breaks at attempt 2
        :param ctx: The context of the command
        :param command_options: All options the command takes in the right order
        :param args: Any other args for the view
        :param kwargs: Any other kwargs for the view
    """

    def __init__(self, ctx: discord.ApplicationContext, command_options: list, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.ctx = ctx
        self.ctx_command = ctx.command
        self.command_args = command_options

        redo_button = discord.ui.Button(label="Run again", emoji="<:retry:1405584711979499560>",
                                        style=discord.ButtonStyle.secondary)
        redo_button.callback = self.redo

        args = list(args) + [redo_button]
        self.disable_on_timeout = True
        self.timeout = 600
        super().__init__(*args, **kwargs)

    async def redo(self, interaction: discord.Interaction):
        self.disable_all_items()
        await self.message.edit(view=self)

        self.ctx.interaction = interaction
        await self.ctx.invoke(self.ctx_command, *self.command_args)
