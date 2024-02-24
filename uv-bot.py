import discord
from discord.ext import commands
from discord import app_commands
import json
import re
from datetime import datetime
import tempfile
from io import BytesIO

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
@app_commands.describe(texte="Le message à envoyer", salon_textuel="Lien du salon textuel")
async def say(interaction: discord.Interaction, texte: str, salon_textuel: discord.TextChannel = None):
    if salon_textuel is not None:  
                await salon_textuel.send(texte)
                embed = discord.Embed(description=f"✅** Bravo!｜**" + "Message envoyé sur " + salon_textuel.jump_url , color=discord.Color.green())
                await interaction.response.send_message(embed=embed)
    else:
            erreur = "Le salon textuel n'existe pas."
            embed = discord.Embed(description=f"❌** Erreur｜**" + f"{erreur}" , color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        

@bot.tree.command(name="avatar",description="Affiche l'avatar d'un utilisateur.")
@app_commands.describe(utilisateur="L'utilisateur dont vous voulez connaitre l'avatar")
async def avatar(interaction: discord.Interaction,  utilisateur: discord.Member ):
    embed = discord.Embed(title=f"Avatar de {utilisateur.display_name}",  color=discord.Color.from_rgb(193,168,233) )
    embed.set_image(url=utilisateur.avatar)
    
    download_link = f"[__Lien de l'image__]({utilisateur.avatar})"
    embed.add_field(name="", value=download_link)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="profileavatar",description="Affiche l'avatar de profil d'un utilisateur.")
@app_commands.describe(utilisateur="L'utilisateur dont vous voulez connaitre l'avatar")
async def profileavatar(interaction: discord.Interaction,  utilisateur: discord.Member ):
    embed = discord.Embed(title=f"Avatar de {utilisateur.display_name}",  color=discord.Color.from_rgb(193,168,233) )
    embed.set_image(url=utilisateur.display_avatar)
    
    download_link = f"[__Lien de l'image__]({utilisateur.display_avatar})"
    embed.add_field(name="", value=download_link)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="servericon",description="Affiche l'icône du serveur actuel.")
