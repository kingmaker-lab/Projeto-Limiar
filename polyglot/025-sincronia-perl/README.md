# Sincronia

Corrige deslocamento e deriva de legendas SRT por escala racional e deslocamento em milissegundos. Preserva o texto de cada bloco e normaliza quebras de linha para LF.

## Executar

Requisitos no Debian. Perl 5. Execute os comandos a partir deste diretório.

```sh
perl main.pl 100 1 2 < example.srt
```

A ordem é deslocamento, numerador e denominador opcionais. Aplica primeiro a escala, arredonda para o milissegundo mais próximo e soma o deslocamento. Se uma legenda torna-se inválida, o comando falha. Descarte a saída parcial e use um arquivo de destino separado.

## Testar

```sh
perl test.pl
```

Licença [MIT](../LICENSE).
