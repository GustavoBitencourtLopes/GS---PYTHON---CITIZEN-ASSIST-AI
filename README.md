# Citizen Assist AI — Primeiro Emprego

Assistente de terminal, feito em Python, que orienta jovens no primeiro emprego sobre documentos, trabalho, educação e benefícios, sempre com base em informações de fontes oficiais, mostrando a fonte e a data de verificação, e sem coletar dados pessoais.

Projeto da **Global Solution 2026.2** — disciplina **Pensamento Computacional e Automação com Python** (FIAP), desafio CitizenTech.

## Integrantes

| Nome | RM |
|---|---|
| Gustavo Bitencourt Lopes | 568885 |
| Daniel Vieira | 573326 |

## Vídeo técnico

Link https://youtu.be/5oDmpqQqMek

## Público e problema

**Público:** jovens que estão procurando ou começando o primeiro emprego.

**Problema:** nessa fase, o jovem precisa resolver ao mesmo tempo várias coisas que nunca fez: tirar documentos (CPF, identidade, título de eleitor), ativar a Carteira de Trabalho Digital, entender o que é Jovem Aprendiz ou estágio e saber de programas como Enem, ProUni, ID Jovem e Pé-de-Meia. A informação existe, mas está espalhada em vários sites, escrita em linguagem técnica e misturada com páginas que parecem oficiais e não são.

**Solução:** um assistente que responde em linguagem simples, usando apenas uma base de conhecimento montada a partir de páginas oficiais, e que mostra em toda resposta de onde veio a informação, quando ela foi verificada e o aviso de que não é um canal oficial.

## ODS relacionados

- **ODS 4 — Educação de qualidade:** orientações sobre Enem, ProUni e Pé-de-Meia.
- **ODS 8 — Trabalho decente e crescimento econômico:** orientações sobre Carteira de Trabalho Digital, Jovem Aprendiz e direitos do estagiário.
- **ODS 10 — Redução das desigualdades:** benefícios voltados a jovens de baixa renda (ID Jovem, Pé-de-Meia, ProUni).
- **ODS 16 — Paz, justiça e instituições eficazes:** acesso à informação pública, com fonte oficial e data de verificação.

## Como executar

Requisitos: Python 3 instalado. O projeto não usa bibliotecas externas.

```bash
git clone https://github.com/GustavoBitencourtLopes/GS---PYTHON---CITIZEN-ASSIST-AI.git
cd GS---PYTHON---CITIZEN-ASSIST-AI
python main.py
```

Menu principal:

```
1. Fazer uma pergunta
2. Navegar por categorias
3. Ver indicadores
4. Exportar atendimentos (CSV)
0. Sair
```

Ao sair (opção 0), o assistente pede uma nota de facilidade de 1 a 5 e exporta o CSV automaticamente.

## Estrutura do projeto

```
├── README.md
├── main.py                  # inicia o programa e mostra o menu principal
├── orientacao.py            # classe Orientacao
├── base_conhecimento.py     # classe BaseConhecimento + normalizar()
├── assistente.py            # classe Assistente
└── data/
    ├── base_conhecimento.json   # 12 orientações, 3 categorias
    ├── historico.json           # atendimentos registrados
    └── atendimentos.csv         # exportação dos atendimentos
```

## Classes e composição

| Classe | Representa | Atributos | Métodos |
|---|---|---|---|
| `Orientacao` | Uma orientação da base (um registro do JSON) | id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em | `exibir()` |
| `BaseConhecimento` | O conjunto de todas as orientações | caminho, orientacoes | `carregar()`, `categorias()`, `por_categoria()`, `pontuar()`, `buscar()`, `confianca()` |
| `Assistente` | Quem conversa com o cidadão | nome, base, historico, caminho_historico, atendimentos_sessao | `perguntar()`, `navegar()`, `registrar()`, `avaliar()`, `indicadores()`, `exportar_csv()` e os validadores `ler_opcao()`, `ler_sim_nao()`, `tem_dado_pessoal()` |

As classes se encaixam por composição:

```
Assistente
 └── base: BaseConhecimento
      └── orientacoes: [Orientacao, Orientacao, ...]
```

## Regra de pontuação

A pergunta, as palavras-chave e o título são comparados depois de passar pela função `normalizar()`, que deixa tudo em minúsculas, sem acentos, sem pontuação e com um espaço no começo e no fim. Esses espaços fazem com que só palavras inteiras sejam comparadas (por exemplo, a palavra-chave "sus" não casa com "susto").

