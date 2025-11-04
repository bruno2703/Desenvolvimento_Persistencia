import httpx

BASE_URL = "http://127.0.0.1:8000"

#cria ou atualiza aluno
def criar_aluno():
    resp = httpx.post(
        f"{BASE_URL}/alunos",
        json = {"nome":"Toistoiano","nota":9.5}
    )

def listar_alunos():
    resp = httpx.get(f"{BASE_URL}/alunos")
    print(resp.json())

criar_aluno()
listar_alunos()