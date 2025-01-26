    match_pato = re.search(r"@MeuPatoCursos", legenda)
    match_receita = re.search(r"@iAzazelOfc", legenda)

    # Conjuntos de padrões para diferentes formatos
    padroes = {
        "padrao1": {  # Exemplo: Eletrônica Fácil
            'autor': r"🔥 By (@\w+)",
            "nome": r"^🌟 Nome: (.+)",
            "categoria": r"📁 Categoria: (.+)",
            "tipo": r"🗂 Tipo: (.+)",
            "tamanho": r"💻 Tamanho: ([\d.]+ ?(?:GB|GiB))",
        },
        "padrao2": {  # Exemplo: Filosofia e Sociologia
            "nome": r"^(.+)-Farias Brito Online-\d{4}",
            "tamanho": r"Tamanho: ([\d.]+ ?(?:GB|GiB))",
            "link": r"Convite: (https?://\S+)|\((https?://\S+)\)",
            "categoria": r"Duração: (.+)",  # Neste caso, duração substitui a categoria
        },
        "padrao3": {  # Exemplo genérico
            "nome": r"^(.+)",
            "tamanho": r"Tamanho: ([\d.]+ ?(?:GB|GiB))",
            "categoria": r"Categoria: (.+)",
        },
    }

    informacoes = {}
    link_curso = None
    nome_padroes_identificado = None  # Armazena o nome do padrão correspondente
    if match_pato:
        nome_padroes_identificado = "padrao3"
    elif match_receita:
        nome_padroes_identificado = "padrao1"

    # Tenta combinar os padrões em ordem
    for nome_padroes, conjunto_padroes in padroes.items():
        for chave, padrao in conjunto_padroes.items():
            match = re.search(padrao, legenda)
            if match:
                informacoes[chave] = match.group(1)

        # Se conseguiu extrair pelo menos o nome, já podemos identificar o padrão usado
        print(informacoes)
    # Extração de links embutidos, se existirem
    if message.caption_entities:
        all_links = []
        for entity in message.caption_entities:
            if entity.type == 'text_link':
                all_links.append(entity.url)
            elif entity.type == 'url':
                offset = entity.offset
                length = entity.length
                all_links.append(legenda[offset:offset + length])

        # Lógica manual para definir o link do curso com base no padrão identificado
        if nome_padroes_identificado == "padrao1":
            print('Padrão 1')
            link_curso = all_links[1] if len(all_links) > 1 else None
        elif nome_padroes_identificado == "padrao2":
            print('Padrão 2')
            link_curso = all_links[0] if len(all_links) > 0 else None
        elif nome_padroes_identificado == "padrao3":
            print('Padrão 3')
            link_curso = all_links[0] if len(all_links) > 0 else None

    # Padroniza a saída
    nome_curso = informacoes.get("nome", "N/A")
    tamanho_curso = informacoes.get("tamanho", "N/A")
    categoria_curso = informacoes.get("categoria", "N/A")
    link_curso = link_curso or informacoes.get("link", "N/A")

    mensagem_padronizada = (
        f"Nome: {nome_curso}\n"
        f"Tamanho: {tamanho_curso}\n"
        f"Categoria: {categoria_curso}\n"
        f"Assista aqui: {link_curso}\n\n"
        f"Compartilhe nosso canal: https://t.me/seu_canal"
    )

    # Envia a mensagem padronizada
    await bot.send_message(message.chat.id, mensagem_padronizada)
