# 🎰 Cassino Simulator - Simulador de Jogo de Slots

Um simulador educativo de cassino desenvolvido em Python com interface gráfica moderna usando **CustomTkinter**. O projeto implementa um sistema realista de apostas com banca virtual, sem envolver dinheiro real.

---

## 📋 Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Instruções de Uso](#instruções-de-uso)
- [Mecânica do Jogo](#mecânica-do-jogo)
- [Estrutura do Código](#estrutura-do-código)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)

---

## ✨ Características

- 🎮 **Interface Gráfica Moderna**: Design elegante com tema escuro vermelho, branco e preto
- 💰 **Sistema de Banca Virtual**: R$ 1.000,00 iniciais para apostas simuladas
- 🎲 **3 Símbolos de Jogo**: 🔥 Fogo, ⭐ Estrela, 🤑 Dinheiro
- 📊 **Probabilidades Realistas**: Sistema de ponderação que simula um cassino real
- 🎪 **Animação de Giro**: Efeito visual realista dos slots girando
- 💵 **Sistema de Prêmios**: Multiplicadores diferentes para cada combinação vencedora
- 📈 **Estatísticas em Tempo Real**: Acompanhamento de tentativas, vitórias e taxa de sucesso
- 🔄 **Novo Jogo**: Opção para resetar e recomeçar com R$ 1.000,00
- ⚠️ **Validações Robustas**: Verificação de apostas inválidas e banca insuficiente

---

## 🛠️ Requisitos

- **Python 3.8+**
- **CustomTkinter** (GUI framework)
- **tkinter** (incluído com Python)
- **Módulos padrão**: `random`, `time`

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

Clique duas vezes no arquivo `cassino.py` (se a extensão .py estiver associada com Python)

### Opção 3: Terminal PowerShell (Windows)

```powershell
python .\cassino.py
```

A janela do aplicativo abrirá automaticamente com o jogo carregado.

---

## 🎮 Instruções de Uso

### Passo 1: Iniciar o Jogo
- Execute o programa conforme instruções acima
- Veja sua banca inicial de R$ 1.000,00 no topo da janela

### Passo 2: Definir a Aposta
- Digite o valor que deseja apostar no campo **"Valor da Aposta (R$)"**
- A aposta deve ser:
  - Maior que 0
  - Não pode exceder sua banca atual

### Passo 3: Girar os Slots
- Clique no botão **"🎰 GIRAR SLOTS 🎰"**
- Observe a animação dos slots girando
- O resultado será mostrado em 1.5 segundos

### Passo 4: Ver o Resultado
- Se ganhar 3 símbolos iguais: **vitória!** 🎉
- Se não conseguir: **derrota** ❌
- A banca é atualizada automaticamente

### Passo 5: Novo Jogo (Opcional)
- Clique em **"🔄 NOVO JOGO"** para resetar tudo
- Banca volta para R$ 1.000,00
- Estatísticas são zeradas

---

## 🎲 Mecânica do Jogo

### Símbolos e Probabilidades

| Símbolo | Chance | Multiplicador | Descrição |
|---------|--------|---------------|-----------|
| 🔥 Fogo | 40% | 2x | Mais comum, prêmio pequeno |
| ⭐ Estrela | 35% | 2x | Intermediário, prêmio pequeno |
| 🤑 Dinheiro | 25% | 3x | Raro (Jackpot), maior prêmio |

### Cálculo de Prêmios

**Vitória com 3 símbolos iguais:**
```
Ganho = Aposta × Multiplicador do Símbolo

Exemplo:
- Apostou: R$ 100
- Resultado: 🔥 🔥 🔥
- Ganho: 100 × 2 = R$ 200
- Nova Banca: Banca_anterior + 200
```

**Derrota:**
```
Perda = Aposta

Exemplo:
- Apostou: R$ 100
- Resultado: Não houve 3 iguais
- Perda: R$ 100
- Nova Banca: Banca_anterior - 100
```

### Probabilidades Reais de Vitória

Levando em conta que cada símbolo deve aparecer 3 vezes:

- **3 Fogos (🔥)**: 40% × 40% × 40% = **6.4% de chance**
- **3 Estrelas (⭐)**: 35% × 35% × 35% = **4.29% de chance**
- **3 Dinheiros (🤑)**: 25% × 25% × 25% = **1.56% de chance (Raro!)**
- **Chance total de vitória**: ~12.25% por rodada

---

## 📊 Interface e Componentes

### Seção de Banca
```
💰 Banca: R$ 1000.00
```
Mostra seu saldo atual em tempo real

### Seção de Apostas
```
Valor da Aposta (R$): [___________]
```
Campo para inserir o valor que deseja apostar

### Seção de Slots
```
    [❓]  [❓]  [❓]
```
Três slots que giram e mostram os resultados

### Seção de Controles
- 🎰 **GIRAR SLOTS**: Inicia a rodada
- 🔄 **NOVO JOGO**: Reseta o jogo completamente

### Seção de Resultados
Mostra mensagens de vitória/derrota e valores ganhos/perdidos

### Seção de Estatísticas
```
Tentativas: X | Vitórias: Y | Taxa de Sucesso: Z%
```
Acompanha suas estatísticas ao longo do jogo

---

## 💻 Estrutura do Código

### Classe Principal: `CassinoSimulator`

#### Atributos Principais
- `banca`: Valor atual da banca do jogador
- `aposta_atual`: Valor da aposta na rodada atual
- `symbols`: Lista com os 3 símbolos do jogo
- `weights`: Pesos para probabilidades ponderadas
- `tentativas`: Total de rodadas jogadas
- `vitorias`: Total de vitórias

#### Métodos Principais

| Método | Descrição |
|--------|-----------|
| `__init__()` | Inicializa a interface e componentes |
| `girar()` | Valida aposta e inicia a rodada |
| `animacao_giro()` | Cria efeito visual de giro |
| `mostrar_resultado()` | Calcula resultado e atualiza banca |
| `resetar_estatisticas()` | Reseta o jogo para começar novamente |

### Fluxo do Programa

```
1. Inicialização
   ↓
2. Usuário define aposta
   ↓
3. Clica em "GIRAR SLOTS"
   ↓
4. Validação da aposta
   ↓
5. Animação de giro (1.5s)
   ↓
6. Geração de resultado
   ↓
7. Cálculo de ganho/perda
   ↓
8. Atualização da banca
   ↓
9. Exibição de resultado
   ↓
10. Pronto para nova rodada
```

---

## 🎨 Customização

### Alterar Valor Inicial da Banca

Abra `cassino.py` e procure:
```python
self.banca = 1000.00
```
Altere para o valor desejado.

### Alterar Cores

Procure pelos hexadecimais no código:
- `#000000` - Preto (fundo)
- `#FFFFFF` - Branco (texto principal)
- `#CC0000` - Vermelho (botões)
- `#1a1a1a` - Cinza escuro (frames)

### Alterar Multiplicadores

Procure na função `mostrar_resultado()`:
```python
multiplicador = 2  # para 🔥 e ⭐
multiplicador = 3  # para 🤑
```

---

## 🔒 Avisos Importantes

⚠️ **Este é um SIMULADOR EDUCATIVO apenas**
- Não envolve dinheiro real
- Não deve ser usado como base para apostas reais
- É apenas para fins de aprendizado

---

## 📝 Comentários do Código

Todos os comentários no código estão em **inglês** para manter padrão profissional de desenvolvimento, enquanto a interface do aplicativo permanece em **português brasileiro**.

---

## 📄 Licença

Este projeto é fornecido como código educativo. Sinta-se livre para estudar e modificar.

---

## 👨‍💻 Autor

Desenvolvido por Caique Crepaldi como projeto educativo de Python com CustomTkinter.

---

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique se o Python 3.8+ está instalado
2. Confirme se customtkinter foi instalado: `pip show customtkinter`
3. Tente recriar o ambiente virtual
4. Execute em um terminal aberto especificamente para este projeto

---

**Versão**: 1.0.0  
**Data**: Maio 2026  
**Status**: Funcional e Testado ✅
