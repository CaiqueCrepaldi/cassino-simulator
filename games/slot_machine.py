import random
import time

import customtkinter as ctk
from tkinter import messagebox


class SlotMachine:
    """
    Slot Machine game.

    The player sets a bet and spins three slots. Getting three identical
    symbols pays a multiplier on the bet; otherwise the bet is lost.

    Symbols and weights
    -------------------
    🔥  Fire   — 40 % — 2× multiplier
    ⭐  Star   — 35 % — 2× multiplier
    🤑  Money  — 25 % — 3× multiplier (jackpot)
    """

    SYMBOLS = ["🔥", "⭐", "🤑"]
    WEIGHTS = [40, 35, 25]
    MULTIPLIERS = {"🔥": 2, "⭐": 2, "🤑": 3}
    INITIAL_BALANCE = 1_000.00

    def __init__(self, root: ctk.CTkToplevel) -> None:
        self.root = root
        self.root.title("🎰 Slot Machine")
        self.root.geometry("600x1150")
        self.root.resizable(False, False)

        # State
        self.balance: float = self.INITIAL_BALANCE
        self.current_bet: float = 0.0
        self.attempts: int = 0
        self.wins: int = 0

        self._build_ui()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        main = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#000000")
        main.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            main,
            text="🎰 CASSINO SIMULATOR 🎰",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF",
        ).pack(pady=20)

        ctk.CTkLabel(
            main,
            text="Tente conseguir 3 símbolos iguais!",
            font=("Arial", 14),
            text_color="#CCCCCC",
        ).pack(pady=(0, 30))

        # Balance
        bank_frame = ctk.CTkFrame(main, fg_color="#1a1a1a", corner_radius=10)
        bank_frame.pack(padx=30, pady=10, fill="x")

        self.balance_label = ctk.CTkLabel(
            bank_frame,
            text=self._balance_text(),
            font=("Arial", 16, "bold"),
            text_color="#00FF00",
        )
        self.balance_label.pack(pady=10, padx=10)

        # Bet entry
        bet_frame = ctk.CTkFrame(main, fg_color="#000000")
        bet_frame.pack(padx=30, pady=10, fill="x")

        ctk.CTkLabel(
            bet_frame,
            text="Valor da Aposta (R$):",
            font=("Arial", 12, "bold"),
            text_color="#FFFFFF",
        ).pack(side="left", padx=10)

        self.bet_entry = ctk.CTkEntry(
            bet_frame,
            placeholder_text="Digite a aposta...",
            font=("Arial", 12),
            corner_radius=8,
            fg_color="#1a1a1a",
            border_color="#CC0000",
            text_color="#FFFFFF",
            width=150,
        )
        self.bet_entry.pack(side="left", padx=10)

        # Slots display
        slots_frame = ctk.CTkFrame(main, corner_radius=15, fg_color="#1a1a1a")
        slots_frame.pack(padx=30, pady=20, fill="x")

        container = ctk.CTkFrame(slots_frame, fg_color="#1a1a1a")
        container.pack(pady=30, padx=20)

        self.slot_labels: list[ctk.CTkLabel] = []
        for _ in range(3):
            slot_frame = ctk.CTkFrame(container, fg_color="#000000", corner_radius=10)
            slot_frame.pack(side="left", padx=10, expand=True)
            label = ctk.CTkLabel(
                slot_frame, text="❓", font=("Arial", 60), text_color="#FFFFFF"
            )
            label.pack(pady=20, padx=20)
            self.slot_labels.append(label)

        # Controls
        controls = ctk.CTkFrame(main, fg_color="#000000")
        controls.pack(pady=20, fill="x", padx=30)

        self.spin_button = ctk.CTkButton(
            controls,
            text="🎰 GIRAR SLOTS 🎰",
            command=self.spin,
            font=("Arial", 18, "bold"),
            corner_radius=10,
            height=60,
            fg_color="#CC0000",
            hover_color="#990000",
            text_color="#FFFFFF",
        )
        self.spin_button.pack(pady=20, fill="x", padx=20)

        ctk.CTkButton(
            controls,
            text="🔄 NOVO JOGO",
            command=self.reset,
            font=("Arial", 14, "bold"),
            corner_radius=10,
            height=40,
            fg_color="#0066CC",
            hover_color="#004499",
            text_color="#FFFFFF",
        ).pack(pady=(0, 20), fill="x", padx=20)

        # Result
        self.result_frame = ctk.CTkFrame(main, corner_radius=10, fg_color="#1a1a1a")
        self.result_frame.pack(padx=30, pady=20, fill="both", expand=True)

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Clique em GIRAR para começar!",
            font=("Arial", 16, "bold"),
            wraplength=400,
            text_color="#FFFFFF",
        )
        self.result_label.pack(padx=20, pady=30)

        # Stats
        stats_frame = ctk.CTkFrame(main, fg_color="#000000")
        stats_frame.pack(pady=(0, 20), fill="x", padx=30)

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text=self._stats_text(),
            font=("Arial", 12),
            text_color="#CCCCCC",
        )
        self.stats_label.pack(pady=10)

    # ── Helpers ──────────────────────────────────────────────

    def _balance_text(self) -> str:
        return f"💰 Banca: R$ {self.balance:.2f}"

    def _stats_text(self) -> str:
        rate = (self.wins / self.attempts * 100) if self.attempts else 0
        return f"Tentativas: {self.attempts} | Vitórias: {self.wins} | Taxa de Sucesso: {rate:.2f}%"

    def _validate_bet(self) -> bool:
        """Validates the bet entry. Shows error dialogs on failure."""
        text = self.bet_entry.get().strip()
        if not text:
            messagebox.showerror("Erro", "Digite um valor de aposta!")
            return False
        try:
            self.current_bet = float(text)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido!")
            return False
        if self.current_bet <= 0:
            messagebox.showerror("Erro", "A aposta deve ser maior que 0!")
            return False
        if self.current_bet > self.balance:
            messagebox.showerror(
                "Erro",
                f"Aposta não pode ser maior que sua banca (R$ {self.balance:.2f})",
            )
            return False
        return True

    # ── Game logic ───────────────────────────────────────────

    def spin(self) -> None:
        """Validate bet, animate slots, then show result."""
        if self.spin_button.cget("state") == "disabled":
            return
        if not self._validate_bet():
            return

        self.spin_button.configure(state="disabled", text="🎰 GIRANDO... 🎰")
        self._animate()
        self.root.after(1500, self._show_result)

    def _animate(self) -> None:
        """Quick shuffle animation while the result is being calculated."""
        animation_symbols = ["🔥", "⭐", "🤑", "🎰", "💎", "🎲", "🎯", "🎪"]
        for _ in range(10):
            for label in self.slot_labels:
                label.configure(text=random.choice(animation_symbols))
            self.root.update()
            time.sleep(0.1)

    def _show_result(self) -> None:
        """Calculate final result, update balance and UI."""
        result = [
            random.choices(self.SYMBOLS, weights=self.WEIGHTS, k=1)[0]
            for _ in range(3)
        ]
        for i, symbol in enumerate(result):
            self.slot_labels[i].configure(text=symbol)

        self.attempts += 1
        won = len(set(result)) == 1

        if won:
            self.wins += 1
            symbol = result[0]
            multiplier = self.MULTIPLIERS[symbol]
            prize = self.current_bet * multiplier
            self.balance += prize

            messages = {
                "🔥": ("🔥 INCRÍVEL! 3 FOGOS IGUAIS! 🔥", "#FF6B35"),
                "⭐": ("⭐ FANTÁSTICO! 3 ESTRELAS IGUAIS! ⭐", "#FFD700"),
                "🤑": ("🤑 JACKPOT! 3 DINHEIROS IGUAIS! 🤑", "#00FF00"),
            }
            msg, color = messages[symbol]

            self.result_label.configure(
                text=f"{msg}\n💰 Ganhou: R$ {prize:.2f}!", text_color=color
            )
            self.result_frame.configure(border_color=color, border_width=3)
            messagebox.showinfo(
                "🎉 VITÓRIA!",
                f"Parabéns! Você conseguiu 3 {symbol} iguais!\n"
                f"Ganhou R$ {prize:.2f}\nNova banca: R$ {self.balance:.2f}",
            )
        else:
            self.balance -= self.current_bet
            self.result_label.configure(
                text=f"❌ Não foi dessa vez! Tente novamente!\n💸 Perdeu: R$ {self.current_bet:.2f}",
                text_color="#FF4444",
            )
            self.result_frame.configure(border_color="#FF4444", border_width=2)
            if self.balance <= 0:
                self.result_label.configure(
                    text="💀 BANCA ZERADA! Você perdeu tudo!", text_color="#FF0000"
                )
                messagebox.showwarning("⚠️ FIM DE JOGO", "Sua banca zerou! O jogo terminou.")

        self.balance_label.configure(text=self._balance_text())
        self.stats_label.configure(text=self._stats_text())

        if self.balance > 0:
            self.spin_button.configure(state="normal", text="🎰 GIRAR SLOTS 🎰")
            self.bet_entry.delete(0, "end")
        else:
            self.spin_button.configure(state="disabled", text="💀 GAME OVER 💀")

    def reset(self) -> None:
        """Reset balance and all statistics to initial state."""
        self.balance = self.INITIAL_BALANCE
        self.current_bet = 0.0
        self.attempts = 0
        self.wins = 0

        self.balance_label.configure(text=self._balance_text())
        self.stats_label.configure(text=self._stats_text())
        self.bet_entry.delete(0, "end")
        self.result_label.configure(
            text="Clique em GIRAR para começar!", text_color="#FFFFFF"
        )
        self.result_frame.configure(border_width=0)
        self.spin_button.configure(state="normal", text="🎰 GIRAR SLOTS 🎰")
        for label in self.slot_labels:
            label.configure(text="❓")
