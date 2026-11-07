from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível iniciar o assistente sem a base de conhecimento.")
        return

    assistente = Assistente("Citizen Assist AI", base)

    print("=" * 50)
    print(f"Olá! Eu sou o {assistente.nome}.")
    print("Tiro dúvidas de jovens no primeiro emprego sobre")
    print("documentos, trabalho, educação e benefícios.")
    print("Não digite dados pessoais (nome, CPF, telefone ou e-mail).")
    print("=" * 50)

    while True:
        print("\n--- Menu principal ---")
        print("1. Fazer uma pergunta")
        print("2. Navegar por categorias")
        print("3. Ver indicadores")
        print("4. Exportar atendimentos (CSV)")
        print("0. Sair")
        opcao = assistente.ler_opcao("Escolha uma opção: ", 4)

        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        else:
            assistente.avaliar()
            assistente.exportar_csv()
            print(f"\nObrigado por usar o {assistente.nome}. Até mais!")
            break


if __name__ == "__main__":
    main()