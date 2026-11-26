# Gabarito · Caderno

**Título sugerido:** a política proposta permite leitura de rascunho privado por outro membro.

Em `lab/politica.json`, o caso `C2` registra `permitir` para um membro classificado como `outra_pessoa`. A regra de negócio exige `negar`. Os casos `C1` e `C3` seguem a regra.

Se o aplicativo aplicar essa política, um membro poderia receber permissão de leitura sobre o rascunho de outra pessoa. A evidência observada é a decisão presente no arquivo fictício.

Ajuste `C2` para `negar`. Uma verificação de regressão deve preservar a leitura pela pessoa proprietária e confirmar a recusa para outros membros e visitantes.
