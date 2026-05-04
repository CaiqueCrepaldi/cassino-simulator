import customtkinter as ctk
import random
import time
import math
from tkinter import messagebox

# Configure theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ─────────────────────────────────────────────
#  TELA PRINCIPAL – MENU DE SELEÇÃO
# ─────────────────────────────────────────────
class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Cassino Simulator – Menu Principal")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        main_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#000000")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Título
        ctk.CTkLabel(
            main_frame,
            text="🎰 CASSINO SIMULATOR 🎰",
            font=("Arial", 28, "bold"),
            text_color="#FFD700"
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            main_frame,
            text="Escolha um jogo para jogar!",
            font=("Arial", 14),
            text_color="#CCCCCC"
        ).pack(pady=(0, 50))

        # Botão Slots
        btn_slots = ctk.CTkButton(
            main_frame,
            text="🎰  SLOT MACHINE",
            command=self.abrir_slots,
            font=("Arial", 20, "bold"),
            corner_radius=12,
            height=90,
            fg_color="#CC0000",
            hover_color="#990000",
            text_color="#FFFFFF"
        )
        btn_slots.pack(pady=15, fill="x", padx=40)

        ctk.CTkLabel(
            main_frame,
            text="Gire os slots e tente 3 símbolos iguais!",
            font=("Arial", 11),
            text_color="#AAAAAA"
        ).pack(pady=(0, 20))

        # Botão Aviator
        btn_aviator = ctk.CTkButton(
            main_frame,
            text="✈️  AVIATOR",
            command=self.abrir_aviator,
            font=("Arial", 20, "bold"),
            corner_radius=12,
            height=90,
            fg_color="#0055CC",
            hover_color="#003D99",
            text_color="#FFFFFF"
        )
        btn_aviator.pack(pady=15, fill="x", padx=40)

        ctk.CTkLabel(
            main_frame,
            text="Aposte e retire antes do avião voar embora!",
            font=("Arial", 11),
            text_color="#AAAAAA"
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            main_frame,
            text="Projeto acadêmico – sem dinheiro real envolvido",
            font=("Arial", 10),
            text_color="#555555"
        ).pack(side="bottom", pady=15)

    def abrir_slots(self):
        janela = ctk.CTkToplevel(self.root)
        CassinoSimulator(janela)

    def abrir_aviator(self):
        janela = ctk.CTkToplevel(self.root)
        AviatorGame(janela)


