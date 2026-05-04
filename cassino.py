import customtkinter as ctk
import random
import time
from tkinter import messagebox

# Configure theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CassinoSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Cassino Simulator")
        self.root.geometry("600x1150")
        self.root.resizable(False, False)

        # Symbol probabilities (harder to get matches)
        self.symbols = ["🔥", "⭐", "🤑"]
        self.weights = [40, 35, 25]  # 🔥 has more chance, 🤑 less

        # Initialize fake bank
        self.banca = 1000.00
        self.aposta_atual = 0.0

        # Main frame
        main_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#000000")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎰 CASSINO SIMULATOR 🎰",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"
        )
        title_label.pack(pady=20)

        # Subtitle
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Tente conseguir 3 símbolos iguais!",
            font=("Arial", 14),
            text_color="#CCCCCC"
        )
        subtitle_label.pack(pady=(0, 30))

        # Bank info frame
        bank_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", corner_radius=10)
        bank_frame.pack(padx=30, pady=10, fill="x")

        # Bank label
        self.banca_label = ctk.CTkLabel(
            bank_frame,
            text=f"💰 Banca: R$ {self.banca:.2f}",
            font=("Arial", 16, "bold"),
            text_color="#00FF00"
        )
        self.banca_label.pack(pady=10, padx=10)

        # Bet frame
        bet_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        bet_frame.pack(padx=30, pady=10, fill="x")

        bet_label = ctk.CTkLabel(
            bet_frame,
            text="Valor da Aposta (R$):",
            font=("Arial", 12, "bold"),
            text_color="#FFFFFF"
        )
        bet_label.pack(side="left", padx=10)

        self.bet_entry = ctk.CTkEntry(
            bet_frame,
            placeholder_text="Digite a aposta...",
            font=("Arial", 12),
            corner_radius=8,
            fg_color="#1a1a1a",
            border_color="#CC0000",
            text_color="#FFFFFF",
            width=150
        )
        self.bet_entry.pack(side="left", padx=10)

        # Slots frame
        slots_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#1a1a1a")
        slots_frame.pack(padx=30, pady=20, fill="x")

        # Container for the 3 slots
        self.slots_container = ctk.CTkFrame(slots_frame, fg_color="#1a1a1a")
        self.slots_container.pack(pady=30, padx=20)

        # Create the 3 slots
        self.slot_labels = []
        for i in range(3):
            slot_frame = ctk.CTkFrame(self.slots_container, fg_color="#000000", corner_radius=10)
            slot_frame.pack(side="left", padx=10, expand=True)

            slot_label = ctk.CTkLabel(
                slot_frame,
                text="❓",
                font=("Arial", 60),
                text_color="#FFFFFF"
            )
            slot_label.pack(pady=20, padx=20)
            self.slot_labels.append(slot_label)

        # Controls frame
        controls_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        controls_frame.pack(pady=20, fill="x", padx=30)

        # Spin button
        self.spin_button = ctk.CTkButton(
            controls_frame,
            text="🎰 GIRAR SLOTS 🎰",
            command=self.girar,
            font=("Arial", 18, "bold"),
            corner_radius=10,
            height=60,
            fg_color="#CC0000",
            hover_color="#990000",
            text_color="#FFFFFF"
        )
        self.spin_button.pack(pady=20, fill="x", padx=20)

        # New game button
        new_game_button = ctk.CTkButton(
            controls_frame,
            text="🔄 NOVO JOGO",
            command=self.resetar_estatisticas,
            font=("Arial", 14, "bold"),
            corner_radius=10,
            height=40,
            fg_color="#0066CC",
            hover_color="#004499",
            text_color="#FFFFFF"
        )
        new_game_button.pack(pady=(0, 20), fill="x", padx=20)

        # Result frame
        self.resultado_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#1a1a1a")
        self.resultado_frame.pack(padx=30, pady=20, fill="both", expand=True)

        # Result label
        self.resultado_label = ctk.CTkLabel(
            self.resultado_frame,
            text="Clique em GIRAR para começar!",
            font=("Arial", 16, "bold"),
            wraplength=400,
            text_color="#FFFFFF"
        )
        self.resultado_label.pack(padx=20, pady=30)

        # Statistics
        stats_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        stats_frame.pack(pady=(0, 20), fill="x", padx=30)

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Tentativas: 0 | Vitórias: 0 | Taxa de Sucesso: 0.00%",
            font=("Arial", 12),
            text_color="#CCCCCC"
        )
        self.stats_label.pack(pady=10)

        # Initialize statistics
        self.tentativas = 0
        self.vitorias = 0

    def girar(self):
        """Execute a game round"""
        if self.spin_button.cget("state") == "disabled":
            return

        # Validate bet
        try:
            aposta_texto = self.bet_entry.get()
            if not aposta_texto:
                messagebox.showerror("Erro", "Digite um valor de aposta!")
                return
            
            self.aposta_atual = float(aposta_texto)
            
            if self.aposta_atual <= 0:
                messagebox.showerror("Erro", "A aposta deve ser maior que 0!")
                return
            
            if self.aposta_atual > self.banca:
                messagebox.showerror("Erro", f"Aposta não pode ser maior que sua banca (R$ {self.banca:.2f})")
                return
        
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido!")
            return

        # Disable button during animation
        self.spin_button.configure(state="disabled", text="🎰 GIRANDO... 🎰")

        # Spin animation
        self.animacao_giro()

        # Schedule result after animation
        self.root.after(1500, self.mostrar_resultado)

    def animacao_giro(self):
        """Slots spinning animation"""
        simbolos_animacao = ["🔥", "⭐", "🤑", "🎰", "💎", "🎲", "🎯", "🎪"]

        for _ in range(10):  # 10 animation iterations
            for label in self.slot_labels:
                simbolo = random.choice(simbolos_animacao)
                label.configure(text=simbolo)
            self.root.update()
            time.sleep(0.1)

    def mostrar_resultado(self):
        """Calculate and show final result"""
        # Generate result based on probabilities
        resultado = []
        for _ in range(3):
            simbolo = random.choices(self.symbols, weights=self.weights, k=1)[0]
            resultado.append(simbolo)

        # Update slots
        for i, simbolo in enumerate(resultado):
            self.slot_labels[i].configure(text=simbolo)

        # Check victory
        self.tentativas += 1
        vitoria = len(set(resultado)) == 1  # All equal

        if vitoria:
            self.vitorias += 1

            # Victory message based on symbol
            simbolo_vitoria = resultado[0]
            if simbolo_vitoria == "🔥":
                mensagem = "🔥 INCRÍVEL! 3 FOGOS IGUAIS! 🔥"
                cor = "#FF6B35"
                multiplicador = 2
            elif simbolo_vitoria == "⭐":
                mensagem = "⭐ FANTÁSTICO! 3 ESTRELAS IGUAIS! ⭐"
                cor = "#FFD700"
                multiplicador = 2
            else:  # 🤑
                mensagem = "🤑 JACKPOT! 3 DINHEIROS IGUAIS! 🤑"
                cor = "#00FF00"
                multiplicador = 3

            # Update bank
            ganho = self.aposta_atual * multiplicador
            self.banca += ganho
            self.banca_label.configure(text=f"💰 Banca: R$ {self.banca:.2f}")

            mensagem_banco = f"{mensagem}\n💰 Ganhou: R$ {ganho:.2f}!"
            self.resultado_label.configure(text=mensagem_banco, text_color=cor)
            self.resultado_frame.configure(border_color=cor, border_width=3)

            # Show victory message
            messagebox.showinfo("🎉 VITÓRIA!", f"Parabéns! Você conseguiu 3 {simbolo_vitoria} iguais!\nGanhou R$ {ganho:.2f}\nNova banca: R$ {self.banca:.2f}")

        else:
            # Loss
            self.banca -= self.aposta_atual
            self.banca_label.configure(text=f"💰 Banca: R$ {self.banca:.2f}")

            mensagem_banco = f"❌ Não foi dessa vez! Tente novamente!\n💸 Perdeu: R$ {self.aposta_atual:.2f}"
            self.resultado_label.configure(
                text=mensagem_banco,
                text_color="#FF4444"
            )
            self.resultado_frame.configure(border_color="#FF4444", border_width=2)

            if self.banca <= 0:
                self.resultado_label.configure(text="💀 BANCA ZERADA! Você perdeu tudo!", text_color="#FF0000")
                messagebox.showwarning("⚠️ FIM DE JOGO", "Sua banca zerou! O jogo terminou.")

        # Update statistics
        taxa_sucesso = (self.vitorias / self.tentativas) * 100 if self.tentativas > 0 else 0
        self.stats_label.configure(
            text=f"Tentativas: {self.tentativas} | Vitórias: {self.vitorias} | Taxa de Sucesso: {taxa_sucesso:.2f}%"
        )

        # Re-enable button (or disable if bank is zero)
        if self.banca > 0:
            self.spin_button.configure(state="normal", text="🎰 GIRAR SLOTS 🎰")
            self.bet_entry.delete(0, "end")
        else:
            self.spin_button.configure(state="disabled", text="💀 GAME OVER 💀")

    def resetar_estatisticas(self):
        """Reset game statistics"""
        self.tentativas = 0
        self.vitorias = 0
        self.banca = 1000.00
        self.aposta_atual = 0.0
        self.banca_label.configure(text=f"💰 Banca: R$ {self.banca:.2f}")
        self.bet_entry.delete(0, "end")
        self.stats_label.configure(text="Tentativas: 0 | Vitórias: 0 | Taxa de Sucesso: 0.00%")
        self.resultado_label.configure(text="Clique em GIRAR para começar!", text_color="#FFFFFF")
        self.resultado_frame.configure(border_width=0)
        self.spin_button.configure(state="normal", text="🎰 GIRAR SLOTS 🎰")

        # Reset slots
        for label in self.slot_labels:
            label.configure(text="❓")

# Create and run application
if __name__ == "__main__":
    root = ctk.CTk()
    app = CassinoSimulator(root)
    root.mainloop()