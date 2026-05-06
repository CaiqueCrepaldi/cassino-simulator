import customtkinter as ctk
from menu import MenuPrincipal

# Configure theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    root = ctk.CTk()
    root.resizable(True, True)
    root.minsize(520, 700)
    root.bind("<F11>", lambda _: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
    root.bind("<Escape>", lambda _: root.attributes("-fullscreen", False))
    app = MenuPrincipal(root)
    root.mainloop()
