# Gaita de Bolso

**Abrir:** https://demma.github.io/Pocket-Harmonica-Guide/

App instalável (PWA) para gaita diatônica de 10 furos (afinação Richter):

- mapa de notas em 12 tons;
- qual gaita usar em cada posição;
- lições do primeiro furo ao overblow;
- riffs de blues na 2ª posição;
- músicas de domínio público com tablatura gerada automaticamente.

Funciona offline depois de instalado.

- iPhone (Safari): Compartilhar → Adicionar à Tela de Início
- Android (Chrome): menu ⋮ → Instalar app

## Estrutura

- `app.html` é a fonte única (HTML + CSS + JS). `python3 build.py` gera `index.html` e atualiza o nome do cache offline a partir de `APP_VERSION`.
- Notação da tablatura:

  | Símbolo | Significado |
  |---|---|
  | `+4` | sopro |
  | `-4` | puxada |
  | `-3'` | bend (cada `'` abaixa meio tom) |
  | `+6o` | overblow |
  | `-7o` | overdraw |
  | `(-123)` | acorde |
  | `_` | pausa |
  | `:2` | duração em tempos |

- O mapa de notas, os bends possíveis e as tablaturas das músicas são calculados a partir da afinação Richter. Uma tablatura impossível, como um bend que não existe naquele furo, gera erro.

A cada mudança: aumente `APP_VERSION`, registre no `CHANGELOG` e rode `python3 build.py`.
