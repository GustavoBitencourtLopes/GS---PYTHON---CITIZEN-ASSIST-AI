import csv
import json
import time
from datetime import datetime


class Assistente:
    def __init__(self, nome, base, caminho_historico="data/historico.json"):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.historico = []
        self.atendimentos_sessao = []
        self.carregar_historico()

    # ---------- Validação de entradas ----------

    def ler_opcao(self, mensagem, maximo, minimo=0):
        while True:
            entrada = input(mensagem).strip()
            if entrada == "":
                print("Entrada vazia. Digite um número.")
            elif not entrada.isdigit():
                print("Digite apenas números.")
            elif int(entrada) < minimo or int(entrada) > maximo:
                print(f"Opção inválida. Escolha entre {minimo} e {maximo}.")
            else:
                return int(entrada)

    def ler_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "n"):
                return resposta == "s"
            print("Resposta inválida. Digite s ou n.")

    def tem_dado_pessoal(self, texto):
        digitos = 0
        for caractere in texto:
            if caractere.isdigit():
                digitos += 1
        return digitos >= 8 or "@" in texto

    # ---------- Atendimento por pergunta ----------

    def perguntar(self):
        inicio = time.time()
        tentativas = 0

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                return
            if pergunta == "":
                print("Você não digitou nada. Escreva sua dúvida.")
                continue
            if len(pergunta) < 3:
                print("Escreva sua dúvida com palavras. Exemplo: como tirar o CPF?")
                continue
            if self.tem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            if not resultados or resultados[0][0] < 3:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras ou navegue pelas categorias:")
                for categoria in self.base.categorias():
                    print(f"  - {categoria}")
                if self.ler_sim_nao("Quer tentar de novo com outras palavras? (s/n): "):
                    continue
                self.registrar("pergunta", pergunta, None, False, False, tentativas, inicio)
                return

            pontos, melhor = resultados[0]
            print(f"\nConfiança da resposta: {self.base.confianca(pontos)} ({pontos} pontos)\n")
            melhor.exibir()

            alternativas = resultados[1:3]
            if alternativas:
                print("\nOutras orientações que podem ajudar:")
                for pontos_alt, orientacao in alternativas:
                    print(f"  - {orientacao.titulo} ({pontos_alt} pontos)")

            ajudou = self.ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            if ajudou:
                self.registrar("pergunta", pergunta, melhor.id, True, True, tentativas, inicio)
                return
            if self.ler_sim_nao("Quer tentar de novo com outras palavras? (s/n): "):
                continue
            self.registrar("pergunta", pergunta, melhor.id, True, False, tentativas, inicio)
            return

    # ---------- Atendimento por categorias ----------

    def navegar(self):
        while True:
            categorias = self.base.categorias()
            print("\nCategorias:")
            for numero, categoria in enumerate(categorias, start=1):
                print(f"  {numero}. {categoria}")
            print("  0. Voltar")
            escolha = self.ler_opcao("Escolha uma categoria: ", len(categorias))
            if escolha == 0:
                return

            categoria = categorias[escolha - 1]
            self.navegar_orientacoes(categoria)

    def navegar_orientacoes(self, categoria):
        while True:
            orientacoes = self.base.por_categoria(categoria)
            print(f"\n{categoria}:")
            for numero, orientacao in enumerate(orientacoes, start=1):
                print(f"  {numero}. {orientacao.titulo}")
            print("  0. Voltar")
            escolha = self.ler_opcao("Escolha uma orientação: ", len(orientacoes))
            if escolha == 0:
                return

            inicio = time.time()
            orientacao = orientacoes[escolha - 1]
            print()
            orientacao.exibir()
            ajudou = self.ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("categoria", orientacao.titulo, orientacao.id, True, ajudou, 1, inicio)

    # ---------- Histórico ----------

    def carregar_historico(self):
        try:
            with open(self.caminho_historico, encoding="utf-8") as arquivo:
                self.historico = json.load(arquivo)
        except FileNotFoundError:
            self.historico = []
        except json.JSONDecodeError:
            print("Aviso: o histórico estava corrompido. Começando um histórico novo.")
            self.historico = []

    def salvar_historico(self):
        with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, inicio):
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": round(time.time() - inicio, 1),
            "facilidade": None,
        }
        self.historico.append(atendimento)
        self.atendimentos_sessao.append(atendimento)
        self.salvar_historico()

    def avaliar(self):
        if not self.atendimentos_sessao:
            return
        nota = self.ler_opcao("\nDe 1 a 5, quão fácil foi usar o assistente? ", 5, minimo=1)
        for atendimento in self.atendimentos_sessao:
            atendimento["facilidade"] = nota
        self.salvar_historico()
        print("Obrigado pela avaliação!")

    # ---------- Indicadores ----------

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("\nAinda não há atendimentos registrados.")
            return None

        encontrados = [a for a in self.historico if a["encontrou"]]
        ajudaram = [a for a in self.historico if a["ajudou"]]
        notas = [a["facilidade"] for a in self.historico if a["facilidade"] is not None]

        tempos = [a["tempo_segundos"] for a in encontrados]
        tentativas = [a["tentativas"] for a in self.historico]

        sem_solucao = []
        for atendimento in self.historico:
            if not atendimento["ajudou"] and atendimento["pergunta"] not in sem_solucao:
                sem_solucao.append(atendimento["pergunta"])

        resultado = {
            "total": total,
            "encontrada_pct": round(len(encontrados) / total * 100, 1),
            "ajudou_pct": round(len(ajudaram) / total * 100, 1),
            "tempo_medio": round(sum(tempos) / len(tempos), 1) if tempos else 0,
            "tentativas_media": round(sum(tentativas) / total, 1),
            "facilidade_media": round(sum(notas) / len(notas), 1) if notas else None,
            "sem_solucao": sem_solucao,
        }

        print(f"\n===== Indicadores ({total} atendimentos) =====")
        print(f"Resposta encontrada: {resultado['encontrada_pct']}%")
        print(f"Taxa de acerto (ajudou): {resultado['ajudou_pct']}%")
        print(f"Tempo médio para encontrar: {resultado['tempo_medio']} s")
        print(f"Tentativas por atendimento: {resultado['tentativas_media']}")
        if resultado["facilidade_media"] is None:
            print("Facilidade de uso: sem avaliações ainda")
        else:
            print(f"Facilidade de uso (1 a 5): {resultado['facilidade_media']}")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")
        else:
            print("  (nenhuma)")
        return resultado

    # ---------- Exportação ----------

    def exportar_csv(self, caminho="data/atendimentos.csv"):
        colunas = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                   "ajudou", "tentativas", "tempo_segundos", "facilidade"]
        try:
            with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=";")
                escritor.writeheader()
                escritor.writerows(self.historico)
            print(f"\n{len(self.historico)} atendimentos exportados para {caminho}")
        except PermissionError:
            print(f"\nNão consegui salvar {caminho}. Feche o arquivo (ex.: no Excel) e tente de novo.")


if __name__ == "__main__":
    from base_conhecimento import BaseConhecimento

    base = BaseConhecimento("data/base_conhecimento.json")
    if base.carregar():
        assistente = Assistente("Citizen Assist AI", base)
        assistente.perguntar()
        assistente.avaliar()
        assistente.indicadores()