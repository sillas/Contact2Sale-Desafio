from config.settings import logger
from client.strings.messages import welcome_message

class Chat:

    def __init__(self, mcp_client, messages):
        self.messages = messages
        self.mcp_client = mcp_client

    async def loop(self):
        """Run an interactive chat loop"""

        logger.info(welcome_message)
        logger.info("Para sair, digite q")

        self.messages.add(welcome_message)

        while True:
            try:
                query = input("\User: ").strip()

                if query.lower() == 'q':
                    logger.info("Até breve")
                    break

                self.messages.add(query, role="user")
                await self.mcp_client.process_query()

                logger.info(f"\n\R: {self.messages}")

            except Exception as e:
                logger.exception(f"\nLoop Error", exc_info=e)


""" instructions
Objetivo:
Uma concessionária que um agente vendedor;

INIT: agente conversa com o usuário
Ele entende o que o usuário está buscando, faz perguntas;
    - As perguntas não precisam seguir um padrão engessado tipo formulário;
Depois de coletar os dados, o cliente MCP envia tudo pro servidor.
O servidor busca no banco e retorna os veículos compatíveis
agente exibe uma resposta amigável com os resultados, incluindo: marca, modelo, ano, cor, quilometragem e preço.
"""