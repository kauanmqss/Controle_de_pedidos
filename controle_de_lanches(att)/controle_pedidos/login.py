# login.py
import tkinter as tk
from tkinter import messagebox
from database import criar_banco_usuarios, verificar_login, registrar_usuario
from PIL import Image, ImageTk

class LoginApp:
    def __init__(self):
        criar_banco_usuarios()
        self.janela = tk.Tk()
        self.janela.title("Login - Sistema de Pedidos")
        self.janela.geometry("800x600")
        self.janela.configure(bg="#F2F2F2")
        self.janela.resizable(True, True)
        
        self.criar_widgets()
        
    def criar_widgets(self):
        frame_principal = tk.Frame(self.janela, bg="#F2F2F2")
        frame_principal.pack(expand=True)
        
        # Título
        titulo_login = tk.Label(frame_principal, text="Login", font=("Century Gothic", 30), bg="#F2F2F2")
        titulo_login.pack(pady=40)
        
        # Usuário
        tk.Label(frame_principal, text="Usuario", font=("Century Gothic", 15), bg="#F2F2F2", fg="black").pack(pady=5)
        self.entry_usuario = tk.Entry(frame_principal, width=30, fg="black", font=("Century Gothic", 12))
        self.entry_usuario.pack(pady=10)
        
        # Senha
        tk.Label(frame_principal, text="Senha", font=("Century Gothic", 15), bg="#F2F2F2", fg="black").pack(pady=5)
        self.entry_senha = tk.Entry(frame_principal, width=50, show="•", fg="black")
        self.entry_senha.pack(pady=10)
        
        # Botões
        btn_login = tk.Button(frame_principal, text="LOGAR", command=self.verificar_login, 
                            fg="black", bg="white", font=("Century Gothic", 15, "bold"), 
                            activebackground="red")
        btn_login.pack(pady=15)
        btn_login.bind("<Enter>", self.em_cima_botao)
        btn_login.bind("<Leave>", self.sair_cima_botao)
        
        btn_registrar = tk.Button(frame_principal, text="REGISTRAR-SE", command=self.abrir_tela_registro, 
                                bg="white", fg="red", font=("Century Gothic", 15, "bold"))
        btn_registrar.pack(pady=5)
        btn_registrar.bind("<Enter>", self.em_cima_botao)
        btn_registrar.bind("<Leave>", self.sair_cima_botao)
    
    def verificar_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Erro ao logar!", "Todos os campos são obrigatórios!")
            return
        
        if verificar_login(usuario, senha):
            messagebox.showinfo("Logado!", "Logado com sucesso!")
            self.janela.destroy()
            from pedidos import PedidosApp
            app = PedidosApp()
            app.run()
        else:
            messagebox.showerror("Erro ao logar!", "Usuário ou senha incorretos!")
    
    def abrir_tela_registro(self):
        self.janela.withdraw()
        janela_registro = tk.Toplevel()
        janela_registro.title("Registro")
        janela_registro.geometry("800x600")
        janela_registro.configure(bg="#D3D3D3")
        
        # Widgets de registro
        frame_principal = tk.Frame(janela_registro, bg="#D3D3D3")
        frame_principal.pack(expand=True)
        
        tk.Label(frame_principal, text="Cadastro", bg="#D3D3D3", fg="black", 
                font=("Century Gothic", 30)).pack(pady=40)
        
        # Entradas
        entrada_usuario = tk.StringVar()
        entrada_senha = tk.StringVar()
        entrada_confirmar_senha = tk.StringVar()
        
        tk.Label(frame_principal, text="Usuário", bg="#D3D3D3", fg="black", 
                font=("Century Gothic", 15)).pack(pady=20)
        tk.Entry(frame_principal, width=28, textvariable=entrada_usuario, 
                fg="black", font=("Century Gothic", 13)).pack(pady=5)
        
        tk.Label(frame_principal, text="Senha", bg="#D3D3D3", fg="black", 
                font=("Century Gothic", 15)).pack(pady=20)
        tk.Entry(frame_principal, width=50, show="•", textvariable=entrada_senha, 
                fg="black").pack(pady=5)
        
        tk.Label(frame_principal, text="Confirmar Senha", bg="#D3D3D3", fg="red", 
                font=("Century Gothic", 15)).pack(pady=20)
        tk.Entry(frame_principal, width=50, show="*", textvariable=entrada_confirmar_senha, 
                fg="red").pack(pady=5)
        
        # Botão Registrar
        btn_registrar = tk.Button(frame_principal, text="Registrar", 
                                command=lambda: self.registrar_usuario(
                                    entrada_usuario.get().strip(),
                                    entrada_senha.get().strip(),
                                    entrada_confirmar_senha.get().strip(),
                                    janela_registro
                                ), 
                                bg="white", fg="red", font=("Century Gothic", 15, "bold"))
        btn_registrar.pack(pady=20)
        btn_registrar.bind("<Enter>", self.em_cima_botao)
        btn_registrar.bind("<Leave>", self.sair_cima_botao)
    
    def registrar_usuario(self, usuario, senha, confirmar_senha, janela_registro):
        if not usuario or not senha or not confirmar_senha:
            messagebox.showwarning("Erro ao registrar!", "Todos os campos são obrigatórios")
            return
        
        if senha != confirmar_senha:
            messagebox.showerror("Erro ao registrar!", "As senhas não coincidem!")
            return
        
        if registrar_usuario(usuario, senha):
            messagebox.showinfo("Registrado!", "Registrado com sucesso!")
            janela_registro.destroy()
            self.janela.deiconify()
        else:
            messagebox.showerror("Erro ao registrar!", "Usuário já existe!")
    
    def em_cima_botao(self, event):
        event.widget["background"] = "#4169E1"
        event.widget["foreground"] = "white"
    
    def sair_cima_botao(self, event):
        event.widget["background"] = "white"
        event.widget["foreground"] = "black"
    
    def run(self):
        self.janela.mainloop()