| Regra | Pontos |
|---|---|
| Palavra-chave da orientação que aparece na pergunta | +3 |
| Palavra da pergunta (4 letras ou mais) que aparece no título | +1 |

| Pontuação da melhor orientação | Resultado |
|---|---|
| 6 ou mais | Confiança ALTA |
| 3 a 5 | Confiança MÉDIA |
| Menos de 3 | "Não encontrei": o assistente sugere outras palavras e mostra as categorias |

O método `buscar()` devolve uma lista de tuplas `(pontos, orientacao)`, da maior para a menor pontuação. O assistente mostra a melhor orientação e até duas alternativas. Usamos os pesos e limites do enunciado, sem alterações.

**Exemplo:** "Como faço a carteira de trabalho?" → orientação 6 (Ativar a Carteira de Trabalho Digital): +3 pela palavra-chave "carteira de trabalho", +1 por "carteira" no título e +1 por "trabalho" no título = **5 pontos, confiança MÉDIA**.

## Decisões técnicas

- **Nomes do `__init__` iguais às chaves do JSON:** permite criar cada objeto com `Orientacao(**item)`, desempacotando o dicionário.
- **Palavras-chave já normalizadas no JSON** (sem acento e em minúsculas), para combinar com a pergunta normalizada. Como o `normalizar()` não remove hífens, o Pé-de-Meia tem as palavras-chave "pe de meia" e "pe-de-meia".
- **Ordenação com `key=lambda tupla: tupla[0]`:** sem o `key`, um empate de pontos faria o Python comparar dois objetos `Orientacao`, o que gera erro.
- **Aviso, fonte e data dentro do `exibir()`:** assim, nenhuma orientação é mostrada sem eles.
- **Um atendimento = uma dúvida, do começo até resolver ou desistir.** Se a pessoa reescreve a pergunta, continua no mesmo atendimento e as tentativas aumentam.
- **O histórico é salvo a cada atendimento**, e não só no fim, para não perder dados se o programa for fechado de repente.
- **CSV com `;` e codificação `utf-8-sig`**, para abrir corretamente no Excel em português.

## Regras de atendimento

- **Navegação por categorias:** categorias e orientações numeradas, com "0 para voltar" em todas as telas.
- **Entradas inválidas:** opção fora da faixa, letras, resposta vazia ou s/n inválido nunca encerram o programa.
- **Dados pessoais:** o assistente nunca pede nome, CPF, telefone ou e-mail. Perguntas com 8 ou mais dígitos ou com @ são recusadas e não são registradas.
- **Transparência:** toda resposta mostra a fonte, a data de verificação e o aviso de que o assistente não é um canal oficial.
- **Arquivos:** JSON da base ausente, corrompido ou com campos faltando não trava o programa. O histórico ausente ou corrompido também não.

## Histórico, indicadores e CSV

Cada atendimento é salvo em `data/historico.json` com: data, origem (pergunta ou categoria), pergunta, id da orientação, se encontrou, se ajudou, tentativas, tempo em segundos e nota de facilidade.

Indicadores calculados (opção 3 do menu): resposta encontrada (%), taxa de acerto (%), tempo médio para encontrar, tentativas por atendimento, facilidade de uso (1 a 5) e lista de dúvidas sem solução.

Os atendimentos são exportados para `data/atendimentos.csv` com `csv.DictWriter`.

## Integrações com outras disciplinas

Não houve integração com outras disciplinas nesta entrega.

## Teste com usuários

O assistente foi testado com **3 pessoas de fora da equipe**, que fizeram **20 atendimentos** no total. Nenhum nome ou dado pessoal dos participantes foi registrado.

### Indicadores obtidos

| Indicador | Resultado |
|---|---|
| Resposta encontrada | 85,0% |
| Taxa de acerto (ajudou) | 60,0% |
| Tempo médio para encontrar | 3,4 s |
| Tentativas por atendimento | 1,2 |
| Facilidade de uso (1 a 5) | 4,5 |

### Dúvidas sem solução

| Registro | Origem | Análise |
|---|---|---|
| teste | Pergunta | Entrada de teste, não é uma dúvida real |
| s | Pergunta | Resposta "sim" digitada no campo de dúvida |
| n | Pergunta | Resposta "não" digitada no campo de dúvida |
| Receber o Pé-de-Meia | Categoria | Orientação aberta e marcada como "não ajudou" |
| Criar a conta gov.br | Categoria | Orientação aberta e marcada como "não ajudou" |
| Ser Jovem Aprendiz | Categoria | Orientação aberta e marcada como "não ajudou" |
| Emitir a Carteira de Identidade Nacional (CIN) | Categoria | Orientação aberta e marcada como "não ajudou" |

