import random
import tkinter as tk

import customtkinter as ctk
from tkinter import messagebox


class DoubleGame:
    """
    Double game — spinning wheel with 14 segments, identical to Blaze Double.

    Segments
    --------
    ⚫ Black  — 7 / 14 ≈ 50.0 %  — pays 2×
    🔴 Red    — 6 / 14 ≈ 42.8 %  — pays 2×
    ⬜ White  — 1 / 14 ≈  7.1 %  — pays 14×  (jackpot)

    Animation
    ---------
    The winning segment is drawn before animation starts (fair play).
    The wheel spins at least 3 full rotations then decelerates progressively
    and stops with the correct segment centred under the golden pointer.

    Canvas rendering
    ----------------
    _draw_wheel(offset) renders the 14 coloured rectangles so that
    SEGMENTS[offset % 14] always appears in the central position (i = 7).
    Formula:  real_index = (offset - 7 + column_index) % 14
    """

    SEGMENTS: list[str] = ["⚫"] * 7 + ["🔴"] * 6 + ["⬜"] * 1

    MULTIPLIER  = {"⚫": 2,        "🔴": 2,        "⬜": 14}
    BG_COLOR    = {"⚫": "#111111", "🔴": "#CC0000", "⬜": "#DDDDDD"}
    TEXT_COLOR  = {"⚫": "#FFFFFF", "🔴": "#FFFFFF", "⬜": "#000000"}
    NAME        = {"⚫": "PRETO",   "🔴": "VERMELHO","⬜": "BRANCO"}

    TICK_MS         = 30   # ms per animation frame
    INITIAL_BALANCE = 1_000.00

    def __init__(self, root: ctk.CTkToplevel) -> None:
        self.root = root
        self.root.title("🎡 Double")
        self.root.geometry("560x860")
        self.root.resizable(True, True)
        self.root.minsize(560, 720)
        self.root.bind("<F11>", lambda _: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda _: self.root.attributes("-fullscreen", False))

        # State
        self.balance: float      = self.INITIAL_BALANCE
        self.current_bet: float  = 0.0
        self.chosen_color: str | None = None
        self.spinning: bool      = False
        self.job_id              = None
        self.history: list[str]  = []

        # Animation
        self._wheel_offset: int  = 0
        self._tick_count: int    = 0
        self._total_ticks: int   = 0
        self._result: str | None = None

        # Stats
        self.rounds: int  = 0
        self.wins: int    = 0

        self._build_ui()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        main = ctk.CTkFrame(self.root, fg_color="#0d0d0d", corner_radius=0)
        main.pack(fill="both", expand=True)

        ctk.CTkLabel(
            main, text="🎡  DOUBLE",
            font=("Arial", 30, "bold"), text_color="#FFD700",
        ).pack(pady=(20, 2))

        ctk.CTkLabel(
            main, text="Aposte em Preto, Vermelho ou Branco!",
            font=("Arial", 12), text_color="#AAAAAA",
        ).pack()

        self.balance_label = ctk.CTkLabel(
            main, text=self._balance_text(),
            font=("Arial", 15, "bold"), text_color="#00FF00",
        )
        self.balance_label.pack(pady=(8, 0))

        # Wheel canvas
        canvas_bg = ctk.CTkFrame(main, fg_color="#1a1a1a", corner_radius=14)
        canvas_bg.pack(padx=20, pady=12, fill="x")

        self.canvas = tk.Canvas(
            canvas_bg,
            bg="#1a1a1a", highlightthickness=0,
        )
        self.canvas.pack(pady=10, padx=10, fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # History bar
        hist_frame = ctk.CTkFrame(main, fg_color="#111111", corner_radius=8)
        hist_frame.pack(padx=20, pady=(0, 10), fill="x")

        ctk.CTkLabel(
            hist_frame, text="Últimos:",
            font=("Arial", 11), text_color="#666666",
        ).pack(side="left", padx=8, pady=6)

        self.history_label = ctk.CTkLabel(
            hist_frame, text="—",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        )
        self.history_label.pack(side="left", padx=4, pady=6)

        # Bet row
        bet_row = ctk.CTkFrame(main, fg_color="#0d0d0d")
        bet_row.pack(padx=20, pady=4, fill="x")

        ctk.CTkLabel(
            bet_row, text="Aposta (R$):",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        ).pack(side="left", padx=8)

        self.bet_entry = ctk.CTkEntry(
            bet_row, placeholder_text="Ex: 50.00",
            font=("Arial", 13), corner_radius=8,
            fg_color="#1a1a1a", border_color="#6600CC",
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

        # Color buttons
        color_row = ctk.CTkFrame(main, fg_color="#0d0d0d")
        color_row.pack(padx=20, pady=10, fill="x")

        self.btn_black = ctk.CTkButton(
            color_row, text="⚫  PRETO\n2×",
            command=lambda: self._select_color("⚫"),
            font=("Arial", 15, "bold"), height=70, corner_radius=10,
            fg_color="#222222", hover_color="#333333", text_color="#FFFFFF",
        )
        self.btn_black.pack(side="left", padx=(0, 6), fill="x", expand=True)

        self.btn_red = ctk.CTkButton(
            color_row, text="🔴  VERMELHO\n2×",
            command=lambda: self._select_color("🔴"),
            font=("Arial", 15, "bold"), height=70, corner_radius=10,
            fg_color="#880000", hover_color="#AA0000", text_color="#FFFFFF",
        )
        self.btn_red.pack(side="left", padx=6, fill="x", expand=True)

        self.btn_white = ctk.CTkButton(
            color_row, text="⬜  BRANCO\n14×",
            command=lambda: self._select_color("⬜"),
            font=("Arial", 15, "bold"), height=70, corner_radius=10,
            fg_color="#444444", hover_color="#555555", text_color="#FFFFFF",
        )
        self.btn_white.pack(side="left", padx=(6, 0), fill="x", expand=True)

        self.selection_label = ctk.CTkLabel(
            main, text="Escolha uma cor para apostar",
            font=("Arial", 13), text_color="#888888",
        )
        self.selection_label.pack(pady=(2, 0))

        # Spin button
        self.spin_button = ctk.CTkButton(
            main, text="🎡  GIRAR",
            command=self.spin,
            font=("Arial", 18, "bold"), height=55, corner_radius=10,
            fg_color="#6600CC", hover_color="#4a0099", text_color="#FFFFFF",
        )
        self.spin_button.pack(padx=20, pady=10, fill="x")

        # Result
        self.result_frame = ctk.CTkFrame(main, fg_color="#111111", corner_radius=10)
        self.result_frame.pack(padx=20, pady=4, fill="x")

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Escolha uma cor e gire a roda!",
            font=("Arial", 15, "bold"), text_color="#CCCCCC", wraplength=480,
        )
        self.result_label.pack(pady=18, padx=16)

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

    # ── Wheel rendering ──────────────────────────────────────

    def _on_canvas_resize(self, event) -> None:
        self._canvas_w = max(event.width, 100)
        self._canvas_h = max(event.height, 60)
        self._draw_wheel(self._wheel_offset)

    def _draw_wheel(self, offset: int = 0) -> None:
        """
        Render the 14 coloured segments on the canvas.

        The segment shown at the central column (i = 7) is always
        SEGMENTS[offset % 14].  Each column index maps to:
            real_index = (offset - 7 + i) % len(SEGMENTS)
        """
        w = getattr(self, "_canvas_w", 500)
        h = getattr(self, "_canvas_h", 110)
        self.canvas.delete("wheel")
        total  = len(self.SEGMENTS)
        seg_w  = w // 14
        mid    = w // 2
        y1     = int(h * 0.22)
        y2     = int(h * 0.88)

        for i in range(16):  # one extra column on each side to avoid gaps
            real_idx = (offset - 7 + i) % total
            color    = self.SEGMENTS[real_idx]
            x1 = i * seg_w - (seg_w // 2)
            x2 = x1 + seg_w - 2

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=self.BG_COLOR[color], outline="#000000", width=2, tags="wheel",
            )
            self.canvas.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2,
                text=color, font=("Arial", 20),
                fill=self.TEXT_COLOR[color], tags="wheel",
            )

        # Golden pointer arrow at top-centre
        self.canvas.create_polygon(
            mid, 4, mid - 8, 18, mid + 8, 18,
            fill="#FFD700", outline="#FFD700", tags="wheel",
        )

        # Golden border on the central segment (the result indicator)
        self.canvas.create_rectangle(
            mid - seg_w // 2, y1 - 2, mid + seg_w // 2, y2 + 2,
            outline="#FFD700", width=3, tags="wheel",
        )

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

    def _select_color(self, color: str) -> None:
        if self.spinning:
            return
        self.chosen_color = color

        styles = {
            "⚫": ("#FFFFFF", "#111111", "#333333"),
            "🔴": ("#FFFFFF", "#CC0000", "#AA0000"),
            "⬜": ("#000000", "#EEEEEE", "#CCCCCC"),
        }
        defaults = {
            "⚫": ("#FFFFFF", "#222222", "#333333"),
            "🔴": ("#FFFFFF", "#880000", "#AA0000"),
            "⬜": ("#FFFFFF", "#444444", "#555555"),
        }

        for symbol, btn in [("⚫", self.btn_black), ("🔴", self.btn_red), ("⬜", self.btn_white)]:
            if symbol == color:
                tc, fc, hc = styles[symbol]
                btn.configure(
                    fg_color=fc, hover_color=hc, text_color=tc,
                    border_color="#FFD700", border_width=3,
                )
            else:
                tc, fc, hc = defaults[symbol]
                btn.configure(fg_color=fc, hover_color=hc, text_color=tc, border_width=0)

        hint_color = self.BG_COLOR[color] if color != "⚫" else "#AAAAAA"
        self.selection_label.configure(
            text=f"Apostando em: {color} {self.NAME[color]}  ({self.MULTIPLIER[color]}×)",
            text_color=hint_color,
        )

    def _update_history(self) -> None:
        if not self.history:
            self.history_label.configure(text="—")
            return
        self.history_label.configure(text="  ".join(self.history[-10:]))

    # ── Game logic ───────────────────────────────────────────

    def spin(self) -> None:
        if self.spinning:
            return
        if self.chosen_color is None:
            messagebox.showerror("Erro", "Escolha uma cor antes de girar!")
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

        self.balance -= self.current_bet
        self.balance_label.configure(text=self._balance_text())

        # Draw result before animation (fair play)
        self._result = random.choice(self.SEGMENTS)
        candidates   = [i for i, s in enumerate(self.SEGMENTS) if s == self._result]
        final_offset = random.choice(candidates)

        # Total ticks = 3 full rotations + steps to reach final_offset
        total        = len(self.SEGMENTS)
        extra_steps  = (final_offset - self._wheel_offset) % total
        self._total_ticks = 3 * total + extra_steps
        self._tick_count  = 0

        self.spinning = True
        self.spin_button.configure(state="disabled", text="🎡 GIRANDO...")
        self.result_label.configure(text="🎡 Girando...", text_color="#FFD700")
        self.result_frame.configure(border_width=0)

        self._animate(final_offset)

    def _animate(self, final_offset: int) -> None:
        """Spin the wheel with progressive deceleration in the last rotation."""
        remaining = self._total_ticks - self._tick_count

        if remaining <= 0:
            # Snap to exact result position
            self._wheel_offset = final_offset
            self._draw_wheel(self._wheel_offset)
            self.spinning = False
            self._show_result()
            return

        # Slow down in the last 14 ticks (one full rotation)
        delay = int(self.TICK_MS + (14 - remaining) * 18) if remaining <= 14 else self.TICK_MS

        self._wheel_offset = (self._wheel_offset + 1) % len(self.SEGMENTS)
        self._draw_wheel(self._wheel_offset)
        self._tick_count += 1

        self.job_id = self.root.after(delay, lambda: self._animate(final_offset))

    def _show_result(self) -> None:
        result = self._result
        self.history.append(result)
        self._update_history()
        self.rounds += 1

        name       = self.NAME[result]
        multiplier = self.MULTIPLIER[result]
        won        = (result == self.chosen_color)

        if won:
            self.wins    += 1
            prize         = round(self.current_bet * multiplier, 2)
            self.balance += prize
            self.balance_label.configure(text=self._balance_text())

            if result == "⬜":
                msg   = f"🏆 JACKPOT BRANCO! {multiplier}× — Ganhou R$ {prize:.2f}!"
                color = "#FFD700"
            else:
                msg   = f"✅ {result} {name}! {multiplier}× — Ganhou R$ {prize:.2f}!"
                color = "#00FF88"

            self.result_label.configure(text=msg, text_color=color)
            self.result_frame.configure(border_color=color, border_width=3)
        else:
            msg = (
                f"❌ Caiu {result} {name}. "
                f"Você apostou em {self.chosen_color} {self.NAME[self.chosen_color]}. "
                f"Perdeu R$ {self.current_bet:.2f}"
            )
            self.result_label.configure(text=msg, text_color="#FF4444")
            self.result_frame.configure(border_color="#FF4444", border_width=2)

            if self.balance <= 0:
                self.result_label.configure(
                    text="💀 BANCA ZERADA! Clique em Novo Jogo.",
                    text_color="#FF0000",
                )

        if self.balance > 0:
            self.spin_button.configure(state="normal", text="🎡  GIRAR")
        else:
            self.spin_button.configure(state="disabled", text="💀 GAME OVER")

        self.stats_label.configure(text=self._stats_text())

    def reset(self) -> None:
        if self.job_id:
            self.root.after_cancel(self.job_id)
            self.job_id = None

        self.balance      = self.INITIAL_BALANCE
        self.current_bet  = 0.0
        self.chosen_color = None
        self.spinning     = False
        self.history      = []
        self.rounds       = 0
        self.wins         = 0
        self._wheel_offset = 0

        self.balance_label.configure(text=self._balance_text())
        self.selection_label.configure(text="Escolha uma cor para apostar", text_color="#888888")
        self.result_label.configure(text="Escolha uma cor e gire a roda!", text_color="#CCCCCC")
        self.result_frame.configure(border_width=0)
        self.history_label.configure(text="—")
        self.stats_label.configure(text=self._stats_text())
        self.spin_button.configure(state="normal", text="🎡  GIRAR")
        self.bet_entry.delete(0, "end")

        for btn, fc, hc, tc in [
            (self.btn_black, "#222222", "#333333", "#FFFFFF"),
            (self.btn_red,   "#880000", "#AA0000", "#FFFFFF"),
            (self.btn_white, "#444444", "#555555", "#FFFFFF"),
        ]:
            btn.configure(fg_color=fc, hover_color=hc, text_color=tc, border_width=0)

        self._draw_wheel(0)
