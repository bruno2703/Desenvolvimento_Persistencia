soma_notas = 0.0
total_alunos = 0
maior_nota = -1.0
menor_nota = 11.0 
aluno_maior_nota = ""
aluno_menor_nota = ""

with open("dados_alunos.txt", 'r', encoding='utf-8') as arquivo:

    for linha in arquivo:
        linha = linha.strip()
         
        
        dados = linha.split('#')
        
        if len(dados) == 3:
            nome = dados[0]
            nota_str = dados[2]
            
            nota = float(nota_str)

            soma_notas += nota
            total_alunos += 1
            
            if nota > maior_nota:
                maior_nota = nota
                aluno_maior_nota = nome
            
            if nota < menor_nota:
                menor_nota = nota
                aluno_menor_nota = nome

if total_alunos > 0:
    media_turma = soma_notas / total_alunos
    
    print(f"Média da turma: {media_turma:.2f}") 
    print(f"Maior nota: {maior_nota:.1f} ({aluno_maior_nota})") 
    print(f"Menor nota: {menor_nota:.1f} ({aluno_menor_nota})")