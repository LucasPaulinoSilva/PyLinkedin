import httpx
from parsel import Selector
import asyncio
import sys
import config

# Cria a classe com os atributos da Vaga de Trabalho
class VagaTrabalho:
    def __init__(self, cargo, empresa, local, link):
        self.cargo = cargo
        self.empresa = empresa
        self.local = local
        self.link = link

    # Formata os atributos para melhor legibilidade no telegram
    def __str__(self):
        return (f'💼 CARGO: {self.cargo}\n\n'
                f'🏭 EMPRESA ANUNCIANTE: {self.empresa}\n\n'
                f'📍 LOCAL: {self.local}\n\n'
                f'🔗 LINK VAGA: {self.link}\n\n')


async def obtemDados():
    # Declara string vazia que será usada para guardar os dados obtidos
    output = ''

    try:
        # Obtem o código fonte da página
        async with httpx.AsyncClient() as client:
            response = await client.get(config.URL_CUSTOM)
            response_content = response.content
            sel = Selector(text=response_content.decode())

            # Encontra quantas vagas existem no código fonte
            vagas = sel.css('div[data-row]')

            # Caso não existam vagas o processo é encerrado
            if len(vagas) == 0:
                output += ' ❌ NÃO FORAM ENCONTRADAS VAGAS NAS ÚLTIMAS 24 HORAS ❌\n'
                return output
                sys.exit()
            else:
                output += f'------------ VAGAS ENCONTRADAS: {len(vagas)} ------------\n'

            # Realiza o loop nas vagas encontradas
            contador = 1
            
            for vaga in vagas:
                # Obtem os textos do "cargo","empresa","local","link" das tags html
                cargo = vaga.css(
                    'h3.base-search-card__title::text').get().strip()
                empresa = vaga.css('a.hidden-nested-link::text').get().strip()
                local = vaga.css(
                    'span.job-search-card__location::text').get().strip()
                link = vaga.css(
                    'a.base-card__full-link::attr(href)').get().strip()

                # Monta a string com as informações obtidas
                vaga_obj = VagaTrabalho(cargo, empresa, local, link)
                output += '---------------------------------------------------------------------\n'
                output += str(
                    f'--------------------------- VAGA: {contador} ---------------------------\n')
                output += str(vaga_obj)

                contador += 1

    except Exception as e:
        # Informa a mensagem de erro capturada
        output = f'Ocorreu um erro: {e}'

    # Retorna a string com as informações obtidas para serem usadas em outra task
    return output

# Método que executa o código separado para fins de testes
if __name__ == "__main__":
    print(f'Mensagem de teste para validar a raspagem dos dados! {asyncio.run(obtemDados())}')