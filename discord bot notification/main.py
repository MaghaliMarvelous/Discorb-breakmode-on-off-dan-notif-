import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

# Set up bot nya
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

#breakmode dan channel ID kalian
breakmode = False
notification_channel_id = 1234567890

#Fungsi notfikasi untuk kasih suatu teks
async def send_notification():
    channel = bot.get_channel(notification_channel_id)
    if channel:
        await channel.send("Time for a break! Reminder sent.")
    else:
        print("Channel not found!")

#Command breakmode (!breakmode on/off)
@bot.command(name="breakmode")
async def toggle_breakmode(ctx):
    global breakmode
    breakmode = not breakmode
    status = "on" if breakmode else "off"
    await ctx.send(f"Breakmode is now {status}.")


@bot.command(name="sendnotif")
async def send_manual_notification(ctx):
    await send_notification()
    await ctx.send("Manual reminder sent!")

#notif setiap 1 jam
@tasks.loop(hours=1)
async def periodic_notification():
    if breakmode:
        await send_notification()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    periodic_notification.start()  


@bot.event
async def on_message(message):
    global breakmode

    
    if message.author == bot.user:
        return

    
    if breakmode:
       
        channel = message.channel
        await channel.send(f"{message.author.mention} is in breakmode! Reminder sent.")
        
    
    await bot.process_commands(message)

#Jalankan bot pake token kamu
bot.run('bot token kamu')
