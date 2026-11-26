# CERBERUS · Testemunha de continuidade em Ruby

A testemunha detecta se um banco voltou a uma versão anterior à última observada, perdeu uma revisão intermediária ou passou a ter um histórico diferente no trecho já observado. Pode ser usada para examinar uma cópia antes de colocá-la em operação.

## Rodar no Debian

Requer Ruby e Python 3, sem gems externas. Execute da raiz da FASE II com um banco CERBERUS inicializado:

```sh
ruby ruby-witness/witness.rb init /caminho/independente/ancora.json estado.sqlite operador.key
ruby ruby-witness/witness.rb verify /caminho/independente/ancora.json copia.sqlite operador.key
ruby ruby-witness/witness.rb advance /caminho/independente/ancora.json estado.sqlite operador.key
python3 -m unittest discover -s ruby-witness -v
```

`init` estabelece a primeira geração confiável. `verify` verifica o prefixo e informa a geração encontrada. `advance` substitui a âncora somente após verificar todo o histórico autenticado. Se não houver âncora, `verify` e `advance` recusam a operação.

## Arquitetura

1. Python lê o banco em uma transação e exporta as revisões em JSON canônico, uma por linha, usando a autenticação HMAC já existente.
2. Ruby verifica a continuidade das gerações, calcula o SHA-256 incremental e compara o prefixo até a geração da âncora. O processo pai só aceita o resultado após a saída bem-sucedida do exportador.
3. Um arquivo de bloqueio serializa operadores da mesma âncora. O avanço grava em temporário privado, sincroniza o arquivo, publica por renomeação e sincroniza o diretório.

A confiança começa em `init`. Guarde a âncora e seu arquivo de bloqueio em um diretório privado que o operador de restauração do banco não possa substituir. Uma cópia antiga que ainda contém todo o prefixo ancorado só passa se todas as suas revisões forem válidas. Alterações posteriores ao último avanço podem escapar à detecção de regressão. A testemunha não protege contra um agente que controle tanto o banco quanto a âncora. A verificação percorre todas as revisões e mantém o bloqueio de escrita do SQLite durante a leitura.

## Testes

Quatro testes passaram no Debian 13.6 com Ruby 3.3.13. Cobrem avanço, restauração antiga, divergência autenticada na mesma geração, lacuna no histórico e falha HMAC. Testes de recusa verificam que a âncora persiste sem alteração.
