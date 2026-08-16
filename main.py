import os
import urllib.parse
import discord

# =========================
# Config
# =========================
WIKI_BASE_URL = "https://ship-community-valrus.fandom.com/wiki/"
WIKI_HOME_URL = "https://ship-community-valrus.fandom.com/wiki/Main_Page"
TRELLO_URL = "https://trello.com/b/B5pWgZ16/my-trello-board"

# Direct wiki routes (for !wiki <term>)
WIKI_ROUTES = {
    "main": "Main_Page",
    "home": "Main_Page",
    "enemies": "Enemies",
    "bosses": "Bosses",
    "factions": "Factions",
    "cannon": "Cannons",
    "cannons": "Cannons",
    "ships": "Ships",
    "islands": "Islands",
    "quests": "Quests",
    "resources": "Resources",
    "port_resources": "Port_Resources",
    "port resources": "Port_Resources",
    "cosmetics": "Cosmetics",
    "badges": "Badges",
}

# Auto-responder keywords (currently cannon-focused + easy to expand)
WIKI_KEYWORDS = {
    "cannon": {
        "title": "Cannons Wiki Page",
        "page": "Cannons",
        "description": "Info about cannons, builds, and references."
    },
    "cannons": {
        "title": "Cannons Wiki Page",
        "page": "Cannons",
        "description": "Info about cannons, builds, and references."
    },
}

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    def build_embed(self, title: str, url: str, description: str, color=0x5865F2):
        embed = discord.Embed(title=title, url=url, description=description, color=color)
        embed.set_footer(text="Polly Bot")
        return embed

    def wiki_url_for_query(self, query: str) -> str:
        if not query:
            return WIKI_HOME_URL

        raw = query.strip()
        page_part = raw
        anchor_part = ""

        # support !wiki cannons#section_name
        if "#" in raw:
            page_part, anchor_part = raw.split("#", 1)
            anchor_part = anchor_part.strip().replace(" ", "_")

        normalized = page_part.strip().lower()

        if normalized in WIKI_ROUTES:
            page = WIKI_ROUTES[normalized]
        else:
            # fallback: convert words to Wiki_Page_Format
            page = page_part.strip().replace(" ", "_")
            page = urllib.parse.quote(page, safe="_()'-")

        url = WIKI_BASE_URL + page

        if anchor_part:
            anchor = urllib.parse.quote(anchor_part, safe="_()-'")
            url += f"#{anchor}"

        return url

    def find_wiki_keyword(self, content: str):
        text = content.lower()
        for keyword, data in WIKI_KEYWORDS.items():
            if keyword in text:
                return keyword, data
        return None, None

    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.strip()

        # !wiki command router
        if content.lower().startswith("!wiki"):
            parts = content.split(" ", 1)
            query = parts[1] if len(parts) > 1 else ""
            url = self.wiki_url_for_query(query)

            title = "Wiki Home" if not query else "Wiki Link"
            description = "Main wiki page." if not query else f"Direct link for: `{query}`"

            embed = self.build_embed(title=title, url=url, description=description, color=0x5865F2)
            await message.channel.send(embed=embed)
            return

        # !trello simple command
        if content.lower().startswith("!trello"):
            embed = self.build_embed(
                title="Trello Board",
                url=TRELLO_URL,
                description="Project board and roadmap.",
                color=0x1D9BF0
            )
            await message.channel.send(embed=embed)
            return

        # Wiki keyword auto-responder (currently cannon/cannons)
        keyword, data = self.find_wiki_keyword(content)
        if keyword:
            url = WIKI_BASE_URL + urllib.parse.quote(data["page"].replace(" ", "_"), safe="_()'-")
            embed = self.build_embed(
                title=data["title"],
                url=url,
                description=f"{data['description']}\n\nMatched keyword: `{keyword}`",
                color=0x2ECC71
            )
            await message.channel.send(embed=embed)
            return


intents = discord.Intents.default()
intents.message

client = Client(intents=intents)
client.run(os.environ["DISCORD_TOKEN"])