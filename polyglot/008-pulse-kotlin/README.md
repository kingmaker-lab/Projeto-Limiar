# Pulse

Aplicativo nativo para Android 6 ou superior. Consulta RAM, espaço do volume do app, núcleos e bateria com APIs públicas e zero permissões declaradas. Use um dispositivo físico para evitar o custo do emulador.

## Executar

Requisitos de execução e compilação. JDK 17, Gradle 8.9 e SDK Android 35.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
gradle --no-daemon assembleDebug
gradle --no-daemon installDebug
```

## Testar

```sh
mkdir -p .build
gradle --no-daemon testDebugUnitTest
```

Licença [MIT](../LICENSE).