async def servericon(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    guild = bot.get_guild(guild_id)
    embed = discord.Embed(title=f"Icône du serveur {guild}",  color=discord.Color.from_rgb(193,168,233) )
    embed.set_image(url=guild.icon.url)
    download_link = f"[__Lien de l'image__]({guild.icon})"
    embed.add_field(name="", value=download_link)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help",description="Affiche des informations concernant [uv]bot.")
async def help(interaction: discord.Interaction):
 
    embed = discord.Embed(title="[uv]bot", description="[uv]bot est un bot discord crée exclusivement pour le serveur ultraviolet et présente de nombreuses fonctionnalitées essentielles. \n\n La liste des commandes et fonctionnalitées est affiché sur le projet Github.", color=discord.Color.from_rgb(193,168,233))
    view = discord.ui.View() # Establish an instance of the discord.ui.View class
    style = discord.ButtonStyle.grey  # The button will be gray in color
    item = discord.ui.Button(style=style, label="Github", url="https://github.com/dxnuv/uv-bot")  # Create an item to pass into the view class.
    view.add_item(item=item)  # Add that item into the view class
    await interaction.response.send_message(embed=embed,view=view)


    
@bot.tree.command(name="loveletter",description="Dévoile l'amour que tu portes envers une personne de ce serveur.")
@app_commands.describe(utilisateur="L'utilisateur dont vous voulez connaitre l'avatar", message="Le message que vous voulez envoyer à votre cutie lover", anonyme="Afichage (ou non) de votre pseudo")
async def loveletter(interaction: discord.Interaction, utilisateur: discord.Member , message: str, anonyme: bool = False):
    guild_id = interaction.guild_id
    guild = bot.get_guild(guild_id)
    
    embed = discord.Embed(title=f"💌 Un membre du serveur {guild} vous a envoyé une lettre d'amour...", color=discord.Color.from_rgb(242, 80, 83))
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Cher,", value=utilisateur.mention, inline=False)
    embed.add_field(name="Message :", value=message, inline=False)
    if anonyme:
        embed.add_field(name="Signé, ", value="pookie bear anonyme 🥰")
    else:
        embed.add_field(name="Signé, ", value=interaction.user.mention + " 🥰")
        # Envoyer l'embed par message privé à l'utilisateur
        await utilisateur.send(embed=embed)
        embed = discord.Embed(description=f"✅** Bravo!｜**" + "💌 Lettre d'amour envoyé à " + utilisateur.mention , color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
@bot.tree.command(name="archive", description="Archive un salon textuel.")
@app_commands.describe(salon_textuel="Lien du salon textuel")
async def archive(interaction: discord.Interaction, salon_textuel: discord.TextChannel):

    if interaction.user.guild_permissions.administrator:
         # Retirer les caractères spéciaux du nom du salon
         nom_salon_archives = re.sub(r'[^\w\s-]', '', salon_textuel.name)
    # Générer la date actuelle au format DD-MM-YY
         date_formattee = datetime.now().strftime("%d-%m-%y")
    # Créer le nouveau nom du salon d'archives
         nom_salon_archives += f"-{date_formattee}"
         categorie_archives = discord.utils.get(interaction.guild.categories, name="📦 archives")

         if categorie_archives is None:
             erreur = "La catégorie '📦 archives' n'a pas été trouvée."
             embed = discord.Embed(description=f"❌** Erreur｜**" + f"{erreur}" , color=discord.Color.red())
             await interaction.response.send_message(embed=embed, ephemeral=True)
         else:
              # Déplacer le salon textuel vers la catégorie "ARCHIVES"
             await salon_textuel.edit(category=categorie_archives)

             salon_textuel_og = salon_textuel.name
         # Renommer le salon textuel avec le nouveau nom d'archives
             await salon_textuel.edit(name=nom_salon_archives)

         # Placer le salon textuel en haut de la liste des salons de la catégorie "ARCHIVES"
             await salon_textuel.edit(position=0)

             embed = discord.Embed(description=f"✅** Bravo!｜**" + f"Le salon textuel '{salon_textuel_og}' a été archivé avec succès." , color=discord.Color.green())
             await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
            erreur = "Vous n'avez pas les permissions requises pour éxécuter cette commande."
            embed = discord.Embed(description=f"❌** Erreur｜**" + f"{erreur}" , color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    
@bot.tree.command(name="lock",description="Désactive un salon textuel.")
@app_commands.describe(salon_textuel="Le salon que vous souhaitez désactiver")
async def lock(interaction: discord.Interaction, salon_textuel: discord.TextChannel = None):
     if interaction.user.guild_permissions.administrator:
          if salon_textuel is None:
                await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
                embed = discord.Embed(description=f"✅** Bravo!｜**" + f"Le salon textuel {interaction.channel.jump_url} a été désactivé avec succès." , color=discord.Color.green())
                await interaction.response.send_message(embed=embed)
          else:
               await salon_textuel.set_permissions(interaction.guild.default_role, send_messages=False)
               embed = discord.Embed(description=f"✅** Bravo!｜**" + f"Le salon textuel {salon_textuel.jump_url} a été désactivé avec succès." , color=discord.Color.green())
               await interaction.response.send_message(embed=embed)


     else:
             erreur = "Vous n'avez pas les permissions requises pour éxécuter cette commande."
             embed = discord.Embed(description=f"❌** Erreur｜**" + f"{erreur}" , color=discord.Color.red())
             await interaction.response.send_message(embed=embed, ephemeral=True)    

@bot.tree.command(name="unlock",description="Réactive un salon textuel désactivé.")
@app_commands.describe(salon_textuel="Le salon que vous souhaitez réactiver")
async def unlock(interaction: discord.Interaction, salon_textuel: discord.TextChannel = None):
     if interaction.user.guild_permissions.administrator:
          if salon_textuel is None:
                await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
                embed = discord.Embed(description=f"✅** Bravo!｜**" + f"Le salon textuel {interaction.channel.jump_url} a été réactivé avec succès." , color=discord.Color.green())
                await interaction.response.send_message(embed=embed)
          else:
               await salon_textuel.set_permissions(interaction.guild.default_role, send_messages=True)
               embed = discord.Embed(description=f"✅** Bravo!｜**" + f"Le salon textuel {salon_textuel.jump_url} a été réactivé avec succès." , color=discord.Color.green())
               await interaction.response.send_message(embed=embed)


     else:
             erreur = "Vous n'avez pas les permissions requises pour éxécuter cette commande."
             embed = discord.Embed(description=f"❌** Erreur｜**" + f"{erreur}" , color=discord.Color.red())
             await interaction.response.send_message(embed=embed, ephemeral=True)    




with open('config.json', encoding="utf-8", errors="ignore") as f:
    data = json.load(f)
    token = data["token"]
bot.run(token)