# ─────────────────────────────────────────────
#  JOGO 1 – SLOT MACHINE  (código original)
# ─────────────────────────────────────────────
class CassinoSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Slot Machine")
        self.root.geometry("600x1150")
        self.root.resizable(False, False)

        self.symbols = ["🔥", "⭐", "🤑"]
        self.weights = [40, 35, 25]

        self.banca = 1000.00
        self.aposta_atual = 0.0

        main_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#000000")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            main_frame,
            text="🎰 CASSINO SIMULATOR 🎰",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=20)

        ctk.CTkLabel(
            main_frame,
            text="Tente conseguir 3 símbolos iguais!",
            font=("Arial", 14),
            text_color="#CCCCCC"
        ).pack(pady=(0, 30))

        bank_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", corner_radius=10)
        bank_frame.pack(padx=30, pady=10, fill="x")

        self.banca_label = ctk.CTkLabel(
            bank_frame,
            text=f"💰 Banca: R$ {self.banca:.2f}",
            font=("Arial", 16, "bold"),
            text_color="#00FF00"
        )
        self.banca_label.pack(pady=10, padx=10)

        bet_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        bet_frame.pack(padx=30, pady=10, fill="x")

        ctk.CTkLabel(
            bet_frame,
            text="Valor da Aposta (R$):",
            font=("Arial", 12, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=10)

        self.bet_entry = ctk.CTkEntry(
            bet_frame,
            placeholder_text="Digite a aposta...",
            font=("Arial", 12),
            corner_radius=8,
            fg_color="#1a1a1a",
            border_color="#CC0000",
            text_color="#FFFFFF",
            width=150
        )
        self.bet_entry.pack(side="left", padx=10)

        slots_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#1a1a1a")
        slots_frame.pack(padx=30, pady=20, fill="x")

        self.slots_container = ctk.CTkFrame(slots_frame, fg_color="#1a1a1a")
        self.slots_container.pack(pady=30, padx=20)

        self.slot_labels = []
        for i in range(3):
            slot_frame = ctk.CTkFrame(self.slots_container, fg_color="#000000", corner_radius=10)
            slot_frame.pack(side="left", padx=10, expand=True)
            slot_label = ctk.CTkLabel(
                slot_frame,
                text="❓",
                font=("Arial", 60),
                text_color="#FFFFFF"
            )
            slot_label.pack(pady=20, padx=20)
            self.slot_labels.append(slot_label)

        controls_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        controls_frame.pack(pady=20, fill="x", padx=30)

        self.spin_button = ctk.CTkButton(
            controls_frame,
            text="🎰 GIRAR SLOTS 🎰",
            command=self.girar,
            font=("Arial", 18, "bold"),
            corner_radius=10,
            height=60,
            fg_color="#CC0000",
            hover_color="#990000",
            text_color="#FFFFFF"
        )
        self.spin_button.pack(pady=20, fill="x", padx=20)

        ctk.CTkButton(
            controls_frame,
            text="🔄 NOVO JOGO",
            command=self.resetar_estatisticas,
            font=("Arial", 14, "bold"),
            corner_radius=10,
            height=40,
            fg_color="#0066CC",
            hover_color="#004499",
            text_color="#FFFFFF"
        ).pack(pady=(0, 20), fill="x", padx=20)

        self.resultado_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#1a1a1a")
        self.resultado_frame.pack(padx=30, pady=20, fill="both", expand=True)

        self.resultado_label = ctk.CTkLabel(
            self.resultado_frame,
            text="Clique em GIRAR para começar!",
            font=("Arial", 16, "bold"),
            wraplength=400,
            text_color="#FFFFFF"
        )
        self.resultado_label.pack(padx=20, pady=30)

        stats_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        stats_frame.pack(pady=(0, 20), fill="x", padx=30)

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Tentativas: 0 | Vitórias: 0 | Taxa de Sucesso: 0.00%",
            font=("Arial", 12),
            text_color="#CCCCCC"
        )
        self.stats_label.pack(pady=10)

        self.tentativas = 0
        self.vitorias = 0

    def girar(self):
        if self.spin_button.cget("state") == "disabled":
            return
        try:
            aposta_texto = self.bet_entry.get()
            if not aposta_texto:
                messagebox.showerror("Erro", "Digite um valor de aposta!")
                return
            self.aposta_atual = float(aposta_texto)
            if self.aposta_atual <= 0:
                messagebox.showerror("Erro", "A aposta deve ser maior que 0!")
                return
            if self.aposta_atual > self.banca:
                messagebox.showerror("Erro", f"Aposta não pode ser maior que sua banca (R$ {self.banca:.2f})")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido!")
            return

        self.spin_button.configure(state="disabled", text="🎰 GIRANDO... 🎰")
        self.animacao_giro()
        self.root.after(1500, self.mostrar_resultado)

    def animacao_giro(self):
        simbolos_animacao = ["🔥", "⭐", "🤑", "🎰", "💎", "🎲", "🎯", "🎪"]
        for _ in range(10):
            for label in self.slot_labels:
                label.configure(text=random.choice(simbolos_animacao))
            self.root.update()
            time.sleep(0.1)

    def mostrar_resultado(self):
        resultado = [random.choices(self.symbols, weights=self.weights, k=1)[0] for _ in range(3)]
        for i, simbolo in enumerate(resultado):
            self.slot_labels[i].configure(text=simbolo)

        self.tentativas += 1
        vitoria = len(set(resultado)) == 1

        if vitoria:
            self.vitorias += 1
            simbolo_vitoria = resultado[0]
            if simbolo_vitoria == "🔥":
                mensagem = "🔥 INCRÍVEL! 3 FOGOS IGUAIS! 🔥"
                cor = "#FF6B35"
                multiplicador = 2
            elif simbolo_vitoria == "⭐":
                mensagem = "⭐ FANTÁSTICO! 3 ESTRELAS IGUAIS! ⭐"
                cor = "#FFD700"
                multiplicador = 2
            else:
                mensagem = "🤑 JACKPOT! 3 DINHEIROS IGUAIS! 🤑"
                cor = "#00FF00"
                multiplicador = 3

            ganho = self.aposta_atual * multiplicador
            self.banca += ganho
            self.banca_label.configure(text=f"💰 Banca: R$ {self.banca:.2f}")
            self.resultado_label.configure(text=f"{mensagem}\n💰 Ganhou: R$ {ganho:.2f}!", text_color=cor)
            self.resultado_frame.configure(border_color=cor, border_width=3)
            messagebox.showinfo("🎉 VITÓRIA!", f"Parabéns! Você conseguiu 3 {simbolo_vitoria} iguais!\nGanhou R$ {ganho:.2f}\nNova banca: R$ {self.banca:.2f}")
        else:
            self.banca -= self.aposta_atual
            self.banca_label.configure(text=f"💰 Banca: R$ {self.banca:.2f}")
            self.resultado_label.configure(
                text=f"❌ Não foi dessa vez! Tente novamente!\n💸 Perdeu: R$ {self.aposta_atual:.2f}",
                text_color="#FF4444"
            )
            self.resultado_frame.configure(border_color="#FF4444", border_width=2)
            if self.banca <= 0:
                self.resultado_label.configure(text="💀 BANCA ZERADA! Você perdeu tudo!", text_color="#FF0000")
                messagebox.showwarning("⚠️ FIM DE JOGO", "Sua banca zerou! O jogo terminou.")

        taxa_sucesso = (self.vitorias / self.tentativas) * 100 if self.tentativas > 0 else 0
        self.stats_label.configure(
            text=f"Tentativas: {self.tentativas} | Vitórias: {self.vitorias} | Taxa de Sucesso: {taxa_sucesso:.2f}%"
        )

        if self.banca > 0:
            self.spin_button.configure(state="normal", text="🎰 GIRAR SLOTS 🎰")
            self.bet_entry.delete(0, "end")
        else:
            self.spin_button.configure(state="disabled", text="💀 GAME OVER 💀")

    def resetar_estatisticas(self):
        self.tentativas = 0
        self.vitorias = 0
        self.banca = 1000.00
        self.aposta_atual = 0.0
        self.banca_label.configure(text=f"💰 Banca: R$ {self.banca:.2f}")
        self.bet_entry.delete(0, "end")
        self.stats_label.configure(text="Tentativas: 0 | Vitórias: 0 | Taxa de Sucesso: 0.00%")
        self.resultado_label.configure(text="Clique em GIRAR para começar!", text_color="#FFFFFF")
        self.resultado_frame.configure(border_width=0)
        self.spin_button.configure(state="normal", text="🎰 GIRAR SLOTS 🎰")
        for label in self.slot_labels:
            label.configure(text="❓")


