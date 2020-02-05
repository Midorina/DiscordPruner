from discord.ext import commands
import asyncio
import logging
import json

with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=config['prefix'])

logging.basicConfig(level=logging.INFO)


@bot.command()
async def prune(ctx):
    if ctx.author.id == config['owner_id']:
        for member in ctx.guild.members:
            if not member.bot and member.id not in config['whitelisted_member_ids']:
                msg = await ctx.send(f"Kicking {str(member)}...")
                counter = 0
                while counter < 3:
                    try:
                        await member.kick(reason="Server prune.")
                        await msg.edit(content=f"Kicking {str(member)}... **Success!**")
                        await asyncio.sleep(1.0)
                        break

                    except Exception as e:
                        print(f"Failed to kick {str(member)}.")
                        print(e)
                        print("Trying again...")
                        counter += 1
                        continue

bot.run(config['bot_token'])
