from bs4 import BeautifulSoup

with open("jogadas.html", encoding="utf-8") as f:
    sopa = BeautifulSoup(f, "html.parser")

#contador de vitorias
vitorias_jogador_1 = 0

REGRAS_VITORIA = {
    "pedra": "tesoura",
    "tesoura": "papel",
    "papel": "pedra"
}

tabela = sopa.find("table", {"id": "tabela-jogadas"})
linhas = tabela.find_all('tr') if tabela else []

for linha in linhas[1:]:

    celulas = linha.find_all('td')

    if len(celulas) == 2:
        j1_jogada = celulas[0].get_text().strip().lower()
        j2_jogada = celulas[1].get_text().strip().lower()

        if j2_jogada == REGRAS_VITORIA.get(j1_jogada):
            vitorias_jogador_1 += 1

print(f"Vitórias do Jogador 1: {vitorias_jogador_1}")