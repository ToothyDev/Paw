import config
import random
import aiohttp
import discord


class Colors:
    blue = 0xadd8e6
    red = 0xf04747
    green = 0x90ee90
    orange = 0xfaa61a


async def interactions(ctx, members, name, error_name, giflist, reason=None, sra_url=None):
    image = ""

    if len(set(members)) == 0:
        return await ctx.send(f'You must specify the user to {error_name}!')
    if reason is not None:
        if len(reason) > 256:
            return await ctx.send(f'{config.crossmark} **You can only put max 256 characters in your reason.**')
    if sra_url is None:
        image = random.choice(giflist)
    else:
        api_random = random.choice(['normal', 'sra'])
        if api_random == 'normal':
            image = random.choice(giflist)
        elif api_random == 'sra':
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://some-random-api.ml/animu/{sra_url}') as r:
                    if r.status == 200:
                        js = await r.json()
                        image = js['link']
                    else:
                        image = random.choice(giflist)
    display_giflist = []
    for x in members:
        display_giflist.append(x.display_name)
    if len(members) >= 3:
        display_giflist.append(f"and {display_giflist.pop(-1)}")
    if len(members) == 2:
        display_giflist = f"{display_giflist[0]} and {display_giflist[1]}"
    else:
        display_giflist = ', '.join(display_giflist)
    embed = discord.Embed(
        description=f"**{ctx.author.display_name}** {name} **" + display_giflist + f"**\n{'' if reason is None else f'**Reason:** {reason}'}",
        color=discord.Color.blue())
    embed.set_thumbnail(url=image)
    await ctx.respond(embed=embed)


async def feelings(ctx, members, name, giflist):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_thumbnail(url=random.choice(giflist))
    if members is None:
        embed.description = f"**{ctx.author.display_name}** {name}!"
    else:
        display_giflist = []
        for x in members:
            display_giflist.append(x.display_name)
        if len(members) >= 3:
            display_giflist.append(f"and {display_giflist.pop(-1)}")
        if len(members) == 2:
            display_giflist = f"{display_giflist[0]} and {display_giflist[1]}"
        else:
            display_giflist = ', '.join(display_giflist)
        embed.description = f"**{ctx.author.display_name}** {name} because of **{display_giflist}**"
    await ctx.respond(embed=embed)
