# Um painel de 4 × 4 pixels

Imagine uma bancada em que um emissor manda um ícone de 4 × 4 pixels para um painel. Cada pixel ocupa um bit. As quatro linhas, lidas da esquerda para a direita e de cima para baixo, formam um único bloco de 16 bits. O emissor transforma o bloco com o Ouroboros. O canal simulado leva dois bytes. O receptor usa a mesma chave de exemplo para recuperar o desenho.

Na raiz do projeto:

```sh
python3 -m ouroboros.phase2.demo
```

O script roda offline, com um ícone e uma chave sintéticos fixos. Depois de mostrar o percurso normal, ele altera um bit nos dois bytes recebidos. O receptor ainda produz um quadro, agora diferente. Esse segundo percurso mostra a diferença entre recuperar um bloco e verificar a integridade de uma mensagem. Para proteger dados reais, use um esquema AEAD estabelecido.
