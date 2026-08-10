import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Scheduler
scheduler = AsyncIOScheduler()

def load_data():
    with open('questions.json', 'r') as f:
        questions = json.load(f)
    return questions

def load_state():
    try:
        with open('state.json', 'r') as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        state = {"index": 0}
        save_state(state)
    return state

def save_state(state):
    with open('state.json', 'w') as f:
        json.dump(state, f)

async def send_daily_question():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Error: Channel with ID {CHANNEL_ID} not found.")
        return

    questions = load_data()
    state = load_state()
    index = state.get("index", 0)

    if index >= len(questions):
        await channel.send("🎉 We have completed all the LeetCode questions in our list! Time to add more.")
        return

    question = questions[index]
    
    desc_text = question.get('description', '')
    embed = discord.Embed(
        title=f"Daily LeetCode Question: {question['title']}",
        url=question['url'],
        color=discord.Color.blue(),
        description=f"**Topic:** {question['topic']}\n\n{desc_text}\n\nGood luck! 🚀"
    )

    await channel.send(content="@everyone 🌅 Good morning! Here is your daily LeetCode challenge:", embed=embed)
    
    # Update state
    state["index"] = index + 1
    save_state(state)
    print(f"Sent question {index}: {question['title']}")

@bot.command(name='test')
async def test_command(ctx):
    """Manually trigger the daily question."""
    await send_daily_question()
    await ctx.send("Test complete!")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    
    # Schedule the task for 9:00 AM every day
    # You can adjust the timezone parameter in CronTrigger if needed. By default it uses local system time.
    scheduler.add_job(send_daily_question, CronTrigger(hour=9, minute=0))
    scheduler.start()
    print("Scheduler started. The bot will send a question daily at 9 AM.")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN is not set.")
    elif not CHANNEL_ID:
        print("Error: CHANNEL_ID is not set.")
    else:
        bot.run(TOKEN)
