
import os
import discord
from discord import app_commands
from deep_translator import GoogleTranslator

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

class TranslateBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.user_languages = {}

    async def on_ready(self):
        await self.tree.sync()
        print(f"✅ Bot is online as {self.user}")

bot = TranslateBot()

@bot.tree.command(name="language", description="Set your preferred language for translations.")
async def set_language(interaction: discord.Interaction, lang_code: str):
    bot.user_languages[str(interaction.user.id)] = lang_code
    await interaction.response.send_message(
        f"✅ Your preferred language has been set to **{lang_code}**.",
        ephemeral=True
    )

@bot.tree.command(name="disable_language", description="Disable automatic translations for you.")
async def disable_language(interaction: discord.Interaction):
    bot.user_languages.pop(str(interaction.user.id), None)
    await interaction.response.send_message(
        "❌ Automatic translations disabled for you.",
        ephemeral=True
    )

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    for user_id, target_lang in bot.user_languages.items():
        if str(message.author.id) != user_id:
            try:
                translated_text = GoogleTranslator(target=target_lang).translate(message.content)
                embed = discord.Embed(
                    title=f"🌐 Translated from {message.author.display_name}",
                    description=translated_text,
                    color=discord.Color.green()
                )
                embed.add_field(name="💬 Original Message", value=message.content, inline=False)
                await message.channel.send(embed=embed, ephemeral=True)
            except Exception as e:
                print(f"Translation error: {e}")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
