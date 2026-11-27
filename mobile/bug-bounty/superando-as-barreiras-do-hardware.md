# Superando as barreiras do hardware

*Projeto Limiar · Mobile Division*

**Resumo.** Quem tem apenas um celular ou tablet já consegue aprender três partes centrais do bug bounty: interpretar o escopo de um programa, avaliar uma hipótese de segurança e escrever um relato que outra pessoa consiga verificar. Este estudo propõe um percurso que começa com navegador e notas, acrescenta uma ferramenta offline quando ela poupa trabalho e produz um relatório de prática desde a primeira sessão. A unidade de progresso é uma observação que você consegue explicar, sustentar e retomar.

## 1. O que cabe no dispositivo que você tem

Um celular de entrada impõe restrições reais. Digitar é mais lento, alternar entre abas custa atenção e o sistema pode encerrar um aplicativo em segundo plano. O plano de trabalho precisa caber nessas condições. A filosofia do Limiar, **extrair o melhor com o mínimo**, aparece na escolha do que executar e do que guardar. Se a pergunta é “quem deveria conseguir ler este rascunho?”, três linhas de uma política de acesso já permitem comparar a regra com a configuração. O valor do trabalho está na precisão dessa comparação.

| Restrição | Como adaptar a sessão | O que fica pronto |
| --- | --- | --- |
| Tela pequena | Mantenha a política em uma aba e a ficha em um aplicativo de notas. Copie para a ficha apenas o trecho relevante e o link. | Uma decisão de escopo que pode ser conferida. |
| Memória limitada | Trabalhe com um ativo por vez e registre o estado da tarefa antes de alternar aplicativos. | Uma sessão que pode ser retomada mesmo se as abas fecharem. |
| Internet intermitente | Guarde a referência e a data da política. Faça o exercício e escreva o relato offline. Reconecte para confirmar as regras atuais. | Um rascunho pronto para revisão. |
| Pouco armazenamento | Registre texto, versão e uma evidência curta quando ela for necessária. | Um relato legível e fácil de compartilhar privadamente. |

Navegador e notas bastam para seguir o percurso em Android, iPhone ou iPad. No Android, o Termux oferece um caminho opcional para organizar listas maiores. Um computador facilita trabalhos que dependem de emuladores, de múltiplos ambientes ou de processos longos. Essas tarefas podem ficar no caderno como pendências específicas enquanto você avança nas etapas que já consegue executar.

## 2. Primeira sessão de bug bounty pelo navegador

Reserve cerca de 30 minutos. Você vai terminar com uma ficha de escopo e um relatório de treino.

