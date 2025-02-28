from telebot.async_telebot import AsyncTeleBot
from decouple import config
import asyncio
import re
import tinydb
from database import insert_curso
bot = AsyncTeleBot('7929476900:AAHiHmi2ZBqPiu8HZnlyjwJy0z6GwXFs458')
#canal produção
canal =  -1002252592068

#canal teste
#canal = -1001790437275

db = tinydb.TinyDB('cursos.json')
-1001790437275


@bot.message_handler(commands=['ping'])
async def handle_ping(message):
    await bot.send_message(message.chat.id, 'Pong!')
    await bot.send_message(canal, 'Pong!')



def escape_markdown(text, version=2):
    """
    Escapa caracteres especiais no formato Markdown para evitar erros.
    Funciona para versões 1 e 2 do Markdown.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    if version == 2:
        return ''.join(f'\\{char}' if char in escape_chars else char for char in text)
    else:
        raise ValueError("Apenas o MarkdownV2 é suportado nesta função.")


def construir_mensagem(
    nome='N/A', categoria='N/A', tipo='N/A',
    tamanho='N/A', duracao='N/A', autor='@mineirocursos',
    link_curso='N/A'):
    """
    Reconstrói a mensagem com os dados fornecidos em um formato estilizado.
    Escapa os caracteres especiais para evitar erros no Markdown.
    """
    nome = escape_markdown(nome, version=2)
    categoria = escape_markdown(categoria, version=2)
    tipo = escape_markdown(tipo, version=2)
    tamanho = escape_markdown(tamanho, version=2)
    duracao = escape_markdown(duracao, version=2)
    autor = escape_markdown(autor, version=2)
    link_curso = escape_markdown(link_curso, version=2)

    mensagem = f"""
🔮 _Nome:_ *{nome}*

📂 _Categoria:_ {categoria}
📁 _Tipo:_ {tipo}
💾 _Tamanho:_ {tamanho}
🕒 _Duração:_ {duracao}

[📺 Assista aqui]({link_curso})


🏴‍☠️ Compartilhe {autor} 🏴‍☠️

