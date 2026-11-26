# CERBERUS · Motor determinístico de admissão em Lua

Motor Lua 5.4 para analisar efeitos de política e sessões a partir de um arquivo de eventos. Pode reproduzir a mesma sequência e comparar estados e vereditos em toda mudança. O módulo `policy.lua` contém as regras de domínio. `replay.lua` adapta entrada e saída por linhas, sem carregar código fornecido no fluxo.

```sh
cd lua-policy
lua5.4 replay.lua <<'TRACE'
publish 0 off 1
admit alpha
admit beta
publish 1 on 1
release alpha
admit beta
publish 2 off 1
admit beta
TRACE
```

A saída registra geração, número de sessões ativas e veredito em TSV. Nesse exemplo, `beta` é recusada primeiro por capacidade, depois por manutenção, e admitida após a reabertura. Uma política nova entra somente quando a geração esperada coincide com a atual. Reduzir a capacidade ou ativar manutenção afeta novas admissões. Sessões existentes permanecem até `release`.

| Evento | Campos | Resultado |
| --- | --- | --- |
| `publish` | geração esperada, `on\|off`, limite 1–10000 | publica, recusa geração obsoleta ou sinaliza esgotamento |
| `admit` | identificador de sessão | aceita ou recusa duplicata, manutenção ou capacidade |
| `release` | identificador de sessão | libera a vaga ou informa sessão ausente |

Identificadores aceitam até 64 letras ASCII, dígitos, traços ou sublinhados. Entradas inválidas têm veredito `invalid` sem alterar o estado. Uma linha acima de 256 bytes encerra a reprodução com código 64. O motor roda em um único processo e mantém o estado em memória. A autenticação HMAC, persistência, recuperação e execução TCP ficam no CERBERUS principal.

## Testes

Da raiz da FASE II, execute `python3 -m unittest discover -s lua-policy -v`. Use `LUA` para indicar o caminho de outro executável Lua 5.4.

Três testes passaram no Debian 13.6 com Lua 5.4.7. A verificação diferencial compara 500 eventos com uma referência independente em Python, além de repetir a mesma entrada para confirmar determinismo. Os outros testes exercitam mudança de política com sessões abertas, geração obsoleta e limites de entrada.
