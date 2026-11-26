# Mobile Division · Primeiros passos no bug bounty

Um percurso em português para quem tem um celular e quer aprender a ler o escopo de um programa, revisar uma política de acesso e escrever um relatório. Reserve cerca de 30 minutos para a primeira sessão. O exercício usa arquivos fictícios e funciona no navegador ou em um terminal Android, sem root.

## 1. Leia o escopo antes de testar

Abra a página pública de um programa e anote estas informações. Faça esta etapa só com a leitura da política.

| Anote | Procure na política |
| --- | --- |
| Ativo | Domínio, aplicativo ou versão explicitamente incluídos |
| Permissão | Tipos de teste permitidos, restrições e ativos excluídos |
| Contas | Regras para contas de teste e dados próprios |
| Envio | Canal privado, requisitos de evidência e regras de divulgação |
| Recompensa | Quais ativos e tipos de achado são elegíveis |

Confira a política na data em que pretende pesquisar. Se um ativo ou uma técnica estiver ambíguo, peça esclarecimento pelo canal do programa antes de testar. Programas de divulgação podem aceitar relatórios sem oferecer recompensa. [VDP e bug bounty no HackerOne](https://docs.hackerone.com/en/articles/8368965-vdp-vs-bbp) · [Safe Harbor e escopo](https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq)

## 2. Revise uma política em um exercício offline

O aplicativo fictício **Caderno** guarda rascunhos privados. Sua regra de negócio exige que apenas a pessoa proprietária leia seu próprio rascunho. O [arquivo de política](lab/politica.json) representa uma proposta de configuração para revisão antes do lançamento. Cada linha em `casos` descreve um papel, sua relação com o rascunho e a decisão configurada.

**Só com navegador:** abra o arquivo, compare os três casos com a regra de negócio e anote a diferença entre o resultado esperado e o que está configurado.

**No Android com Termux:** instale o aplicativo por uma das fontes indicadas na [documentação oficial do Termux](https://github.com/termux/termux-app#installation). Se já tem uma cópia do repositório, abra sua pasta no Termux. Para baixar os arquivos numa primeira sessão:

```sh
pkg install git python
git clone https://github.com/kingmaker-lab/Projeto-Limiar.git limiar-bounty
cd limiar-bounty
if [ ! -f mobile/bug-bounty/lab/politica.json ]; then
    git switch feat/mobile-bug-bounty
fi
python3 -m json.tool mobile/bug-bounty/lab/politica.json
```

Depois de baixar os arquivos e instalar os pacotes, o comando de leitura funciona offline. Em iPhone, siga a trilha do navegador. Ela usa o mesmo arquivo e o mesmo modelo de relatório.

1. Identifique o único caso em que a configuração diverge da regra.
2. Registre o caminho do arquivo, o ID do caso, a decisão esperada e a decisão configurada.
3. Explique a consequência **condicional** da configuração e proponha uma correção.
4. Escreva um relatório com o [modelo](MODELO-RELATORIO.md) e confira sua leitura no [gabarito](lab/GABARITO.md). Guarde este relatório como exercício.

## 3. Prepare seu primeiro relatório real

Use o canal privado indicado pelo programa. Relate somente o que conseguiu observar e separe esse resultado do impacto possível. Inclua a evidência mínima e remova tokens, cookies, e-mails e outros dados sensíveis de capturas ou anexos. Se aparecerem dados de terceiros, interrompa a interação e siga as instruções do programa para relatar a exposição. [Guia de envio do HackerOne](https://docs.hackerone.com/en/articles/8473994-submitting-reports)