Todas as perguntas reais escritas pelos participantes foram encontradas pela busca: os atendimentos não encontrados foram as entradas "teste", "s" e "n". Nos quatro atendimentos por categoria marcados como "não ajudou", não registramos durante o teste o motivo de cada pessoa, então a causa não foi identificada.

### Melhoria feita a partir do teste

No teste, entradas como "s" e "n" foram digitadas no campo de dúvida, provavelmente por confusão com a pergunta anterior "Quer tentar de novo com outras palavras? (s/n)". Elas foram registradas como dúvidas sem solução e reduziram a taxa de resposta encontrada.

**Melhoria:** o método `perguntar()` passou a recusar perguntas com menos de 3 caracteres, mostrando um exemplo de como escrever a dúvida. Essas entradas não contam como tentativa e não são registradas.

## Fontes consultadas

Todas as orientações foram conferidas em fontes oficiais em 05/11/2026.

| id | Orientação | Fonte |
|---|---|---|
| 1 | Tirar o CPF | https://www.gov.br/pt-br/servicos/inscrever-no-cpf |
| 2 | Carteira de Identidade Nacional (CIN) | https://www.gov.br/governodigital/pt-br/identidade/cin/perguntas-frequentes-sobre-a-cin |
| 3 | Primeiro título de eleitor | https://www.tse.jus.br/servicos-eleitorais/servicos/carta-de-servicos-ao-eleitor |
| 4 | Alistamento militar | https://www.gov.br/defesa/pt-br/acesso-a-informacao/lei-geral-de-protecao-de-dados-pessoais-lgpd/termo-de-uso-e-aviso-de-privacidade/termo-de-uso_smo.pdf |
| 5 | Conta gov.br | https://www.gov.br/governodigital/pt-br/identidade/conta-gov-br/niveis-da-conta-govbr |
| 6 | Carteira de Trabalho Digital | https://portalfat.trabalho.gov.br/programas-e-acoes-2/carteira-de-trabalho-ctps/ |
| 7 | Jovem Aprendiz | https://www.trt4.jus.br/portais/trt4/jovem-aprendiz |
| 8 | Direitos do estagiário | https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/lei/l11788.htm |
| 9 | Inscrição no Enem | https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/enem/enem-2026-saiba-quem-tem-direito-a-isencao-da-taxa-de-inscricao |
| 10 | ID Jovem | https://www.gov.br/pt-br/servicos/obter-a-carteira-de-identidade-jovem |
| 11 | ProUni | https://www.gov.br/pt-br/servicos/obter-bolsa-de-estudo-do-prouni |
| 12 | Pé-de-Meia | https://www.caixa.gov.br/programas-sociais/pe-de-meia/Paginas/default.aspx |

**Uso de IA:** com autorização do professor, usamos IA como apoio na pesquisa e coleta das informações. Todo o conteúdo foi conferido nas páginas oficiais listadas acima, e informações que só apareciam em sites não oficiais foram removidas da base.

## Limitações

- **A busca compara palavras, não entende o sentido da frase.** "Como faço a carteira de trabalho?" também dá 1 ponto para a CIN, porque "carteira" aparece no título dela.
- **Empates de pontuação acontecem.** "preciso do enem pro prouni" dá 4 pontos para o Enem e 4 para o ProUni; nesse caso, vale a ordem do JSON.
- **Sinônimos fora das palavras-chave não são encontrados.** "tenho que servir no quartel?" não encontra o alistamento militar, porque "quartel" não é palavra-chave.
- **O bloqueio de dados pessoais pode recusar perguntas legítimas**, como uma data de nascimento escrita só com números (8 dígitos).
- **Histórico corrompido:** se o `historico.json` estiver corrompido, o assistente começa um histórico novo, e os registros antigos são perdidos no próximo salvamento.
- **As regras mudam com o tempo** (valores, prazos e requisitos de programas como ProUni, ID Jovem e Pé-de-Meia). A base precisa ser conferida de novo periodicamente, e cada orientação mostra a data da última verificação.
- **Este assistente não é um canal oficial** e não substitui o atendimento dos órgãos responsáveis.
