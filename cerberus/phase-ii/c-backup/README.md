# CERBERUS · Backup SQLite em C

Ferramenta de linha de comando em C17 para copiar um banco ativo do CERBERUS em Debian. Usa a API de backup do SQLite para incluir transações confirmadas no WAL e obter um arquivo autossuficiente.

## Compilar e testar

Dependências Debian: `build-essential`, `libsqlite3-dev` e `python3`. Na raiz da FASE II:

```sh
make -C c-backup test
```

## Operação

Use um diretório privado e um nome de destino novo. Mantenha uma cópia da chave do operador separada do backup do banco.

```sh
c-backup/cerberus-backup estado.sqlite copia.sqlite
python3 -m cerberus --key operador.key --db copia.sqlite status
```

O segundo comando autentica a revisão ativa da cópia com a chave já utilizada pelo CERBERUS. Para ensaiar a recuperação, copie o backup verificado para um novo caminho operacional e inicialize o serviço apontando para esse caminho. Preserve o backup original para futuras recuperações.

## Propriedades e limites

- A ferramenta abre a origem sem criar um banco ausente. Copia para um temporário privado de modo 0600 no diretório de destino.
- Antes de publicar, executa `PRAGMA quick_check(1)`, confirma a leitura da revisão mais recente, fecha o SQLite e sincroniza o arquivo.
- A publicação por link físico recusa um destino existente. O temporário fica no mesmo filesystem do destino e o diretório é sincronizado após a publicação. Se a sincronização final falhar, o nome pode existir e a ferramenta retorna erro.
- O backup valida a estrutura do SQLite. A autenticação da revisão ativa depende do comando `status` e da chave preservada. A sequência numérica do banco restaurado também precisa ser comparada com um registro externo quando houver risco de restaurar uma cópia antiga.
- Uma interrupção abrupta pode deixar um arquivo `.partial.*`. Recupere somente a partir de uma cópia publicada e autenticada. O diretório deve ficar sob controle do operador.

## Resultado reproduzido

Três testes passaram no Debian 13.6. O primeiro copiou uma revisão confirmada no WAL enquanto outra transação mantinha uma alteração pendente, removeu o banco de origem descartável e autenticou a revisão na cópia. Na cópia, PHOENIX criou a geração 2 a partir da revisão 0. Os demais testes verificaram destino preexistente e rejeição de origem ausente, corrompida ou de outro esquema.

A perda tolerada depende da frequência dos backups. Este ensaio comprova recuperação funcional em um banco pequeno. RPO e RTO sob carga representativa continuam por medir.
