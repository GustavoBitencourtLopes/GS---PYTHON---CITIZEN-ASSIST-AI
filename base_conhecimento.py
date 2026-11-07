import json
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        self.orientacoes = []
        try:
            with open(self.caminho, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            for item in dados:
                self.orientacoes.append(Orientacao(**item))
            return True
        except FileNotFoundError:
            print(f"Erro: o arquivo {self.caminho} não foi encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro: o arquivo {self.caminho} está corrompido (JSON inválido).")
            return False
        except TypeError:
            print("Erro: alguma orientação do JSON tem campo faltando ou sobrando.")
            self.orientacoes = []
            return False

    def categorias(self):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        resultado = []
        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                resultado.append(orientacao)
        return resultado

    def pontuar(self, pergunta, orientacao):
        pergunta_norm = normalizar(pergunta)
        titulo_norm = normalizar(orientacao.titulo)
        pontos = 0

        for chave in orientacao.palavras_chave:
            if normalizar(chave) in pergunta_norm:
                pontos += 3

        for palavra in pergunta_norm.split():
            if len(palavra) >= 4 and f" {palavra} " in titulo_norm:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda tupla: tupla[0], reverse=True)
        return resultados

    def confianca(self, pontos):
        if pontos >= 6:
            return "ALTA"
        elif pontos >= 3:
            return "MÉDIA"
        else:
            return "BAIXA"


if __name__ == "__main__":
    base = BaseConhecimento("data/base_conhecimento.json")
    if base.carregar():
        perguntas = [
            "Como faço a carteira de trabalho?",
            "quero tirar o RG",
            "esqueci a senha do gov.br",
            "como abrir conta no banco?",
        ]
        for pergunta in perguntas:
            print(f"\nPergunta: {pergunta}")
            print(f"Normalizada: '{normalizar(pergunta)}'")
            resultados = base.buscar(pergunta)
            if resultados and resultados[0][0] >= 3:
                for pontos, orientacao in resultados[:3]:
                    print(f"  {pontos} pontos ({base.confianca(pontos)}) -> {orientacao.titulo}")
            else:
                print("  Não encontrei uma orientação para essa dúvida.")