import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
from triagem import Triagem
from medicamento import Medicamento

class ControladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Triagem - UBS")
        self.root.geometry("600x550")
        self.root.configure(bg="#f4f4f9")
        
        # Criação/limpeza do log temporário ao iniciar a sessão (Acesso local) 
        self.arquivo_log = "log_sessao.txt"
        if os.path.exists(self.arquivo_log):
            os.remove(self.arquivo_log)

        # Aviso ético e de privacidade destacado no topo [cite: 19, 91]
        lbl_aviso = tk.Label(root, text="⚠ AVISO: Este sistema é um apoio à triagem e não substitui o diagnóstico médico.\nNenhum dado sensível ou identificável do paciente será armazenado.", 
                             font=("Arial", 9, "bold"), fg="#856404", bg="#fff3cd", wraplength=550, justify="center")
        lbl_aviso.pack(pady=10, fill="x", padx=10)

        # Interface desenhada para acessibilidade (fontes maiores e contraste) 
        tk.Label(root, text="Sintomas do Paciente:", font=("Arial", 12, "bold"), bg="#f4f4f9").pack(pady=(10,0))
        tk.Label(root, text="(Separe por vírgulas. Ex: febre, dor no peito)", font=("Arial", 9), bg="#f4f4f9").pack()
        self.entry_sintomas = tk.Entry(root, width=50, font=("Arial", 12))
        self.entry_sintomas.pack(pady=5)

        tk.Label(root, text="Medicamentos de Uso Contínuo:", font=("Arial", 12, "bold"), bg="#f4f4f9").pack(pady=(15,0))
        tk.Label(root, text="(Separe por vírgulas. Ex: ibuprofeno, varfarina)", font=("Arial", 9), bg="#f4f4f9").pack()
        self.entry_medicamentos = tk.Entry(root, width=50, font=("Arial", 12))
        self.entry_medicamentos.pack(pady=5)

        # Botão de processamento com alto contraste
        btn_triagem = tk.Button(root, text="REALIZAR TRIAGEM", command=self.processar_triagem, 
                                bg="#0056b3", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
        btn_triagem.pack(pady=20)

        # Áreas para exibição dos resultados (Triagem e Alertas) [cite: 15]
        self.lbl_risco = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#f4f4f9")
        self.lbl_risco.pack(pady=10)
        
        self.lbl_alertas = tk.Label(root, text="", font=("Arial", 11, "bold"), fg="red", bg="#f4f4f9", justify="center", wraplength=550)
        self.lbl_alertas.pack(pady=10)

    def registrar_log(self, mensagem: str):
        """Mantém histórico temporário das interações para rastreabilidade de erros de digitação."""
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.arquivo_log, "a", encoding="utf-8") as f:
            f.write(f"[{agora}] {mensagem}\n")

    def processar_triagem(self):
        """Controlador que orquestra o fluxo de dados entre os módulos[cite: 80, 84]."""
        entrada_sintomas = self.entry_sintomas.get()
        entrada_medicamentos = self.entry_medicamentos.get()

        # Validação de campos vazios [cite: 89]
        if not entrada_sintomas.strip():
            messagebox.showwarning("Atenção", "O campo de sintomas não pode estar vazio.")
            return

        sintomas_raw = entrada_sintomas.split(',')
        medicamentos_raw = entrada_medicamentos.split(',')

        # Processamento - Módulo Triagem [cite: 77, 81]
        triagem = Triagem(sintomas_raw)
        risco = triagem.classificar_risco()
        
        if risco == "ERRO_VALIDACAO":
            messagebox.showerror("Erro de Formatação", "Os sintomas contêm caracteres especiais inválidos.")
            return

        cor = "black"
        bg_cor = "#f4f4f9"
        if "VERMELHO" in risco:
            cor = "white"; bg_cor = "#dc3545" # Alto contraste para acessibilidade 
        elif "AMARELO" in risco:
            cor = "black"; bg_cor = "#ffc107"
        elif "VERDE" in risco:
            cor = "white"; bg_cor = "#28a745"
        
        self.lbl_risco.config(text=f" Classificação: {risco} ", fg=cor, bg=bg_cor)

        # Processamento - Módulo de Interações [cite: 77, 82]
        medicamento = Medicamento(medicamentos_raw)
        alertas = medicamento.verificar_interacoes()

        if "ERRO_VALIDACAO" in alertas:
            messagebox.showerror("Erro de Formatação", "Os medicamentos contêm caracteres especiais inválidos.")
            self.lbl_alertas.config(text="")
            return

        # Exibição do Alerta [cite: 15]
        if alertas:
            texto_alertas = "\n".join(alertas)
            mensagem_final = f"⚠ INTERAÇÃO PERIGOSA DETECTADA:\n{texto_alertas}"
            self.lbl_alertas.config(text=mensagem_final)
            self.registrar_log(mensagem_final.replace("\n", " ")) # Grava no log de sessão 
            messagebox.showerror("ALERTA DE RISCO", mensagem_final)
        else:
            self.lbl_alertas.config(text="✓ Nenhuma interação perigosa detectada.")
            self.registrar_log("Nenhuma interação detectada para os medicamentos informados.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ControladorApp(root)
    root.mainloop()