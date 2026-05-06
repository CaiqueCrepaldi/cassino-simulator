import random

import customtkinter as ctk
from tkinter import messagebox


class Baccarat:
    """
    Baccarat — classic casino card game.

    Rules
    -----
    - Standard 52-card deck, reshuffled each round.
    - Card values: A=1, 2-9=face, 10/J/Q/K=0. Only last digit of total counts.
    - Natural: 8 or 9 on initial 2 cards → no more cards drawn.
    - Player draws a third card if total is 0-5; stands on 6-7.
    - Banker drawing depends on Player's third card (standard rules).
    - Bet on Player (1×), Banker (0.95× after 5% commission), or Tie (8×).
    """

    SUITS = ["♠", "♥", "♦", "♣"]
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    RED_SUITS = {"♥", "♦"}
    INITIAL_BALANCE = 1_000.00

    CARD_W     = 52
    CARD_H     = 76
    ANIM_STEPS = 10
    ANIM_MS    = 14

    def __init__(self, root: ctk.CTk, container: ctk.CTkFrame, back_callback, bank) -> None:
        self.root = root
        self.container = container
        self.back_callback = back_callback
        self.bank = bank
        self.root.title("🎴 Baccarat")
        self.current_bet: float = 0.0
        self.chosen_side: str | None = None   # "player", "banker", "tie"
        self.game_active: bool = False

        self.rounds: int = 0
        self.wins: int = 0

        self._build_ui()

    @property
    def balance(self) -> float:
        return self.bank.balance

    @balance.setter
    def balance(self, v: float) -> None:
        self.bank.balance = v

    def _go_back(self) -> None:
        self.back_callback()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        BG = "#0a0a2e"
        bg = ctk.CTkFrame(self.container, fg_color=BG, corner_radius=0)
        bg.pack(fill="both", expand=True)

        main = ctk.CTkFrame(bg, fg_color=BG)
        main.pack(expand=True, fill="y", anchor="center")
        ctk.CTkFrame(main, width=580, height=1, fg_color=BG).pack()

        ctk.CTkButton(
            main, text="← Menu",
            command=self._go_back,
            width=120, height=28,
            fg_color="#14143a", hover_color="#1e1e50",
            text_color="#8888CC", corner_radius=6,
            font=("Arial", 11, "bold"),
        ).pack(pady=(6, 2), anchor="w", padx=8)

        ctk.CTkLabel(
            main, text="🎴  BACCARAT",
            font=("Arial", 26, "bold"), text_color="#FFD700",
        ).pack(pady=(2, 0))

        ctk.CTkLabel(
            main, text="Chegue mais perto do 9 — Jogador: 1×  |  Banca: 0.95×  |  Empate: 8×",
            font=("Arial", 10), text_color="#888899",
        ).pack()

        self.balance_label = ctk.CTkLabel(
            main, text=self._balance_text(),
            font=("Arial", 14, "bold"), text_color="#FFD700",
        )
        self.balance_label.pack(pady=(4, 0))

        # ── Cards row: BANCA (esq.) e JOGADOR (dir.) lado a lado ──
        cards_row = ctk.CTkFrame(main, fg_color=BG)
        cards_row.pack(padx=20, pady=8, fill="x")

        # Banca
        banker_col = ctk.CTkFrame(cards_row, fg_color="#1a0a2e", corner_radius=10)
        banker_col.pack(side="left", fill="both", expand=True, padx=(0, 6))
        banker_col.pack_propagate(False)
        banker_col.configure(height=120)

        ctk.CTkLabel(
            banker_col, text="🟥 BANCA",
            font=("Arial", 12, "bold"), text_color="#FF8888",
        ).pack(pady=(6, 2))

        self.banker_cards_frame = ctk.CTkFrame(banker_col, fg_color="#1a0a2e")
        self.banker_cards_frame.pack(expand=True)

        self.banker_score_label = ctk.CTkLabel(
            banker_col, text="—",
            font=("Arial", 12, "bold"), text_color="#CCCCCC",
        )
        self.banker_score_label.pack(pady=(2, 6))

        # Jogador
        player_col = ctk.CTkFrame(cards_row, fg_color="#0a1a2e", corner_radius=10)
        player_col.pack(side="left", fill="both", expand=True, padx=(6, 0))
        player_col.pack_propagate(False)
        player_col.configure(height=120)

        ctk.CTkLabel(
            player_col, text="🟦 JOGADOR",
            font=("Arial", 12, "bold"), text_color="#88CCFF",
        ).pack(pady=(6, 2))

        self.player_cards_frame = ctk.CTkFrame(player_col, fg_color="#0a1a2e")
        self.player_cards_frame.pack(expand=True)

        self.player_score_label = ctk.CTkLabel(
            player_col, text="—",
            font=("Arial", 12, "bold"), text_color="#CCCCCC",
        )
        self.player_score_label.pack(pady=(2, 6))

        # ── Bet side selector ────────────────────────────────
        side_row = ctk.CTkFrame(main, fg_color=BG)
        side_row.pack(padx=20, pady=(4, 2), fill="x")

        self.side_buttons: dict[str, ctk.CTkButton] = {}
        sides = [
            ("player", "🟦 JOGADOR", "#0055CC", "#003D99"),
            ("tie",    "🟨 EMPATE",  "#886600", "#664400"),
            ("banker", "🟥 BANCA",   "#880000", "#660000"),
        ]
        for key, label, fg, hover in sides:
            btn = ctk.CTkButton(
                side_row, text=label,
                command=lambda k=key: self._choose_side(k),
                font=("Arial", 13, "bold"), height=40, corner_radius=10,
                fg_color=fg, hover_color=hover, text_color="#FFFFFF",
            )
            btn.pack(side="left", padx=3, fill="x", expand=True)
            self.side_buttons[key] = btn

        self.chosen_label = ctk.CTkLabel(
            main, text="Nenhuma aposta selecionada",
            font=("Arial", 11), text_color="#888888",
        )
        self.chosen_label.pack(pady=(2, 0))

        # ── Bet row ──────────────────────────────────────────
        bet_row = ctk.CTkFrame(main, fg_color=BG)
        bet_row.pack(padx=20, pady=6, fill="x")

        ctk.CTkLabel(
            bet_row, text="Aposta (R$):",
            font=("Arial", 12, "bold"), text_color="#FFFFFF",
        ).pack(side="left", padx=8)

        self.bet_entry = ctk.CTkEntry(
            bet_row, placeholder_text="Ex: 50.00",
            font=("Arial", 12), corner_radius=8,
            fg_color="#14143a", border_color="#FFD700",
            text_color="#FFFFFF", width=130,
        )
        self.bet_entry.pack(side="left", padx=6)

        for v in [10, 25, 50, 100]:
            ctk.CTkButton(
                bet_row, text=f"+{v}",
                command=lambda val=v: self._add_bet(val),
                font=("Arial", 11, "bold"), width=44, height=28,
                fg_color="#14143a", hover_color="#1e1e50",
                text_color="#FFD700", corner_radius=6,
            ).pack(side="left", padx=2)

        # ── Deal button ──────────────────────────────────────
        self.deal_button = ctk.CTkButton(
            main, text="🎴  DISTRIBUIR",
            command=self.deal,
            font=("Arial", 17, "bold"), height=50, corner_radius=10,
            fg_color="#FFD700", hover_color="#CCA800", text_color="#000000",
        )
        self.deal_button.pack(padx=20, pady=(6, 2), fill="x")

        ctk.CTkButton(
            main, text="🔄 NOVO JOGO (resetar banca)",
            command=self.reset,
            font=("Arial", 11, "bold"), height=30, corner_radius=8,
            fg_color="#14143a", hover_color="#1e1e50", text_color="#888888",
        ).pack(padx=20, pady=(0, 4), fill="x")

        # ── Result ───────────────────────────────────────────
        self.result_frame = ctk.CTkFrame(main, fg_color="#0a0a1e", corner_radius=10)
        self.result_frame.pack(padx=20, pady=4, fill="x")

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Selecione sua aposta e clique em DISTRIBUIR!",
            font=("Arial", 13, "bold"), text_color="#AAAADD", wraplength=540,
        )
        self.result_label.pack(pady=10, padx=16)

        self.stats_label = ctk.CTkLabel(
            main, text=self._stats_text(),
            font=("Arial", 11), text_color="#555588",
        )
        self.stats_label.pack(pady=(2, 8))

    # ── Card rendering ───────────────────────────────────────

    def _card_widget(self, parent: ctk.CTkFrame, card: tuple) -> ctk.CTkFrame:
        rank, suit = card
        frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=8, width=self.CARD_W, height=self.CARD_H)
        frame.pack_propagate(False)
        frame.pack(side="left", padx=3)
        color = "#CC0000" if suit in self.RED_SUITS else "#000000"
        ctk.CTkLabel(frame, text=f"{rank}\n{suit}", font=("Arial", 14, "bold"), text_color=color).pack(expand=True)
        return frame

    def _animate_card_in(self, parent: ctk.CTkFrame, card: tuple, on_done=None) -> None:
        rank, suit = card
        frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=8, width=0, height=self.CARD_H)
        frame.pack_propagate(False)
        frame.pack(side="left", padx=3)
        color = "#CC0000" if suit in self.RED_SUITS else "#000000"
        ctk.CTkLabel(frame, text=f"{rank}\n{suit}", font=("Arial", 14, "bold"), text_color=color).pack(expand=True)

        def step(n):
            frame.configure(width=int(self.CARD_W * n / self.ANIM_STEPS))
            if n < self.ANIM_STEPS:
                self.root.after(self.ANIM_MS, lambda: step(n + 1))
            elif on_done:
                on_done()
        step(1)

    def _deal_sequence(self, specs: list, on_complete=None) -> None:
        def next_card(i):
            if i >= len(specs):
                if on_complete:
                    on_complete()
                return
            parent, card = specs[i]
            self._animate_card_in(parent, card, on_done=lambda: next_card(i + 1))
        next_card(0)

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

    def _card_rank_value(self, rank: str) -> int:
        if rank in ("10", "J", "Q", "K"):
            return 0
        if rank == "A":
            return 1
        return int(rank)

    def _bac_value(self, hand: list) -> int:
        return sum(self._card_rank_value(r) for r, _ in hand) % 10

    def _new_deck(self) -> list:
        deck = [(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(deck)
        return deck

    def _choose_side(self, side: str) -> None:
        if self.game_active:
            return
        self.chosen_side = side
        UNSEL = {"player": "#0055CC", "tie": "#886600", "banker": "#880000"}
        SEL   = {"player": "#0088FF", "tie": "#CCAA00", "banker": "#FF2222"}
        labels = {"player": "🟦 JOGADOR (1×)", "banker": "🟥 BANCA (0.95×)", "tie": "🟨 EMPATE (8×)"}
        for k, btn in self.side_buttons.items():
            btn.configure(
                fg_color=SEL[k] if k == side else UNSEL[k],
                border_width=3 if k == side else 0,
                border_color="#FFD700",
            )
        self.chosen_label.configure(
            text=f"Apostando em: {labels[side]}", text_color="#FFD700"
        )

    def _validate_bet(self) -> bool:
        if not self.chosen_side:
            messagebox.showerror("Erro", "Selecione em quem deseja apostar!")
            return False
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
            messagebox.showerror("Erro", f"Aposta maior que sua banca (R$ {self.balance:.2f})")
            return False
        return True

    # ── Drawing rules ────────────────────────────────────────

    def _should_player_draw(self, p_val: int) -> bool:
        return p_val <= 5

    def _should_banker_draw(self, b_val: int, player_drew: bool, p3_rank: str | None) -> bool:
        if not player_drew:
            return b_val <= 5
        p3 = self._card_rank_value(p3_rank) if p3_rank else None
        if b_val <= 2:
            return True
        if b_val == 3:
            return p3 != 8
        if b_val == 4:
            return p3 in (2, 3, 4, 5, 6, 7)
        if b_val == 5:
            return p3 in (4, 5, 6, 7)
        if b_val == 6:
            return p3 in (6, 7)
        return False   # b_val == 7

    # ── Game logic ───────────────────────────────────────────

    def deal(self) -> None:
        if self.game_active:
            return
        if not self._validate_bet():
            return

        self.game_active = True
        self.deal_button.configure(state="disabled")
        self.bet_entry.configure(state="disabled")
        self.result_frame.configure(border_width=0)
        self.result_label.configure(text="Distribuindo...", text_color="#AAAAAA")

        # Pre-compute all cards before animating
        deck = self._new_deck()
        p_hand = [deck.pop(), deck.pop()]
        b_hand = [deck.pop(), deck.pop()]

        p_val = self._bac_value(p_hand)
        b_val = self._bac_value(b_hand)
        p3_rank: str | None = None
        player_drew = False

        if p_val < 8 and b_val < 8:
            if self._should_player_draw(p_val):
                p3 = deck.pop()
                p_hand.append(p3)
                p3_rank = p3[0]
                player_drew = True
            b_val = self._bac_value(b_hand)
            if self._should_banker_draw(b_val, player_drew, p3_rank):
                b_hand.append(deck.pop())

        # Clear card areas
        for w in self.player_cards_frame.winfo_children(): w.destroy()
        for w in self.banker_cards_frame.winfo_children(): w.destroy()

        # Build interleaved animation: p1, b1, p2, b2, (p3), (b3)
        specs: list[tuple] = []
        for i in range(max(len(p_hand), len(b_hand))):
            if i < len(p_hand):
                specs.append((self.player_cards_frame, p_hand[i]))
            if i < len(b_hand):
                specs.append((self.banker_cards_frame, b_hand[i]))

        def show_result():
            p_final = self._bac_value(p_hand)
            b_final = self._bac_value(b_hand)
            self.player_score_label.configure(text=f"Pontos: {p_final}")
            self.banker_score_label.configure(text=f"Pontos: {b_final}")
            self.rounds += 1

            winner = "player" if p_final > b_final else ("banker" if b_final > p_final else "tie")

            if self.chosen_side == winner:
                if winner == "player":
                    prize = self.current_bet * 2
                    msg = f"🟦 JOGADOR venceu {p_final} × {b_final}!\n💰 Ganhou R$ {self.current_bet:.2f}!"
                    color = "#4488FF"
                elif winner == "banker":
                    net = round(self.current_bet * 0.95, 2)
                    prize = self.current_bet + net
                    msg = f"🟥 BANCA venceu {b_final} × {p_final}!\n💰 Ganhou R$ {net:.2f} (após 5% comissão)!"
                    color = "#FF4444"
                else:
                    prize = self.current_bet * 9
                    msg = f"🟨 EMPATE! {p_final} × {b_final}!\n💰 Ganhou R$ {self.current_bet * 8:.2f}! (8×)"
                    color = "#FFD700"
                self.wins += 1
                self.balance += prize
            else:
                self.balance -= self.current_bet
                winner_names = {"player": "Jogador", "banker": "Banca", "tie": "Empate"}
                msg = (
                    f"❌ {winner_names[winner]} venceu ({p_final} × {b_final})!\n"
                    f"💸 Perdeu R$ {self.current_bet:.2f}"
                )
                color = "#FF4444"

            self.balance_label.configure(text=self._balance_text())
            self.result_label.configure(text=msg, text_color=color)
            self.result_frame.configure(border_color=color, border_width=3)
            self.stats_label.configure(text=self._stats_text())
            self.game_active = False

            if self.balance > 0:
                self.deal_button.configure(state="normal")
                self.bet_entry.configure(state="normal")
                self.bet_entry.delete(0, "end")
            else:
                self.result_label.configure(text="💀 BANCA ZERADA! Clique em Novo Jogo.", text_color="#FF0000")

        self._deal_sequence(specs, on_complete=show_result)

    def reset(self) -> None:
        self.balance = self.INITIAL_BALANCE
        self.current_bet = 0.0
        self.chosen_side = None
        self.game_active = False
        self.rounds = 0
        self.wins = 0

        self.balance_label.configure(text=self._balance_text())
        self.result_label.configure(
            text="Selecione sua aposta e clique em DISTRIBUIR!", text_color="#AAAADD"
        )
        self.result_frame.configure(border_width=0)
        self.player_score_label.configure(text="—")
        self.banker_score_label.configure(text="—")
        self.stats_label.configure(text=self._stats_text())
        self.deal_button.configure(state="normal")
        self.bet_entry.configure(state="normal")
        self.bet_entry.delete(0, "end")
        self.chosen_label.configure(text="Nenhuma aposta selecionada", text_color="#888888")

        UNSEL = {"player": "#0055CC", "tie": "#886600", "banker": "#880000"}
        for k, btn in self.side_buttons.items():
            btn.configure(fg_color=UNSEL[k], border_width=0)

        for w in self.player_cards_frame.winfo_children():
            w.destroy()
        for w in self.banker_cards_frame.winfo_children():
            w.destroy()
