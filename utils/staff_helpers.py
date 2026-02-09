import zipfile

import aiohttp
import discord


class AssetDownloader:
    """ Helper class for downloading emojis, stickers and role icons """

    def __init__(self, zipped_f: zipfile.ZipFile, guild: discord.Guild, interaction: discord.Interaction):
        """ Initialize the AssetDownloader with a zip file, guild and interaction object """
        self.zipped_f = zipped_f
        self.guild = guild
        self.interaction = interaction

        self.current = 0
        self.last_percentage = 0
        self.total = len(guild.emojis) + len(guild.stickers) + len([role for role in guild.roles if role.icon])

    async def download_all(self):
        """ Download all emojis, stickers and role icons """
        await self.download_emojis()
        await self.download_stickers()
        await self.download_role_icons()

    async def download_emojis(self):
        """ Download all emojis in the server and save them in the provided zip file"""
        saved_emojis = []
        for emoji in self.guild.emojis:
            emoji_name = emoji.name if emoji.name not in saved_emojis else emoji.name + str(
                saved_emojis.count(emoji.name) + 1)
            self.zipped_f.writestr(f"emojis/{emoji_name + "." + emoji.extension}", await emoji.read())
            saved_emojis.append(emoji.name)
            await self._handle_percentage_update()

    async def download_stickers(self):
        """ Download all stickers in the server and save them in the provided zip file """
        saved_stickers = []
        async with aiohttp.ClientSession() as session:
            for sticker in self.guild.stickers:
                async with session.get(sticker.url) as response:
                    sticker_file_name = (sticker.name if sticker.name not in saved_stickers else sticker.name + str(
                        saved_stickers.count(sticker.name) + 1)) + ".png"
                    self.zipped_f.writestr(f"stickers/{sticker_file_name}", await response.read())
                    saved_stickers.append(sticker.name)
                    await self._handle_percentage_update()

    async def download_role_icons(self):
        """ Download all role icons in the server and save them in the provided zip file """
        saved_role_icons = []
        for role in self.guild.roles:
            if role.icon:
                role_icon_file_name = (role.name if role.name not in saved_role_icons else role.name + str(
                    saved_role_icons.count(role.name) + 1)) + ".png"
                self.zipped_f.writestr(f"role_icons/{role_icon_file_name.replace("/", " ")}", await role.icon.read())
                saved_role_icons.append(role.name)
                await self._handle_percentage_update()

    async def _handle_percentage_update(self):
        """ Handles counting the downloaded assets and updating the progress at every 10% downloaded"""
        self.current += 1
        current_percentage = (self.current * 100) // self.total
        if current_percentage % 10 == 0 and current_percentage != self.last_percentage:
            self.last_percentage = current_percentage
            await self.interaction.edit_original_response(
                content=f"Downloading, this might take some time... ({self.last_percentage}%)")
