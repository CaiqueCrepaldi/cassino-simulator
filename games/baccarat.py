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

    def __init__(self, root: ctk.CTk, container: ctk.CTkFrame, back_callback) -> None:
        self.root = root
        self.container = container
        self.back_callback = back_callback
        self.root.title("🎴 Baccarat")

        self.balance: float = self.INITIAL_BALANCE
        self.current_bet: float = 0.0
        self.chosen_side: str | None = None   # "player", "banker", "tie"
        self.game_active: bool = False

        self.rounds: int = 0
        self.wins: int = 0

        self._build_ui()

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
            font=("Arial", 30, "bold"), text_color="#FFD700",
        ).pack(pady=(4, 2))

        ctk.CTkLabel(
            main, text="Aposte em Jogador, Banca ou Empate — chegue mais perto do 9!",
            font=("Arial", 11), text_color="#AAAADD",
        ).pack()

        self.balance_label = ctk.CTkLabel(
            main, text=self._balance_text(),
            font=("Arial", 15, "bold"), text_color="#FFD700",
        )
        self.balance_label.pack(pady=(6, 0))

        # Payout table
        pay_frame = ctk.CTkFrame(main, fg_color="#14143a", corner_radius=10)
        pay_frame.pack(padx=20, pady=8, fill="x")
        ctk.CTkLabel(
            pay_frame,
            text="💡  Jogador: 1×  |  Banca: 0.95× (5% comissão)  |  Empate: 8×",
            font=("Arial", 11), text_color="#AAAADD",
        ).pack(pady=8)

        # ── Banker area ──────────────────────────────────────
        ctk.CTkLabel(
            main, text="BANCA",
            font=("Arial", 13, "bold"), text_color="#FF8888",
        ).pack(pady=(10, 2))

        self.banker_frame = ctk.CTkFrame(main, fg_color="#1a0a2e", corner_radius=10)
        self.banker_frame.pack(padx=20, fill="x")

        self.banker_cards_frame = ctk.CTkFrame(self.banker_frame, fg_color="#1a0a2e")
        self.banker_cards_frame.pack(pady=10, padx=10)

        self.banker_score_label = ctk.CTkLabel(
            self.banker_frame, text="",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        )
        self.banker_score_label.pack(pady=(0, 8))

        # ── Player area ──────────────────────────────────────
        ctk.CTkLabel(
            main, text="JOGADOR",
            font=("Arial", 13, "bold"), text_color="#88CCFF",
        ).pack(pady=(10, 2))

        self.player_frame = ctk.CTkFrame(main, fg_color="#0a1a2e", corner_radius=10)
        self.player_frame.pack(padx=20, fill="x")

        self.player_cards_frame = ctk.CTkFrame(self.player_frame, fg_color="#0a1a2e")
        self.player_cards_frame.pack(pady=10, padx=10)

        self.player_score_label = ctk.CTkLabel(
            self.player_frame, text="",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        )
        self.player_score_label.pack(pady=(0, 8))

        # ── Bet side selector ────────────────────────────────
        side_row = ctk.CTkFrame(main, fg_color=BG)
        side_row.pack(padx=20, pady=8, fill="x")

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
                font=("Arial", 14, "bold"), height=46, corner_radius=10,
                fg_color=fg, hover_color=hover, text_color="#FFFFFF",
            )
            btn.pack(side="left", padx=4, fill="x", expand=True)
            self.side_buttons[key] = btn

        self.chosen_label = ctk.CTkLabel(
            main, text="Nenhuma aposta selecionada",
            font=("Arial", 12), text_color="#888888",
        )
        self.chosen_label.pack(pady=(0, 4))

        # ── Bet row ──────────────────────────────────────────
        bet_row = ctk.CTkFrame(main, fg_color=BG)
        bet_row.pack(padx=20, pady=6, fill="x")

        ctk.CTkLabel(
            bet_row, text="Aposta (R$):",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        ).pack(side="left", padx=8)

        self.bet_entry = ctk.CTkEntry(
            bet_row, placeholder_text="Ex: 50.00",
            font=("Arial", 13), corner_radius=8,
            fg_color="#14143a", border_color="#FFD700",
            text_color="#FFFFFF", width=140,
        )
        self.bet_entry.pack(side="left", padx=8)

        for v in [10, 25, 50, 100]:
            ctk.CTkButton(
                bet_row, text=f"+{v}",
                command=lambda val=v: self._add_bet(val),
                font=("Arial", 11, "bold"), width=45, height=30,
                fg_color="#14143a", hover_color="#1e1e50",
                text_color="#FFD700", corner_radius=6,
            ).pack(side="left", padx=2)

        # ── Deal button ──────────────────────────────────────
        self.deal_button = ctk.CTkButton(
            main, text="🎴  DISTRIBUIR",
            command=self.deal,
            font=("Arial", 18, "bold"), height=55, corner_radius=10,
            fg_color="#FFD700", hover_color="#CCA800", text_color="#000000",
        )
        self.deal_button.pack(padx=20, pady=8, fill="x")

        ctk.CTkButton(
            main, text="🔄 NOVO JOGO (resetar banca)",
            command=self.reset,
            font=("Arial", 12, "bold"), height=34, corner_radius=8,
            fg_color="#14143a", hover_color="#1e1e50", text_color="#888888",
        ).pack(padx=20, pady=(0, 4), fill="x")

        # ── Result ───────────────────────────────────────────
        self.result_frame = ctk.CTkFrame(main, fg_color="#0a0a1e", corner_radius=10)
        self.result_frame.pack(padx=20, pady=6, fill="x")

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Selecione sua aposta e clique em DISTRIBUIR!",
            font=("Arial", 14, "bold"), text_color="#AAAADD", wraplength=540,
        )
        self.result_label.pack(pady=14, padx=16)

        self.stats_label = ctk.CTkLabel(
            main, text=self._stats_text(),
            font=("Arial", 11), text_color="#555588",
        )
        self.stats_label.pack(pady=(0, 10))

    # ── Card rendering ───────────────────────────────────────

    def _card_widget(self, parent: ctk.CTkFrame, card: tuple) -> ctk.CTkFrame:
        rank, suit = card
        frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=8, width=58, height=82)
        frame.pack_propagate(False)
        frame.pack(side="left", padx=3)
        color = "#CC0000" if suit in self.RED_SUITS else "#000000"
        ctk.CTkLabel(
            frame, text=f"{rank}\n{suit}",
            font=("Arial", 15, "bold"), text_color=color,
        ).pack(expand=True)
        return frame

    def _render_hands(self, p_hand: list, b_hand: list) -> None:
        for w in self.player_cards_frame.winfo_children():
            w.destroy()
        for w in self.banker_cards_frame.winfo_children():
            w.destroy()

        for card in p_hand:
            self._card_widget(self.player_cards_frame, card)
        for card in b_hand:
            self._card_widget(self.banker_cards_frame, card)

        self.player_score_label.configure(text=f"Jogador: {self._bac_value(p_hand)}")
        self.banker_score_label.configure(text=f"Banca: {self._bac_value(b_hand)}")

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

        deck = self._new_deck()
        p_hand = [deck.pop(), deck.pop()]
        b_hand = [deck.pop(), deck.pop()]

        p_val = self._bac_value(p_hand)
        b_val = self._bac_value(b_hand)

        p3_rank: str | None = None
        player_drew = False

        # Natural check: no more cards if either hand is 8 or 9
        if p_val < 8 and b_val < 8:
            if self._should_player_draw(p_val):
                p3 = deck.pop()
                p_hand.append(p3)
                p3_rank = p3[0]
                player_drew = True

            p_val = self._bac_value(p_hand)
            b_val = self._bac_value(b_hand)

            if self._should_banker_draw(b_val, player_drew, p3_rank):
                b_hand.append(deck.pop())

        p_final = self._bac_value(p_hand)
        b_final = self._bac_value(b_hand)

        self._render_hands(p_hand, b_hand)
        self.rounds += 1

        # Determine winner
        if p_final > b_final:
            winner = "player"
        elif b_final > p_final:
            winner = "banker"
        else:
            winner = "tie"

        # Calculate prize
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
            else:  # tie
                prize = self.current_bet * 9
                msg = f"🟨 EMPATE! {p_final} × {b_final}!\n💰 Ganhou R$ {self.current_bet * 8:.2f}! (8×)"
                color = "#FFD700"
            self.wins += 1
            self.balance += prize
        else:
            prize = 0
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
        self.player_score_label.configure(text="")
        self.banker_score_label.configure(text="")
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
