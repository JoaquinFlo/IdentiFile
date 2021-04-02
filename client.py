import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()

CMD_PREFIX = os.getenv('CMD_PREFIX')
client = commands.Bot(command_prefix=CMD_PREFIX, help_command=None)
enabled = True

def code_format(message: str):
    return '```\n' + message + '\n```'

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if len(message.attachments) < 1 or not enabled:
        await client.process_commands(message)
        return
    else:
        attachment = message.attachments[0]
        file_name = attachment.filename
        file_extension = file_name.split('.')[1]

        if file_extension != 'txt':
            return
        file_content = await attachment.read()
        encoding = 'utf-8'
        file_content = file_content.decode(encoding)
        file_char_count = len(file_content)
        char_limit = 1992  # + 6 backticks and 2 line breaks (for code formatting) = 2000 characters per message

        if file_name == 'message.txt' and file_char_count >= char_limit:
            for i in range(0, file_char_count, char_limit):
                start = i
                end = i + char_limit
                msg = code_format(file_content[start:end])
                await message.channel.send(msg)
        else:
            if file_char_count >= char_limit:
                msg = code_format(file_content[:file_char_count - char_limit])
                await message.channel.send(msg)
            else:
                msg = code_format(file_content)
                await message.channel.send(msg)
    await client.process_commands(message)

@client.command()
async def enable(ctx):
    global enabled
    enabled = True
    await ctx.send('`Bot is Enabled` :unlock:')

@client.command()
async def disable(ctx):
    global enabled
    enabled = False
    await ctx.send('`Bot is Disabled` :lock:')

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title='Help',
        color=0x3792cb
    )
    embed.add_field(name=f'Enable', value=f'`{CMD_PREFIX}enable`', inline=True)
    embed.add_field(name=f'Disable', value=f'`{CMD_PREFIX}disable`', inline=True)
    embed.add_field(name='Help', value=f'`{CMD_PREFIX}help`', inline=True)
    embed.add_field(name='About', value=f'`{CMD_PREFIX}about`', inline=False)

    await ctx.send(embed=embed)

@client.command()
async def about(ctx):
    description = os.getenv('DESCRIPTION')
    msg = code_format(description)
    await ctx.send(msg)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(code_format('That command does not exist'))
    else:
        print('Ignoring exception in command')

if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    client.run(TOKEN)
