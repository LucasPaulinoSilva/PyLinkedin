import httpx
import config
import asyncio
import sys

async def telegramAPI(token, chat_id, mensagem):
    # Insere o token na url base
    url = config.URL_BASE.replace('{token}', token)
    
    # Atribui o ID e o conteúdo na mensagem 
    dados = {'chat_id': chat_id, 'text': mensagem}

    # Faz o post utilizando a API do Telegram
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=dados)

        if response.status_code == 200:
            pass
        else:
            sys.exit()


async def enviaMensagemTelegram(output):
    # Obtém o Token e o ID do arquivo de config
    token = config.TOKEN
    chat_id = config.CHAT_ID

    # Faz a solicitação do envio da mensagem para o Telegram e aguarda a conclusão
    await telegramAPI(token, chat_id, output)

# Método que executa o código separado para fins de testes
if __name__ == '__main__':
    asyncio.run(enviaMensagemTelegram("Mensagem teste para validar envio!"))