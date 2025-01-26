import re
texto = """Desvendando a Matematica 3 0-Universo Narrado-2022

Tamanho: 6.7 gb
Duração: 20h 12min

➡️Assistir Curso⬅️

https://s.shopee.com.br/9Uif68E5E5
👆👆👆
"""

nome_curso = texto.split("\n")[0]
tamanho = f'Tamanho {re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", texto, re.IGNORECASE).group(1)}'
duracao_match = re.search(r"Duração: (\d+)h (\d+)min", texto, re.IGNORECASE)
duracao = f'Duração {duracao_match.group(1)}h {duracao_match.group(2)}min' if duracao_match else "Duração N/A"

print(nome_curso, tamanho, duracao)


texto2 = """Curso Prático de Reparo em Placa Mãe de Desktop - Magnata Silva
#hardware

📅| Lançamento: 2022
💾| Tamanho: 12.5 gb
🕒| Duração: 11h 6min
©️| Magnata Silva

⬇️Assistir Curso⬇️
"""

# Nome do curso
nome_curso = texto2.split("\n")[0]

# Tamanho
tamanho_match = re.search(r"Tamanho: ([\d.]+ ?(?:GB|GiB))", texto2, re.IGNORECASE)
tamanho = f"Tamanho {tamanho_match.group(1)}" if tamanho_match else "Tamanho N/A"

# Duração
duracao_match = re.search(r"Duração: (\d+)h (\d+)min", texto2, re.IGNORECASE)
duracao = f"Duração {duracao_match.group(1)}h {duracao_match.group(2)}min" if duracao_match else "Duração N/A"

# Lançamento
lancamento_match = re.search(r"Lançamento: (\d+)", texto2, re.IGNORECASE)
lancamento = f"Lançamento {lancamento_match.group(1)}" if lancamento_match else "Lançamento N/A"

# Autor
autor_match = re.search(r"©️\| (.+)", texto2)
autor = f"Autor: {autor_match.group(1)}" if autor_match else "Autor N/A"

# Exibe os resultados
print(nome_curso)
print(tamanho)
print(duracao)
print(lancamento)
print(autor)


texto3 = """🌟 Nome: IA Revolution Academy 2.0 - Sancler Miranda
➿➿➿➿➿➿➿➿
📁 Categoria: Receitas
🗂 Tipo: #Automação
💻 Tamanho: 3.14 GiB
➿➿➿➿➿➿➿➿
🔥 By @TopsCursos"""

nome = re.search(r' Nome:(.+)', texto3).group(1)
print(nome)