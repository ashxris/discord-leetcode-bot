# Discord LeetCode Bot

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2)

A Discord bot that posts a daily LeetCode challenge in your server. It walks through 90 curated problems (5 per topic, 18 topics) in a sensible order, so your community can grind consistently without deciding what to solve next.

## Features

- Sends one LeetCode question per day at **9:00 AM IST** (configurable)
- 90 questions across 18 topics, from Arrays & Hashing to Math & Geometry
- Each post includes the topic, a short description, and a hint
- Tracks progress in `state.json`, so it always posts the next question
- `!test` command to trigger a post immediately
- Questions are fully editable in `questions.json`

## Tech Stack

- [discord.py](https://github.com/Rapptz/discord.py) for the bot
- [APScheduler](https://apscheduler.readthedocs.io/) for the daily schedule
- [python-dotenv](https://github.com/theskumar/python-dotenv) for configuration

## Prerequisites

- Python 3.8 or newer
- A Discord account and a server where you have permission to add bots
- A Discord application with a bot token (created below)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ashxris/discord-leetcode-bot.git
cd discord-leetcode-bot
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows, use `venv\Scripts\activate` instead.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the Discord bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Open the **Bot** tab and click **Reset Token**, then copy the token. Keep it secret.
3. On the same page, scroll to **Privileged Gateway Intents** and enable **Message Content Intent**. The bot will not receive commands without it.
4. Go to **OAuth2 > URL Generator**, select the `bot` scope and the `Send Messages`, `Embed Links`, and `Mention Everyone` permissions.
5. Open the generated URL and invite the bot to your server.

### 5. Get your channel ID

1. In Discord, go to **User Settings > Advanced** and enable **Developer Mode**.
2. Right-click the channel where you want daily questions and click **Copy Channel ID**.

### 6. Configure the environment

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_bot_token_here
CHANNEL_ID=your_channel_id_here
```

### 7. Run the bot

```bash
python bot.py
```

You should see `Logged in as <bot name>` and `Scheduler started` in the console. The first question goes out at the next 9:00 AM IST.

## Usage

| Command | Description |
| --- | --- |
| `!test` | Posts the next question immediately and advances the schedule |

The bot also posts automatically every day at **9:00 AM IST**, mentioning `@everyone` with an embed containing the question's title, topic, description, and a link to the problem.

## Configuration

- **Schedule time**: edit the `CronTrigger` in `on_ready` in `bot.py`:

  ```python
  scheduler.add_job(send_daily_question, CronTrigger(hour=9, minute=0, timezone='Asia/Kolkata'))
  ```

  Change `hour`, `minute`, or `timezone` to match your server's schedule.

- **Channel**: update `CHANNEL_ID` in `.env`.
- **Questions**: edit `questions.json`. Each entry looks like:

  ```json
  {
    "topic": "Arrays & Hashing",
    "title": "Two Sum",
    "url": "https://leetcode.com/problems/two-sum/",
    "description": "Short problem summary and a hint."
  }
  ```

- **Reset progress**: stop the bot, delete `state.json`, and start it again. The bot recreates the file and begins from the first question.

## Project Structure

```
discord-leetcode-bot/
|-- bot.py                 # Bot setup, scheduler, and commands
|-- questions.json         # The 90-question curriculum
|-- state.json             # Progress tracker (generated, not committed)
|-- add_descriptions.py    # One-time helper to add descriptions to questions
|-- update_urls.py         # One-time helper to regenerate problem URLs
|-- requirements.txt
|-- .env                   # Your secrets (not committed)
|-- .gitignore
```

## Helper Scripts

These were used to build `questions.json` and are safe to ignore during normal use:

- `add_descriptions.py` adds a short description to every question.
- `update_urls.py` regenerates each LeetCode URL from the question title.

## Troubleshooting

- **`PrivilegedIntentsRequired` on startup**: enable **Message Content Intent** in the Developer Portal under **Bot > Privileged Gateway Intents**.
- **`Error: Channel with ID ... not found`**: double-check `CHANNEL_ID`, and make sure the bot is in the same server as the channel.
- **`Error: DISCORD_TOKEN is not set`**: make sure `.env` exists in the project root and contains `DISCORD_TOKEN`.
- **The bot never posts**: the schedule is 9:00 AM IST. Use `!test` to verify the bot works, and check that the process stays running.
