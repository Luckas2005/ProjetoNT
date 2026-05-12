import tkinter as tk
from tkinter import messagebox
from triagem import Triagem
from medicamento import Medicamento

class ControladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Triagem - UBS")
        self.root.geometry("500x450")
        
        # Interface gráfica intuitiva [cite: 17]
        tk.Label(root, text="Sintomas do Paciente (separados por vírgula):", font=("Arial", 10, "bold")).pack(pady=5)
        self.entry_sintomas = tk.Entry(root, width=50)
        self.entry_sintomas.pack(pady=5)

        tk.Label(root, text="Medicamentos em Uso (separados por vírgula):", font=("Arial", 10, "bold")).pack(pady=5)
        self.entry_medicamentos = tk.Entry(root, width=50)
        self.entry_medicamentos.pack(pady=5)

        tk.Button(root, text="Realizar Triagem", command=self.processar_triagem, bg="lightblue", font=("Arial", 10, "bold")).pack(pady=20)

        # Labels para exibir os resultados [cite: 15]
        self.lbl_risco = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.lbl_risco.pack(pady=10)
        
        self.lbl_alertas = tk.Label(root, text="", font=("Arial", 10), fg="red", justify="left")
        self.lbl_alertas.pack(pady=10)

        # Aviso ético obrigatório [cite: 19]
        tk.Label(root, text="Aviso: Este sistema não substitui o diagnóstico médico.", font=("Arial", 8, "italic"), fg="gray").pack(side="bottom", pady=10)

    def processar_triagem(self):
        """Método controlador que orquestra as chamadas aos módulos[cite: 76, 80]."""
        sintomas_raw = self.entry_sintomas.get().split(',')
        medicamentos_raw = self.entry_medicamentos.get().split(',')

        # 1. Validação simples para evitar campos vazios [cite: 89]
        if not self.entry_sintomas.get().strip():
            messagebox.showwarning("Aviso", "Por favor, insira os sintomas.")
            return

        # 2. Módulo de Triagem [cite: 77]
        triagem = Triagem(sintomas_raw)
        risco = triagem.classificar_risco()
        
        # Definindo cores visuais do alerta [cite: 12]
        cor = "black"
        if "VERMELHO" in risco: cor = "red"
        elif "AMARELO" in risco: cor = "orange"
        elif "VERDE" in risco: cor = "green"
        
        self.lbl_risco.config(text=f"Classificação: {risco}", fg=cor)

        # 3. Módulo de Interações [cite: 77]
        medicamento = Medicamento(medicamentos_raw)
        alertas = medicamento.verificar_interacoes()

        # 4. Exibir Alertas [cite: 84]
        if alertas:
            texto_alertas = "\n".join(alertas)
            self.lbl_alertas.config(text="INTERAÇÃO DETECTADA:\n" + texto_alertas)
            messagebox.showerror("Risco de Interação Medicamentosa", texto_alertas)
        else:
            self.lbl_alertas.config(text="Nenhuma interação perigosa detectada no banco atual.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ControladorApp(root)
    root.mainloop()