# ─────────────────────────────────────────────
#  JOGO 2 – AVIATOR
# ─────────────────────────────────────────────
class AviatorGame:
    """
    Aviator simulado com lógica fiel ao jogo real:
    - Multiplicador começa em 1.00x e cresce exponencialmente
    - O avião "voa embora" num momento aleatório (crash)
    - O jogador deve clicar em RETIRAR antes do crash
    - Se não retirar a tempo, perde a aposta
    - O multiplicador de crash é gerado com distribuição exponencial
      (maioria pequenos, raramente muito altos) – igual ao original
    """

    INTERVALO_MS = 100          # atualiza a cada 100 ms
    CRESCIMENTO   = 0.05        # quanto o multiplicador cresce por tick
    CANVAS_W      = 540
    CANVAS_H      = 280

    def __init__(self, root):
        self.root = root
        self.root.title("✈️ Aviator")
        self.root.geometry("580x820")
        self.root.resizable(False, False)

        # Estado do jogo
        self.banca          = 1000.00
        self.aposta_atual   = 0.0
        self.multiplicador  = 1.00
        self.crash_em       = 1.00
        self.rodando        = False
        self.retirou        = False
        self.job_id         = None

        # Histórico dos últimos crashes
        self.historico: list[float] = []

        # Trilha do avião (lista de pontos)
        self.trilha: list[tuple[int, int]] = []

        # ── Layout ──────────────────────────────────────────
        main_frame = ctk.CTkFrame(root, fg_color="#000000", corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Título
        ctk.CTkLabel(
            main_frame,
            text="✈️  AVIATOR",
            font=("Arial", 30, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(20, 2))

        ctk.CTkLabel(
            main_frame,
            text="Retire antes do avião voar embora!",
            font=("Arial", 12),
            text_color="#AAAAAA"
        ).pack(pady=(0, 10))

        # Banca
        self.banca_label = ctk.CTkLabel(
            main_frame,
            text=f"💰 Banca: R$ {self.banca:.2f}",
            font=("Arial", 15, "bold"),
            text_color="#00FF00"
        )
        self.banca_label.pack()

        # ── Canvas de animação ───────────────────────────────
        import tkinter as tk
        self.canvas_frame = ctk.CTkFrame(main_frame, fg_color="#0a0a1a", corner_radius=12)
        self.canvas_frame.pack(padx=20, pady=12, fill="x")

        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.CANVAS_W,
            height=self.CANVAS_H,
            bg="#0a0a1a",
            highlightthickness=0
        )
        self.canvas.pack(padx=5, pady=5)

        # Multiplicador grande no centro do canvas
        self.mult_canvas_text = self.canvas.create_text(
            self.CANVAS_W // 2, self.CANVAS_H // 2,
            text="1.00x",
            font=("Arial", 56, "bold"),
            fill="#FFFFFF"
        )

        # Avião (texto emoji)
        self.plane_obj = self.canvas.create_text(
            60, self.CANVAS_H - 40,
            text="✈️",
            font=("Arial", 32),
            fill="#FFFFFF"
        )

        # Linha de grade (decorativa)
        for y in range(0, self.CANVAS_H, 40):
            self.canvas.create_line(0, y, self.CANVAS_W, y, fill="#111133", width=1)
        for x in range(0, self.CANVAS_W, 60):
            self.canvas.create_line(x, 0, x, self.CANVAS_H, fill="#111133", width=1)

        # ── Histórico de crashes ─────────────────────────────
        hist_frame = ctk.CTkFrame(main_frame, fg_color="#0d0d0d", corner_radius=8)
        hist_frame.pack(padx=20, pady=(0, 8), fill="x")

        ctk.CTkLabel(
            hist_frame,
            text="Últimos crashes:",
            font=("Arial", 11),
            text_color="#888888"
        ).pack(side="left", padx=8, pady=6)

        self.historico_label = ctk.CTkLabel(
            hist_frame,
            text="—",
            font=("Arial", 11, "bold"),
            text_color="#FFD700"
        )
        self.historico_label.pack(side="left", padx=4, pady=6)

        # ── Aposta ──────────────────────────────────────────
        bet_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        bet_frame.pack(padx=20, pady=4, fill="x")

        ctk.CTkLabel(
            bet_frame,
            text="Aposta (R$):",
            font=("Arial", 13, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=8)

        self.bet_entry = ctk.CTkEntry(
            bet_frame,
            placeholder_text="Ex: 50.00",
            font=("Arial", 13),
            corner_radius=8,
            fg_color="#1a1a1a",
            border_color="#0055CC",
            text_color="#FFFFFF",
            width=140
        )
        self.bet_entry.pack(side="left", padx=8)

        # Botões de atalho de aposta
        for valor in [10, 25, 50, 100]:
            ctk.CTkButton(
                bet_frame,
                text=f"+{valor}",
                command=lambda v=valor: self._adicionar_aposta(v),
                font=("Arial", 11, "bold"),
                width=45,
                height=30,
                fg_color="#1a1a2e",
                hover_color="#16213e",
                text_color="#AAAAFF",
                corner_radius=6
            ).pack(side="left", padx=2)

        # ── Botões principais ────────────────────────────────
        btn_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        btn_frame.pack(padx=20, pady=10, fill="x")

        self.btn_apostar = ctk.CTkButton(
            btn_frame,
            text="✈️  APOSTAR & VOAR",
            command=self.iniciar_rodada,
            font=("Arial", 17, "bold"),
            height=55,
            corner_radius=10,
            fg_color="#0055CC",
            hover_color="#003D99",
            text_color="#FFFFFF"
        )
        self.btn_apostar.pack(side="left", padx=(0, 8), fill="x", expand=True)

        self.btn_retirar = ctk.CTkButton(
            btn_frame,
            text="💰  RETIRAR",
            command=self.retirar,
            font=("Arial", 17, "bold"),
            height=55,
            corner_radius=10,
            fg_color="#CC7700",
            hover_color="#995500",
            text_color="#FFFFFF",
            state="disabled"
        )
        self.btn_retirar.pack(side="left", fill="x", expand=True)

        # ── Botão novo jogo ──────────────────────────────────
        ctk.CTkButton(
            main_frame,
            text="🔄 NOVO JOGO (resetar banca)",
            command=self.resetar,
            font=("Arial", 12, "bold"),
            height=35,
            corner_radius=8,
            fg_color="#222222",
            hover_color="#333333",
            text_color="#AAAAAA"
        ).pack(padx=20, pady=(0, 8), fill="x")

        # ── Status / resultado ───────────────────────────────
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Defina sua aposta e clique em APOSTAR!",
            font=("Arial", 14, "bold"),
            text_color="#CCCCCC",
            wraplength=500
        )
        self.status_label.pack(pady=8, padx=20)

        # Estatísticas
        self.stats_label = ctk.CTkLabel(
            main_frame,
            text="Rodadas: 0 | Vitórias: 0 | Maior multiplicador: —",
            font=("Arial", 11),
            text_color="#666666"
        )
        self.stats_label.pack(pady=(0, 10))

        self.rodadas   = 0
        self.vitorias  = 0
        self.maior_mult = 0.0

    # ── Auxiliares ──────────────────────────────────────────

    def _adicionar_aposta(self, valor):
        atual = self.bet_entry.get().strip()
        try:
            novo = float(atual) + valor if atual else float(valor)
        except ValueError:
            novo = float(valor)
        self.bet_entry.delete(0, "end")
        self.bet_entry.insert(0, f"{novo:.2f}")

    def _gerar_crash(self) -> float:
        """
        Gera o ponto de crash com distribuição exponencial truncada.
        A maioria dos crashes ocorre entre 1x e 3x, com raridades altas.
        Fórmula inspirada no Aviator real: crash = 0.99 / (1 - u)
        onde u é uniforme em [0, 1).
        """
        u = random.random()
        crash = 0.99 / (1.0 - u * 0.99)   # garante mínimo ≈ 1.00
        # Limita em 100x para evitar valores absurdos na UI
        return round(min(crash, 100.0), 2)

    def _cor_multiplicador(self, m: float) -> str:
        if m < 1.5:
            return "#FFFFFF"
        elif m < 2.0:
            return "#FFD700"
        elif m < 5.0:
            return "#FF8800"
        else:
            return "#FF4444"

    def _cor_historico(self, m: float) -> str:
        if m < 2.0:
            return "#FF4444"
        elif m < 5.0:
            return "#FFD700"
        else:
            return "#00FF88"

    def _atualizar_historico(self):
        if not self.historico:
            self.historico_label.configure(text="—", text_color="#FFD700")
            return
        partes = []
        for m in self.historico[-8:]:
            cor = self._cor_historico(m)
            partes.append(f"{m:.2f}x")
        self.historico_label.configure(text="  ".join(partes), text_color="#FFD700")

    def _limpar_canvas(self):
        self.canvas.delete("trilha")
        self.canvas.delete("plane_shadow")
        self.trilha = []
        self.canvas.itemconfig(self.mult_canvas_text, text="1.00x", fill="#FFFFFF")
        self.canvas.coords(self.plane_obj, 60, self.CANVAS_H - 40)
        self.canvas.itemconfig(self.plane_obj, text="✈️")

    # ── Lógica principal ─────────────────────────────────────

    def iniciar_rodada(self):
        if self.rodando:
            return

        # Valida aposta
        try:
            txt = self.bet_entry.get().strip()
            if not txt:
                messagebox.showerror("Erro", "Digite um valor de aposta!")
                return
            self.aposta_atual = float(txt)
            if self.aposta_atual <= 0:
                messagebox.showerror("Erro", "A aposta deve ser maior que 0!")
                return
            if self.aposta_atual > self.banca:
                messagebox.showerror("Erro", f"Aposta maior que sua banca (R$ {self.banca:.2f})")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido!")
            return

        # Desconta aposta da banca imediatamente (como no jogo real)
        self.banca -= self.aposta_atual
        self.banca_label.configure(text=f"💰 Banca: R$ {self.banca:.2f}")

        # Gera crash
        self.crash_em      = self._gerar_crash()
        self.multiplicador = 1.00
        self.retirou       = False
        self.rodando       = True

        self._limpar_canvas()

        self.btn_apostar.configure(state="disabled")
        self.btn_retirar.configure(state="normal")
        self.bet_entry.configure(state="disabled")

        self.status_label.configure(
            text=f"✈️ Voando... Aposta: R$ {self.aposta_atual:.2f} | Retira: R$ {self.aposta_atual * self.multiplicador:.2f}",
            text_color="#FFFFFF"
        )

        self._tick()

    def _tick(self):
        """Chamado a cada INTERVALO_MS para atualizar o multiplicador."""
        if not self.rodando:
            return

        # Crescimento exponencial suave
        self.multiplicador = round(self.multiplicador + self.CRESCIMENTO * (self.multiplicador ** 0.5), 2)

        # Atualiza canvas
        cor = self._cor_multiplicador(self.multiplicador)
        self.canvas.itemconfig(
            self.mult_canvas_text,
            text=f"{self.multiplicador:.2f}x",
            fill=cor
        )

        # Movimenta o avião em curva ascendente
        progresso = min(self.multiplicador / max(self.crash_em, 2), 1.0)
        px = int(60 + progresso * (self.CANVAS_W - 100))
        py = int((self.CANVAS_H - 40) - progresso * (self.CANVAS_H - 60) * 0.85)
        self.canvas.coords(self.plane_obj, px, py)

        # Desenha trilha
        self.trilha.append((px, py))
        if len(self.trilha) >= 2:
            x1, y1 = self.trilha[-2]
            x2, y2 = self.trilha[-1]
            self.canvas.create_line(x1, y1, x2, y2, fill="#4488FF", width=2, tags="trilha")

        self.status_label.configure(
            text=f"✈️ Voando... {self.multiplicador:.2f}x | "
                 f"Retire agora: R$ {self.aposta_atual * self.multiplicador:.2f}",
            text_color=cor
        )

        # Verifica crash
        if self.multiplicador >= self.crash_em:
            self._crash()
        else:
            self.job_id = self.root.after(self.INTERVALO_MS, self._tick)

    def _crash(self):
        """O avião voou embora."""
        self.rodando = False

        # Muda avião para explosão
        self.canvas.itemconfig(self.plane_obj, text="💥")
        self.canvas.itemconfig(self.mult_canvas_text, text=f"💥 {self.crash_em:.2f}x", fill="#FF2222")

        self.historico.append(self.crash_em)
        self._atualizar_historico()
        self.rodadas += 1

        self.btn_retirar.configure(state="disabled")
        self.btn_apostar.configure(state="normal")
        self.bet_entry.configure(state="normal")

        if not self.retirou:
            # Perdeu
            self.status_label.configure(
                text=f"💥 CRASH em {self.crash_em:.2f}x! Perdeu R$ {self.aposta_atual:.2f}",
                text_color="#FF3333"
            )
            if self.banca <= 0:
                self.status_label.configure(
                    text="💀 BANCA ZERADA! Clique em Novo Jogo.",
                    text_color="#FF0000"
                )
                self.btn_apostar.configure(state="disabled")
        else:
            # Já retirou antes, status já foi atualizado
            pass

        self._atualizar_stats()

    def retirar(self):
        """Jogador clica em Retirar antes do crash."""
        if not self.rodando or self.retirou:
            return

        self.retirou   = True
        ganho          = round(self.aposta_atual * self.multiplicador, 2)
        self.banca    += ganho
        self.vitorias += 1

        if self.multiplicador > self.maior_mult:
            self.maior_mult = self.multiplicador

        self.banca_label.configure(text=f"💰 Banca: R$ {self.banca:.2f}")
        self.status_label.configure(
            text=f"✅ Retirou em {self.multiplicador:.2f}x! Ganhou R$ {ganho:.2f}",
            text_color="#00FF88"
        )

        self.btn_retirar.configure(state="disabled")
        # Deixa o avião continuar voando até o crash (comportamento real)

    def resetar(self):
        if self.job_id:
            self.root.after_cancel(self.job_id)
            self.job_id = None

        self.rodando       = False
        self.retirou       = False
        self.banca         = 1000.00
        self.aposta_atual  = 0.0
        self.multiplicador = 1.00
        self.rodadas       = 0
        self.vitorias      = 0
        self.maior_mult    = 0.0
        self.historico     = []

        self.banca_label.configure(text=f"💰 Banca: R$ {self.banca:.2f}")
        self.status_label.configure(text="Defina sua aposta e clique em APOSTAR!", text_color="#CCCCCC")
        self.historico_label.configure(text="—")
        self.stats_label.configure(text="Rodadas: 0 | Vitórias: 0 | Maior multiplicador: —")

        self.btn_apostar.configure(state="normal")
        self.btn_retirar.configure(state="disabled")
        self.bet_entry.configure(state="normal")
        self.bet_entry.delete(0, "end")

        self._limpar_canvas()

    def _atualizar_stats(self):
        maior = f"{self.maior_mult:.2f}x" if self.maior_mult > 0 else "—"
        self.stats_label.configure(
            text=f"Rodadas: {self.rodadas} | Vitórias: {self.vitorias} | Maior multiplicador: {maior}"
        )


# ─────────────────────────────────────────────
#  INICIALIZAÇÃO
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = ctk.CTk()
    app = MenuPrincipal(root)
    root.mainloop()
