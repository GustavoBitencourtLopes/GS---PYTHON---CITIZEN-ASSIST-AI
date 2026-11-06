import json
from orientacao import Orientacao


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


if __name__ == "__main__":
    base = BaseConhecimento("data/base_conhecimento.json")
    if base.carregar():
        print(len(base.orientacoes), "orientações carregadas")
        print("Categorias:", base.categorias())
        trabalho = base.por_categoria("Trabalho")
        print(len(trabalho), "orientações em Trabalho")
        trabalho[0].exibir()

    print("\n--- Teste com arquivo que não existe ---")
    base_errada = BaseConhecimento("data/nao_existe.json")
    base_errada.carregar()
    print("O programa continuou rodando!")