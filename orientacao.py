class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self):
        print(f">> {self.titulo}  [{self.categoria}]")
        print(self.resposta)
        print("Documentos necessários:")
        for documento in self.documentos:
            print(f"  - {documento}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print("Aviso: este assistente NÃO é um canal oficial.")


if __name__ == "__main__":
    teste = Orientacao(
        1,
        "Documentos",
        "Tirar o CPF",
        ["cpf", "tirar cpf"],
        "A inscrição no CPF é grátis...",
        ["Documento de identificação oficial com foto"],
        "Site da Receita Federal",
        "https://www.gov.br/pt-br/servicos/inscrever-no-cpf",
        "2026-11-05"
    )
    teste.exibir()