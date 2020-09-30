# coding=utf-8
# Androxus bot
# OnMessageEvent.py

__author__ = 'Rafael'

from discord_bot.utils.Utils import pegar_o_prefixo
from discord_bot.dao.BlacklistDao import BlacklistDao
from discord_bot.dao.ComandoDesativadoDao import ComandoDesativadoDao
from discord_bot.dao.ComandoPersonalizadoDao import ComandoPersonalizadoDao
from datetime import datetime
import discord
from stopwatch import Stopwatch


async def on_message_event(bot, message):
    if not bot.is_ready(): return
    prefixo = pegar_o_prefixo(None, message)
    if BlacklistDao().get_pessoa(message.author.id) or message.author.bot: return
    if message.author.id == bot.user.id: return
    if isinstance(message.channel, discord.DMChannel):  # se a mensagem foi enviada no dm
        embed = discord.Embed(title=f'O(A) {message.author} mandou mensagem no meu dm',
                              colour=0xfdfd96,
                              description=f'{message.content}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{message.author.id}', icon_url='https://media-exp1.licdn.com/dms/image/C510BAQHhOjPujl' +
                                                               'cgfQ/company-logo_200_200/0?e=2159024400&v=beta&t=49' +
                                                               'Ex7j5UkZroF7-uzYIxMXPCiV7dvtvMNDz3syxcLG8')
        if len(message.attachments) != 0:
            for attachment in message.attachments:
                embed.set_image(url=attachment.url)
        embed.set_thumbnail(url=message.author.avatar_url)
        await bot.dm_channel_log.send(embed=embed)
    tempo_para_executar_comando = Stopwatch()
    if message.mention_everyone:  # verifica se marcou here ou everyone
        emoji = bot.get_emoji(755774680220172340)  # emoji de ping pistola
        await message.add_reaction(emoji)  # adiciona a reação com o emoji
    if message.guild is not None:  # Se foi usado num server, vai ver se o comando está desativado
        # aqui, vai verificar se o comando foi desativado
        for comandos_desativados in ComandoDesativadoDao().get_comandos(message.guild.id):
            # aqui, estamos retirando o prefixo da mensagem, e pegando apenas a primeira palavra da mensagem
            if message.content.lower().replace(prefixo, '').split(' ')[0] in comandos_desativados:
                # se ela corresponder, a um comando que está desativado:
                await message.channel.send('<a:no_no:755774680325029889> Este comando ' +
                                           'foi desativado por um administrador do servidor!')
                tempo_para_executar_comando.stop()
                return
    channel = message.channel
    prefixo = pegar_o_prefixo(None, message)
    usando_comando = False
    if message.guild is not None:  # se a mensagem foi enviar num servidor
        try:
            #  como tem 3 for, um dentro do outro, é mais facil força um erro, do que ir dando break em cada um
            for cog in bot.cogs:  # verifica se a mensagem, está chamando algum comando
                for command in bot.get_cog(
                        cog).get_commands():  # laço que vai passar por todos os comandos que o bot tem
                    if message.content.lower().startswith(f'{prefixo}{command.name}'):  # Se a mensagem tiver o comando
                        usando_comando = True
                        raise Exception()  # para o laço
                    for aliases in command.aliases:
                        if message.content.lower().startswith(f'{prefixo}{aliases}'):  # se achar o comando
                            usando_comando = True
                            raise Exception()  # para o laço
        except Exception:
            pass
        if not usando_comando:  # se não estiver usando um comando do bot
            # vai ver se a pessoa usou algum comando personalizado
            # só existem comandos personalizados em servidores, então aqui verifica se está num server
            if message.guild is not None:
                for comando in ComandoPersonalizadoDao().get_comandos(message.guild.id):
                    if comando[0].lower() in message.content.lower():  # se identificar o comando, na mensagem
                        enviar_mensagem = True
                        # aqui vai ver a resposta, e se é ou não para ignorar a posição do comando
                        resposta, inText = ComandoPersonalizadoDao().get_resposta(message.guild.id, comando[0])
                        if not inText:  # se não for para ignorar a posição, vai ver se a mensagem inicia com o comando
                            if not message.content.lower().startswith(comando[0].lower()):
                                # se for obrigatorio que a mensagem comesse com o comando, e ela não estiver começando
                                enviar_mensagem = False  # não vai responder
                        if enviar_mensagem:
                            tempo_para_executar_comando.stop()
                            await channel.send(resposta.format(tempo=str(tempo_para_executar_comando)))
                            return
    if (f'<@{str(bot.user.id)}>' == message.content) or (f'<@!{str(bot.user.id)}>' == message.content):
        await channel.send(f'Use o comando ``{prefixo}help`` para obter ajuda!')
        await channel.send('<a:hello:755774680949850173>')
    tempo_para_executar_comando.stop()
    await bot.process_commands(message)
