import pandas as pd


receitas = pd.Series(
    data=[12000, 17500, 14300, 16000, 19500],
    index=["Luca Brasi", "Peter Clemenza", "Sal Tessio", "Tom Hagen", "Michael Corleone"]
)


total_arrecadado = receitas.sum()
print(f'Total arrecadado na semana: ${total_arrecadado}')

media_receitas = receitas.mean()
print(f'Média das receitas: ${media_receitas:.2f}')

associado_mais_arrecadou = receitas.idxmax()
print(f'Associado que mais arrecadou: {associado_mais_arrecadou}')


acima_da_media = receitas[receitas > media_receitas]
print('Associados que arrecadaram acima da média:')
print(acima_da_media)
