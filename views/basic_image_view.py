import discord


class BasicImageView(discord.ui.View):
    def __init__(self, image_url: str, *args, **kwargs):
        components = [
            discord.ui.Container(
                discord.ui.MediaGallery(
                    discord.MediaGalleryItem(url=image_url)
                ),
                color=discord.Color.random()
            )
        ]

        super().__init__(*components, *args, **kwargs)
