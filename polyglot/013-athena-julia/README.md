# Athena

Monte Carlo Bernoulli com semente explícita e intervalo de Wilson de 95%. O consumo de memória é independente do número de amostras. A medição inclui a primeira chamada e o custo de compilação JIT associado.

## Executar

Requisitos de execução e compilação. Julia 1.10+ com Random e Test.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
julia --startup-file=no main.jl 10000 0.4 42
julia --startup-file=no main.jl 1000000 0.4 42
```

## Testar

```sh
mkdir -p .build
julia --startup-file=no test.jl
```

Licença [MIT](../LICENSE).
