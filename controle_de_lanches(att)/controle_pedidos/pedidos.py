# pedidos.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import criar_banco_pedidos, obter_pedidos, adicionar_pedido, atualizar_pedido, remover_pedido
from PIL import Image, ImageTk

class PedidosApp:
    def __init__(self):
        criar_banco_pedidos()
        self.janela = tk.Tk()
        self.janela.geometry("900x600")
        self.janela.title("Controle de Pedidos")
        self.janela.configure(bg="#F2F2F2")
        self.janela.resizable(False, False)
        
        self.opcoes_itens = [
            "Hambúrguer com queijo e maionese",
            "Hambúrguer com queijo e BBQ",
            "Hambúrguer com salada e maionese",
            "Batata frita com cheddar e bacon",
            "Sorvete de chocolate",
            "Sorvete de baunilha",
            "Guaraná Coca-Cola",
            "Guaraná Antártica",
        ]
        
        self.criar_widgets()
        self.listar_pedidos()
    
    def criar_widgets(self):
        # Carregar imagem
        try:
            img = Image.open("images/kfc.png")
            img = img.resize((100, 50))
            img_tk = ImageTk.PhotoImage(img)
            label_img = tk.Label(self.janela, image=img_tk)
            label_img.pack(pady=8)
            label_img.image = img_tk
        except:
            pass
        
        # Formulário de pedidos
        tk.Label(self.janela, text="Cliente", bg="#F2F2F2", 
                font=("Century Gothic", 12)).pack()
        self.entry_cliente = tk.Entry(self.janela, width=30, 
                                    font=("Century Gothic", 10))
        self.entry_cliente.pack(pady=5)
        
        tk.Label(self.janela, text="Item", bg="#F2F2F2", 
                font=("Century Gothic", 12)).pack()
        self.combobox_item = ttk.Combobox(self.janela, 
                                        values=self.opcoes_itens, width=35, 
                                        font=("Century Gothic", 10), state="readonly")
        self.combobox_item.pack(pady=5)
        self.combobox_item.set("Escolha um item")
        
        tk.Label(self.janela, text="Quantidade", bg="#F2F2F2", 
                font=("Century Gothic", 12)).pack()
        vcmd = self.janela.register(self.validar_numeros)
        self.spinbox_quantidade = tk.Spinbox(self.janela, from_=1, to=100, 
                                           width=28, font=("Century Gothic", 10), 
                                           validate="key", validatecommand=(vcmd, "%P"))
        self.spinbox_quantidade.pack(pady=5)
        
        tk.Label(self.janela, text="Observações", bg="#F2F2F2", 
                font=("Century Gothic", 12)).pack()
        self.entry_observacao = tk.Text(self.janela, height=2, width=35, 
                                      font=("Century Gothic", 10))
        self.entry_observacao.pack(pady=(0,20))
        
        # Botões
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack()
        
        tk.Button(frame_botoes, text="Cadastrar pedido", bg="#D41C00", fg="white", 
                 font=("Verdana", 12, "bold"), command=self.cadastrar_pedido
                 ).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Editar pedidos", bg="#D41C00", fg="white", 
                 font=("Verdana", 12, "bold"), command=self.editar_pedido
                 ).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Excluir pedido", bg="red", fg="white", 
                 font=("Verdana", 12, "bold"), command=self.excluir_pedido
                 ).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Relatórios", bg="#D41C00", fg="white", 
                 font=("Verdana", 12, "bold"), command=self.exibir_relatorios
                 ).pack(side="left", padx=5)
        
        # Lista de pedidos
        self.tree_lista = ttk.Treeview(self.janela, 
                                      columns=("ID", "Cliente", "Item", "Quantidade", "Observação"), 
                                      show="headings")
        for col in ("ID", "Cliente", "Item", "Quantidade", "Observação"):
            self.tree_lista.heading(col, text=col)
        
        self.tree_lista.column("ID", width=50, stretch=False)
        self.tree_lista.column("Cliente", width=150)
        self.tree_lista.column("Item", width=250)
        self.tree_lista.column("Quantidade", width=50)
        self.tree_lista.column("Observação", width=250)
        
        self.tree_lista.pack(expand=True, fill="both", pady=15)
    
    def cadastrar_pedido(self):
        cliente = self.entry_cliente.get().strip()
        item = self.combobox_item.get().strip()
        quantidade = self.spinbox_quantidade.get().strip()
        observacao = self.entry_observacao.get("1.0", tk.END).strip()
        
        if not cliente or item == "Escolha um item" or not quantidade.isdigit():
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        adicionar_pedido(cliente, item, quantidade, observacao)
        self.listar_pedidos()
        self.limpar_campos()
    
    def listar_pedidos(self):
        pedidos = obter_pedidos()
        self.tree_lista.delete(*self.tree_lista.get_children())
        for pedido in pedidos:
            self.tree_lista.insert("", tk.END, values=pedido)
    
    def editar_pedido(self):
        selecionado = self.tree_lista.selection()
        if not selecionado:
            messagebox.showwarning("Atenção!", "Selecione um item para editar!")
            return
        
        valores = self.tree_lista.item(selecionado)["values"]
        pedido_id = valores[0]

        janela_edicao = tk.Toplevel()
        janela_edicao.title("Editar itens")
        janela_edicao.geometry("400x300")
        janela_edicao.configure(bg="#F2F2F2")
        janela_edicao.resizable(False, False)
        janela_edicao.grab_set()

        # Widgets de edição
        tk.Label(janela_edicao, text="Editar cliente").pack()
        edicao_cliente_entry = tk.Entry(janela_edicao, width=20)
        edicao_cliente_entry.pack(pady=5)
        edicao_cliente_entry.insert(0, valores[1])

        tk.Label(janela_edicao, text="Editar os itens").pack()
        edicao_item = ttk.Combobox(janela_edicao, values=self.opcoes_itens, width=20)
        edicao_item.pack(pady=5)
        edicao_item.set(valores[2])

        tk.Label(janela_edicao, text="Editar quantidade").pack()
        edicao_quantidade = tk.Spinbox(janela_edicao, from_=1, to=100, width=20)
        edicao_quantidade.pack(pady=5)
        edicao_quantidade.delete(0, tk.END)
        edicao_quantidade.insert(0, valores[3])

        tk.Label(janela_edicao, text="Editar observação").pack()
        edicao_observacao = tk.Text(janela_edicao, width=20, height=5)
        edicao_observacao.pack(pady=5)
        edicao_observacao.insert("1.0", valores[4])

        def salvar_edicao():
            novo_cliente = edicao_cliente_entry.get().strip()
            novo_item = edicao_item.get().strip()
            nova_quantidade = edicao_quantidade.get().strip()
            nova_observacao = edicao_observacao.get("1.0", tk.END).strip()
            
            if not novo_cliente or novo_item == "Escolha um item" or not nova_quantidade.isdigit():
                messagebox.showerror("Erro!", "Preencha todos os campos corretamente")
                return

            atualizar_pedido(pedido_id, novo_cliente, novo_item, nova_quantidade, nova_observacao)
            messagebox.showinfo("Confirmação", "Editado com sucesso!")
            janela_edicao.destroy()
            self.listar_pedidos()

        tk.Button(janela_edicao, text="Salvar alterações", command=salvar_edicao).pack()
    
    def excluir_pedido(self):
        selecionado = self.tree_lista.selection()
        if not selecionado:
            messagebox.showwarning("Atenção!", "Selecione um item para apagar!")
            return
        
        confirmado = messagebox.askyesno("Atenção!", "Deseja realmente excluir?")
        if not confirmado:
            return
        
        pedido_id = self.tree_lista.item(selecionado)["values"][0]
        remover_pedido(pedido_id)
        self.listar_pedidos()
    
    def exibir_relatorios(self):
        relatorios_janela = tk.Toplevel()
        relatorios_janela.title("Relatório")
        relatorios_janela.geometry("800x700")
        relatorios_janela.resizable(True, False)
        relatorios_janela.configure(bg="#F2F2F2")
        relatorios_janela.grab_set()

        tree_relatorio = ttk.Treeview(relatorios_janela, 
                                    columns=("ID", "Cliente", "Item", "Quantidade", "Observação"), 
                                    show="headings")
        for col in ("ID", "Cliente", "Item", "Quantidade", "Observação"):
            tree_relatorio.heading(col, text=col)
        
        tree_relatorio.column("ID", width=20)
        tree_relatorio.column("Cliente", width=150)
        tree_relatorio.column("Item", width=250)
        tree_relatorio.column("Quantidade", width=80)
        tree_relatorio.column("Observação", width=250)

        tree_relatorio.pack(expand=True, fill="both", pady=20, padx=10)

        pedidos = obter_pedidos()
        for pedido in pedidos:
            tree_relatorio.insert("", tk.END, values=pedido)
    
    def limpar_campos(self):
        self.entry_cliente.delete(0, tk.END)
        self.combobox_item.set("Escolha um item")
        self.spinbox_quantidade.delete(0, tk.END)
        self.spinbox_quantidade.insert(0, "1")
        self.entry_observacao.delete("1.0", tk.END)
    
    def validar_numeros(self, texto):
        return texto.isdigit()
    
    def run(self):
        self.janela.mainloop()