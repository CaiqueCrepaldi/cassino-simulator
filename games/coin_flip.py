import random
import time

import customtkinter as ctk
from tkinter import messagebox


class CoinFlip:
    """
    Coin Flip — 50/50 bet, pays 2×.

    Extras
    ------
    - Streak tracker: consecutive wins/losses highlighted.
    - Gambler's Fallacy counter: shows last 10 flips so the player
      can observe randomness regardless of past results.
    - Auto-flip mode: flips automatically until the player stops or
      the balance runs out (configurable delay).
    """

    INITIAL_BALANCE = 1_000.00
    FACES = {"cara": "🪙", "coroa": "👑"}

    def __init__(self, root: ctk.CTk, container: ctk.CTkFrame, back_callback, bank) -> None:
        self.root = root
        self.container = container
        self.back_callback = back_callback
        self.bank = bank
        self.root.title("🪙 Coin Flip")

        # State
        self.current_bet: float  = 0.0
        self.chosen_side: str | None = None
        self.flipping: bool      = False
        self.auto_mode: bool     = False
        self.auto_job            = None

        # Stats
        self.rounds: int    = 0
        self.wins: int      = 0
        self.streak: int    = 0         # positive = win streak, negative = loss streak
        self.history: list[str] = []    # "cara" or "coroa"

        self._build_ui()

    @property
    def balance(self) -> float:
        return self.bank.balance

    @balance.setter
    def balance(self, v: float) -> None:
        self.bank.balance = v

    def _go_back(self) -> None:
        self._stop_auto()
        self.back_callback()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        BG = "#0d0d0d"
        bg = ctk.CTkFrame(self.container, fg_color=BG, corner_radius=0)
        bg.pack(fill="both", expand=True)

        main = ctk.CTkFrame(bg, fg_color=BG)
        main.pack(expand=True, fill="y", anchor="center")
        ctk.CTkFrame(main, width=500, height=1, fg_color=BG).pack()

        ctk.CTkButton(
            main, text="← Menu",
            command=self._go_back,
            width=120, height=28,
            fg_color="#1a1a1a", hover_color="#2a2a2a",
            text_color="#888888", corner_radius=6,
            font=("Arial", 11, "bold"),
        ).pack(pady=(6, 2), anchor="w", padx=8)

        ctk.CTkLabel(
            main, text="🪙  COIN FLIP",
            font=("Arial", 32, "bold"), text_color="#FFD700",
        ).pack(pady=(4, 2))

        ctk.CTkLabel(
            main, text="Cara ou Coroa? Acerte e dobre sua aposta!",
            font=("Arial", 12), text_color="#AAAAAA",
        ).pack()

        self.balance_label = ctk.CTkLabel(
            main, text=self._balance_text(),
            font=("Arial", 15, "bold"), text_color="#00FF00",
        )
        self.balance_label.pack(pady=(8, 0))

        # Coin display
        coin_frame = ctk.CTkFrame(main, fg_color="#1a1a1a", corner_radius=16)
        coin_frame.pack(padx=40, pady=14, fill="x")

        self.coin_label = ctk.CTkLabel(
            coin_frame, text="🪙",
            font=("Arial", 100), text_color="#FFD700",
        )
        self.coin_label.pack(pady=16)

        self.coin_text = ctk.CTkLabel(
            coin_frame, text="?",
            font=("Arial", 18, "bold"), text_color="#AAAAAA",
        )
        self.coin_text.pack(pady=(0, 14))

        # History strip
        hist_frame = ctk.CTkFrame(main, fg_color="#111111", corner_radius=8)
        hist_frame.pack(padx=20, pady=(0, 8), fill="x")

        ctk.CTkLabel(
            hist_frame, text="Últimos:",
            font=("Arial", 11), text_color="#666666",
        ).pack(side="left", padx=8, pady=6)

        self.history_label = ctk.CTkLabel(
            hist_frame, text="—",
            font=("Arial", 13), text_color="#FFD700",
        )
        self.history_label.pack(side="left", padx=4, pady=6)

        # Streak
        self.streak_label = ctk.CTkLabel(
            main, text="",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        )
        self.streak_label.pack(pady=(0, 4))

        # Side selection
        choice_row = ctk.CTkFrame(main, fg_color="#0d0d0d")
        choice_row.pack(padx=20, pady=4, fill="x")

        self.btn_cara = ctk.CTkButton(
            choice_row, text="🪙  CARA",
            command=lambda: self._select_side("cara"),
            font=("Arial", 18, "bold"), height=65, corner_radius=12,
            fg_color="#555500", hover_color="#777700", text_color="#FFD700",
        )
        self.btn_cara.pack(side="left", padx=(0, 8), fill="x", expand=True)

        self.btn_coroa = ctk.CTkButton(
            choice_row, text="👑  COROA",
            command=lambda: self._select_side("coroa"),
            font=("Arial", 18, "bold"), height=65, corner_radius=12,
            fg_color="#004455", hover_color="#006677", text_color="#AADDFF",
        )
        self.btn_coroa.pack(side="left", fill="x", expand=True)

        self.chosen_label = ctk.CTkLabel(
            main, text="Escolha Cara ou Coroa",
            font=("Arial", 12), text_color="#888888",
        )
        self.chosen_label.pack(pady=(4, 0))

        # Bet row
        bet_row = ctk.CTkFrame(main, fg_color="#0d0d0d")
        bet_row.pack(padx=20, pady=8, fill="x")

        ctk.CTkLabel(
            bet_row, text="Aposta (R$):",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        ).pack(side="left", padx=8)

        self.bet_entry = ctk.CTkEntry(
            bet_row, placeholder_text="Ex: 50.00",
            font=("Arial", 13), corner_radius=8,
            fg_color="#1a1a1a", border_color="#FFD700",
            text_color="#FFFFFF", width=130,
        )
        self.bet_entry.pack(side="left", padx=8)

        for v in [10, 25, 50, 100]:
            ctk.CTkButton(
                bet_row, text=f"+{v}",
                command=lambda val=v: self._add_bet(val),
                font=("Arial", 11, "bold"), width=45, height=30,
                fg_color="#1a1a2e", hover_color="#16213e",
                text_color="#AAAAFF", corner_radius=6,
            ).pack(side="left", padx=2)

        # Flip + auto buttons
        self.flip_button = ctk.CTkButton(
            main, text="🪙  JOGAR MOEDA",
            command=self.flip,
            font=("Arial", 18, "bold"), height=55, corner_radius=10,
            fg_color="#CC8800", hover_color="#AA6600", text_color="#FFFFFF",
        )
        self.flip_button.pack(padx=20, pady=(8, 4), fill="x")

        auto_row = ctk.CTkFrame(main, fg_color="#0d0d0d")
        auto_row.pack(padx=20, pady=(0, 4), fill="x")

        self.auto_button = ctk.CTkButton(
            auto_row, text="⚡ AUTO FLIP",
            command=self._toggle_auto,
            font=("Arial", 13, "bold"), height=36, corner_radius=8,
            fg_color="#1a1a2e", hover_color="#2a2a4e", text_color="#AAAAFF",
        )
        self.auto_button.pack(side="left", fill="x", expand=True, padx=(0, 4))

        ctk.CTkButton(
            auto_row, text="🔄 NOVO JOGO",
            command=self.reset,
            font=("Arial", 13, "bold"), height=36, corner_radius=8,
            fg_color="#1a1a1a", hover_color="#2a2a2a", text_color="#888888",
        ).pack(side="left", fill="x", expand=True)

        # Result
        self.result_frame = ctk.CTkFrame(main, fg_color="#111111", corner_radius=10)
        self.result_frame.pack(padx=20, pady=6, fill="x")

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Escolha um lado e jogue a moeda!",
            font=("Arial", 14, "bold"), text_color="#CCCCCC", wraplength=440,
        )
        self.result_label.pack(pady=14, padx=16)

        self.stats_label = ctk.CTkLabel(
            main, text=self._stats_text(),
            font=("Arial", 11), text_color="#555555",
        )
        self.stats_label.pack(pady=(4, 10))

    # ── Helpers ──────────────────────────────────────────────

    def _balance_text(self) -> str:
        return f"💰 Banca: R$ {self.balance:.2f}"

    def _stats_text(self) -> str:
        rate = (self.wins / self.rounds * 100) if self.rounds else 0
        return f"Rodadas: {self.rounds} | Vitórias: {self.wins} | Taxa: {rate:.2f}%"

    def _add_bet(self, value: int) -> None:
        text = self.bet_entry.get().strip()
        try:
            new_value = float(text) + value if text else float(value)
        except ValueError:
            new_value = float(value)
        self.bet_entry.delete(0, "end")
        self.bet_entry.insert(0, f"{new_value:.2f}")

    def _select_side(self, side: str) -> None:
        if self.flipping:
            return
        self.chosen_side = side

        if side == "cara":
            self.btn_cara.configure(border_color="#FFD700", border_width=3, fg_color="#888800")
            self.btn_coroa.configure(border_width=0, fg_color="#004455")
            self.chosen_label.configure(text="Escolhido: 🪙 CARA", text_color="#FFD700")
        else:
            self.btn_coroa.configure(border_color="#AADDFF", border_width=3, fg_color="#006688")
            self.btn_cara.configure(border_width=0, fg_color="#555500")
            self.chosen_label.configure(text="Escolhido: 👑 COROA", text_color="#AADDFF")

    def _animate_flip(self) -> None:
        frames = ["🪙", "👑", "🪙", "👑", "🪙", "👑", "🪙", "👑"]
        for frame in frames:
            self.coin_label.configure(text=frame)
            self.root.update()
            time.sleep(0.08)

    def _update_history(self) -> None:
        if not self.history:
            self.history_label.configure(text="—")
            return
        icons = [self.FACES[s] for s in self.history[-12:]]
        self.history_label.configure(text=" ".join(icons))

    def _update_streak(self, won: bool) -> None:
        if won:
            self.streak = self.streak + 1 if self.streak > 0 else 1
        else:
            self.streak = self.streak - 1 if self.streak < 0 else -1

        if self.streak >= 3:
            self.streak_label.configure(
                text=f"🔥 {self.streak} vitórias seguidas!", text_color="#FF8800"
            )
        elif self.streak <= -3:
            self.streak_label.configure(
                text=f"❄️ {abs(self.streak)} derrotas seguidas...", text_color="#4488FF"
            )
        else:
            self.streak_label.configure(text="")

    # ── Game logic ───────────────────────────────────────────

    def flip(self) -> None:
        if self.flipping:
            return
        if self.chosen_side is None:
            messagebox.showerror("Erro", "Escolha Cara ou Coroa!")
            return

        try:
            text = self.bet_entry.get().strip()
            if not text:
                messagebox.showerror("Erro", "Digite um valor de aposta!")
                return
            self.current_bet = float(text)
            if self.current_bet <= 0:
                messagebox.showerror("Erro", "A aposta deve ser maior que 0!")
                return
            if self.current_bet > self.balance:
                messagebox.showerror("Erro", f"Aposta maior que sua banca (R$ {self.balance:.2f})")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido!")
            return

        self.flipping = True
        self.flip_button.configure(state="disabled", text="🪙 JOGANDO...")
        self.result_frame.configure(border_width=0)

        self._animate_flip()
        self.root.after(50, self._show_result)

    def _show_result(self) -> None:
        result = random.choice(["cara", "coroa"])
        self.history.append(result)
        self._update_history()

        self.coin_label.configure(text=self.FACES[result])
        name = "CARA" if result == "cara" else "COROA"
        self.coin_text.configure(
            text=name,
            text_color="#FFD700" if result == "cara" else "#AADDFF",
        )

        self.rounds += 1
        won = result == self.chosen_side

        if won:
            self.wins   += 1
            prize        = self.current_bet * 2
            self.balance += prize
            msg   = f"✅ {self.FACES[result]} {name}! Você acertou!\n💰 Ganhou R$ {self.current_bet:.2f}!"
            color = "#00FF88"
            self.result_frame.configure(border_color=color, border_width=3)
        else:
            self.balance -= self.current_bet
            msg   = f"{self.FACES[result]} {name}! Você errou.\n💸 Perdeu R$ {self.current_bet:.2f}"
            color = "#FF4444"
            self.result_frame.configure(border_color=color, border_width=2)

        self._update_streak(won)
        self.result_label.configure(text=msg, text_color=color)
        self.balance_label.configure(text=self._balance_text())
        self.stats_label.configure(text=self._stats_text())

        self.flipping = False

        if self.balance <= 0:
            self.result_label.configure(text="💀 BANCA ZERADA! Clique em Novo Jogo.", text_color="#FF0000")
            self.flip_button.configure(state="disabled", text="💀 GAME OVER")
            self._stop_auto()
        else:
            self.flip_button.configure(state="normal", text="🪙  JOGAR MOEDA")
            if not self.auto_mode:
                self.bet_entry.delete(0, "end")

    def _toggle_auto(self) -> None:
        if self.auto_mode:
            self._stop_auto()
        else:
            self._start_auto()

    def _start_auto(self) -> None:
        if self.chosen_side is None:
            messagebox.showerror("Erro", "Escolha Cara ou Coroa para o auto flip!")
            return
        self.auto_mode = True
        self.auto_button.configure(text="⏹ PARAR AUTO", fg_color="#440000", hover_color="#660000")
        self._auto_tick()

    def _stop_auto(self) -> None:
        self.auto_mode = False
        if self.auto_job:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None
        self.auto_button.configure(text="⚡ AUTO FLIP", fg_color="#1a1a2e", hover_color="#2a2a4e")

    def _auto_tick(self) -> None:
        if not self.auto_mode or self.balance <= 0:
            self._stop_auto()
            return
        self.flip()
        self.auto_job = self.root.after(600, self._auto_tick)

    def reset(self) -> None:
        self._stop_auto()
        self.balance     = self.INITIAL_BALANCE
        self.current_bet = 0.0
        self.chosen_side = None
        self.flipping    = False
        self.rounds      = 0
        self.wins        = 0
        self.streak      = 0
        self.history     = []

        self.balance_label.configure(text=self._balance_text())
        self.result_label.configure(text="Escolha um lado e jogue a moeda!", text_color="#CCCCCC")
        self.result_frame.configure(border_width=0)
        self.coin_label.configure(text="🪙")
        self.coin_text.configure(text="?", text_color="#AAAAAA")
        self.chosen_label.configure(text="Escolha Cara ou Coroa", text_color="#888888")
        self.streak_label.configure(text="")
        self.stats_label.configure(text=self._stats_text())
        self.history_label.configure(text="—")
        self.flip_button.configure(state="normal", text="🪙  JOGAR MOEDA")
        self.bet_entry.delete(0, "end")

        self.btn_cara.configure(border_width=0, fg_color="#555500")
        self.btn_coroa.configure(border_width=0, fg_color="#004455")
