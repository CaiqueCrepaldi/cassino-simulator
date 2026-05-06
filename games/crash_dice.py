import random
import time

import customtkinter as ctk
from tkinter import messagebox


class CrashDice:
    """
    Crash Dice game.

    The player picks one or more numbers (1–6) and rolls two dice.
    Payout rules
    ------------
    - Exact match on both dice (doubles) → 5×
    - One die matches the chosen number  → 2×
    - Sum of dice equals chosen number   → 3×
    - No match                           → lose bet

    The player may select up to 3 numbers before rolling.
    """

    INITIAL_BALANCE = 1_000.00
    DICE_FACES = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    ANIMATION_SYMBOLS = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

    def __init__(self, root: ctk.CTk, container: ctk.CTkFrame, back_callback, bank) -> None:
        self.root = root
        self.container = container
        self.back_callback = back_callback
        self.bank = bank
        self.root.title("🎲 Crash Dice")

        # State
        self.current_bet: float  = 0.0
        self.chosen_numbers: set[int] = set()
        self.rolling: bool       = False
        self._result_job         = None

        # Stats
        self.rounds: int = 0
        self.wins: int   = 0

        self._build_ui()

    @property
    def balance(self) -> float:
        return self.bank.balance

    @balance.setter
    def balance(self, v: float) -> None:
        self.bank.balance = v

    def _go_back(self) -> None:
        if self._result_job:
            self.root.after_cancel(self._result_job)
        self.back_callback()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        BG = "#0d0d0d"
        bg = ctk.CTkFrame(self.container, fg_color=BG, corner_radius=0)
        bg.pack(fill="both", expand=True)

        main = ctk.CTkFrame(bg, fg_color=BG)
        main.pack(expand=True, fill="y", anchor="center")
        ctk.CTkFrame(main, width=540, height=1, fg_color=BG).pack()

        ctk.CTkButton(
            main, text="← Menu",
            command=self._go_back,
            width=120, height=28,
            fg_color="#1a1a1a", hover_color="#2a2a2a",
            text_color="#888888", corner_radius=6,
            font=("Arial", 11, "bold"),
        ).pack(pady=(6, 2), anchor="w", padx=8)

        ctk.CTkLabel(
            main, text="🎲  CRASH DICE",
            font=("Arial", 30, "bold"), text_color="#FFD700",
        ).pack(pady=(4, 2))

        ctk.CTkLabel(
            main, text="Escolha até 3 números e role os dados!",
            font=("Arial", 12), text_color="#AAAAAA",
        ).pack()

        self.balance_label = ctk.CTkLabel(
            main, text=self._balance_text(),
            font=("Arial", 15, "bold"), text_color="#00FF00",
        )
        self.balance_label.pack(pady=(8, 0))

        # Payout table
        pay_frame = ctk.CTkFrame(main, fg_color="#1a1a1a", corner_radius=10)
        pay_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(
            pay_frame,
            text="💡  Dupla exata: 5×  |  Um dado bate: 2×  |  Soma bate: 3×",
            font=("Arial", 11), text_color="#AAAAAA",
        ).pack(pady=8)

        # Dice display
        dice_frame = ctk.CTkFrame(main, fg_color="#1a1a1a", corner_radius=14)
        dice_frame.pack(padx=20, pady=10, fill="x")

        dice_inner = ctk.CTkFrame(dice_frame, fg_color="#1a1a1a")
        dice_inner.pack(pady=20)

        self.dice_labels: list[ctk.CTkLabel] = []
        for _ in range(2):
            lbl = ctk.CTkLabel(
                dice_inner, text="🎲",
                font=("Arial", 72), text_color="#FFFFFF",
            )
            lbl.pack(side="left", padx=20)
            self.dice_labels.append(lbl)

        self.sum_label = ctk.CTkLabel(
            dice_frame, text="",
            font=("Arial", 13), text_color="#888888",
        )
        self.sum_label.pack(pady=(0, 10))

        # Number selector
        num_frame = ctk.CTkFrame(main, fg_color="#0d0d0d")
        num_frame.pack(padx=20, pady=6, fill="x")

        ctk.CTkLabel(
            num_frame, text="Escolha seus números (até 3):",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        ).pack(pady=(6, 4))

        btn_row = ctk.CTkFrame(num_frame, fg_color="#0d0d0d")
        btn_row.pack()

        self.num_buttons: dict[int, ctk.CTkButton] = {}
        for n in range(1, 7):
            btn = ctk.CTkButton(
                btn_row, text=f"{self.DICE_FACES[n-1]}\n{n}",
                command=lambda num=n: self._toggle_number(num),
                font=("Arial", 18, "bold"), width=70, height=70,
                corner_radius=10, fg_color="#222222",
                hover_color="#333333", text_color="#FFFFFF",
            )
            btn.pack(side="left", padx=4)
            self.num_buttons[n] = btn

        self.chosen_label = ctk.CTkLabel(
            main, text="Nenhum número selecionado",
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
            fg_color="#1a1a1a", border_color="#FF8800",
            text_color="#FFFFFF", width=140,
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

        # Roll button
        self.roll_button = ctk.CTkButton(
            main, text="🎲  ROLAR DADOS",
            command=self.roll,
            font=("Arial", 18, "bold"), height=55, corner_radius=10,
            fg_color="#FF8800", hover_color="#CC6600", text_color="#FFFFFF",
        )
        self.roll_button.pack(padx=20, pady=10, fill="x")

        # Result
        self.result_frame = ctk.CTkFrame(main, fg_color="#111111", corner_radius=10)
        self.result_frame.pack(padx=20, pady=4, fill="x")

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Escolha seus números e role os dados!",
            font=("Arial", 14, "bold"), text_color="#CCCCCC", wraplength=480,
        )
        self.result_label.pack(pady=16, padx=16)

        ctk.CTkButton(
            main, text="🔄 NOVO JOGO (resetar banca)",
            command=self.reset,
            font=("Arial", 12, "bold"), height=34, corner_radius=8,
            fg_color="#1a1a1a", hover_color="#2a2a2a", text_color="#888888",
        ).pack(padx=20, pady=(6, 2), fill="x")

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

    def _toggle_number(self, number: int) -> None:
        if self.rolling:
            return
        if number in self.chosen_numbers:
            self.chosen_numbers.discard(number)
            self.num_buttons[number].configure(fg_color="#222222", border_width=0)
        else:
            if len(self.chosen_numbers) >= 3:
                messagebox.showwarning("Aviso", "Você pode escolher no máximo 3 números!")
                return
            self.chosen_numbers.add(number)
            self.num_buttons[number].configure(
                fg_color="#FF8800", border_color="#FFD700", border_width=2
            )

        if self.chosen_numbers:
            names = " ".join(f"{self.DICE_FACES[n-1]}{n}" for n in sorted(self.chosen_numbers))
            self.chosen_label.configure(text=f"Selecionados: {names}", text_color="#FFD700")
        else:
            self.chosen_label.configure(text="Nenhum número selecionado", text_color="#888888")

    def _animate_dice(self) -> None:
        for _ in range(12):
            for lbl in self.dice_labels:
                lbl.configure(text=random.choice(self.ANIMATION_SYMBOLS))
            self.root.update()
            time.sleep(0.07)

    # ── Game logic ───────────────────────────────────────────

    def roll(self) -> None:
        if self.rolling:
            return
        if not self.chosen_numbers:
            messagebox.showerror("Erro", "Escolha pelo menos um número!")
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

        self.rolling = True
        self.roll_button.configure(state="disabled", text="🎲 ROLANDO...")
        self.result_frame.configure(border_width=0)

        self._animate_dice()
        self._result_job = self.root.after(100, self._show_result)

    def _show_result(self) -> None:
        self._result_job = None
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        total = d1 + d2

        self.dice_labels[0].configure(text=self.DICE_FACES[d1 - 1])
        self.dice_labels[1].configure(text=self.DICE_FACES[d2 - 1])
        self.sum_label.configure(text=f"Soma: {total}")

        self.rounds += 1
        chosen = self.chosen_numbers
        multiplier = 0
        reason = ""

        # Priority: doubles > sum match > single die match
        if d1 == d2 and d1 in chosen:
            multiplier = 5
            reason = f"🎯 DUPLA EXATA! {self.DICE_FACES[d1-1]}{self.DICE_FACES[d2-1]} — 5×"
        elif total in chosen:
            multiplier = 3
            reason = f"➕ SOMA {total} ACERTOU! — 3×"
        elif d1 in chosen or d2 in chosen:
            multiplier = 2
            matched = d1 if d1 in chosen else d2
            reason = f"✅ Dado {self.DICE_FACES[matched-1]} acertou! — 2×"

        if multiplier > 0:
            self.wins += 1
            prize = round(self.current_bet * multiplier, 2)
            self.balance += prize
            msg = f"{reason}\n💰 Ganhou R$ {prize:.2f}!"
            color = "#00FF88"
            self.result_frame.configure(border_color=color, border_width=3)
        else:
            self.balance -= self.current_bet
            msg = f"❌ Nenhum acerto! Dados: {self.DICE_FACES[d1-1]} {self.DICE_FACES[d2-1]}\n💸 Perdeu R$ {self.current_bet:.2f}"
            color = "#FF4444"
            self.result_frame.configure(border_color=color, border_width=2)

        self.result_label.configure(text=msg, text_color=color)
        self.balance_label.configure(text=self._balance_text())
        self.stats_label.configure(text=self._stats_text())

        if self.balance <= 0:
            self.result_label.configure(text="💀 BANCA ZERADA! Clique em Novo Jogo.", text_color="#FF0000")
            self.roll_button.configure(state="disabled", text="💀 GAME OVER")
        else:
            self.roll_button.configure(state="normal", text="🎲  ROLAR DADOS")
            self.bet_entry.delete(0, "end")

        self.rolling = False

    def reset(self) -> None:
        self.balance       = self.INITIAL_BALANCE
        self.current_bet   = 0.0
        self.chosen_numbers = set()
        self.rolling       = False
        self.rounds        = 0
        self.wins          = 0

        self.balance_label.configure(text=self._balance_text())
        self.stats_label.configure(text=self._stats_text())
        self.result_label.configure(text="Escolha seus números e role os dados!", text_color="#CCCCCC")
        self.result_frame.configure(border_width=0)
        self.roll_button.configure(state="normal", text="🎲  ROLAR DADOS")
        self.bet_entry.delete(0, "end")
        self.chosen_label.configure(text="Nenhum número selecionado", text_color="#888888")
        self.sum_label.configure(text="")

        for n, btn in self.num_buttons.items():
            btn.configure(fg_color="#222222", border_width=0)

        for lbl in self.dice_labels:
            lbl.configure(text="🎲")
