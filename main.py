import customtkinter as ctk
import importlib

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

GAMES = {
    "slot":       ("games.slot_machine", "SlotMachine"),
    "aviator":    ("games.aviator",      "AviatorGame"),
    "double":     ("games.double",       "DoubleGame"),
    "crash_dice": ("games.crash_dice",   "CrashDice"),
    "blackjack":  ("games.blackjack",    "Blackjack"),
    "roulette":   ("games.roulette",     "Roulette"),
    "coin_flip":  ("games.coin_flip",    "CoinFlip"),
}


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
        mod_path, cls_name = GAMES[name]
        mod = importlib.import_module(mod_path)
        cls = getattr(mod, cls_name)
        cls(self.root, self._container, self.show_menu)


if __name__ == "__main__":
    App()
