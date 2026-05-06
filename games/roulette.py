import random
import tkinter as tk

import customtkinter as ctk
from tkinter import messagebox


class Roulette:
    """
    European Roulette — 37 pockets (0–36).

    Bet types supported
    -------------------
    - Single number (0–36)  : pays 35×
    - Red / Black           : pays 2×
    - Even / Odd            : pays 2×
    - Low (1–18) / High (19–36): pays 2×
    - Dozens (1–12 / 13–24 / 25–36): pays 3×
    - Column (columns 1/2/3): pays 3×

    The player may place multiple bets simultaneously.
    All bets are resolved on each spin.
    """

    INITIAL_BALANCE = 1_000.00

    RED_NUMBERS = {
        1, 3, 5, 7, 9, 12, 14, 16, 18,
        19, 21, 23, 25, 27, 30, 32, 34, 36,
    }

    # Layout: rows of 3 numbers for the roulette grid (1–36)
    GRID = [
        [1,  2,  3],
        [4,  5,  6],
        [7,  8,  9],
        [10, 11, 12],
        [13, 14, 15],
        [16, 17, 18],
        [19, 20, 21],
        [22, 23, 24],
        [25, 26, 27],
        [28, 29, 30],
        [31, 32, 33],
        [34, 35, 36],
    ]

    def __init__(self, root: ctk.CTkToplevel) -> None:
        self.root = root
        self.root.title("🎡 Roleta")
        self.root.geometry("700x900")
        self.root.resizable(False, False)

        # State
        self.balance: float          = self.INITIAL_BALANCE
        self.bets: dict[str, float]  = {}   # bet_key -> amount
        self.spinning: bool          = False
        self.job_id                  = None

        # Wheel animation
        self._angle: float = 0.0

        # Stats
        self.rounds: int = 0
        self.wins: int   = 0

        self._build_ui()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        main = ctk.CTkFrame(self.root, fg_color="#0a1a0a", corner_radius=0)
        main.pack(fill="both", expand=True)

        ctk.CTkLabel(
            main, text="🎡  ROLETA EUROPEIA",
            font=("Arial", 28, "bold"), text_color="#FFD700",
        ).pack(pady=(14, 2))

        ctk.CTkLabel(
            main, text="37 números (0–36) | Aposte em quantas opções quiser!",
            font=("Arial", 11), text_color="#AAAAAA",
        ).pack()

        self.balance_label = ctk.CTkLabel(
            main, text=self._balance_text(),
            font=("Arial", 14, "bold"), text_color="#00FF00",
        )
        self.balance_label.pack(pady=(4, 0))

        # ── Wheel canvas ─────────────────────────────────────
        wheel_frame = ctk.CTkFrame(main, fg_color="#111111", corner_radius=12)
        wheel_frame.pack(padx=20, pady=8, fill="x")

        self.canvas = tk.Canvas(
            wheel_frame, width=640, height=90,
            bg="#111111", highlightthickness=0,
        )
        self.canvas.pack(pady=8, padx=8)
        self._draw_strip(0)

        # Golden pointer
        self.canvas.create_polygon(
            320, 4, 313, 16, 327, 16,
            fill="#FFD700", outline="#FFD700",
        )

        # Result display
        self.result_circle = ctk.CTkLabel(
            wheel_frame, text="?",
            font=("Arial", 28, "bold"), text_color="#FFFFFF",
            fg_color="#333333", corner_radius=30, width=60, height=60,
        )
        self.result_circle.pack(pady=(0, 8))

        # ── Bet amount ───────────────────────────────────────
        bet_row = ctk.CTkFrame(main, fg_color="#0a1a0a")
        bet_row.pack(padx=20, pady=4, fill="x")

        ctk.CTkLabel(
            bet_row, text="Valor por aposta (R$):",
            font=("Arial", 12, "bold"), text_color="#FFFFFF",
        ).pack(side="left", padx=8)

        self.bet_entry = ctk.CTkEntry(
            bet_row, placeholder_text="Ex: 20.00",
            font=("Arial", 12), corner_radius=8,
            fg_color="#1a1a1a", border_color="#FFD700",
            text_color="#FFFFFF", width=120,
        )
        self.bet_entry.pack(side="left", padx=6)

        for v in [5, 10, 25, 50]:
            ctk.CTkButton(
                bet_row, text=f"+{v}",
                command=lambda val=v: self._add_bet_amount(val),
                font=("Arial", 10, "bold"), width=40, height=28,
                fg_color="#1a2a1a", hover_color="#2a3a2a",
                text_color="#AAFFAA", corner_radius=6,
            ).pack(side="left", padx=2)

        # ── Outside bets ─────────────────────────────────────
        outside_frame = ctk.CTkFrame(main, fg_color="#0a1a0a")
        outside_frame.pack(padx=20, pady=4, fill="x")

        row1 = ctk.CTkFrame(outside_frame, fg_color="#0a1a0a")
        row1.pack(fill="x", pady=2)

        self._outside_btn(row1, "🔴 Vermelho (2×)", "red",   "#CC0000", "#990000")
        self._outside_btn(row1, "⚫ Preto (2×)",    "black", "#222222", "#333333")
        self._outside_btn(row1, "🟢 Zero (35×)",    "0",     "#006600", "#004400")

        row2 = ctk.CTkFrame(outside_frame, fg_color="#0a1a0a")
        row2.pack(fill="x", pady=2)

        self._outside_btn(row2, "Par (2×)",       "even", "#1a3a1a", "#2a4a2a")
        self._outside_btn(row2, "Ímpar (2×)",     "odd",  "#1a3a1a", "#2a4a2a")
        self._outside_btn(row2, "1–18 (2×)",      "low",  "#1a1a3a", "#2a2a4a")
        self._outside_btn(row2, "19–36 (2×)",     "high", "#1a1a3a", "#2a2a4a")

        row3 = ctk.CTkFrame(outside_frame, fg_color="#0a1a0a")
        row3.pack(fill="x", pady=2)

        self._outside_btn(row3, "1ª Dúzia (3×)",  "dozen1", "#3a1a1a", "#4a2a2a")
        self._outside_btn(row3, "2ª Dúzia (3×)",  "dozen2", "#3a1a1a", "#4a2a2a")
        self._outside_btn(row3, "3ª Dúzia (3×)",  "dozen3", "#3a1a1a", "#4a2a2a")

        # ── Active bets display ──────────────────────────────
        bets_frame = ctk.CTkFrame(main, fg_color="#111111", corner_radius=8)
        bets_frame.pack(padx=20, pady=4, fill="x")

        bets_header = ctk.CTkFrame(bets_frame, fg_color="#111111")
        bets_header.pack(fill="x", padx=8, pady=(6, 0))

        ctk.CTkLabel(
            bets_header, text="Apostas ativas:",
            font=("Arial", 11, "bold"), text_color="#AAAAAA",
        ).pack(side="left")

        ctk.CTkButton(
            bets_header, text="🗑 Limpar tudo",
            command=self._clear_bets,
            font=("Arial", 10), width=100, height=24,
            fg_color="#330000", hover_color="#440000", text_color="#FF8888",
            corner_radius=6,
        ).pack(side="right")

        self.bets_label = ctk.CTkLabel(
            bets_frame, text="Nenhuma aposta ainda.",
            font=("Arial", 11), text_color="#888888", wraplength=620,
        )
        self.bets_label.pack(padx=8, pady=(2, 8))

        # ── Spin & reset buttons ──────────────────────────────
        self.spin_button = ctk.CTkButton(
            main, text="🎡  GIRAR ROLETA",
            command=self.spin,
            font=("Arial", 17, "bold"), height=50, corner_radius=10,
            fg_color="#006600", hover_color="#004400", text_color="#FFFFFF",
        )
        self.spin_button.pack(padx=20, pady=(6, 2), fill="x")

        ctk.CTkButton(
            main, text="🔄 NOVO JOGO (resetar banca)",
            command=self.reset,
            font=("Arial", 12, "bold"), height=34, corner_radius=8,
            fg_color="#1a1a1a", hover_color="#2a2a2a", text_color="#888888",
        ).pack(padx=20, pady=(2, 4), fill="x")

        # ── Result ───────────────────────────────────────────
        self.result_frame = ctk.CTkFrame(main, fg_color="#111111", corner_radius=10)
        self.result_frame.pack(padx=20, pady=4, fill="x")

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Coloque suas apostas e gire a roleta!",
            font=("Arial", 13, "bold"), text_color="#CCCCCC", wraplength=640,
        )
        self.result_label.pack(pady=12, padx=16)

        self.stats_label = ctk.CTkLabel(
            main, text=self._stats_text(),
            font=("Arial", 11), text_color="#555555",
        )
        self.stats_label.pack(pady=(2, 8))

    def _outside_btn(
        self, parent, text: str, key: str, fg: str, hover: str
    ) -> None:
        ctk.CTkButton(
            parent, text=text,
            command=lambda k=key: self._place_bet(k),
            font=("Arial", 11, "bold"), height=34, corner_radius=8,
            fg_color=fg, hover_color=hover, text_color="#FFFFFF",
        ).pack(side="left", padx=3, fill="x", expand=True)

    # ── Wheel strip ──────────────────────────────────────────

    def _num_color(self, n: int) -> str:
        if n == 0:      return "#006600"
        if n in self.RED_NUMBERS: return "#CC0000"
        return "#111111"

    def _draw_strip(self, offset: int) -> None:
        """Render a scrolling strip of roulette numbers centred on offset."""
        self.canvas.delete("strip")
        numbers = [0] + list(range(1, 37))   # 37 pockets
        total   = len(numbers)
        seg_w   = 640 // 14
        # centre column index = 7 → shows numbers[(offset) % total]

        for i in range(16):
            idx = (offset - 7 + i) % total
            num = numbers[idx]
            bg  = self._num_color(num)
            x1  = i * seg_w - seg_w // 2
            x2  = x1 + seg_w - 2
            y1, y2 = 20, 82

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg, outline="#333333", width=1, tags="strip")
            self.canvas.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2,
                text=str(num), font=("Arial", 13, "bold"),
                fill="#FFFFFF", tags="strip",
            )

        mid = 320
        self.canvas.create_rectangle(
            mid - seg_w // 2, 18, mid + seg_w // 2, 84,
            outline="#FFD700", width=3, tags="strip",
        )

    # ── Helpers ──────────────────────────────────────────────

    def _balance_text(self) -> str:
        return f"💰 Banca: R$ {self.balance:.2f}"

    def _stats_text(self) -> str:
        rate = (self.wins / self.rounds * 100) if self.rounds else 0
        return f"Rodadas: {self.rounds} | Rodadas vencidas: {self.wins} | Taxa: {rate:.2f}%"

    def _add_bet_amount(self, value: int) -> None:
        text = self.bet_entry.get().strip()
        try:
            new_value = float(text) + value if text else float(value)
        except ValueError:
            new_value = float(value)
        self.bet_entry.delete(0, "end")
        self.bet_entry.insert(0, f"{new_value:.2f}")

    def _bet_amount(self) -> float | None:
        try:
            amount = float(self.bet_entry.get().strip())
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor de aposta válido!")
            return None

    def _place_bet(self, key: str) -> None:
        if self.spinning:
            return
        amount = self._bet_amount()
        if amount is None:
            return
        if amount > self.balance:
            messagebox.showerror("Erro", f"Saldo insuficiente (R$ {self.balance:.2f})")
            return
        self.bets[key] = self.bets.get(key, 0) + amount
        self._refresh_bets_label()

    def _clear_bets(self) -> None:
        self.bets = {}
        self._refresh_bets_label()

    def _refresh_bets_label(self) -> None:
        if not self.bets:
            self.bets_label.configure(text="Nenhuma aposta ainda.")
            return

        label_map = {
            "red": "Vermelho", "black": "Preto", "0": "Zero",
            "even": "Par", "odd": "Ímpar", "low": "1–18", "high": "19–36",
            "dozen1": "1ª Dúzia", "dozen2": "2ª Dúzia", "dozen3": "3ª Dúzia",
        }
        parts = []
        total = 0
        for key, amount in self.bets.items():
            name = label_map.get(key, f"Nº {key}")
            parts.append(f"{name}: R${amount:.0f}")
            total += amount
        self.bets_label.configure(
            text="  |  ".join(parts) + f"   [Total: R$ {total:.2f}]"
        )

    def _resolve_bet(self, key: str, result: int) -> float:
        """Return the prize (including stake) for a single bet key given the result."""
        r = result
        if key == str(r):             return 36   # single number 35×+stake
        if key == "red"   and r in self.RED_NUMBERS and r != 0: return 2
        if key == "black" and r not in self.RED_NUMBERS and r != 0: return 2
        if key == "even"  and r != 0 and r % 2 == 0: return 2
        if key == "odd"   and r != 0 and r % 2 == 1: return 2
        if key == "low"   and 1 <= r <= 18:  return 2
        if key == "high"  and 19 <= r <= 36: return 2
        if key == "dozen1" and 1 <= r <= 12:  return 3
        if key == "dozen2" and 13 <= r <= 24: return 3
        if key == "dozen3" and 25 <= r <= 36: return 3
        return 0

    # ── Game logic ───────────────────────────────────────────

    def spin(self) -> None:
        if self.spinning:
            return
        if not self.bets:
            messagebox.showerror("Erro", "Coloque pelo menos uma aposta antes de girar!")
            return
        total_bet = sum(self.bets.values())
        if total_bet > self.balance:
            messagebox.showerror("Erro", f"Apostas excedem sua banca (R$ {self.balance:.2f})")
            return

        self.balance -= total_bet
        self.balance_label.configure(text=self._balance_text())
        self.spinning = True
        self.spin_button.configure(state="disabled", text="🎡 GIRANDO...")
        self.result_frame.configure(border_width=0)

        result_number = random.randint(0, 36)
        numbers = [0] + list(range(1, 37))
        final_offset = numbers.index(result_number)

        # Animate
        self._strip_offset = 0
        total_ticks = 3 * 37 + (final_offset - self._strip_offset) % 37
        self._animate_strip(final_offset, total_ticks, 0, result_number)

    def _animate_strip(
        self, final_offset: int, total_ticks: int, tick: int, result_number: int
    ) -> None:
        remaining = total_ticks - tick
        if remaining <= 0:
            self._strip_offset = final_offset
            self._draw_strip(self._strip_offset)
            self.spinning = False
            self._show_result(result_number)
            return

        delay = int(30 + (37 - remaining) * 15) if remaining <= 37 else 30
        self._strip_offset = (self._strip_offset + 1) % 37
        self._draw_strip(self._strip_offset)
        self.job_id = self.root.after(
            delay, lambda: self._animate_strip(final_offset, total_ticks, tick + 1, result_number)
        )

    def _show_result(self, result: int) -> None:
        color = self._num_color(result)
        display_color = "#CC0000" if result in self.RED_NUMBERS else ("#006600" if result == 0 else "#FFFFFF")
        self.result_circle.configure(
            text=str(result), fg_color=color, text_color=display_color if result != 0 else "#FFFFFF"
        )

        self.rounds += 1
        total_prize = 0.0
        winning_bets = []
        losing_bets  = []

        for key, amount in self.bets.items():
            mult = self._resolve_bet(key, result)
            if mult > 0:
                prize = amount * mult
                total_prize += prize
                label_map = {
                    "red": "Vermelho", "black": "Preto", "0": "Zero",
                    "even": "Par", "odd": "Ímpar", "low": "1–18", "high": "19–36",
                    "dozen1": "1ª Dúzia", "dozen2": "2ª Dúzia", "dozen3": "3ª Dúzia",
                }
                name = label_map.get(key, f"Nº {key}")
                winning_bets.append(f"{name}(+R${prize:.0f})")
            else:
                label_map = {
                    "red": "Vermelho", "black": "Preto", "0": "Zero",
                    "even": "Par", "odd": "Ímpar", "low": "1–18", "high": "19–36",
                    "dozen1": "1ª Dúzia", "dozen2": "2ª Dúzia", "dozen3": "3ª Dúzia",
                }
                name = label_map.get(key, f"Nº {key}")
                losing_bets.append(name)

        total_staked = sum(self.bets.values())
        net = total_prize - total_staked

        if total_prize > 0:
            self.wins    += 1
            self.balance += total_prize
            color_msg = "#00FF88"
            result_color_name = "🔴 Vermelho" if result in self.RED_NUMBERS else ("🟢 Zero" if result == 0 else "⚫ Preto")
            msg = (
                f"Saiu: {result} {result_color_name}\n"
                f"✅ Ganhou: {', '.join(winning_bets)}"
            )
            if losing_bets:
                msg += f"\n❌ Perdeu: {', '.join(losing_bets)}"
            msg += f"\n💰 Saldo líquido: {'+' if net >= 0 else ''}R$ {net:.2f}"
        else:
            color_msg = "#FF4444"
            result_color_name = "🔴 Vermelho" if result in self.RED_NUMBERS else ("🟢 Zero" if result == 0 else "⚫ Preto")
            msg = (
                f"Saiu: {result} {result_color_name}\n"
                f"❌ Todas as apostas perderam. -R$ {total_staked:.2f}"
            )

        self.balance_label.configure(text=self._balance_text())
        self.result_label.configure(text=msg, text_color=color_msg)
        self.result_frame.configure(
            border_color=color_msg, border_width=3
        )
        self.stats_label.configure(text=self._stats_text())
        self.bets = {}
        self._refresh_bets_label()

        if self.balance > 0:
            self.spin_button.configure(state="normal", text="🎡  GIRAR ROLETA")
        else:
            self.result_label.configure(text="💀 BANCA ZERADA! Clique em Novo Jogo.", text_color="#FF0000")
            self.spin_button.configure(state="disabled", text="💀 GAME OVER")

    def reset(self) -> None:
        if self.job_id:
            self.root.after_cancel(self.job_id)
            self.job_id = None

        self.balance  = self.INITIAL_BALANCE
        self.bets     = {}
        self.spinning = False
        self.rounds   = 0
        self.wins     = 0
        self._strip_offset = 0

        self.balance_label.configure(text=self._balance_text())
        self.result_label.configure(
            text="Coloque suas apostas e gire a roleta!", text_color="#CCCCCC"
        )
        self.result_frame.configure(border_width=0)
        self.result_circle.configure(text="?", fg_color="#333333", text_color="#FFFFFF")
        self.stats_label.configure(text=self._stats_text())
        self.spin_button.configure(state="normal", text="🎡  GIRAR ROLETA")
        self.bet_entry.delete(0, "end")
        self._refresh_bets_label()
        self._draw_strip(0)
