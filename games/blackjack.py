import random

import customtkinter as ctk
from tkinter import messagebox


class Blackjack:
    """
    Blackjack (21) — classic casino rules.

    Rules implemented
    -----------------
    - Standard 52-card deck, reshuffled each round.
    - Player and dealer each receive 2 cards; dealer's second card is hidden.
    - Player actions: Hit (draw), Stand (end turn), Double Down (2× bet, one card).
    - Dealer draws until reaching 17 or above (hard rule).
    - Blackjack (Ace + 10-value on first 2 cards) pays 1.5× the bet.
    - Win pays 1×, push (tie) returns the bet, bust/loss loses the bet.
    - Aces count as 11 or 1 (whichever keeps the hand ≤ 21).
    """

    SUITS   = ["♠", "♥", "♦", "♣"]
    RANKS   = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    INITIAL_BALANCE = 1_000.00

    # Card face colors
    RED_SUITS   = {"♥", "♦"}

    def __init__(self, root: ctk.CTkToplevel) -> None:
        self.root = root
        self.root.title("🃏 Blackjack")
        self.root.geometry("620x860")
        self.root.resizable(True, True)
        self.root.minsize(620, 700)
        self.root.bind("<F11>", lambda _: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda _: self.root.attributes("-fullscreen", False))

        # State
        self.balance: float     = self.INITIAL_BALANCE
        self.current_bet: float = 0.0
        self.deck: list[tuple]  = []
        self.player_hand: list  = []
        self.dealer_hand: list  = []
        self.game_active: bool  = False
        self.doubled_down: bool = False

        # Stats
        self.rounds: int = 0
        self.wins: int   = 0

        self._build_ui()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        main = ctk.CTkFrame(self.root, fg_color="#076324", corner_radius=0)
        main.pack(fill="both", expand=True)

        ctk.CTkLabel(
            main, text="🃏  BLACKJACK",
            font=("Arial", 30, "bold"), text_color="#FFD700",
        ).pack(pady=(18, 2))

        ctk.CTkLabel(
            main, text="Chegue em 21 sem ultrapassar — mas supere o dealer!",
            font=("Arial", 11), text_color="#CCFFCC",
        ).pack()

        self.balance_label = ctk.CTkLabel(
            main, text=self._balance_text(),
            font=("Arial", 15, "bold"), text_color="#FFD700",
        )
        self.balance_label.pack(pady=(6, 0))

        # ── Dealer area ──────────────────────────────────────
        ctk.CTkLabel(
            main, text="DEALER",
            font=("Arial", 13, "bold"), text_color="#CCFFCC",
        ).pack(pady=(12, 2))

        self.dealer_frame = ctk.CTkFrame(main, fg_color="#055120", corner_radius=10)
        self.dealer_frame.pack(padx=20, fill="x")

        self.dealer_cards_frame = ctk.CTkFrame(self.dealer_frame, fg_color="#055120")
        self.dealer_cards_frame.pack(pady=10, padx=10)

        self.dealer_score_label = ctk.CTkLabel(
            self.dealer_frame, text="",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        )
        self.dealer_score_label.pack(pady=(0, 8))

        # ── Player area ──────────────────────────────────────
        ctk.CTkLabel(
            main, text="VOCÊ",
            font=("Arial", 13, "bold"), text_color="#CCFFCC",
        ).pack(pady=(14, 2))

        self.player_frame = ctk.CTkFrame(main, fg_color="#055120", corner_radius=10)
        self.player_frame.pack(padx=20, fill="x")

        self.player_cards_frame = ctk.CTkFrame(self.player_frame, fg_color="#055120")
        self.player_cards_frame.pack(pady=10, padx=10)

        self.player_score_label = ctk.CTkLabel(
            self.player_frame, text="",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        )
        self.player_score_label.pack(pady=(0, 8))

        # ── Bet row ──────────────────────────────────────────
        bet_row = ctk.CTkFrame(main, fg_color="#076324")
        bet_row.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(
            bet_row, text="Aposta (R$):",
            font=("Arial", 13, "bold"), text_color="#FFFFFF",
        ).pack(side="left", padx=8)

        self.bet_entry = ctk.CTkEntry(
            bet_row, placeholder_text="Ex: 50.00",
            font=("Arial", 13), corner_radius=8,
            fg_color="#044018", border_color="#FFD700",
            text_color="#FFFFFF", width=140,
        )
        self.bet_entry.pack(side="left", padx=8)

        for v in [10, 25, 50, 100]:
            ctk.CTkButton(
                bet_row, text=f"+{v}",
                command=lambda val=v: self._add_bet(val),
                font=("Arial", 11, "bold"), width=45, height=30,
                fg_color="#044018", hover_color="#055120",
                text_color="#FFD700", corner_radius=6,
            ).pack(side="left", padx=2)

        # ── Action buttons ───────────────────────────────────
        action_row = ctk.CTkFrame(main, fg_color="#076324")
        action_row.pack(padx=20, pady=4, fill="x")

        self.deal_button = ctk.CTkButton(
            action_row, text="🃏  DISTRIBUIR",
            command=self.deal,
            font=("Arial", 16, "bold"), height=50, corner_radius=10,
            fg_color="#FFD700", hover_color="#CCA800", text_color="#000000",
        )
        self.deal_button.pack(side="left", padx=(0, 6), fill="x", expand=True)

        self.hit_button = ctk.CTkButton(
            action_row, text="➕  PEDIR",
            command=self.hit,
            font=("Arial", 16, "bold"), height=50, corner_radius=10,
            fg_color="#0055CC", hover_color="#003D99", text_color="#FFFFFF",
            state="disabled",
        )
        self.hit_button.pack(side="left", padx=6, fill="x", expand=True)

        self.stand_button = ctk.CTkButton(
            action_row, text="✋  PARAR",
            command=self.stand,
            font=("Arial", 16, "bold"), height=50, corner_radius=10,
            fg_color="#CC0000", hover_color="#990000", text_color="#FFFFFF",
            state="disabled",
        )
        self.stand_button.pack(side="left", padx=(6, 0), fill="x", expand=True)

        self.double_button = ctk.CTkButton(
            main, text="💰  DOBRAR APOSTA (Double Down)",
            command=self.double_down,
            font=("Arial", 13, "bold"), height=38, corner_radius=8,
            fg_color="#6600CC", hover_color="#4a0099", text_color="#FFFFFF",
            state="disabled",
        )
        self.double_button.pack(padx=20, pady=(4, 0), fill="x")

        ctk.CTkButton(
            main, text="🔄 NOVO JOGO (resetar banca)",
            command=self.reset,
            font=("Arial", 12, "bold"), height=34, corner_radius=8,
            fg_color="#044018", hover_color="#055120", text_color="#AAAAAA",
        ).pack(padx=20, pady=(6, 0), fill="x")

        # ── Result / status ──────────────────────────────────
        self.result_frame = ctk.CTkFrame(main, fg_color="#033010", corner_radius=10)
        self.result_frame.pack(padx=20, pady=8, fill="x")

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Defina sua aposta e clique em DISTRIBUIR!",
            font=("Arial", 14, "bold"), text_color="#CCFFCC", wraplength=540,
        )
        self.result_label.pack(pady=14, padx=16)

        self.stats_label = ctk.CTkLabel(
            main, text=self._stats_text(),
            font=("Arial", 11), text_color="#88CC88",
        )
        self.stats_label.pack(pady=(0, 10))

    # ── Card rendering ───────────────────────────────────────

    def _card_widget(self, parent, card, hidden: bool = False) -> ctk.CTkFrame:
        """Create a card widget. If hidden=True renders a face-down card."""
        frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=8, width=58, height=82)
        frame.pack_propagate(False)
        frame.pack(side="left", padx=3)

        if hidden:
            ctk.CTkLabel(
                frame, text="🂠", font=("Arial", 38), text_color="#000080",
            ).pack(expand=True)
        else:
            rank, suit = card
            color = "#CC0000" if suit in self.RED_SUITS else "#000000"
            ctk.CTkLabel(
                frame, text=f"{rank}\n{suit}",
                font=("Arial", 15, "bold"), text_color=color,
            ).pack(expand=True)

        return frame

    def _render_hands(self, hide_dealer: bool = True) -> None:
        """Redraw both hands on screen."""
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()

        for i, card in enumerate(self.dealer_hand):
            hidden = hide_dealer and i == 1
            self._card_widget(self.dealer_cards_frame, card, hidden=hidden)

        for card in self.player_hand:
            self._card_widget(self.player_cards_frame, card)

        if hide_dealer:
            visible = self._hand_value([self.dealer_hand[0]])
            self.dealer_score_label.configure(text=f"Dealer: {visible} + ?")
        else:
            dealer_val = self._hand_value(self.dealer_hand)
            self.dealer_score_label.configure(text=f"Dealer: {dealer_val}")

        player_val = self._hand_value(self.player_hand)
        self.player_score_label.configure(text=f"Sua mão: {player_val}")

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

    def _new_deck(self) -> list:
        deck = [(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(deck)
        return deck

    def _card_value(self, rank: str) -> int:
        if rank in ("J", "Q", "K"):
            return 10
        if rank == "A":
            return 11
        return int(rank)

    def _hand_value(self, hand: list) -> int:
        total = sum(self._card_value(r) for r, _ in hand)
        aces  = sum(1 for r, _ in hand if r == "A")
        while total > 21 and aces:
            total -= 10
            aces  -= 1
        return total

    def _is_blackjack(self, hand: list) -> bool:
        return len(hand) == 2 and self._hand_value(hand) == 21

    def _set_action_buttons(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.hit_button.configure(state=state)
        self.stand_button.configure(state=state)
        self.double_button.configure(state=state)

    # ── Game logic ───────────────────────────────────────────

    def deal(self) -> None:
        if self.game_active:
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
        self.deck        = self._new_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.game_active = True
        self.doubled_down = False

        self.balance_label.configure(text=self._balance_text())
        self.result_label.configure(text=f"Aposta: R$ {self.current_bet:.2f} | Sua vez!", text_color="#FFFFFF")
        self.result_frame.configure(border_width=0)
        self.deal_button.configure(state="disabled")
        self.bet_entry.configure(state="disabled")
        self._set_action_buttons(True)
        self._render_hands(hide_dealer=True)

        # Check player blackjack immediately
        if self._is_blackjack(self.player_hand):
            self._resolve(force_reveal=True)

    def hit(self) -> None:
        if not self.game_active:
            return
        self.player_hand.append(self.deck.pop())
        self.double_button.configure(state="disabled")
        self._render_hands(hide_dealer=True)

        if self._hand_value(self.player_hand) > 21:
            self._resolve(force_reveal=True)

    def stand(self) -> None:
        if not self.game_active:
            return
        self._dealer_draw()
        self._resolve(force_reveal=True)

    def double_down(self) -> None:
        if not self.game_active:
            return
        extra = min(self.current_bet, self.balance)
        self.balance      -= extra
        self.current_bet  += extra
        self.doubled_down  = True
        self.balance_label.configure(text=self._balance_text())
        self.result_label.configure(
            text=f"Double Down! Aposta: R$ {self.current_bet:.2f}", text_color="#FFD700"
        )
        self.player_hand.append(self.deck.pop())
        self._render_hands(hide_dealer=True)

        if self._hand_value(self.player_hand) > 21:
            self._resolve(force_reveal=True)
        else:
            self._dealer_draw()
            self._resolve(force_reveal=True)

    def _dealer_draw(self) -> None:
        """Dealer draws until reaching 17 or above."""
        while self._hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

    def _resolve(self, force_reveal: bool = False) -> None:
        self.game_active = False
        self._set_action_buttons(False)
        self._render_hands(hide_dealer=False)
        self.rounds += 1

        player_val = self._hand_value(self.player_hand)
        dealer_val = self._hand_value(self.dealer_hand)

        player_bj = self._is_blackjack(self.player_hand)
        dealer_bj = self._is_blackjack(self.dealer_hand)

        # Determine outcome
        if player_val > 21:
            outcome, color, prize = "bust", "#FF4444", 0
        elif dealer_val > 21:
            outcome, color, prize = "win", "#00FF88", self.current_bet * 2
        elif player_bj and not dealer_bj:
            outcome, color, prize = "blackjack", "#FFD700", self.current_bet * 2.5
        elif dealer_bj and not player_bj:
            outcome, color, prize = "dealer_bj", "#FF4444", 0
        elif player_val > dealer_val:
            outcome, color, prize = "win", "#00FF88", self.current_bet * 2
        elif player_val == dealer_val:
            outcome, color, prize = "push", "#AAAAAA", self.current_bet
        else:
            outcome, color, prize = "lose", "#FF4444", 0

        messages = {
            "bust":      f"💥 ESTOUROU! Sua mão: {player_val}. Perdeu R$ {self.current_bet:.2f}",
            "win":       f"🎉 VOCÊ GANHOU! {player_val} vs {dealer_val}. +R$ {prize - self.current_bet:.2f}",
            "blackjack": f"🃏 BLACKJACK! Pagamento 3:2. +R$ {prize - self.current_bet:.2f}",
            "dealer_bj": f"😱 Dealer tem Blackjack! Perdeu R$ {self.current_bet:.2f}",
            "push":      f"🤝 EMPATE! {player_val} vs {dealer_val}. Aposta devolvida.",
            "lose":      f"❌ Dealer venceu! {dealer_val} vs {player_val}. Perdeu R$ {self.current_bet:.2f}",
        }

        if prize > 0:
            self.wins    += 1
            self.balance += prize

        self.balance_label.configure(text=self._balance_text())
        self.result_label.configure(text=messages[outcome], text_color=color)
        border = color if outcome not in ("push",) else "#AAAAAA"
        self.result_frame.configure(border_color=border, border_width=3)
        self.stats_label.configure(text=self._stats_text())

        if self.balance > 0:
            self.deal_button.configure(state="normal")
            self.bet_entry.configure(state="normal")
            self.bet_entry.delete(0, "end")
        else:
            self.result_label.configure(text="💀 BANCA ZERADA! Clique em Novo Jogo.", text_color="#FF0000")
            self.deal_button.configure(state="disabled")

    def reset(self) -> None:
        self.balance      = self.INITIAL_BALANCE
        self.current_bet  = 0.0
        self.player_hand  = []
        self.dealer_hand  = []
        self.game_active  = False

        self.balance_label.configure(text=self._balance_text())
        self.result_label.configure(
            text="Defina sua aposta e clique em DISTRIBUIR!", text_color="#CCFFCC"
        )
        self.result_frame.configure(border_width=0)
        self.dealer_score_label.configure(text="")
        self.player_score_label.configure(text="")
        self.stats_label.configure(text=self._stats_text())
        self.deal_button.configure(state="normal")
        self.bet_entry.configure(state="normal")
        self.bet_entry.delete(0, "end")
        self._set_action_buttons(False)

        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()

        self.rounds = 0
        self.wins   = 0
