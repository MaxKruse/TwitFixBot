import youtube_dl
import json
import re
import os
from datetime import date


import discord

client = discord.Client()

pathregex = re.compile("https://twitter.com/\\w{1,15}\\/(status|statuses)\\/\\d{2,20}")
generate_embed_user_agents = [
    "facebookexternalhit/1.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 10.0; en-US; Valve Steam Client/default/1596241936; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 10.0; en-US; Valve Steam Client/default/0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.4 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.4 facebookexternalhit/1.1 Facebot Twitterbot/1.0", 
    "facebookexternalhit/1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; Valve Steam FriendsUI Tenfoot/0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36", 
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0", 
    "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)", 
    "TelegramBot (like TwitterBot)", 
    "Mozilla/5.0 (compatible; January/1.0; +https://gitlab.insrt.uk/revolt/january)", 
    "test"]

# Read config from config.json. If it does not exist, create new.
if not os.path.exists("config.json"):
    with open("config.json", "w") as outfile:
        default_config = {
            "discord": {
                "token": "[discord token goes here]"
            }
        }
        json.dump(default_config, outfile, indent=4, sort_keys=True)

    config = default_config
else:
    f = open("config.json")
    config = json.load(f)
    f.close()


def isTwitterVideoLink(link: str):
    isTwitterLink = pathregex.findall(link)
    print(isTwitterLink)

    if not isTwitterLink:
        return False

    try:
        # check if this is a twitter video or gif link
        with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(link, download=False)

            if info["ext"] == "mp4" or info["ext"] == "webm" or info["ext"] == "gif":
                return True

    except:
        return False

def getTwitterEmbed(link: str):

    # check if this is a twitter video or gif link
    with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(link, download=False)
    
    return f'<{link}>\r\n{info["url"]}'


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    # check if we got mentioned
    if not client.user.mentioned_in(message):
        return

    # format the message's content to only be the link
    link = message.content.replace("<@{}>".format(client.user.id), "")
    link = link.replace(" ", "")

    print(link)

    if isTwitterVideoLink(link):
        # try deleting the original message
        try:
            await message.delete()
        except:
            pass

        await message.channel.send(getTwitterEmbed(link=link))

if __name__ == "__main__":
    print("Starting bot...")
    print("Invite link:")
    print("https://discord.com/api/oauth2/authorize?client_id=866363946440065035&permissions=108544&scope=bot")
    client.run(config['discord']['token'])
