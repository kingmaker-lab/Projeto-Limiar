# Do Termux a Bug Hunter

Dez ferramentas offline para transformar arquivos que você já tem em um inventário revisado, uma linha do tempo e um rascunho de relatório. O exemplo acompanha o Caderno, uma aplicação fictícia. Você pode executar todos os comandos com o próprio celular ou tablet Android.

## Prepare o Termux

Requer Python 3.9 ou posterior. Instale Git e Python e abra a pasta do kit:

```sh
pkg install git python
git clone https://github.com/kingmaker-lab/Projeto-Limiar.git limiar-kit
cd limiar-kit
if [ ! -f mobile/recon/kit.py ]; then
    git switch feat/mobile-recon
fi
cd mobile/recon
```

Depois de instalar os pacotes e copiar o repositório, os comandos funcionam offline. Os arquivos de entrada ficam nesta pasta e em [exemplos](exemplos/). Cada comando pode rodar por conta própria.

## Rode sua primeira prática

```sh
sh pratica.sh
```

O comando imprime o caminho de uma pasta nova com os resultados das dez ferramentas. Comece por `caderno.md` para revisar o escopo e termine em `relatorio.md` para comparar o resultado esperado com o observado. A prática calcula o hash da resposta fictícia original e verifica a cópia criada na pasta. Cada execução cria uma pasta própria, inclusive quando você roda o mesmo exercício de novo. Passe o caminho de uma pasta existente como argumento para escolher onde guardar os resultados.

## Revise o escopo e o contrato

### 1. Inventário de escopo

```sh
python3 recon.py --scope escopo.exemplo.txt --urls urls.exemplo.txt --format markdown
```

Compare as quatro origens de exemplo com a lista fornecida. Duas correspondem. As caixas do caderno servem para marcar o que você conferiu na política. Para salvar, acrescente `> caderno.md`. Para usar JSON, omita `--format markdown`.

### 2. Explorador passivo de endpoints

```sh
python3 endpoints.py openapi.exemplo.json
```

A saída lista três operações declaradas no contrato local. Observe como `GET` e `POST` na mesma rota aparecem separadamente. Parâmetros ficam no formato documentado e referências externas permanecem pendentes.

### 3. Comparador de escopo

```sh
python3 kit.py diff-escopo escopo.exemplo.txt exemplos/escopo-revisado.txt
```

Leia primeiro a versão antiga, depois a nova. A revisão fictícia inclui `https://docs.example.com` e remove `https://api.example.com:8443`. Use essa diferença para atualizar seu caderno após conferir a política vigente.

### 4. Comparador de contratos de API

```sh
python3 kit.py diff-api openapi.exemplo.json exemplos/openapi-revisada.json
```

A revisão acrescenta `GET /status` e retira `POST /rascunhos`. O resultado descreve o que mudou na documentação. Consulte também o campo de referências pendentes para saber quais trechos ficaram fora da comparação.

## Organize a evidência

### 5. Revisor de cabeçalhos

```sh
python3 kit.py revisar-cabecalhos exemplos/resposta-http.txt
```

Use um arquivo de texto com uma linha de status HTTP seguida dos cabeçalhos de uma única resposta. O comando mostra o status e quais cabeçalhos da lista de revisão estão presentes ou ausentes naquela resposta. A ausência indica um ponto para examinar no contexto da aplicação. O conteúdo após a linha em branco fica fora da análise.

### 6. Resumo de cabeçalhos para revisão

```sh
python3 kit.py resumo-cabecalhos exemplos/resposta-http.txt
```

A saída contém só o status e a contagem dos nomes selecionados na lista fixa. Confira que o valor fictício do cookie, os valores dos cabeçalhos e o corpo ficaram de fora. Revise a saída antes de anexá-la e mantenha a captura original em local privado.

### 7. Impressão digital da evidência

```sh
python3 kit.py hash-evidencia exemplos/resposta-http.txt
```

Registre o SHA-256 de 64 caracteres e o tamanho do arquivo. Para evidências próprias, calcule o hash da versão que pretende guardar ou compartilhar. Qualquer edição muda o resultado.

### 8. Verificador de integridade

```sh
python3 kit.py verificar-evidencia exemplos/resposta-http.txt 64dcd5de9b22f8b77c6a94e434c5b65ebe040bea9ca43458bcb8df5a15c727b2
```

O segundo argumento é o hash conhecido da cópia de exemplo. Para seu arquivo, use o hash registrado no passo anterior. O comando encerra com código 1 se os bytes divergirem. Faça a comparação com o valor guardado no momento em que registrou a evidência.

### 9. Linha do tempo

```sh
python3 kit.py linha-do-tempo exemplos/eventos.csv
```

Use CSV com as colunas `quando,evento` e datas ISO 8601 com fuso explícito. O comando ordena os eventos e converte os horários para UTC. No exemplo, a política foi conferida às 12:03 UTC e o rascunho foi revisado às 12:18 UTC.

## Prepare o relato

### 10. Gerador de rascunho

```sh
python3 kit.py rascunho exemplos/ficha.json > relatorio.md
cat relatorio.md
```

Copie a ficha JSON e preencha os campos com texto. O Markdown mantém o esperado, o observado e o impacto em seções próprias. Campos vazios aparecem como `[A preencher]`. Na ficha de treino, o impacto depende da aplicação da política fictícia. Em um relatório real, revise as afirmações, confira a autorização e envie pelo canal privado indicado pelo programa.

O exercício termina quando você consegue apontar a mudança de escopo, verificar a integridade do arquivo e explicar uma observação no rascunho. Para conferir a instalação, rode `python3 -m unittest -v`.
