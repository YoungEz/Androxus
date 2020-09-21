# coding=utf-8
# Androxus bot
# Calc.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.Utils import random_color
import asyncio


class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __calcular(self, x):  # declaração de um método privado
        return await eval(x)

    @commands.command(hidden=True, aliases=['help_calcular'])
    async def help_calc(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.calc.name,
                          descricao='Para multiplicar, use ``*``. Para dividir use ``/``. Para usar potência, ' +
                                    'use ``**``. Coloque números decimais com pon' +
                                    'to em vez de virgula' +
                                    '. Você **não** deve fazer isso: ``3,14``, e **sim**: ``3.14``.Use ' +
                                    '**()** para dar preferencia na ' +
                                    'hora de fazer os calculos!',
                          parametros=['<Operação(ões)>'],
                          exemplos=['``{pref}calc`` ``2 + 5 * 2``',
                                    '``{pref}calcular`` ``(2 + 5) * 2``',
                                    '``{pref}calc`` ``5 ** 5``',
                                    '``{pref}calc`` ``2.5 * 4``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.calc.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['calcular'], description='Vou virar uma calculadora xD')
    async def calc(self, ctx, *args):
        chars_aceitaveis = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '+', '/', '%', '*', '-', '(', ')',
                            '.']
        if len(args) == 0:
            await self.help_calc(ctx)
            return
        args = ' '.join(args)

        for char in args:
            if not (char in chars_aceitaveis):
                await ctx.send(f'O caracter ``{char}`` não é nem um número, nem uma operação!')
                return

        try:
            # o tempo limite para executar a equação, é 5 vezes a latência do bot
            resultado = await asyncio.wait_for(self.__calcular(args), timeout=(self.bot.latency * 5))
        except asyncio.TimeoutError:
            # se passar mais de 5 vezes, a latencia do bot, sem segundos, para fazer a equação:
            await ctx.send(f'Está equação é muito grande para mim! <a:sad:755774681008832623>')
            return
        except SyntaxError as error:
            onde_foi_o_erro = ' ' * (error.offset - 1) + '👆'
            await ctx.send(f'Equação inválida!\n```{error.text}\n{onde_foi_o_erro}```')
            return
        except ZeroDivisionError:
            await ctx.send(
                'Equação inválida! Ainda não sou capaz de resolver divisões por 0!\n<a:sad:755774681008832623>')
            return
        if len(str(resultado)) >= 6000:
            await ctx.send('O resultado desta equação é tão grande que não consigo enviar\n<a:sad:755774681008832623>')
            return
        embed = discord.Embed(title=f'<:calculator:757079712077053982> Resultado:',
                              colour=discord.Colour(random_color()),
                              description=f'{resultado}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Calc(bot))
