# coding=utf-8
# Androxus bot
# ServidorRepository.py

__author__ = 'Rafael'

import psycopg2

from database.Conexao import Conexao
from database.Repositories.Interfaces.IServidorRepository import IServidorRepository
from database.Servidor import Servidor


class ServidorRepository(IServidorRepository):

    # método privado
    def __existe(self, conn: Conexao, servidor: Servidor):
        # vai tentar pegar o prefixo, se não vier um prefixo
        # é porque o servidor não existe no banco
        if self.get_servidor(conn, servidor.id) is None:
            return False  # se ele não existir, retorna False
        return True  # se ele não passou pelo return False, vai retornar True

    def create(self, conn: Conexao, servidor: Servidor):
        """
        :param conn: Conexão com o banco de dados
        :param servidor: Servidor que vai ser criado no banco
        :type conn: Conexao
        :type servidor: Servidor
        :return: None
        :rtype: None
        """
        cursor = conn.cursor()  # pega o cursor
        try:
            query = 'CALL server_add(%s, %s);'  # query sql
            # o cursor vai colocar o id do servidor no lugar do primeiro "%s"
            # e o prefixo no lugar do segundos "%s" e executar a query
            cursor.execute(query, (servidor.id, servidor.prefixo,))
            conn.salvar()  # se tudo ocorrer bem, ele vai salvar as alterações
        except psycopg2.IntegrityError as e:
            # se tentar adicionar um item que já existe
            if str(e).startswith('duplicate key value violates unique constraint'):
                raise Exception('duplicate servidor')
            else:  # se acontecer outro erro:
                raise Exception(e)
        except Exception as e:  # se acontecer outro erro:
            raise Exception(e)

    def get_servidor(self, conn: Conexao, serverId: int):
        """
        :param conn: Conexão com o banco de dados
        :param serverId: Id do servidor
        :type conn: Conexao
        :type serverId: int
        :return: Vai retornar um objeto Servidor com todas as informações que estiverem salvas no banco
        :rtype: Servidor
        """
        cursor = conn.cursor()  # pega o cursor
        try:
            query = 'SELECT * FROM get_server(%s);'  # select para pegar o prefixo
            cursor.execute(query, (serverId,))  # vai trocar o %s pelo id do servidor
            resposta = cursor.fetchone()  # e depois, vai pegar o resultado do select
            # como o fetchone vai retornar uma tupla, vamos retornar apenas o
            # primeiro valor dessa tupla
            if resposta:  # se vier alguma coisa:
                # apenas encurtando a variavel, para que a linha do return não ficasse muito grande
                r = resposta
                return Servidor(serverId, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9])
            return None  # se não veio nada, retorna Nulo
        except Exception as e:
            raise e  # se acontecer algum erro...

    def update(self, conn: Conexao, servidor: Servidor):
        """
        :param conn: Conexão com o banco de dados
        :param servidor: O servidor que vai ser alterado
        :type conn: Conexao
        :type servidor: Servidor
        :return: Vai sincronizar o objeto Servidor passado, com o servidor que existir no banco
        :rtype: bool
        """
        cursor = conn.cursor()  # pega o cursor
        # se o servidor não existir no banco, vai criar ele
        if not self.__existe(conn, servidor):
            self.create(conn, servidor)
            return True  # vai retornar True, pra dizer que não houve nenhum erro
        try:  # se ele já existe, vai atualizar
            query = 'CALL server_update(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            # vai substituir os %s pelos valores do servidor passado, respectivamente
            cursor.execute(query, (servidor.prefixo,
                                   servidor.channel_id_log,
                                   servidor.mensagem_deletada,
                                   servidor.mensagem_editada,
                                   servidor.avatar_alterado,
                                   servidor.nome_alterado,
                                   servidor.tag_alterado,
                                   servidor.nick_alterado,
                                   servidor.role_alterado,
                                   servidor.sugestao_de_comando,
                                   servidor.id,))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
        return False

    def delete(self, conn: Conexao, servidor: Servidor):
        """
        :param conn: Conexão com o banco de dados
        :param servidor: O servidor que vai ser alterado
        :type conn: Conexao
        :type servidor: Servidor
        :return: Vai deletar o servidor e tudo que estiver atrelados a ele do banco
        :rtype: bool
        """
        cursor = conn.cursor()  # pega o cursor
        try:
            query = 'CALL server_remove(%s);'
            cursor.execute(query, (servidor.id,))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
