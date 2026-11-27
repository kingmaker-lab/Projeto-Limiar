# Recon offline · Inventário de escopo pelo celular

Ferramenta de linha de comando para organizar URLs que você já coletou. Compara as origens com uma lista de escopo declarada por você, remove duplicatas e produz um inventário JSON. Funciona sem conexão depois que os arquivos e o Python estiverem instalados. A ferramenta lê apenas arquivos locais.

## Executar no Android com Termux

Requer Python 3.9 ou posterior. No Termux, baixe o repositório e abra a pasta da ferramenta:

```sh
pkg install git python
git clone https://github.com/kingmaker-lab/Projeto-Limiar.git limiar-recon
cd limiar-recon
if [ ! -f mobile/recon/recon.py ]; then
    git switch feat/mobile-recon
fi
cd mobile/recon
```

Execute o exemplo:

```sh
python3 recon.py --scope escopo.exemplo.txt --urls urls.exemplo.txt
```

O exemplo classifica quatro origens. Duas correspondem à lista. HTTP e HTTPS são origens diferentes, assim como um domínio e seu subdomínio. Para salvar o resultado, acrescente `> inventario.json`. Execute os testes com `python3 -m unittest -v`.

## Usar com seu próprio inventário

1. Crie `escopo.txt` com uma origem HTTP ou HTTPS por linha, conforme a política atual do programa. Inclua a porta quando o programa definir uma porta específica.
2. Crie `urls.txt` com uma URL por linha. Linhas vazias e comentários iniciados com `#` são aceitos nos dois arquivos. Evite guardar URLs com segredos nos arquivos de entrada.
3. Execute `python3 recon.py --scope escopo.txt --urls urls.txt`. Revise `matched` e `unmatched` antes de usar o inventário.

A saída conserva somente esquema, host e porta. Caminho, parâmetros e fragmento são descartados. A correspondência é exata após a normalização da origem, incluindo a remoção de portas padrão. Uma entrada inválida interrompe a exportação e informa arquivo e linha.

Se uma regra usa curingas, caminhos ou restrições de técnica, confira a política manualmente. `matched` indica correspondência com o arquivo fornecido. A autorização depende das regras do programa.
