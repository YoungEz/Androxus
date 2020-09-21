# coding=utf-8
# Androxus bot
# OwnerOnly.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from discord_bot.Utils import get_emoji_dance, random_color
from datetime import datetime


class OwnerOnly(commands.Cog):
    # algumas outras funções que só o dono do bot pode usar
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['desativar_tratamento_de_erro', 'erros_off'], hidden=True)
    @commands.is_owner()
    async def desativar_erros(self, ctx):
        self.bot.tratar_erros = False
        await ctx.send('Tratamento de erro desativado!')

    @commands.command(aliases=['ativar_tratamento_de_erro', 'erros_on'], hidden=True)
    @commands.is_owner()
    async def ativar_erros(self, ctx):
        self.bot.tratar_erros = True
        await ctx.send('Tratamento de erro ativado!')

    @commands.command(aliases=['jogar', 'status'], hidden=True)
    @commands.is_owner()
    async def game(self, ctx, *args):
        if (len(args) == 1) and (args[0] == '-1'):  # se só tiver um item, e for -1
            self.bot.mudar_status = True
            embed = discord.Embed(title=f'Agora meus status vão ficar alterado!',
                                  colour=discord.Colour(random_color()),
                                  description=get_emoji_dance(),
                                  timestamp=datetime.utcnow())
            embed.set_author(name='Androxus', icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        else:
            self.bot.mudar_status = False
            await self.bot.change_presence(activity=discord.Game(name=" ".join(args)))
            embed = discord.Embed(title=f'Status alterado!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Agora eu estou jogando ``{" ".join(args)}``',
                                  timestamp=datetime.utcnow())
            embed.set_author(name='Androxus', icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pv'], hidden=True)
    @commands.is_owner()
    async def dm(self, ctx, id: int, *args):
        user = self.bot.get_user(id)
        if user is not None:
            if ctx.guild.id != 405826835793051649:
                try:
                    await ctx.message.delete()
                except discord.errors.Forbidden:
                    pass
            user_dm_criado = user.dm_channel
            try:
                if user_dm_criado != None:
                    await user_dm_criado.send(" ".join(args))
                else:
                    await user.create_dm()
                    await user.dm_channel.send(" ".join(args))
                foi = True
            except discord.errors.Forbidden:
                foi = False
            try:
                if foi and ctx.guild.id == 405826835793051649:
                    embed = discord.Embed(title=f'Mensagem enviada!',
                                          colour=discord.Colour(random_color()),
                                          description=f'{" ".join(args)}',
                                          timestamp=datetime.utcnow())
                    embed.set_author(name='Androxus', icon_url=self.bot.user.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)
                    await ctx.send(embed=embed)
            except:
                pass
        else:
            if ctx.guild.id == 405826835793051649:
                await ctx.send('Não achei o usuário')


def setup(bot):
    bot.add_cog(OwnerOnly(bot))