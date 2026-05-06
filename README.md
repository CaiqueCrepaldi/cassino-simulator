# 🎰 Cassino Simulator - Simulador de Jogos de Cassino

Um simulador educativo de cassino desenvolvido em Python com interface gráfica moderna usando **CustomTkinter**. O projeto implementa dois jogos com sistema realista de apostas e banca virtual, sem envolver dinheiro real.

---

## 📋 Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Jogos Disponíveis](#jogos-disponíveis)
- [Instruções de Uso](#instruções-de-uso)
- [Mecânica dos Jogos](#mecânica-dos-jogos)
- [Estrutura do Código](#estrutura-do-código)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)

---

## ✨ Características

- 🏠 **Menu Principal**: Tela de seleção com acesso aos três jogos
- 🎰 **Slot Machine**: Jogue nos caça-níqueis com 3 símbolos e animação de giro
- ✈️ **Aviator**: Aposte e retire antes do avião voar embora — mecânica idêntica ao jogo real
- 🎡 **Double**: Roda com 14 segmentos (Preto, Vermelho e Branco) — igual ao Double real
- 💰 **Sistema de Banca Virtual**: R$ 1.000,00 iniciais por jogo, sem dinheiro real envolvido
- 📊 **Probabilidades Realistas**: Distribuição exponencial no Aviator, pesos ponderados no Slot, 14 segmentos reais no Double
- 🎪 **Animações em Tempo Real**: Canvas animado no Aviator; roda giratória com desaceleração no Double; animação de giro no Slot
- 📈 **Estatísticas em Tempo Real**: Tentativas, vitórias, taxa de sucesso e maior multiplicador
- 🔄 **Reinício Independente**: Cada jogo pode ser resetado sem afetar o outro

---

## 🛠️ Requisitos

- **Python 3.8+**
- **CustomTkinter** (GUI framework)
- **tkinter** (incluído com Python)
- **Módulos padrão**: `random`, `time`, `math`

---

## 📦 Instalação

### 1. Clonar ou Baixar o Projeto

```bash
git clone https://github.com/CaiqueCrepaldi/cassino-simulator.git
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install customtkinter
```

---

## 🚀 Como Executar

### Opção 1: Linha de Comando

```bash
python cassino.py
```

### Opção 2: Executar Direto no Windows

Clique duas vezes no arquivo `cassino.py` (se a extensão `.py` estiver associada com Python)

### Opção 3: Terminal PowerShell (Windows)

```powershell
python .\cassino.py
```

O **Menu Principal** abrirá automaticamente. A partir dele, selecione o jogo desejado.

---

## 🎮 Jogos Disponíveis

### 🎰 Slot Machine
Gire os 3 slots e tente obter 3 símbolos iguais. Cada símbolo possui uma probabilidade e um multiplicador de prêmio diferente.

### ✈️ Aviator
Aposte antes do voo começar. O multiplicador sobe enquanto o avião voa — clique em **RETIRAR** a tempo para embolsar o ganho. Se o avião voar antes de você retirar, a aposta é perdida.

### 🎡 Double
Escolha uma cor (Preto, Vermelho ou Branco) e gire a roda com 14 segmentos. Se a roda parar na cor apostada, você ganha o multiplicador correspondente. O Branco é raríssimo e paga 14×.

---

## 🕹️ Instruções de Uso

### Menu Principal

1. Execute o programa — a tela de seleção abre automaticamente
2. Escolha **🎰 SLOT MACHINE** ou **✈️ AVIATOR**
3. Cada jogo abre em uma janela própria (ambos podem rodar ao mesmo tempo)

---

### 🎰 Slot Machine — Passo a Passo

**Passo 1:** Veja sua banca inicial de R$ 1.000,00 no topo da janela

**Passo 2:** Digite o valor da aposta no campo **"Valor da Aposta (R$)"**
- Deve ser maior que 0
- Não pode exceder a banca atual

**Passo 3:** Clique em **"🎰 GIRAR SLOTS 🎰"** e aguarde a animação (1,5 segundos)

**Passo 4:** Veja o resultado — 3 iguais = vitória 🎉, caso contrário = derrota ❌

**Passo 5 (opcional):** Clique em **"🔄 NOVO JOGO"** para resetar banca e estatísticas

---

### ✈️ Aviator — Passo a Passo

**Passo 1:** Defina o valor da aposta no campo ou use os botões de atalho (+10, +25, +50, +100)

**Passo 2:** Clique em **"✈️ APOSTAR & VOAR"** — a aposta é descontada imediatamente e o avião decola

**Passo 3:** Observe o multiplicador subindo em tempo real no canvas

**Passo 4:** Clique em **"💰 RETIRAR"** antes do crash para embolsar:
```
Ganho = Aposta × Multiplicador atual
```

**Passo 5:** Se não retirar a tempo → crash! A aposta é perdida

**Passo 6 (opcional):** Clique em **"🔄 NOVO JOGO"** para resetar banca e histórico

---

### 🎡 Double — Passo a Passo

**Passo 1:** Veja sua banca inicial de R$ 1.000,00 no topo da janela

**Passo 2:** Digite o valor da aposta ou use os atalhos (+10, +25, +50, +100)

**Passo 3:** Clique em uma das cores para selecionar sua aposta:
- ⚫ **PRETO** — paga 2× se acertar
- 🔴 **VERMELHO** — paga 2× se acertar
- ⬜ **BRANCO** — paga 14× se acertar (muito raro!)

**Passo 4:** Clique em **"🎡 GIRAR"** — a roda gira com desaceleração progressiva

**Passo 5:** O segmento central (marcado com borda dourada) define o resultado

**Passo 6 (opcional):** Clique em **"🔄 NOVO JOGO"** para resetar banca e histórico

---

## 🎲 Mecânica dos Jogos

### 🎰 Slot Machine

#### Símbolos, Probabilidades e Multiplicadores

| Símbolo | Chance por slot | Multiplicador | Tipo |
|---------|----------------|---------------|------|
| 🔥 Fogo | 40% | 2× | Mais comum |
| ⭐ Estrela | 35% | 2× | Intermediário |
| 🤑 Dinheiro | 25% | 3× | Jackpot (raro) |

#### Probabilidades Reais de Vitória (3 iguais)

| Combinação | Cálculo | Chance |
|-----------|---------|--------|
| 3 × 🔥 | 0.40³ | 6,40% |
| 3 × ⭐ | 0.35³ | 4,29% |
| 3 × 🤑 | 0.25³ | 1,56% |
| **Total** | | **~12,25%** |

#### Cálculo de Prêmio

```
Vitória → Ganho = Aposta × Multiplicador do símbolo
Derrota → Perda = Aposta
```

---

### ✈️ Aviator

#### Como o Multiplicador Cresce

O multiplicador começa em **1,00×** e sobe de forma exponencial a cada 100 ms. O crescimento acelera conforme o valor aumenta — igual ao comportamento do jogo original.

#### Geração do Ponto de Crash

O crash é gerado com **distribuição exponencial** antes do voo começar (o jogador não sabe quando vai acontecer):

```
crash = 0.99 / (1 - u × 0.99)    onde u ∈ [0, 1) aleatório
```

Isso resulta em:
- Maioria dos crashes entre **1× e 3×** (crashes frequentes e baixos)
- Crashes acima de **10×** são raros
- Máximo limitado a **100×** na UI

#### Histórico de Crashes

O painel lateral exibe os últimos 8 crashes com código de cores:

| Cor | Faixa |
|-----|-------|
| 🔴 Vermelho | Abaixo de 2× |
| 🟡 Amarelo | Entre 2× e 5× |
| 🟢 Verde | Acima de 5× |

#### Atalhos de Aposta

Botões **+10 / +25 / +50 / +100** somam ao valor atual no campo de aposta, facilitando ajustes rápidos.

---

### 🎡 Double

#### Segmentos da Roda

A roda possui **14 segmentos** com a seguinte distribuição, igual ao Double real:

| Cor | Segmentos | Chance | Multiplicador |
|-----|-----------|--------|---------------|
| ⚫ Preto | 7/14 | ~50,0% | 2× |
| 🔴 Vermelho | 6/14 | ~42,8% | 2× |
| ⬜ Branco | 1/14 | ~7,1% | 14× |

#### Como o Resultado é Gerado

O resultado é sorteado **antes** da animação começar, garantindo imparcialidade total. A roda faz pelo menos 3 voltas completas e para com precisão no segmento sorteado, usando desaceleração progressiva nos últimos passos — igual ao comportamento do Double real.

#### Histórico

O painel exibe os últimos 10 resultados com os emojis de cada cor para referência rápida.

---

## 💻 Estrutura do Código

### Visão Geral das Classes

```
cassino.py
│
├── MenuPrincipal          ← Tela inicial de seleção
│   ├── abrir_slots()      ← Abre janela do Slot Machine
│   ├── abrir_aviator()    ← Abre janela do Aviator
│   └── abrir_double()     ← Abre janela do Double
│
├── CassinoSimulator       ← Jogo 1: Slot Machine
│   ├── girar()
│   ├── animacao_giro()
│   ├── mostrar_resultado()
│   └── resetar_estatisticas()
│
├── AviatorGame            ← Jogo 2: Aviator
│   ├── iniciar_rodada()
│   ├── _tick()            ← Loop de animação (a cada 100ms)
│   ├── _crash()           ← Finaliza o voo
│   ├── retirar()          ← Cashout antecipado
│   ├── _gerar_crash()     ← Distribuição exponencial
│   └── resetar()
│
└── DoubleGame             ← Jogo 3: Double
    ├── girar()
    ├── _desenhar_roda()   ← Renderiza os 14 segmentos no canvas
    ├── _animar()          ← Loop com desaceleração progressiva
    ├── _mostrar_resultado()
    ├── _selecionar_cor()
    └── resetar()
```

### Fluxo do Aviator

```
1. Jogador define aposta
         ↓
2. Clica em APOSTAR & VOAR
         ↓
3. Aposta descontada da banca
         ↓
4. Crash gerado internamente (oculto)
         ↓
5. _tick() roda a cada 100ms → multiplicador sobe
         ↓
    ┌────┴────┐
    │         │
Retirou    Não retirou
    │         │
Ganho =   _crash() →
Aposta ×   Perdeu a
Mult atual  aposta
```

---

### Fluxo do Double

```
1. Jogador escolhe a cor (Preto / Vermelho / Branco)
         ↓
2. Define a aposta e clica em GIRAR
         ↓
3. Aposta descontada da banca
         ↓
4. Resultado sorteado internamente (oculto)
         ↓
5. Roda anima: 3 voltas + desaceleração até o segmento sorteado
         ↓
6. Segmento central (borda dourada) = resultado
         ↓
    ┌────┴────┐
    │         │
  Acertou   Errou
    │         │
Ganho =    Perdeu
Aposta ×   a aposta
Mult
```

---

## 🎨 Customização

### Alterar Banca Inicial

Em ambas as classes (`CassinoSimulator` e `AviatorGame`):
```python
self.banca = 1000.00  # altere para o valor desejado
```

### Alterar Velocidade do Aviator

```python
INTERVALO_MS = 100   # menor = mais rápido (padrão: 100ms)
CRESCIMENTO   = 0.05 # maior = multiplicador sobe mais depressa
```

### Alterar Multiplicadores do Slot

Em `mostrar_resultado()`:
```python
multiplicador = 2  # para 🔥 e ⭐
multiplicador = 3  # para 🤑 (jackpot)
```

### Alterar Velocidade da Roda (Double)

Em `DoubleGame`:
```python
TICK_MS   = 30   # ms entre frames (menor = mais rápido)
```

### Alterar Cores

Principais hexadecimais usados:
| Cor | Código | Onde |
|-----|--------|------|
| Preto (fundo) | `#000000` | Frames principais |
| Vermelho (Slot) | `#CC0000` | Botão girar |
| Azul (Aviator) | `#0055CC` | Botão apostar |
| Laranja (Retirar) | `#CC7700` | Botão cashout |
| Roxo (Double) | `#6600CC` | Botão girar Double |
| Verde (ganho) | `#00FF00` | Banca / vitória |

---

## 🔒 Avisos Importantes

> ⚠️ **Este é um SIMULADOR EDUCATIVO apenas**
> - Não envolve dinheiro real
> - Não deve ser usado como referência para apostas reais
> - Desenvolvido exclusivamente para fins acadêmicos

---

## 📝 Padrões de Código

- Comentários em **inglês** (padrão profissional de desenvolvimento)
- Interface em **português brasileiro**
- Código orientado a objetos com classes separadas por responsabilidade

---

## 📄 Licença

Código educativo de livre uso para estudo e modificação.

---

## 👨‍💻 Autor

Desenvolvido como projeto acadêmico de Python com CustomTkinter.

---

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique se o Python 3.8+ está instalado: `python --version`
2. Confirme a instalação do CustomTkinter: `pip show customtkinter`
3. Tente recriar o ambiente virtual e reinstalar as dependências
4. Execute em um terminal aberto especificamente para este projeto

---

**Versão**: 3.0.0
**Data**: Maio 2026
**Status**: Funcional e Testado ✅
**Novidades v3.0**: Jogo Double · Roda animada com 14 segmentos · Correção de bug na exibição do resultado
**Novidades v2.0**: Menu Principal · Jogo Aviator · Canvas animado · Histórico de crashes
