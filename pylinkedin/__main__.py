import asyncio
from dados_vagas import obtemDados
from envio_telegram import enviaMensagemTelegram

async def main():
    # Executa o método que irá obter as vagas no Linkedin
    output = await obtemDados()
    
    # Recebe as vagas obtidas e executa o método que enviará a mensagem para o Telegram
    await enviaMensagemTelegram(output)

if __name__ == "__main__":
    asyncio.run(main())