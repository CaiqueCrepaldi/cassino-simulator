import random
import tkinter as tk

import customtkinter as ctk
from tkinter import messagebox


class AviatorGame:
    """
    Aviator game — faithful recreation of the real Aviator mechanic.

    How it works
    ------------
    - A crash multiplier is drawn from an exponential distribution before
      the round starts (the player never sees it in advance).
    - The multiplier grows exponentially every TICK_MS milliseconds.
    - The player must click RETIRAR (cash out) before the crash to win
      Bet × current multiplier.  Missing the crash means losing the bet.

    Crash distribution
    ------------------
    crash = 0.99 / (1 - u * 0.99),  u ~ Uniform[0, 1)
    Most crashes happen between 1× and 3×; very high multipliers are rare.
    Maximum displayed value is capped at 100×.
    """

    TICK_MS    = 100    # ms between multiplier updates
    GROWTH     = 0.05   # multiplier increment factor per tick
    CANVAS_W   = 540
    CANVAS_H   = 280
    INITIAL_BALANCE = 1_000.00

    def __init__(self, root: ctk.CTkToplevel) -> None:
        self.root = root
        self.root.title("✈️ Aviator")
        self.root.geometry("580x820")
        self.root.resizable(True, True)
        self.root.minsize(580, 720)
        self.root.bind("<F11>", lambda _: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda _: self.root.attributes("-fullscreen", False))

        # State
        self.balance: float     = self.INITIAL_BALANCE
        self.current_bet: float = 0.0
        self.multiplier: float  = 1.00
        self.crash_at: float    = 1.00
        self.running: bool      = False
        self.cashed_out: bool   = False
        self.job_id             = None
        self.history: list[float]        = []
        self.trail: list[tuple[int,int]] = []

        # Auto cash out
        self.auto_cashout_enabled: bool  = False
        self.auto_cashout_mult: float    = 0.0

        # Stats
        self.rounds: int     = 0
        self.wins: int       = 0
        self.best_mult: float = 0.0

        self._build_ui()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        main = ctk.CTkFrame(self.root, fg_color="#000000", corner_radius=0)
        main.pack(fill="both", expand=True)

        ctk.CTkLabel(
            main, text="✈️  AVIATOR",
            font=("Arial", 30, "bold"), text_color="#FFFFFF",
        ).pack(pady=(20, 2))

        ctk.CTkLabel(
            main, text="Retire antes do avião voar embora!",
            font=("Arial", 12), text_color="#AAAAAA",
        ).pack(pady=(0, 10))

        self.balance_label = ctk.CTkLabel(
            main, text=self._balance_text(),
            font=("Arial", 15, "bold"), text_color="#00FF00",
        )
        self.balance_label.pack()

        # Canvas
        canvas_frame = ctk.CTkFrame(main, fg_color="#0a0a1a", corner_radius=12)
        canvas_frame.pack(padx=20, pady=12, fill="x")

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#0a0a1a", highlightthickness=0,
        )
        self.canvas.pack(padx=5, pady=5, fill="both", expand=True)

        self.mult_text = self.canvas.create_text(
            self.CANVAS_W // 2, self.CANVAS_H // 2,
            text="1.00x", font=("Arial", 56, "bold"), fill="#FFFFFF",
        )
        self.plane_obj = self.canvas.create_text(
            60, self.CANVAS_H - 40,
            text="✈️", font=("Arial", 32), fill="#FFFFFF",
        )

        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # History bar
        hist_frame = ctk.CTkFrame(main, fg_color="#0d0d0d", corner_radius=8)
        hist_frame.pack(padx=20, pady=(0, 8), fill="x")

        ctk.CTkLabel(
            hist_frame, text="Últimos crashes:",
            font=("Arial", 11), text_color="#888888",
        ).pack(side="left", padx=8, pady=6)

        self.history_label = ctk.CTkLabel(
            hist_frame, text="—",
            font=("Arial", 11, "bold"), text_color="#FFD700",
        )
        self.history_label.pack(side="left", padx=4, pady=6)

        # Auto cash out row
        auto_row = ctk.CTkFrame(main, fg_color="#0d1a0d", corner_radius=8)
        auto_row.pack(padx=20, pady=(4, 0), fill="x")

        ctk.CTkLabel(
            auto_row, text="⚡ Saque Automático:",
            font=("Arial", 13, "bold"), text_color="#00CC66",
        ).pack(side="left", padx=8, pady=8)

        self.auto_entry = ctk.CTkEntry(
            auto_row, placeholder_text="Ex: 2.00x",
            font=("Arial", 13), corner_radius=8,
            fg_color="#1a1a1a", border_color="#00AA44",
            text_color="#FFFFFF", width=110,
        )
        self.auto_entry.pack(side="left", padx=6, pady=8)

        self.auto_toggle = ctk.CTkButton(
            auto_row, text="OFF",
            command=self._toggle_auto_cashout,
            font=("Arial", 13, "bold"), width=70, height=32,
            corner_radius=8,
            fg_color="#333333", hover_color="#444444", text_color="#888888",
        )
        self.auto_toggle.pack(side="left", padx=6, pady=8)

        self.auto_status = ctk.CTkLabel(
            auto_row, text="Desativado",
            font=("Arial", 11), text_color="#555555",
        )
        self.auto_status.pack(side="left", padx=6)

        # Bet row
        bet_row = ctk.CTkFrame(main, fg_color="#000000")
        bet_row.pack(padx=20, pady=4, fill="x")

        ctk.CTkLabel(
            bet_row, text="Aposta (R$):",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        ).pack(side="left", padx=8)

        self.bet_entry = ctk.CTkEntry(
            bet_row, placeholder_text="Ex: 50.00",
            font=("Arial", 13), corner_radius=8,
            fg_color="#1a1a1a", border_color="#0055CC",
            text_color="#FFFFFF", width=140,
        )
        self.bet_entry.pack(side="left", padx=8)

        for value in [10, 25, 50, 100]:
            ctk.CTkButton(
                bet_row, text=f"+{value}",
                command=lambda v=value: self._add_bet(v),
                font=("Arial", 11, "bold"), width=45, height=30,
                fg_color="#1a1a2e", hover_color="#16213e",
                text_color="#AAAAFF", corner_radius=6,
            ).pack(side="left", padx=2)

        # Action buttons
        btn_row = ctk.CTkFrame(main, fg_color="#000000")
        btn_row.pack(padx=20, pady=10, fill="x")

        self.bet_button = ctk.CTkButton(
            btn_row, text="✈️  APOSTAR & VOAR",
            command=self.start_round,
            font=("Arial", 17, "bold"), height=55, corner_radius=10,
            fg_color="#0055CC", hover_color="#003D99", text_color="#FFFFFF",
        )
        self.bet_button.pack(side="left", padx=(0, 8), fill="x", expand=True)

        self.cash_button = ctk.CTkButton(
            btn_row, text="💰  RETIRAR",
            command=self.cash_out,
            font=("Arial", 17, "bold"), height=55, corner_radius=10,
            fg_color="#CC7700", hover_color="#995500", text_color="#FFFFFF",
            state="disabled",
        )
        self.cash_button.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            main, text="🔄 NOVO JOGO (resetar banca)",
            command=self.reset,
            font=("Arial", 12, "bold"), height=35, corner_radius=8,
            fg_color="#222222", hover_color="#333333", text_color="#AAAAAA",
        ).pack(padx=20, pady=(0, 8), fill="x")

        self.status_label = ctk.CTkLabel(
            main, text="Defina sua aposta e clique em APOSTAR!",
            font=("Arial", 14, "bold"), text_color="#CCCCCC", wraplength=500,
        )
        self.status_label.pack(pady=8, padx=20)

        self.stats_label = ctk.CTkLabel(
            main, text=self._stats_text(),
            font=("Arial", 11), text_color="#666666",
        )
        self.stats_label.pack(pady=(0, 10))

    # ── Helpers ──────────────────────────────────────────────

    def _on_canvas_resize(self, event) -> None:
        self.CANVAS_W = event.width
        self.CANVAS_H = event.height
        self.canvas.delete("grid")
        for y in range(0, self.CANVAS_H, 40):
            self.canvas.create_line(0, y, self.CANVAS_W, y, fill="#111133", width=1, tags="grid")
        for x in range(0, self.CANVAS_W, 60):
            self.canvas.create_line(x, 0, x, self.CANVAS_H, fill="#111133", width=1, tags="grid")
        self.canvas.coords(self.mult_text, self.CANVAS_W // 2, self.CANVAS_H // 2)
        if not self.running:
            self.canvas.coords(self.plane_obj, 60, self.CANVAS_H - 40)
        self.canvas.tag_raise(self.mult_text)
        self.canvas.tag_raise(self.plane_obj)

    def _balance_text(self) -> str:
        return f"💰 Banca: R$ {self.balance:.2f}"

    def _stats_text(self) -> str:
        best = f"{self.best_mult:.2f}x" if self.best_mult > 0 else "—"
        return f"Rodadas: {self.rounds} | Vitórias: {self.wins} | Maior multiplicador: {best}"

    def _toggle_auto_cashout(self) -> None:
        if self.auto_cashout_enabled:
            self.auto_cashout_enabled = False
            self.auto_toggle.configure(
                text="OFF", fg_color="#333333",
                hover_color="#444444", text_color="#888888",
            )
            self.auto_status.configure(text="Desativado", text_color="#555555")
        else:
            raw = self.auto_entry.get().strip()
            try:
                value = float(raw)
                if value <= 1.0:
                    messagebox.showerror("Erro", "O multiplicador de saque automático deve ser maior que 1.00x!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Digite um multiplicador válido (Ex: 2.00)")
                return
            self.auto_cashout_mult    = value
            self.auto_cashout_enabled = True
            self.auto_toggle.configure(
                text="ON", fg_color="#007733",
                hover_color="#005522", text_color="#FFFFFF",
            )
            self.auto_status.configure(
                text=f"Saque em {value:.2f}x", text_color="#00FF88",
            )

    def _add_bet(self, value: int) -> None:
        current = self.bet_entry.get().strip()
        try:
            new_value = float(current) + value if current else float(value)
        except ValueError:
            new_value = float(value)
        self.bet_entry.delete(0, "end")
        self.bet_entry.insert(0, f"{new_value:.2f}")

    def _multiplier_color(self, m: float) -> str:
        if m < 1.5:   return "#FFFFFF"
        if m < 2.0:   return "#FFD700"
        if m < 5.0:   return "#FF8800"
        return "#FF4444"

    def _history_color(self, m: float) -> str:
        if m < 2.0:   return "#FF4444"
        if m < 5.0:   return "#FFD700"
        return "#00FF88"

    def _generate_crash(self) -> float:
        """Exponential distribution — same formula as real Aviator."""
        u = random.random()
        return round(min(0.99 / (1.0 - u * 0.99), 100.0), 2)

    def _clear_canvas(self) -> None:
        self.canvas.delete("trail")
        self.trail = []
        self.canvas.itemconfig(self.mult_text, text="1.00x", fill="#FFFFFF")
        self.canvas.coords(self.plane_obj, 60, self.CANVAS_H - 40)
        self.canvas.itemconfig(self.plane_obj, text="✈️")

    def _update_history(self) -> None:
        if not self.history:
            self.history_label.configure(text="—", text_color="#FFD700")
            return
        self.history_label.configure(
            text="  ".join(f"{m:.2f}x" for m in self.history[-8:]),
            text_color="#FFD700",
        )

    # ── Game logic ───────────────────────────────────────────

    def start_round(self) -> None:
        if self.running:
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

        self.balance    -= self.current_bet
        self.crash_at    = self._generate_crash()
        self.multiplier  = 1.00
        self.cashed_out  = False
        self.running     = True

        self._clear_canvas()
        self.balance_label.configure(text=self._balance_text())
        self.bet_button.configure(state="disabled")
        self.cash_button.configure(state="normal")
        self.bet_entry.configure(state="disabled")
        self.auto_entry.configure(state="disabled")
        self.auto_toggle.configure(state="disabled")
        self.status_label.configure(
            text=f"✈️ Voando... Aposta: R$ {self.current_bet:.2f}",
            text_color="#FFFFFF",
        )

        self._tick()

    def _tick(self) -> None:
        if not self.running:
            return

        self.multiplier = round(
            self.multiplier + self.GROWTH * (self.multiplier ** 0.5), 2
        )
        color = self._multiplier_color(self.multiplier)

        self.canvas.itemconfig(
            self.mult_text, text=f"{self.multiplier:.2f}x", fill=color
        )

        # Move plane along a rising curve
        progress = min(self.multiplier / max(self.crash_at, 2), 1.0)
        px = int(60 + progress * (self.CANVAS_W - 100))
        py = int((self.CANVAS_H - 40) - progress * (self.CANVAS_H - 60) * 0.85)
        self.canvas.coords(self.plane_obj, px, py)

        # Draw trail
        self.trail.append((px, py))
        if len(self.trail) >= 2:
            x1, y1 = self.trail[-2]
            x2, y2 = self.trail[-1]
            self.canvas.create_line(x1, y1, x2, y2, fill="#4488FF", width=2, tags="trail")

        self.status_label.configure(
            text=f"✈️ Voando... {self.multiplier:.2f}x | "
                 f"Retire agora: R$ {self.current_bet * self.multiplier:.2f}",
            text_color=color,
        )

        if self.auto_cashout_enabled and not self.cashed_out and self.multiplier >= self.auto_cashout_mult:
            self.cash_out()

        if self.multiplier >= self.crash_at:
            self._crash()
        else:
            self.job_id = self.root.after(self.TICK_MS, self._tick)

    def _crash(self) -> None:
        self.running = False

        self.canvas.itemconfig(self.plane_obj, text="💥")
        self.canvas.itemconfig(
            self.mult_text, text=f"💥 {self.crash_at:.2f}x", fill="#FF2222"
        )

        self.history.append(self.crash_at)
        self._update_history()
        self.rounds += 1

        self.cash_button.configure(state="disabled")
        self.bet_button.configure(state="normal")
        self.bet_entry.configure(state="normal")
        self.auto_entry.configure(state="normal")
        self.auto_toggle.configure(state="normal")

        if not self.cashed_out:
            self.status_label.configure(
                text=f"💥 CRASH em {self.crash_at:.2f}x! Perdeu R$ {self.current_bet:.2f}",
                text_color="#FF3333",
            )
            if self.balance <= 0:
                self.status_label.configure(
                    text="💀 BANCA ZERADA! Clique em Novo Jogo.",
                    text_color="#FF0000",
                )
                self.bet_button.configure(state="disabled")

        self.stats_label.configure(text=self._stats_text())

    def cash_out(self) -> None:
        if not self.running or self.cashed_out:
            return

        self.cashed_out = True
        prize = round(self.current_bet * self.multiplier, 2)
        self.balance += prize
        self.wins    += 1

        if self.multiplier > self.best_mult:
            self.best_mult = self.multiplier

        self.balance_label.configure(text=self._balance_text())
        self.status_label.configure(
            text=f"✅ Retirou em {self.multiplier:.2f}x! Ganhou R$ {prize:.2f}",
            text_color="#00FF88",
        )
        self.cash_button.configure(state="disabled")

    def reset(self) -> None:
        if self.job_id:
            self.root.after_cancel(self.job_id)
            self.job_id = None

        self.balance     = self.INITIAL_BALANCE
        self.current_bet = 0.0
        self.multiplier  = 1.00
        self.running     = False
        self.cashed_out  = False
        self.rounds      = 0
        self.wins        = 0
        self.best_mult   = 0.0
        self.history     = []

        self.auto_cashout_enabled = False
        self.auto_cashout_mult    = 0.0

        self.balance_label.configure(text=self._balance_text())
        self.status_label.configure(
            text="Defina sua aposta e clique em APOSTAR!", text_color="#CCCCCC"
        )
        self.history_label.configure(text="—")
        self.stats_label.configure(text=self._stats_text())
        self.bet_button.configure(state="normal")
        self.cash_button.configure(state="disabled")
        self.bet_entry.configure(state="normal")
        self.bet_entry.delete(0, "end")
        self.auto_entry.configure(state="normal")
        self.auto_entry.delete(0, "end")
        self.auto_toggle.configure(
            text="OFF", fg_color="#333333",
            hover_color="#444444", text_color="#888888", state="normal",
        )
        self.auto_status.configure(text="Desativado", text_color="#555555")
        self._clear_canvas()
