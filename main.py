import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
from datetime import datetime
from triagem import Triagem
from medicamento import Medicamento

class ControladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Triagem - UBS")
        self.root.geometry("650x600")
        self.root.configure(bg="#f4f4f9")
        
        # Dados de sessão do usuário logado
        self.usuario_atual = None
        self.perfil_atual = None
        
        # Base de usuários simulada (Credenciais de exemplo)
        self.usuarios_cadastrados = {
            "medico1": {"senha": "123", "perfil": "Médico", "nome": "Dr. Lucas Moreira"},
            "enfermeira1": {"senha": "456", "perfil": "Enfermeiro(a)", "nome": "Enf. Ketlen Santos"}
        }
        
        # Histórico de sessão (Log temporário local)
        self.arquivo_log = "log_sessao.txt"
        if os.path.exists(self.arquivo_log):
            os.remove(self.arquivo_log)

        # Containers principais para alternância de telas
        self.container_login = tk.Frame(self.root, bg="#f4f4f9")
        self.container_principal = tk.Frame(self.root, bg="#f4f4f9")
        
        # Inicializa exibindo a tela de login
        self.construir_tela_login()
        self.container_login.pack(fill="both", expand=True)

    def registrar_log(self, mensagem: str):
        """Grava eventos no log associando a ação ao usuário logado."""
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usuario_info = f"[{self.perfil_atual}: {self.usuario_atual}]" if self.usuario_atual else "[SISTEMA]"
        with open(self.arquivo_log, "a", encoding="utf-8") as f:
            f.write(f"[{agora}] {usuario_info} {mensagem}\n")

  
    # CONSTRUÇÃO DA INTERFACE: TELA DE LOGIN
    def construir_tela_login(self):
        # Título Principal
        lbl_titulo = tk.Label(self.container_login, text="Acesso ao Sistema UBS", 
                              font=("Arial", 18, "bold"), fg="#0056b3", bg="#f4f4f9")
        lbl_titulo.pack(pady=(50, 20))
        
        # Caixa de Login
        frame_card = tk.LabelFrame(self.container_login, text=" Autenticação Requerida ", 
                                   font=("Arial", 10, "bold"), bg="white", padx=20, pady=20, fg="#666")
        frame_card.pack(pady=10, padx=50, fill="x")
        
        # Campo: Perfil profissional
        tk.Label(frame_card, text="Tipo de Usuário:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(5, 2))
        self.combo_perfil = ttk.Combobox(frame_card, values=["Médico", "Enfermeiro(a)"], font=("Arial", 11), state="readonly")
        self.combo_perfil.set("Enfermeiro(a)") # Padrão inicial
        self.combo_perfil.pack(fill="x", pady=(0, 15))
        
        # Campo: Usuário
        tk.Label(frame_card, text="Usuário (Login):", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(5, 2))
        self.entry_usuario = tk.Entry(frame_card, font=("Arial", 11))
        self.entry_usuario.pack(fill="x", pady=(0, 15))
        
        # Campo: Senha
        tk.Label(frame_card, text="Senha:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(5, 2))
        self.entry_senha = tk.Entry(frame_card, font=("Arial", 11), show="*")
        self.entry_senha.pack(fill="x", pady=(0, 20))
        
        # Botão de Entrada
        btn_entrar = tk.Button(frame_card, text="ENTRAR NO SISTEMA", command=self.autenticar_usuario, 
                               bg="#28a745", fg="white", font=("Arial", 11, "bold"), pady=5, cursor="hand2")
        btn_entrar.pack(fill="x")

        # Rodapé ético fixo na tela de login
        lbl_rodape = tk.Label(self.container_login, text="Segurança de dados em conformidade com as normas de saúde.\nUso restrito a profissionais autorizados.", 
                              font=("Arial", 8, "italic"), fg="gray", bg="#f4f4f9", justify="center")
        lbl_rodape.pack(side="bottom", pady=20)

    def autenticar_usuario(self):
        """Valida as credenciais inseridas e gerencia a transição de telas."""
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()
        perfil_selecionado = self.combo_perfil.get()
        
        if not usuario or not senha:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos de login.")
            return
            
        if usuario in self.usuarios_cadastrados:
            dados = self.usuarios_cadastrados[usuario]
            if dados["senha"] == senha and dados["perfil"] == perfil_selecionado:
                # Autenticação bem-sucedida: define variáveis de estado
                self.usuario_atual = dados["nome"]
                self.perfil_atual = dados["perfil"]
                
                self.registrar_log("Autenticação realizada com sucesso.")
                
                # Transição visual: Remove tela de login e constrói a tela principal
                self.container_login.pack_forget()
                self.construir_tela_principal()
                self.container_principal.pack(fill="both", expand=True)
                return
                
        # Registro de tentativa incorreta para segurança
        self.perfil_atual = perfil_selecionado
        self.usuario_atual = usuario
        self.registrar_log("Tentativa de login malsucedida.")
        self.usuario_atual = None
        self.perfil_atual = None
        
        messagebox.showerror("Erro de Acesso", "Usuário, senha ou tipo de perfil incorretos.")

    # CONSTRUÇÃO DA INTERFACE: SISTEMA PRINCIPAL DE TRIAGEM
    def construir_tela_principal(self):
        # Barra superior informativa do usuário logado (Acessibilidade e Controle)
        frame_usuario = tk.Frame(self.container_principal, bg="#0056b3", pady=5)
        frame_usuario.pack(fill="x")
        
        lbl_user_info = tk.Label(frame_usuario, text=f"Sessão Ativa: {self.usuario_atual} ({self.perfil_atual})", 
                                 font=("Arial", 10, "bold"), fg="white", bg="#0056b3")
        lbl_user_info.pack(side="left", padx=15)
        
        btn_logout = tk.Button(frame_usuario, text="Sair / Logout", command=self.realizar_logout, 
                               font=("Arial", 9, "bold"), bg="#dc3545", fg="white", bd=0, padx=8, cursor="hand2")
        btn_logout.pack(side="right", padx=15)

        # Aviso ético obrigatório destacado no topo do painel
        lbl_aviso = tk.Label(self.container_principal, text="⚠ AVISO: Sistema de apoio à decisão clínica. Não substitui o diagnóstico médico.\nNenhum dado sensível ou identificável do paciente será armazenado.", 
                             font=("Arial", 9, "bold"), fg="#856404", bg="#fff3cd", wraplength=600, justify="center")
        lbl_aviso.pack(pady=10, fill="x", padx=15)

        # Formulário de Triagem
        tk.Label(self.container_principal, text="Sintomas do Paciente:", font=("Arial", 12, "bold"), bg="#f4f4f9").pack(pady=(10,0))
        tk.Label(self.container_principal, text="(Separe por vírgulas. Ex: febre, dor no peito)", font=("Arial", 9), bg="#f4f4f9").pack()
        self.entry_sintomas = tk.Entry(self.container_principal, width=55, font=("Arial", 12))
        self.entry_sintomas.pack(pady=5)

        tk.Label(self.container_principal, text="Medicamentos de Uso Contínuo:", font=("Arial", 12, "bold"), bg="#f4f4f9").pack(pady=(15,0))
        tk.Label(self.container_principal, text="(Separe por vírgulas. Ex: ibuprofeno, varfarina)", font=("Arial", 9), bg="#f4f4f9").pack()
        self.entry_medicamentos = tk.Entry(self.container_principal, width=55, font=("Arial", 12))
        self.entry_medicamentos.pack(pady=5)

        # Botão de processamento
        btn_triagem = tk.Button(self.container_principal, text="REALIZAR TRIAGEM CLÍNICA", command=self.processar_triagem, 
                                bg="#28a745", fg="white", font=("Arial", 12, "bold"), padx=15, pady=6, cursor="hand2")
        btn_triagem.pack(pady=15)

        # Áreas para exibição dos resultados em Alto Contraste
        self.lbl_risco = tk.Label(self.container_principal, text="", font=("Arial", 16, "bold"), bg="#f4f4f9")
        self.lbl_risco.pack(pady=10)
        
        self.lbl_alertas = tk.Label(self.container_principal, text="", font=("Arial", 11, "bold"), fg="red", bg="#f4f4f9", justify="center", wraplength=580)
        self.lbl_alertas.pack(pady=10)

    def processar_triagem(self):
        """Orquestra o fluxo de dados entre os módulos injetando metadados de auditoria."""
        entrada_sintomas = self.entry_sintomas.get()
        entrada_medicamentos = self.entry_medicamentos.get()

        if not entrada_sintomas.strip():
            messagebox.showwarning("Atenção", "O campo de sintomas não pode estar vazio.")
            return

        sintomas_raw = entrada_sintomas.split(',')
        medicamentos_raw = entrada_medicamentos.split(',')

        # Execução do Módulo Triagem
        triagem = Triagem(sintomas_raw)
        risco = triagem.classificar_risco()
        
        if risco == "ERRO_VALIDACAO":
            messagebox.showerror("Erro de Formatação", "Os sintomas contêm caracteres especiais inválidos.")
            return

        # Lógica de Cores de Risco para Acessibilidade Visual
        cor, bg_cor = "black", "#f4f4f9"
        if "VERMELHO" in risco:
            cor, bg_cor = "white", "#dc3545"
        elif "AMARELO" in risco:
            cor, bg_cor = "black", "#ffc107"
        elif "VERDE" in risco:
            cor, bg_cor = "white", "#28a745"
        
        self.lbl_risco.config(text=f" Classificação: {risco} ", fg=cor, bg=bg_cor)

        # Execução do Módulo Medicamento
        medicamento = Medicamento(medicamentos_raw)
        alertas = medicamento.verificar_interacoes()

        if "ERRO_VALIDACAO" in alertas:
            messagebox.showerror("Erro de Formatação", "Os medicamentos contêm caracteres especiais inválidos.")
            self.lbl_alertas.config(text="")
            return

        # Tratamento e exibição de alertas de interação
        if alertas:
            texto_alertas = "\n".join(alertas)
            mensagem_final = f"⚠ INTERAÇÃO PERIGOSA DETECTADA:\n{texto_alertas}"
            self.lbl_alertas.config(text=mensagem_final)
            self.registrar_log(f"Alerta gerado: {texto_alertas.replace('\n', ' ')}")
            messagebox.showerror("ALERTA DE RISCO", mensagem_final)
        else:
            self.lbl_alertas.config(text="✓ Nenhuma interação perigosa detectada.")
            self.registrar_log("Triagem realizada. Nenhuma interação medicamentosa encontrada.")

    def realizar_logout(self):
        """Encerra a sessão atual de forma limpa e retorna para a tela de login."""
        self.registrar_log("Logoff efetuado voluntariamente.")
        
        # Limpa dados de sessão e campos
        self.usuario_atual = None
        self.perfil_atual = None
        self.entry_usuario.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.lbl_risco.config(text="", bg="#f4f4f9")
        self.lbl_alertas.config(text="")
        
        # Inverte visibilidade de containers
        self.container_principal.pack_forget()
        self.container_login.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ControladorApp(root)
    root.mainloop()