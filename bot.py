import os
import discord
from discord import app_commands
import google.generativeai as genai

# 🔑 Defina suas chaves
DISCORD_TOKEN = "SEU_TOKEN_DISCORD"
GEMINI_API_KEY = "SUA_CHAVE_GEMINI"

# Configura Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Escolher modelo de imagens
model = genai.GenerativeModel("gemini-1.5-pro")

# Prompts fixos (resumidos)
PROMPTS = {
    "alunogrifinoria": """A 17-year-old male Hogwarts student from Gryffindor [...]""",
    "alunosonserina": """A 17-year-old male Hogwarts student from Slytherin [...]""",
    "alunoravenclaw": """A 17-year-old male Hogwarts student from Ravenclaw [...]""",
    "alunohufflepuff": """A 17-year-old male Hogwarts student from Hufflepuff [...]""",
    "alunoumbra": """A 17-year-old male Hogwarts student from House Umbra [...]""",
    "alunagrifinoria": """A 19-year-old female Hogwarts student from Gryffindor [...]""",
    "alunasonserina": """A 19-year-old female Hogwarts student from Slytherin [...]""",
    "alunacorvinal": """A 19-year-old female Hogwarts student from Ravenclaw [...]""",
    "alunalufa": """A 19-year-old female Hogwarts student from Hufflepuff [...]""",
    "alunaumbra": """A 19-year-old female Hogwarts student from House Umbra [...]""",
}

# Configuração do bot
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Bot conectado como {bot.user}")

# Criar comandos automáticos a partir do dicionário
for cmd, prompt in PROMPTS.items():
    @tree.command(name=cmd, description=f"Gera um {cmd}")
    async def generate(interaction: discord.Interaction, p=prompt):
        await interaction.response.defer()
        response = model.generate_content(p)
        # Gemini às vezes retorna link da imagem em `response`
        try:
            image_url = response.candidates[0].content.parts[0].text
            await interaction.followup.send(image_url)
        except Exception:
            await interaction.followup.send("⚠️ Não consegui gerar a imagem agora.")

bot.run(DISCORD_TOKEN)
