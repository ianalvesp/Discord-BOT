import discord
import json
import os
from discord.ext import commands

# Ativar Intents para capturar mudanças de avatar
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necessário para detectar mudanças no perfil

# Criar o bot
bot = commands.Bot(command_prefix="!", intents=intents)

pasta = r"D:\Codigos\Discord\dados"
AVATAR_DB = os.path.join(pasta, "avatar_data.json")

# Verifica se a pasta existe, se não, cria ela
if not os.path.exists(pasta):
    os.makedirs(pasta)

# Verifica se o arquivo JSON existe e carrega ou cria um novo
if os.path.exists(AVATAR_DB):
    try:
        with open(AVATAR_DB, "r") as f:
            avatar_data = json.load(f)
        print("Dados carregados:", avatar_data)  # Verifique os dados carregados
    except json.JSONDecodeError:
        # Caso o arquivo esteja vazio ou corrompido, cria-se um novo dicionário
        print("Arquivo JSON vazio ou corrompido. Criando novo arquivo.")
        avatar_data = {}
        with open(AVATAR_DB, "w") as f:
            json.dump(avatar_data, f, indent=4)  # Cria o arquivo vazio corretamente
else:
    avatar_data = {}
    with open(AVATAR_DB, "w") as f:
        json.dump(avatar_data, f, indent=4)  # Cria o arquivo corretamente
    print("Nenhum dado anterior encontrado. Criando novo arquivo.")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    # Salvar a URL do avatar de todos os membros quando o bot iniciar
    for guild in bot.guilds:
        for member in guild.members:
            user_id = str(member.id)
            if user_id not in avatar_data:
                avatar_data[user_id] = {
                    "count": 0,
                    "avatar_url": member.avatar.url if member.avatar else member.default_avatar.url
                }

    # Salvar os dados no arquivo JSON
    with open(AVATAR_DB, "w") as f:
        json.dump(avatar_data, f, indent=4)

@bot.event
async def on_member_update(before, after):
    # Log para ver se o evento está sendo chamado
    print(f"Evento on_member_update acionado para: {after.name}")

    # Obtém as URLs dos avatares antes e depois
    avatar_before = avatar_data.get(str(before.id), {}).get("avatar_url", None)
    avatar_after = after.avatar.url if after.avatar else after.default_avatar.url

    # Exibe as URLs dos avatares antes e depois
    print(f"URL do avatar antes: {avatar_before}")
    print(f"URL do avatar depois: {avatar_after}")

    # Verifica se a URL do avatar foi alterada
    if avatar_before != avatar_after:
        print(f"Detectando atualização de {after.name}....")

        # Atualiza o contador de trocas de avatar
        user_id = str(after.id)
        if user_id not in avatar_data:
            avatar_data[user_id] = {"count": 0, "avatar_url": avatar_after}

        # Atualiza a contagem de trocas de foto de perfil
        avatar_data[user_id]["count"] += 1
        avatar_data[user_id]["avatar_url"] = avatar_after  # Atualiza a URL do avatar

        # Salva os dados no arquivo JSON
        with open(AVATAR_DB, "w") as f:
            json.dump(avatar_data, f, indent=4)

        # Log para verificar se a atualização foi bem-sucedida
        print(f"Avatar de {after.name} atualizado! Total de {avatar_data[user_id]['count']} trocas.")
        print("Dados gravados no arquivo:", avatar_data)
    else:
        print(f"A foto de {after.name} não foi alterada.")


@bot.command()
async def trocas(ctx, member: discord.Member = None):
    """Mostra quantas vezes um usuário trocou de avatar"""
    member = member or ctx.author  # Se não for passado um usuário, pega quem chamou o comando
    user_id = str(member.id)

    trocas = avatar_data.get(user_id, {}).get("count", 0)
    await ctx.send(f"{member.mention} trocou de avatar {trocas} vezes.")

@bot.command()
async def oi(ctx):
    await ctx.send("Olá! Como posso te ajudar? 😊")

# Rodar o bot (Substitua "SEU_TOKEN_AQUI" pelo seu token)
bot.run("MTM1NjQxMDIyMDM5NzcyODAwNg.GSE6-j.FsOF18qeEsEbK7v3q3yg40FMFr1rQjoy8CGVQ8")
