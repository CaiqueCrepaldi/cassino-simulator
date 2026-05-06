import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.title("🎰 Cassino Simulator")
        self.root.geometry("640x900")
        self.root.resizable(True, True)
        self.root.minsize(620, 720)
        self.root.bind("<F11>", lambda _: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda _: self.root.attributes("-fullscreen", False))

        self._container = ctk.CTkFrame(self.root, fg_color="#0d0d0d", corner_radius=0)
        self._container.pack(fill="both", expand=True)

        self.show_menu()
        self.root.mainloop()

    def _clear(self) -> None:
        for w in self._container.winfo_children():
            w.destroy()

    def show_menu(self) -> None:
        self._clear()
        from menu import MenuPrincipal
        MenuPrincipal(self.root, self._container, self.show_game)

    def show_game(self, name: str) -> None:
        self._clear()
        if name == "slot":
            from games.slot_machine import SlotMachine
            SlotMachine(self.root, self._container, self.show_menu)
        elif name == "aviator":
            from games.aviator import AviatorGame
            AviatorGame(self.root, self._container, self.show_menu)
        elif name == "double":
            from games.double import DoubleGame
            DoubleGame(self.root, self._container, self.show_menu)
        elif name == "crash_dice":
            from games.crash_dice import CrashDice
            CrashDice(self.root, self._container, self.show_menu)
        elif name == "blackjack":
            from games.blackjack import Blackjack
            Blackjack(self.root, self._container, self.show_menu)
        elif name == "roulette":
            from games.roulette import Roulette
            Roulette(self.root, self._container, self.show_menu)
        elif name == "coin_flip":
            from games.coin_flip import CoinFlip
            CoinFlip(self.root, self._container, self.show_menu)
        elif name == "baccarat":
            from games.baccarat import Baccarat
            Baccarat(self.root, self._container, self.show_menu)


if __name__ == "__main__":
    App()