"""
    return mensagem






@bot.message_handler(content_types=['photo', ])
async def handle_message(message):
    # Extrai a legenda, se existir
    legenda = message.caption or message.text
    print(legenda)
    
    padroes = {
        'padrao1': {
            'bt_assistir': r'➡️Assistir Curso⬅️'
        },
        
        'padrao3': {
            'autor': r"@iAzazelOfc",
        },
        'padrao4': {
            'autor': r'@MeuPatoCursos'
        },
        'padrao5': {
            'nome ': r'🌟 Nome:',

        },
        'padrao6': {
            'convite': r'Convite: (https?://\S+)|\((https?://\S+)\)',
        },
        'padrao7': {
            'assistir': r'👉Assistir Curso👈',
        },
        'padrao8': {
            'assistir': r'→ ASSISTIR CURSO',
        },
        'padrao9': {
            'assistir': r'Assistir Curso (https?://\S+)',
        },
        'padrao10': {
            'assistir': r'@Extreme_CursosGratis',
        },

        'padrao11': {
            'assistir': r'⬇️Assistir Curso⬇️',
        },
        
    }
    
    for nome_padroes, conjunto_padroes in padroes.items():
        
        for chave, padrao in conjunto_padroes.items():
            match = re.search(padrao, legenda)
            if match:
                print(f'padrao encontrado', nome_padroes)


                if nome_padroes == 'padrao1':
                    imagem = message.photo[-1].file_id
                    byte = await bot.get_file(imagem)
                    file_path = byte.file_path
                    download = await bot.download_file(file_path)
                    
                    print(byte)
                    nome_curso = legenda.split('\n')[0]
                    tamanho = f'{re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE).group(1)}'
                    duracao_match = re.search(r"Duração: (\d+)h (\d+)min", legenda, re.IGNORECASE)
                    duracao = f'{duracao_match.group(1)}h {duracao_match.group(2)}min' if duracao_match else "Duração N/A"
                    
                    # extrair link do curso
                    links = message.caption_entities
                    for link in links:
                        if link.type == 'text_link':
                            link_curso = link.url
                
                    await bot.send_photo(canal, imagem,
                    caption= construir_mensagem(nome_curso,tamanho=tamanho,duracao=duracao,link_curso=link_curso), parse_mode='Markdownv2')
                    
                    insert_curso(imagem=download, nome=nome_curso, categoria=None,
                                        tipo=None, tamanho=tamanho, duracao=duracao, autor=None, link_curso=link_curso)                                            
                
                elif nome_padroes == 'padrao2':
                    imagem = message.photo[-1].file_id
                    # Nome do curso
                    
                         
                    byte =  await bot.get_file(imagem)
                    file_path = byte.file_path
                    download = await bot.download_file(byte)
                    print(download)

                    nome_curso = legenda.split("\n")[0]
                    tamanho_match = re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE)
                    tamanho = f"{tamanho_match.group(1)}" if tamanho_match else "Tamanho N/A"
                    duracao_match = re.search(r"Duração: (\d+)h (\d+)min", legenda, re.IGNORECASE)
                    duracao = f"{duracao_match.group(1)}h {duracao_match.group(2)}min" if duracao_match else "Duração N/A"
                    
                    lancamento_match = re.search(r"Lançamento: (\d+)", legenda, re.IGNORECASE)
                    lancamento = f"{lancamento_match.group(1)}" if lancamento_match else "Lançamento N/A"
                    autor_match = re.search(r"©️\| (.+)", legenda)
                    autor = f"Autor: {autor_match.group(1)}" if autor_match else "Autor N/A"
        
                    try:
                        links = message.caption_entities
                        lista_links = []
                        for link in links:
                            if link.type == "text_link":
                                lista_links.append(link.url)
                        link_curso = lista_links[-1]
                        print(link_curso)
                    except:
                        link_match = re.search(r"⬇️Assistir Curso⬇️\n(https?://\S+)", legenda)
                        link_curso = link_match.group(1) if link_match else "Link não encontrado"
                    
                    await bot.send_photo(canal, imagem,
                    caption=construir_mensagem(nome_curso,tamanho=tamanho,duracao=duracao,link_curso=link_curso), parse_mode='Markdownv2')

                    insert_curso(imagem=download, nome=nome_curso, categoria=None,
                                        tipo=None, tamanho=tamanho, duracao=duracao, autor=None, link_curso=link_curso)                                            
                



                elif nome_padroes == 'padrao3':
                    imagem = message.photo[-1].file_id
                        
                    byte =  await bot.get_file(imagem)
                    file_path = byte.file_path
                    download = await bot.download_file(file_path)
                    print(download)

                    nome_match = re.search(r'Nome: (.+)', legenda)
                    nome = f"{nome_match.group(1)}" if nome_match else "Nome N/A"
                    categoria_match = re.search(r'Tipo: (.+)', legenda)
                    categoria = f"{categoria_match.group(1)}" if categoria_match else "Categoria N/A"
                    tamanho_match = re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE)
                    tamanho = f"{tamanho_match.group(1)}" if tamanho_match else "Tamanho N/A"
                    duracao_match = re.search(r"Duração: (\d+)h (\d+)min", legenda, re.IGNORECASE)
                    duracao = f"{duracao_match.group(1)}h {duracao_match.group(2)}min" if duracao_match else "Duração N/A"
                    links = message.caption_entities
                    lista_links = []
                    for link in links:
                        if link.type == "text_link":
                            lista_links.append(link.url)
                            print(link.url)
                    link_curso = lista_links[1]
                    
                    await bot.send_photo(canal, imagem,
                    caption= construir_mensagem(nome=nome,tamanho=tamanho,categoria=categoria ,duracao=duracao,link_curso=link_curso), parse_mode='Markdownv2')
                    
                    insert_curso(imagem=download, nome=nome, categoria=categoria,tipo=None, tamanho=tamanho,
                                        duracao=None, autor=None, link_curso=link_curso)
                elif nome_padroes == 'padrao4':
                    imagem = message.photo[-1].file_id
                   
                        
                    byte =  await bot.get_file(imagem)
                    file_path = byte.file_path
                    download = await bot.download_file(file_path)
                    print(download)

                    match = re.search(r'CLIQUE AQUI PARA ASSISTIR', legenda)
                    if match:
                        nome_match = re.search(r'Nome: (.+)', legenda)
                        nome = f"{nome_match.group(1)}" if nome_match else "Nome N/A"
                        if nome == 'Nome N/A':
                            nome = legenda.split("\n")[0]
                        categoria_match = re.search(r'Categoria: (.+)', legenda)
                        categoria = f"{categoria_match.group(1)}" if categoria_match else "Categoria N/A"
                        tamanho_match = re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE)
                        tamanho = f"{tamanho_match.group(1)}" if tamanho_match else "Tamanho N/A"
                        links = message.caption_entities
                        lista_links = []
                        for link in links:
                            if link.type == "text_link":
                                lista_links.append(link.url)
                        link_curso = lista_links[0]
                        await bot.send_photo(canal, imagem,
                        caption= construir_mensagem(nome=nome,tamanho=tamanho,categoria=categoria, link_curso=link_curso), parse_mode='Markdownv2')
                        
                        insert_curso(nome=nome,imagem=download, tamanho=tamanho,categoria=categoria, link_curso=link_curso)
    
                elif nome_padroes == 'padrao5':
                    match = re.search(r'CLIQUE AQUI PARA ASSISTIR', legenda)
                    
                    if  not match:
                        pass
                    else:
                        imagem = message.photo[-1].file_id
                        
                    
                        byte =  await bot.get_file(imagem)
                        file_path = byte.file_path
                        download = await bot.download_file(file_path)
                        print(download)

                        nome_match = re.search(r'Nome:(.+)', legenda)
                        nome = f"{nome_match.group(1)}" if nome_match else "Nome N/A"
                        categoria_match = re.search(r'📁 Categoria:  (.+)', legenda)
                        categoria = f" {categoria_match.group(1)}" if categoria_match else "Categoria N/A"
                        tamanho_match = re.search(r"🗂 Tipo: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE)
                        tamanho = f"{tamanho_match.group(1)}" if tamanho_match else "Tamanho N/A"
                        links = message.caption_entities
                        lista_links = []
                        for link in links:
                            if link.type == "text_link":
                                lista_links.append(link.url)
                        link_curso = lista_links[0]
                        print(link_curso)
                        await bot.send_photo(canal, imagem,
                        caption= construir_mensagem(nome=nome,tamanho=tamanho,categoria=categoria,
                                                    link_curso=link_curso), parse_mode='Markdownv2')

                        insert_curso(imagem=download, nome=nome, tamanho=tamanho,categoria=categoria, link_curso=link_curso )
                elif nome_padroes == 'padrao6':
                
                    imagem = message.photo[-1].file_id
                    
                    byte =  await bot.get_file(imagem)
                    file_path = byte.file_path
                    download = await bot.download_file(file_path)
                    print(download)
                    nome = legenda.split("\n")[0]
                    tamanho = re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE).group(1)
                    duracao_match = re.search(r"Duração: (\d+)h (\d+)min", legenda, re.IGNORECASE)
                    duracao = f"{duracao_match.group(1)}h {duracao_match.group(2)}min" if duracao_match else "Duração N/A"
                    convite = re.search(r"Convite: (https?://\S+)", legenda).group(1)
                    await bot.send_photo(canal, imagem,
                    caption= construir_mensagem(nome=nome,tamanho=tamanho,duracao=duracao,link_curso=convite), parse_mode='Markdownv2')
                    
                    insert_curso(imagem=download, nome=nome, tamanho=tamanho,duracao=duracao,link_curso=convite)



                elif nome_padroes == 'padrao7':
                    imagem = message.photo[-1].file_id
                    byte =  await bot.get_file(imagem)
                    file_path = byte.file_path
                    download = await bot.download_file(file_path)
                    nome = legenda.split("\n")[0]
                    tamanho = re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE).group(1)
                    duracao_match = re.search(r"Duração: (\d+)h (\d+)min", legenda, re.IGNORECASE)
                    duracao = f"{duracao_match.group(1)}h {duracao_match.group(2)}min" if duracao_match else "Duração N/A"
                    
                    print(nome)
                    links = message.caption_entities
                    lista_links = []
                    for link in links:
                        if link.type == "text_link":
                            lista_links.append(link.url)
                    link_curso = lista_links[0]
                    
                    await bot.send_photo(canal, imagem, caption=construir_mensagem(nome=nome,tamanho=tamanho,duracao=duracao,link_curso=link_curso), parse_mode='Markdownv2')
                    insert_curso(imagem=download, nome=nome, tamanho=tamanho,duracao=duracao,link_curso=link_curso)

                elif nome_padroes == 'padrao8':
                    imagem = message.photo[-1].file_id
                    byte =  await bot.get_file(imagem)
                    file_path = byte.file_path
                    download = await bot.download_file(file_path)
                    nome = legenda.split("\n")[0]
                    tamanho = re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE).group(1)
                    duracao_match = re.search(r"Duração: (\d+)h (\d+)min", legenda, re.IGNORECASE)
                    duracao = f"{duracao_match.group(1)}h {duracao_match.group(2)}min" if duracao_match else "Duração N/A"
                    
                    print(nome)
                    links = message.caption_entities
                    lista_links = []
                    for link in links:
                        if link.type == "text_link":
                            lista_links.append(link.url)
                    link_curso = lista_links[0]
                    
                    await bot.send_photo(canal, imagem, caption=construir_mensagem(nome=nome,tamanho=tamanho,duracao=duracao,link_curso=link_curso), parse_mode='Markdownv2')
                    insert_curso(imagem=download, nome=nome, tamanho=tamanho,duracao=duracao,link_curso=link_curso)
                    
                elif nome_padroes == 'padrao10':

                    #resolver conflito de outro padrao
                    match_op = re.search(r'👉Assistir Curso👈', legenda)
                    if match_op:
                        return
    

                    imagem = message.photo[-1].file_id
                    byte =  await bot.get_file(imagem)
                    file_path = byte.file_path
                    download = await bot.download_file(file_path)
                    nome = legenda.split("\n")[0]
                    tamanho = re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE).group(1)
                    duracao_match = re.search(r"Duração: (\d+)h (\d+)min", legenda, re.IGNORECASE)
                    duracao = f"{duracao_match.group(1)}h {duracao_match.group(2)}min" if duracao_match else "Duração N/A"
                    
                    print(nome)
                    links = message.caption_entities
                    lista_links = []
                    for link in links:
                        if link.type == "text_link":
                            lista_links.append(link.url)
                            
                    link_curso = lista_links[0]
                    await bot.send_photo(canal, imagem,
                                          caption=construir_mensagem(nome=nome,tamanho=tamanho,duracao=duracao,link_curso=link_curso), parse_mode='Markdownv2')
                
                elif nome_padroes == 'padrao11':

           

                    imagem = message.photo[-1].file_id
                    byte =  await bot.get_file(imagem)
                    file_path = byte.file_path
                    download = await bot.download_file(file_path)
                    nome = legenda.split("\n")[0]
                    tamanho = re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", legenda, re.IGNORECASE).group(1)
                    duracao_match = re.search(r"Duração: (\d+)h (\d+)min", legenda, re.IGNORECASE)
                    duracao = f"{duracao_match.group(1)}h {duracao_match.group(2)}min" if duracao_match else "Duração N/A"  
                    
                    print(nome)
                    links = message.caption_entities
                    lista_links = []
                    for link in links:
                        if link.type == "text_link":
                            lista_links.append(link.url)
                    link_curso = lista_links[0]


async def main():
    await bot.polling(none_stop=True)


if __name__ == '__main__':
    asyncio.run(main())