1. **Leia a política de um programa público por 10 minutos.** Escolha um único ativo listado. Anote o endereço ou a versão exata, a data da consulta, os métodos permitidos, os tipos de achado excluídos e o canal privado de envio. Marque como pendente qualquer regra que você ainda precise confirmar. Um programa de divulgação pode receber relatos sem oferecer recompensa. [Diferença entre VDP e bug bounty](https://docs.hackerone.com/en/articles/8368965-vdp-vs-bbp)
2. **Revise a política fictícia do Caderno por 10 minutos.** O aplicativo permite que cada pessoa leia seus próprios rascunhos privados. Abra o arquivo de exemplo. Para cada caso, escreva “decisão esperada” e “decisão registrada”. Localize a única diferença e formule uma frase de impacto condicional. [Arquivo do exercício](https://github.com/kingmaker-lab/Projeto-Limiar/blob/f9ec420a3d4d45cf0a9d949c1adc1e0e613e29ff/mobile/bug-bounty/lab/politica.json)
3. **Escreva e confira seu relato em 10 minutos.** Registre o ID do caso, a decisão observada e a regra que ela contraria. Sugira uma correção pequena e indique como verificar que a leitura pela pessoa proprietária continua funcionando. Compare sua versão com o gabarito depois de escrever. Guarde o resultado como prática. [Modelo de relatório](https://github.com/kingmaker-lab/Projeto-Limiar/blob/f9ec420a3d4d45cf0a9d949c1adc1e0e613e29ff/mobile/bug-bounty/MODELO-RELATORIO.md) · [Gabarito](https://github.com/kingmaker-lab/Projeto-Limiar/blob/f9ec420a3d4d45cf0a9d949c1adc1e0e613e29ff/mobile/bug-bounty/lab/GABARITO.md)

Use esta ficha nas próximas sessões:

```text
Programa e link da política
Data da consulta e ativo exato
Métodos permitidos, restrições e canal de envio
Pergunta que estou tentando responder
Evidência que já tenho
Dúvida pendente e próxima ação
```

Uma boa próxima ação cabe em uma linha, como “confirmar se a versão móvel está listada” ou “escrever o resultado observado com referência ao caso”. Essa frase preserva o contexto quando o aparelho fecha uma aba ou quando você precisa encerrar a sessão.

## 3. Quando vale usar o Recon no Termux

Com duas ou três URLs, a comparação manual cabe na ficha. Quando uma lista começa a acumular duplicatas, o Recon da Mobile Division pode comparar as origens com um arquivo de escopo e devolver um inventário JSON. A ferramenta trabalha com URLs já coletadas e preserva somente esquema, host e porta. Caminhos, parâmetros e fragmentos ficam de fora da saída. Isso reduz o volume de dados que você precisa revisar no telefone. [Recon offline · instalação e arquivos de exemplo](https://github.com/kingmaker-lab/Projeto-Limiar/blob/d994d54db652e1897c75041f2c2cdec8898b5099/mobile/recon/README.md)

Com os arquivos de exemplo baixados, execute na pasta da ferramenta:

```sh
python3 recon.py --scope escopo.exemplo.txt --urls urls.exemplo.txt
```

O exemplo devolve quatro origens distintas, duas com correspondência exata. Cada correspondência cobre apenas o que você registrou no arquivo. Leia separadamente as regras sobre caminhos, curingas, contas e técnicas. A CLI foi testada em Linux e o roteiro Android aguarda validação em aparelho. Se você estiver em iPhone ou iPad, faça a mesma comparação em uma nota com as colunas “origem”, “regra” e “pendência”.

## 4. Da prática ao primeiro relatório elegível

Ao voltar ao programa real, confirme a versão da política e se a atividade pretendida está autorizada para aquele ativo. Se a regra estiver ambígua, anote a dúvida e peça esclarecimento pelo canal do programa antes de testar. Trabalhe com dados e contas próprios quando permitido. Preserve a evidência mínima e use o canal privado indicado.

Estruture o relato em três partes. **Esperado** descreve a regra que deveria valer. **Observado** descreve o que você confirmou e em que condições. **Impacto** explica quem seria afetado e até onde a evidência sustenta essa conclusão. No Caderno, por exemplo, a política escrita permite uma ação incompatível com a regra de negócio. O efeito sobre um rascunho seria possível se o aplicativo adotasse a configuração. Essa distinção dá a quem recebe o relato uma pergunta verificável. [Orientações de envio de relatórios](https://docs.hackerone.com/en/articles/8473994-submitting-reports)

## 5. Como saber se o método está funcionando

Ao fim de cada sessão, escolha uma evidência do seu progresso: um ativo cujo escopo você conseguiu explicar, uma conclusão corrigida após revisão ou um relato que outra pessoa poderia entender sem conversar com você. Registre também uma limitação concreta do aparelho, quando ela interferir. Depois de algumas sessões, esse histórico mostra quais etapas ficaram mais rápidas com o método e quais realmente precisam de outra máquina.

A ficha, a hipótese e o relato continuam úteis quando você ganha acesso a hardware melhor. Um computador pode ampliar o que você consegue medir. A clareza sobre **o que medir, com qual autorização e com que evidência** já pode ser construída na tela que você tem hoje.
