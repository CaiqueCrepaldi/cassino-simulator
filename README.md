# 🎰 Cassino Simulator

Um simulador educativo de cassino desenvolvido em Python com interface gráfica moderna usando **CustomTkinter**. O projeto conta com **8 jogos** completos, navegação em janela única e **banca compartilhada** entre todos os jogos, sem envolver dinheiro real.

---

## 📋 Índice

- [Características](#características)
- [Jogos Disponíveis](#jogos-disponíveis)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Banca Global](#banca-global)
- [Mecânica dos Jogos](#mecânica-dos-jogos)
- [Estrutura do Código](#estrutura-do-código)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)

---

## ✨ Características

- 🏠 **Menu Principal** com exibição da banca e botão de reset
- 🎰 **8 jogos** com mecânicas distintas e probabilidades realistas
- 💰 **Banca global compartilhada** — saldo único que persiste entre todos os jogos
- 🖼️ **Janela única** — navegação fluida sem abrir múltiplas janelas
- 📊 **Estatísticas em tempo real** em cada jogo (rodadas, vitórias, taxa)
- 🎪 **Animações** em canvas e labels em todos os jogos
- 🔄 **Reset por jogo** — cada jogo tem seu próprio botão "Novo Jogo"
- 📦 **Executável Windows** disponível (`dist/CassinoSimulator.exe`)

---

## 🎮 Jogos Disponíveis

| # | Jogo | Descrição curta |
|---|------|-----------------|
| 1 | 🎰 Slot Machine | Gire 3 slots e tente 3 símbolos iguais |
| 2 | ✈️ Aviator | Retire antes do avião crashar para embolsar o multiplicador |
| 3 | 🎡 Double | Roda com 14 segmentos — Preto (2×), Vermelho (2×), Branco (14×) |
| 4 | 🎲 Crash Dice | Escolha até 3 números e role 2 dados — dupla, soma ou face |
| 5 | 🎠 Roleta | Roleta europeia com 37 números e múltiplos tipos de aposta |
| 6 | 🪙 Coin Flip | Cara ou coroa — simples e direto |
| 7 | 🃏 Blackjack | 21 contra o dealer com Hit, Stand, Double Down e Split |
| 8 | 🎴 Baccarat | Jogador vs Banker — aposte no vencedor ou no empate |

---

## 🛠️ Requisitos

- **Python 3.10+**
- **CustomTkinter** (`pip install customtkinter`)
- **tkinter** (incluído com Python)
- **Módulos padrão**: `random`, `time`, `math`

---

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/CaiqueCrepaldi/cassino-simulator.git
cd cassino-simulator
```

### 2. Criar ambiente virtual (recomendado)

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install customtkinter
```

---

## 🚀 Como Executar

### Opção 1 — Python direto

```bash
python main.py
```

### Opção 2 — Executável Windows (sem Python)

Clique duas vezes em `dist/CassinoSimulator.exe` — nenhuma instalação necessária.

### Opção 3 — PowerShell

```powershell
python .\main.py
```

O **Menu Principal** abre automaticamente. Escolha um jogo, jogue e volte ao menu com o botão **← Menu**.

---

## 💰 Banca Global

O simulador mantém **uma única banca compartilhada** entre todos os jogos:

- Banca inicial: **R$ 1.000,00**
- O saldo é exibido no **menu principal** e dentro de cada jogo
- Ganhos e perdas em qualquer jogo refletem imediatamente no saldo global
- **Menu → botão "Resetar Banca"**: zera e redefine para R$ 1.000,00
- **Cada jogo → botão "Novo Jogo"**: também reseta a banca para R$ 1.000,00

---

## 🎲 Mecânica dos Jogos

### 🎰 Slot Machine

Gire 3 slots e torça por 3 símbolos iguais.

| Símbolo | Chance por slot | Multiplicador |
|---------|----------------|---------------|
| 🔥 Fogo | 40% | 2× |
| ⭐ Estrela | 35% | 2× |
| 🤑 Dinheiro | 25% | 3× |

Chance total de vitória (3 iguais): **~12,25%**

---

### ✈️ Aviator

O multiplicador sobe a partir de **1,00×** enquanto o avião voa. Clique em **RETIRAR** antes do crash para embolsar `aposta × multiplicador`. O ponto de crash é gerado com distribuição exponencial — a maioria entre 1× e 3×, crashes acima de 10× são raros.

O jogo também suporta **saque automático**: defina um multiplicador-alvo e o cashout acontece automaticamente ao atingi-lo.

Histórico dos últimos crashes exibido com código de cores:
- 🔴 Abaixo de 2× · 🟡 Entre 2× e 5× · 🟢 Acima de 5×

---

### 🎡 Double

Roda com 14 segmentos igual ao Double real.

| Cor | Segmentos | Chance | Multiplicador |
|-----|-----------|--------|---------------|
| ⚫ Preto | 7/14 | ~50,0% | 2× |
| 🔴 Vermelho | 6/14 | ~42,8% | 2× |
| ⬜ Branco | 1/14 | ~7,1% | 14× |

Resultado sorteado antes da animação para garantir imparcialidade. A roda anima com pelo menos 3 voltas completas e desaceleração progressiva.

---

### 🎲 Crash Dice

Escolha até **3 números** (1–6) e role 2 dados. Regras de pagamento:

| Condição | Multiplicador |
|----------|---------------|
| Dupla exata (ambos os dados = número escolhido) | 5× |
| Soma dos dados = número escolhido | 3× |
| Um dado = número escolhido | 2× |
| Nenhum acerto | Perde a aposta |

---

### 🎠 Roleta

Roleta europeia com **37 números** (0–36). Tipos de aposta disponíveis:

| Tipo | Cobertura | Pagamento |
|------|-----------|-----------|
| Número exato | 1/37 | 35× |
| Cor (Vermelho/Preto) | 18/37 | 1× |
| Par/Ímpar | 18/37 | 1× |
| Baixo (1–18) / Alto (19–36) | 18/37 | 1× |
| Dúzia (1ª/2ª/3ª) | 12/37 | 2× |
| Coluna | 12/37 | 2× |

---

### 🪙 Coin Flip

Escolha **Cara** ou **Coroa**. Acertou → dobra a aposta (2×). Errou → perde a aposta. Probabilidade: 50/50.

---

### 🃏 Blackjack

Blackjack clássico contra o dealer com as seguintes opções:

- **Hit** — pega mais uma carta
- **Stand** — para com as cartas atuais
- **Double Down** — dobra a aposta e recebe exatamente mais uma carta
- **Split** — divide um par em duas mãos separadas

Blackjack natural paga **3:2**. Dealer bate em soft 17.

---

### 🎴 Baccarat

Aposte antes das cartas serem distribuídas:

| Aposta | Paga | Casa |
|--------|------|------|
| Jogador vence | 1× | ~1,24% |
| Banker vence | 0,95× (5% comissão) | ~1,06% |
| Empate | 8× | ~14,4% |

Regras de terceira carta do Baccarat aplicadas automaticamente.

---

## 💻 Estrutura do Código

```
basicos py/
│
├── main.py                 ← Ponto de entrada; classes Bank e App
├── menu.py                 ← MenuPrincipal (exibe banca + botão reset)
│
├── games/
│   ├── slot_machine.py     ← SlotMachine
│   ├── aviator.py          ← AviatorGame
│   ├── double.py           ← DoubleGame
│   ├── crash_dice.py       ← CrashDice
│   ├── roulette.py         ← RouletteGame
│   ├── coin_flip.py        ← CoinFlip
│   ├── blackjack.py        ← BlackjackGame
│   └── baccarat.py         ← BaccaratGame
│
├── CassinoSimulator.spec   ← Configuração PyInstaller
├── casino.ico              ← Ícone do executável
└── dist/
    └── CassinoSimulator.exe ← Executável Windows
```

### Padrão de navegação (janela única)

```
App (main.py)
 ├── Bank  ← banca global, passada a todos os jogos
 │
 ├── show_menu() → MenuPrincipal(root, container, show_game, bank)
 │
 └── show_game(name) → <Jogo>(root, container, show_menu, bank)
```

Cada jogo expõe `self.balance` como `@property` que lê/escreve `self.bank.balance`, mantendo toda a lógica de ganhos e perdas inalterada.

---

## 🔒 Aviso

> ⚠️ **Simulador educativo apenas** — não envolve dinheiro real e não deve ser usado como referência para apostas reais.

---

## 📄 Licença

Código educativo de livre uso para estudo e modificação.

---

## 👨‍💻 Autor

**Caique Crepaldi** — [@CaiqueCrepaldi](https://github.com/CaiqueCrepaldi)

---

**Versão**: 4.0.0  
**Data**: Maio 2026  
**Status**: Funcional e Testado ✅  
**Novidades v4.0**: Banca global compartilhada · Exibição da banca no menu · Botão de reset no menu  
**Novidades v3.x**: Blackjack · Baccarat · Roleta · Coin Flip · Crash Dice · Janela única · Tela cheia  
**Novidades v2.0**: Aviator · Double · Menu Principal
