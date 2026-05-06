import customtkinter as ctk
from typing import Callable


class MenuPrincipal:
    """Main menu — single-window navigation via callback."""

    GAMES = [
        {
            "text":     "🎰  SLOT MACHINE",
            "subtitle": "Gire os slots e tente 3 símbolos iguais!",
            "fg":       "#CC0000",
            "hover":    "#990000",
            "key":      "slot",
        },
        {
            "text":     "✈️  AVIATOR",
            "subtitle": "Aposte e retire antes do avião voar embora!",
            "fg":       "#0055CC",
            "hover":    "#003D99",
            "key":      "aviator",
        },
        {
            "text":     "🎡  DOUBLE",
            "subtitle": "Aposte em Preto (2×), Vermelho (2×) ou Branco (14×)!",
            "fg":       "#6600CC",
            "hover":    "#4a0099",
            "key":      "double",
        },
        {
            "text":     "🎲  CRASH DICE",
            "subtitle": "Escolha números e role 2 dados — combos especiais pagam mais!",
            "fg":       "#FF8800",
            "hover":    "#CC6600",
            "key":      "crash_dice",
        },
        {
            "text":     "🃏  BLACKJACK",
            "subtitle": "Chegue em 21 sem ultrapassar e supere o dealer!",
            "fg":       "#006622",
            "hover":    "#004416",
            "key":      "blackjack",
        },
        {
            "text":     "🎡  ROLETA",
            "subtitle": "Aposte em números, cores e dezenas — até 35× de retorno!",
            "fg":       "#880044",
            "hover":    "#660033",
            "key":      "roulette",
        },
        {
            "text":     "🪙  COIN FLIP",
            "subtitle": "Cara ou Coroa? 50/50 — com modo auto flip e streak tracker!",
            "fg":       "#555500",
            "hover":    "#777700",
            "key":      "coin_flip",
        },
        {
            "text":     "🎴  BACCARAT",
            "subtitle": "Aposte em Jogador, Banca ou Empate — chegue mais perto do 9!",
            "fg":       "#1a1a6e",
            "hover":    "#0a0a4e",
            "key":      "baccarat",
        },
    ]

    def __init__(self, root: ctk.CTk, container: ctk.CTkFrame, show_game: Callable) -> None:
        self.root = root
        self.container = container
        self.show_game = show_game
        self.root.title("🎰 Cassino Simulator – Menu Principal")
        self._build_ui()

    def _build_ui(self) -> None:
        bg = ctk.CTkFrame(self.container, fg_color="#000000", corner_radius=0)
        bg.pack(fill="both", expand=True)

        main = ctk.CTkFrame(bg, fg_color="#000000", corner_radius=10)
        main.pack(expand=True, fill="y", anchor="center")
        ctk.CTkFrame(main, width=620, height=1, fg_color="#000000").pack()

        ctk.CTkLabel(
            main,
            text="🎰 CASSINO SIMULATOR 🎰",
            font=("Arial", 26, "bold"),
            text_color="#FFD700",
        ).pack(pady=(20, 4))

        ctk.CTkLabel(
            main,
            text="Escolha um jogo para jogar!",
            font=("Arial", 13),
            text_color="#CCCCCC",
        ).pack(pady=(0, 14))

        # Grade 2 colunas × 4 linhas
        grid = ctk.CTkFrame(main, fg_color="#000000")
        grid.pack(padx=20, fill="x")

        left_col  = ctk.CTkFrame(grid, fg_color="#000000")
        right_col = ctk.CTkFrame(grid, fg_color="#000000")
        left_col.pack(side="left", fill="x", expand=True, padx=(0, 6))
        right_col.pack(side="left", fill="x", expand=True, padx=(6, 0))

        half = len(self.GAMES) // 2
        for i, game in enumerate(self.GAMES):
            col = left_col if i < half else right_col
            ctk.CTkButton(
                col,
                text=game["text"],
                command=lambda k=game["key"]: self.show_game(k),
                font=("Arial", 14, "bold"),
                corner_radius=10,
                height=52,
                fg_color=game["fg"],
                hover_color=game["hover"],
                text_color="#FFFFFF",
            ).pack(pady=(0, 2), fill="x")

            ctk.CTkLabel(
                col,
                text=game["subtitle"],
                font=("Arial", 9),
                text_color="#777777",
                wraplength=260,
            ).pack(pady=(0, 10))

        ctk.CTkLabel(
            main,
            text="Projeto acadêmico – sem dinheiro real envolvido",
            font=("Arial", 10),
            text_color="#444444",
        ).pack(pady=10)
