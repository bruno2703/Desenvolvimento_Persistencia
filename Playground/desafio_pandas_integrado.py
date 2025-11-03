import pandas as pd

df_projetos = pd.read_csv("./arquivos/desempenho_projetos.csv")
#print(df_projetos)

tempo_series = df_projetos["Tempo_Entrega"]
#print("antes:\n",tempo_series)
tempo_series = tempo_series.astype("int32")
#print("depois:\n",tempo_series)

df_projetos["Tempo_Entrega"] = tempo_series
#print(df_projetos)

#imprimir as tres primeiras linhas
#print(df_projetos.head(3))


media_qualidade = df_projetos["Pontuacao_Qualidade"].mean()
#print("a media de qualidade e: ",media_qualidade)

custo_menor = df_projetos["Custo_Total"].min()
projeto_menor_custo = df_projetos[df_projetos["Custo_Total"]==custo_menor]

#print(projeto_menor_custo)


media_tempo = df_projetos["Tempo_Entrega"].mean()
#print("a media de tempo dos projetos e:",media_tempo)

projetos_rapidos = df_projetos[df_projetos["Tempo_Entrega"] < media_tempo]
#print("esses projetos foram mais rapidos que a media:",projetos_rapidos)


def determinar_status(pontuacao):
    if pontuacao >= 90:
        return "Excelente"
    elif pontuacao >= 80:
        return "Aprovado"
    else:
        return "Revisão"
    
df_projetos["Status"] = df_projetos["Pontuacao_Qualidade"].apply(determinar_status)
#print(df_projetos)


#Crie uma segunda nova coluna chamada Bonus_Equipe e a inicialize com 0.
#Use uma filtragem booleana seguida de atribuição para definir: se o Status do projeto for 'Excelente', o Bonus_Equipe deve ser 5000.
#Imprima o DataFrame final, ordenado de forma descendente pela coluna Bonus_Equipe.

df_projetos["Bonus_Equipe"] = 0

df_projetos.loc[df_projetos["Status"] == "Excelente", "Bonus_Equipe"] = 5000

df_projetos = df_projetos.sort_values(by="Bonus_Equipe", ascending=False)

print(df_projetos)