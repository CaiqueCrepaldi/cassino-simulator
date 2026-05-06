import customtkinter as ctk
from menu import MenuPrincipal

# Configure theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MenuPrincipal(root)
    root.mainloop()
