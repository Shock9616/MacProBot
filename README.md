# MacProBot

The official discord bot for the Mac Gaming discord server hosted by MacProTips!

## Deployment

This bot is deployed on [PythonAnywhere](https://www.pythonanywhere.com), but
can easily be deployed on any hosting service that supports Python

## Available Commands

This is only the list of currently available commands. More features are in the
works and will be added in the future.

### Standard Commands

- `/agwcheck <game name>`
  - Get the compatibility ratings for the searched game from
    [AppleGamingWiki](https://www.applegamingwiki.com/wiki/Home)
- `/cxcheck <game name>`
  - Get the searched game's star rating on the CrossOver
    [Compatibility Database](https://www.codeweavers.com/compatibility)
- `/define <term>`
  - Get a definition from a glossary of Mac gaming related terms
- `/metalhud`
  - Instructions for setting up the Metal HUD toolbar shortcut
- `/screenrecord`
  - Quick instructions for how to record your mac's screen
- `/sikarugir`
  - Useful links for learning about
    [Sikarugir](https://github.com/Sikarugir-App/Sikarugir)
- `/support`
  - A quick form to fill out to help with game troubleshooting gaming
- `/updatedxmt`
  - Link to a quick tutorial on how to update DXMT in CrossOver
- `/wallpaper`
  - Randomly select a wallpaper from the #wallpapers channel

### Admin/Mod Commands

- `/announce`
  - Send an announcement in the configured announcements channel

The bot also responds to pings and has a small chance to respond to any message
in the server with a snarky AI generated response

## Running For Yourself

This bot is entirely focused on being useful for MacProTips' "Mac Gaming"
discord server, but if you find yourself wanting to try it for yourself, here's
how to do it:

1. Clone this repository

```bash
git clone https://github.com/Shock9616/MacProBot
```

2. Create and activate virtual environment in repository root (optional but
   _HIGHLY_ recommended)

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create necessary environment variables in a file called `.env` in the root of
   the repository with the following contents (replace `<>` with required
   value):

```
TOKEN = <DISCORD_BOT_TOKEN>
AI_API_KEY = <OPENROUTER_API_KEY>
ANNOUNCEMENTS_CHANNEL_ID = <1234567890>
MOD_CHANNEL_ID = <1234567890>
WALLPAPERS_CHANNEL_ID = <1234567890>
```

- `TOKEN` is the secret key that is used to connect to discord. To get this
  token, you need to create an application on the
  [Discord Developer Portal](https://discord.com/developers/applications)
- `AI_API_KEY` Is used to connect to an LLM on OpenRouter for unprompted
  responses. This is not necessary to run the bot, but the AI responses will not
  work without it
- `ANNOUNCEMENTS_CHANNEL_ID`, `MOD_CHANNEL_ID`, and `WALLPAPERS_CHANNEL_ID` are
  the unique identifiers for the channels used for the `/announce` and
  `/wallpaper` commands. These aren't necessary to run the bot, but the commands
  won't work without them

5. Run the bot

```bash
python main.py
```
