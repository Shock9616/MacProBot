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
  - Searches AppleGamingWiki and retrieves all compatibility ratings for the
    searched game
- `/cxcheck <game name>`
  - Searches the CrossOver compatibility database and retrieves the current
    compatibility rating for the searched game
- `/define <term>`
  - Responds with a quick definition for one of a number of common Mac gaming
    related terms
- `/ev` (environment variables)
  - Lists common CrossOver bottle environment variables
- `/metalhud`
  - Lists some helpful utilities/instructions for the Metal HUD
- `/support`
  - Lists some common info that is helpful for troubleshooting issues with Mac
    gaming
- `/support1`
  - Gives some helpful tips for recording footage for troubleshooting
- `/updatedxmt`
  - Gives a link for the MacProTips tutorial for updating DXMT in CrossOver, and
    a link to download the latest version

### Admin/Mod Commands

- `/announce`
  - Send an announcement in the configured announcements channel

The bot also responds to pings and has a small chance to respond to any message
in the server with a snarky AI generated response
