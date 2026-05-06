import customtkinter as ctk
from games.slot_machine import SlotMachine
from games.aviator import AviatorGame
from games.double import DoubleGame
from games.crash_dice import CrashDice
from games.blackjack import Blackjack
from games.roulette import Roulette
from games.coin_flip import CoinFlip


class MenuPrincipal:
    """Main menu screen — lets the player choose which game to open."""

    GAMES = [
        {
            "text":     "🎰  SLOT MACHINE",
            "subtitle": "Gire os slots e tente 3 símbolos iguais!",
            "fg":       "#CC0000",
            "hover":    "#990000",
            "handler":  "open_slots",
        },
        {
            "text":     "✈️  AVIATOR",
            "subtitle": "Aposte e retire antes do avião voar embora!",
            "fg":       "#0055CC",
            "hover":    "#003D99",
            "handler":  "open_aviator",
        },
        {
            "text":     "🎡  DOUBLE",
            "subtitle": "Aposte em Preto (2×), Vermelho (2×) ou Branco (14×)!",
            "fg":       "#6600CC",
            "hover":    "#4a0099",
            "handler":  "open_double",
        },
        {
            "text":     "🎲  CRASH DICE",
            "subtitle": "Escolha números e role 2 dados — combos especiais pagam mais!",
            "fg":       "#FF8800",
            "hover":    "#CC6600",
            "handler":  "open_crash_dice",
        },
        {
            "text":     "🃏  BLACKJACK",
            "subtitle": "Chegue em 21 sem ultrapassar e supere o dealer!",
            "fg":       "#006622",
            "hover":    "#004416",
            "handler":  "open_blackjack",
        },
        {
            "text":     "🎡  ROLETA",
            "subtitle": "Aposte em números, cores e dezenas — até 35× de retorno!",
            "fg":       "#880044",
            "hover":    "#660033",
            "handler":  "open_roulette",
        },
        {
            "text":     "🪙  COIN FLIP",
            "subtitle": "Cara ou Coroa? 50/50 — com modo auto flip e streak tracker!",
            "fg":       "#555500",
            "hover":    "#777700",
            "handler":  "open_coin_flip",
        },
    ]

    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self.root.title("🎰 Cassino Simulator – Menu Principal")
        self.root.geometry("520x920")
        self.root.resizable(False, False)
        self._build_ui()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        main = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#000000")
        main.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            main,
            text="🎰 CASSINO SIMULATOR 🎰",
            font=("Arial", 26, "bold"),
            text_color="#FFD700",
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            main,
            text="Escolha um jogo para jogar!",
            font=("Arial", 13),
            text_color="#CCCCCC",
        ).pack(pady=(0, 18))

        for game in self.GAMES:
            ctk.CTkButton(
                main,
                text=game["text"],
                command=getattr(self, game["handler"]),
                font=("Arial", 17, "bold"),
                corner_radius=10,
                height=52,
                fg_color=game["fg"],
                hover_color=game["hover"],
                text_color="#FFFFFF",
            ).pack(pady=(0, 3), fill="x", padx=30)

            ctk.CTkLabel(
                main,
                text=game["subtitle"],
                font=("Arial", 10),
                text_color="#888888",
            ).pack(pady=(0, 10))

        ctk.CTkLabel(
            main,
            text="Projeto acadêmico – sem dinheiro real envolvido",
            font=("Arial", 10),
            text_color="#444444",
        ).pack(side="bottom", pady=12)

    # ── Navigation ───────────────────────────────────────────

    def _new_window(self, game_class, *args, **kwargs) -> None:
        window = ctk.CTkToplevel(self.root)
        game_class(window, *args, **kwargs)

    def open_slots(self)      -> None: self._new_window(SlotMachine)
    def open_aviator(self)    -> None: self._new_window(AviatorGame)
    def open_double(self)     -> None: self._new_window(DoubleGame)
    def open_crash_dice(self) -> None: self._new_window(CrashDice)
    def open_blackjack(self)  -> None: self._new_window(Blackjack)
    def open_roulette(self)   -> None: self._new_window(Roulette)
    def open_coin_flip(self)  -> None: self._new_window(CoinFlip)
