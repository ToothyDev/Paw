# Introduction

Paw is the open-source GitHub repository for Paw, the discord bot powering [The Paw Kingdom](https://discord.gg/tpk)!

Paw was built on code from a former project known as [exorium](https://github.com/MiataBoy/exorium) by current developers MiataBoy and ToothyDev.

# Functionalities
Paw can provide a variety of things to your server! For example:

😘 interaction commands!

🐕 Sona generators!

# Self-hosting
Paw is self-hosted with ease, as it was made to be minimal and compact.

1. Create a bot account on https://discord.com/developers/applications
2. Invite the bot with oauth scopes `bot` and `application.commands` to a guild of choice
3. clone this repository onto a server (If you don't have one, you may find VPS's for cheap at https://ovh.com) with `git clone https://github.com/MiataBoy/Paw.git`
4. Make sure Python 3.11+ is installed
5. Run `pip install -r requirements.txt`
6. Use PM2 or a similar tool to run the bot (`pm2 start bot.py --name Paw --interpreter python3`)

#### ⚠ **We will not provide further support with self-hosting.** ⚠
**Joining TPK with the sole intent of requesting support with self-hosting may result in a ban.**