import discord
from discord.ext import commands
from discord import app_commands
from googletrans import Translator
from datetime import datetime
import json
import re

intents = discord.Intents.default()
intents.messages = True  
intents.message_content = True  
intents.members = True
intents.presences = True


bot = commands.Bot(command_prefix='uv!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/help｜ultraviolet [uv]'))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
        
@bot.event
async def on_message(message):
    if "y/n" in message.content:
        await message.add_reaction('⬆️')
        await message.add_reaction('⬇️')

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
    view = discord.ui.View() 
    style = discord.ButtonStyle.grey 
    item = discord.ui.Button(style=style, label="Github", url="https://github.com/dxnuv/uv-bot")  
    view.add_item(item=item)
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
        await utilisateur.send(embed=embed)
        embed = discord.Embed(description=f"✅** Bravo!｜**" + "💌 Lettre d'amour envoyé à " + utilisateur.mention , color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
@bot.tree.command(name="archive", description="Archive un salon textuel.")
@app_commands.describe(salon_textuel="Lien du salon textuel")
async def archive(interaction: discord.Interaction, salon_textuel: discord.TextChannel):

    if interaction.user.guild_permissions.administrator:
         date_formattee = datetime.now().strftime("%d-%m-%y")
         nom_salon_archives = f"{salon_textuel.name}-{date_formattee}"  
         categorie_archives = discord.utils.get(interaction.guild.categories, name="📦 archives")

         if categorie_archives is None:
             erreur = "La catégorie '📦 archives' n'a pas été trouvée."
             embed = discord.Embed(description=f"❌** Erreur｜**" + f"{erreur}" , color=discord.Color.red())
             await interaction.response.send_message(embed=embed, ephemeral=True)
         else:
             await salon_textuel.edit(category=categorie_archives)

             salon_textuel_og = salon_textuel.name
             await salon_textuel.edit(name=nom_salon_archives)

             await salon_textuel.edit(position=0)

             embed = discord.Embed(description=f"✅** Bravo!｜**" + f"Le salon textuel `{salon_textuel_og}` a été archivé avec succès." , color=discord.Color.green())
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


@bot.tree.command(name="rename", description="Renomme un salon textuel.")
@app_commands.describe(salon_textuel="Lien du salon textuel", nouveau_nom="Nouveau nom du salon textuel")
async def rename(interaction: discord.Interaction, salon_textuel: discord.TextChannel, nouveau_nom: str):
    if interaction.user.guild_permissions.administrator:
        try:
            nom_actuel = salon_textuel.name
            if '｜' in nom_actuel:  # Vérification s'il y a des caractères spéciaux
                nom_actuel = nom_actuel.split('｜', 1)[-1]
                nouveau_nom_complet = f"{salon_textuel.name.split('｜', 1)[0]}｜{nouveau_nom}"
            else:
                nouveau_nom_complet = nouveau_nom
            await salon_textuel.edit(name=nouveau_nom_complet)
            embed = discord.Embed(description=f"✅** Bravo!｜** Le salon textuel `{nom_actuel}` a été renommé en `{nouveau_nom_complet}` avec succès.", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            erreur = f"Une erreur s'est produite lors du renommage du salon textuel : {e}"
            embed = discord.Embed(description=f"❌** Erreur｜** {erreur}", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
    else:
        erreur = "Vous n'avez pas les permissions requises pour exécuter cette commande."
        embed = discord.Embed(description=f"❌** Erreur｜** {erreur}", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

# Charger les tags à partir du fichier JSON
def load_tags():
    try:
        with open('tags.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Enregistrer les tags dans le fichier JSON
def save_tags(tags):
    with open('tags.json', 'w') as file:
        json.dump(tags, file, indent=4)

tag_group = app_commands.Group(name="tag", description="Manipule les tags.")

@tag_group.command(name="use", description="Utilise un tag enregistré.")
@app_commands.describe(tag_nom="Nom du tag")
async def use_tag(interaction: discord.Interaction, tag_nom: str):
    tags = load_tags()
    if tag_nom in tags:
        texte = tags[tag_nom]["texte"]
        await interaction.response.send_message(texte)
    else:
        embed = discord.Embed( description="❌ **Erreur｜** Ce tag n'existe pas.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

@tag_group.command(name="new", description="Crée un nouveau tag.")
@app_commands.describe(tag_nom="Nom du tag", texte="Texte intégré au tag")
async def create_tag(interaction: discord.Interaction, tag_nom: str, texte: str):
    tags = load_tags()
    user_id = str(interaction.user.id)
    if tag_nom in tags:
        embed = discord.Embed(description=f"❌ **Erreur｜** Le tag `{tag_nom}` existe déjà.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    tags[tag_nom] = {"texte": texte, "creator_id": user_id}
    save_tags(tags)
    embed = discord.Embed(description=f"✅ **Bravo!｜** Le tag `{tag_nom}` a été créé avec succès !", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@tag_group.command(name="remove", description="Supprime un tag créé par vous.")
@app_commands.describe(tag_nom="Nom du tag")
async def remove_tag(interaction: discord.Interaction, tag_nom: str):
    tags = load_tags()
    user_id = str(interaction.user.id)
    if tag_nom in tags and tags[tag_nom]["creator_id"] == user_id:
        del tags[tag_nom]
        save_tags(tags)
        embed = discord.Embed(description=f"✅ **Bravo!｜** Le tag `{tag_nom}` a été supprimé avec succès !", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(description="❌ **Erreur｜** Vous n'êtes pas l'auteur de ce tag ou le tag n'existe pas.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

@tag_group.command(name="list", description="Affiche la liste des tags.")
async def list_tags(interaction: discord.Interaction):
    tags = load_tags()
    if not tags:
        embed = discord.Embed(title="Liste des Tags", description="Aucun tag n'a été créé 😔. Utilisez `/tag new` pour créer un nouveau tag.", color=discord.Color.from_rgb(193, 168, 233))
        await interaction.response.send_message(embed=embed)
        return
    sorted_tags = sorted(tags.items())  # Trie les tags par ordre alphabétique
    embed = discord.Embed(title="Liste des Tags", color=discord.Color.from_rgb(193,168,233))
    for tag_nom, data in sorted_tags:
        creator = interaction.guild.get_member(int(data["creator_id"]))
        if creator:
            creator_name = creator.display_name
        else:
            creator_name = "Utilisateur Inconnu"
        embed.add_field(name=f"{tag_nom}", value=f"\n`Auteur` : {creator_name}", inline=False)
        embed.set_footer(text=f"Utilisez `/tag new` pour créer un nouveau tag.")
    await interaction.response.send_message(embed=embed)




bot.tree.add_command(tag_group)

with open('config.json', encoding="utf-8", errors="ignore") as f:
    datatoken = json.load(f)
    token = datatoken["token"]
bot.run(token)
