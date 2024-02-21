import discord
from discord.ext import commands
from discord import app_commands
import json
import re

# Définir les intentions de votre bot
intents = discord.Intents.default()
intents.messages = True  # Activer les intentions liées aux messages
intents.message_content = True  # Activer les intentions liées aux messages
intents.presences = True

# Initialiser le bot avec les intentions
bot = commands.Bot(command_prefix='uv!', intents=intents)

# Événement pour détecter quand le bot est prêt
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    
# Événement pour détecter les messages entrants
@bot.event
async def on_message(message):
    # Vérifier si le message contient exactement "y/n" en tant que mot distinct
    if "y/n" in message.content:
        # Répondre "Bonjour!"
        # Ajouter une réaction avec l'emoji vers le haut (flèche)
        await message.add_reaction('⬆️')
        # Ajouter une réaction avec l'emoji vers le bas
        await message.add_reaction('⬇️')
    
    # Toujours nécessaire pour gérer les autres événements de message
    await bot.process_commands(message)

@bot.tree.command(name="uvmcsmp",description="Présente des informations sur l'event [uv]mcsmp.")
async def smp(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} https://discord.gg/D2peqCa4vA?event=1207816940626771968")

@bot.tree.command(name="say", description="Envoie un message personnalisé sur un salon textuel.")
@app_commands.describe(texte="Que devrais-je dire ?", salon_url="Lien du salon textuel (facultatif)")
async def say(interaction: discord.Interaction, texte: str, salon_url: str = None):
    if salon_url is not None:  # Vérifier si salon_url est non nul
        match = re.match(r'<#(\d+)>', salon_url)
        if match:
            cleaned_link = salon_url.replace('<', '').replace('#', '').replace('>', '')
            channel_id = cleaned_link
        else:
            channel_id = salon_url.split('/')[-1]

        try:
            # Tentative de conversion de channel_id en entier
            channel_id_int = int(channel_id)
            # Vérification si channel_id_int est un ID de canal valide
            channel = interaction.guild.get_channel(channel_id_int)
            if channel:
                await channel.send(texte)
                await interaction.response.send_message("Message envoyé sur " + salon_url)
            else:
                erreur = "Le salon spécifié n'existe pas."
                embed = discord.Embed(description="❌ Error ｜" + f"`{erreur}`" , color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            # Si la conversion de channel_id en entier échoue, cela signifie que le lien du salon n'est pas valide
            erreur = "Le lien du salon textuel n'est pas valide."
            embed = discord.Embed(description="❌ Error ｜" + f"`{erreur}`" , color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(texte)
        await interaction.response.send_message("Message envoyé sur " + salon_url)

@bot.tree.command(name="avatar",description="Affiche l'avatar d'un utilisateur.")
async def smp(interaction: discord.Interaction,  utilisateur: discord.Member ):
    embed = discord.Embed(title=f"Avatar de {utilisateur.display_name}",  color=discord.Color.from_rgb(193,168,233) )
    embed.set_image(url=utilisateur.avatar)
    
    download_link = f"[__Lien de l'image__]({utilisateur.avatar})"
    embed.add_field(name="", value=download_link)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="profileavatar",description="Affiche l'avatar de profil d'un utilisateur.")
async def smp(interaction: discord.Interaction,  utilisateur: discord.Member ):
    embed = discord.Embed(title=f"Avatar de {utilisateur.display_name}",  color=discord.Color.from_rgb(193,168,233) )
    embed.set_image(url=utilisateur.display_avatar)
    
    download_link = f"[__Lien de l'image__]({utilisateur.display_avatar})"
    embed.add_field(name="", value=download_link)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="servericon",description="Affiche l'icône du serveur actuel.")
async def smp(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    guild = bot.get_guild(guild_id)
    embed = discord.Embed(title=f"Icône du serveur {guild}",  color=discord.Color.from_rgb(193,168,233) )
    embed.set_image(url=guild.icon.url)
    download_link = f"[__Lien de l'image__]({guild.icon})"
    embed.add_field(name="", value=download_link)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help",description="Affiche des informations concernant [uv]bot")
async def help(interaction: discord.Interaction):
 
    embed = discord.Embed(title="[uv]bot", description="[uv]bot est un bot discord crée exclusivement pour le serveur ultraviolet et présente de nombreuses fonctionnalitées essentielles. \n\n La liste des commandes et fonctionnalitées est affiché sur le projet Github.", color=discord.Color.from_rgb(193,168,233))
    view = discord.ui.View() # Establish an instance of the discord.ui.View class
    style = discord.ButtonStyle.grey  # The button will be gray in color
    item = discord.ui.Button(style=style, label="Github", url="https://github.com/dxnuv/uv-bot")  # Create an item to pass into the view class.
    view.add_item(item=item)  # Add that item into the view class
    await interaction.response.send_message(embed=embed,view=view)

    

with open('config.json') as f:
    data = json.load(f)
    token = data["token"]
bot.run(token)
