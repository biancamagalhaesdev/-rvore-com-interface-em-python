import customtkinter as ctk
from tkinter import messagebox

class Node:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None

class BST:
    def __init__(self):
        self.raiz = None
    
    def isEmpty(self):
        return self.raiz is None
    
    def inserir(self, chave):
        if self.raiz is None:
            self.raiz = Node(chave)
            return True
        else:
            return self._inserir_rec(self.raiz, chave)

    def _inserir_rec(self, no, chave):
        if chave == no.chave:
            return False  
        if chave < no.chave:
            if no.esquerda is None:
                no.esquerda = Node(chave)
                return True
            else:
                return self._inserir_rec(no.esquerda, chave)
        else:
            if no.direita is None:
                no.direita = Node(chave)
                return True
            else:
                return self._inserir_rec(no.direita, chave)

    def tamanho(self):
        return self._tamanho_rec(self.raiz)

    def _tamanho_rec(self, no):
        if no is None:
            return 0
        return 1 + self._tamanho_rec(no.esquerda) + self._tamanho_rec(no.direita)

    def altura(self):
        return self._altura_rec(self.raiz)

    def _altura_rec(self, no):
        if no is None:
            return -1
        return 1 + max(self._altura_rec(no.esquerda), self._altura_rec(no.direita))

    def menor(self):
        if self.raiz is None:
            return None
        atual = self.raiz
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual.chave

    def maior(self):
        if self.raiz is None:
            return None
        atual = self.raiz
        while atual.direita is not None:
            atual = atual.direita
        return atual.chave

    def esta_balanceada(self):
        return self._esta_balanceada_rec(self.raiz)

    def _esta_balanceada_rec(self, no):
        if no is None:
            return True
        altura_esquerda = self._altura_rec(no.esquerda)
        altura_direita = self._altura_rec(no.direita)
        balanceado = abs(altura_esquerda - altura_direita) <= 1
        return balanceado and self._esta_balanceada_rec(no.esquerda) and self._esta_balanceada_rec(no.direita)
        
    def comprimento(self):
        return self._comprimento_rec(self.raiz)

    def _comprimento_rec(self, no):
        if no is None:
            return 0
        esquerda = self._comprimento_rec(no.esquerda)
        direita = self._comprimento_rec(no.direita)
        return max(esquerda, direita) + 1

    def percurso(self, tipo):
        resultado = []
        if tipo == "pre":
            self._pre_ordem(self.raiz, resultado)
        elif tipo == "em":
            self._em_ordem(self.raiz, resultado)
        elif tipo == "pos":
            self._pos_ordem(self.raiz, resultado)
        elif tipo == "nivel":
            resultado = self.level_order()
        return resultado

    def _pre_ordem(self, no, resultado):
        if no:
            resultado.append(no.chave)
            self._pre_ordem(no.esquerda, resultado)
            self._pre_ordem(no.direita, resultado)

    def _em_ordem(self, no, resultado):
        if no:
            self._em_ordem(no.esquerda, resultado)
            resultado.append(no.chave)
            self._em_ordem(no.direita, resultado)

    def _pos_ordem(self, no, resultado):
        if no:
            self._pos_ordem(no.esquerda, resultado)
            self._pos_ordem(no.direita, resultado)
            resultado.append(no.chave)

    def level_order(self):
        fila = [self.raiz] if self.raiz else []
        resultado = []
        while fila:
            atual = fila.pop(0)
            resultado.append(atual.chave)
            if atual.esquerda:
                fila.append(atual.esquerda)
            if atual.direita:
                fila.append(atual.direita)
        return resultado

class InterfaceABB(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Árvore Binária de Busca")
        self.geometry("1000x600")
        self.config(bg="#222222")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.arvore = BST()
        self.raio_no = 25
        self.altura_nivel = 90

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite um número natural",
                                  fg_color="#333333", text_color="white", border_color="#ff69b4")
        self.entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkButton(self, text="Inserir", command=self.inserir_chave,
                      fg_color="#ff69b4", hover_color="#ff85c1").grid(row=0, column=1, padx=10, pady=10)

        botoes_frame = ctk.CTkFrame(self, fg_color="#1e1e1e")
        botoes_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        acoes = [
            ("Tamanho", lambda: self.mostrar_valor("Tamanho", self.arvore.tamanho())),
            ("Altura", lambda: self.mostrar_valor("Altura", self.arvore.altura())),
            ("Menor", lambda: self.mostrar_valor("Menor", self.arvore.menor())),
            ("Maior", lambda: self.mostrar_valor("Maior", self.arvore.maior())),
            ("Balanceada?", self.mostrar_balanceamento),
            ("Pré-Ordem", lambda: self.mostrar_percurso("Pré", self.arvore.percurso("pre"))),
            ("Em-Ordem", lambda: self.mostrar_percurso("Em", self.arvore.percurso("em"))),
            ("Pós-Ordem", lambda: self.mostrar_percurso("Pós", self.arvore.percurso("pos"))),
            ("Nível-Ordem", lambda: self.mostrar_percurso("Nível", self.arvore.percurso("nivel"))),
            ("Comprimento", lambda: self.mostrar_valor("Comprimento da Árvore", self.arvore.comprimento()))
        ]

        for i, (txt, cmd) in enumerate(acoes):
            ctk.CTkButton(botoes_frame, text=txt, command=cmd,
                          fg_color="#ff69b4", hover_color="#ff85c1").grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="nsew")
            
        for col in range(3):  
            botoes_frame.grid_columnconfigure(col, weight=1)

        self.resultado = ctk.CTkLabel(self, text="", font=("Arial", 14), text_color="#ffb6c1")
        self.resultado.grid(row=2, column=0, columnspan=2, pady=10)

        canvas_frame = ctk.CTkFrame(self)
        canvas_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        scroll_y = ctk.CTkScrollbar(canvas_frame, orientation="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = ctk.CTkScrollbar(canvas_frame, orientation="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        self.canvas = ctk.CTkCanvas(canvas_frame, bg="#222222", highlightthickness=0,
                            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        scroll_y.configure(command=self.canvas.yview)
        scroll_x.configure(command=self.canvas.xview)

        self.interno_canvas = ctk.CTkFrame(self.canvas, fg_color="#222222")
        self.canvas.create_window((0, 0), window=self.interno_canvas, anchor="nw")

        self.interno_canvas.bind("<Configure>", lambda e: 
        self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.bind("<Configure>", lambda e: self.desenhar_arvore())

    def inserir_chave(self):
        chave = self.entry.get()
        if not chave.isdigit():
            messagebox.showerror("Erro", "Digite apenas números naturais.")
            self.entry.delete(0, "end")
            return
        a = self.arvore.inserir(int(chave))
        if a is False:
            self.resultado.configure(text=f"Chave {chave} já existe na árvore.", text_color="#ffb6c1")
            self.entry.delete(0, "end")
        else:
            self.resultado.configure(text=f"Chave {chave} inserida com sucesso!", text_color="#ffb6c1")
            self.entry.delete(0, "end")
            self.desenhar_arvore()

    def mostrar_valor(self, nome, valor):
        if valor is None:
            self.resultado.configure(text="Árvore vazia.", text_color="#ffb6c1")
        else:
            self.resultado.configure(text=f"{nome}: {valor}", text_color="#ffb6c1")

    def mostrar_balanceamento(self):
        if self.arvore.isEmpty():
            self.resultado.configure(text="Árvore vazia.", text_color="#ffb6c1")
        else:
            if self.arvore.esta_balanceada():
                self.resultado.configure(text="Árvore balanceada: Sim ✅", text_color="#2ecc71")
            else:
                self.resultado.configure(text="Árvore balanceada: Não ❌", text_color="#e74c3c")  

    def mostrar_percurso(self, tipo, resultado):
        self.resultado.configure(text=f"{tipo}-Ordem: {resultado}", text_color="#ffb6c1")

    def desenhar_arvore(self):
        self.canvas.delete("all")

        if self.arvore.raiz is None:
            return
            
        largura = self.canvas.winfo_width()
        if largura < 100:
            largura = 900

        altura_inicial=50
        cores = ["#ff69b4", "#ff85c1", "#ffa6d3", "#ffb8dc"]

        def desenha(no, x, y, espacamento, cor_index=0):
            if no.esquerda:
                x_esq = x - espacamento
                y_novo = y + self.altura_nivel
                self.canvas.create_line(x, y, x_esq, y_novo, fill="white", width=2)
                desenha(no.esquerda, x_esq, y_novo, espacamento / 2, (cor_index + 1) % len(cores))
            if no.direita:
                x_dir = x + espacamento
                y_novo = y + self.altura_nivel
                self.canvas.create_line(x, y, x_dir, y_novo, fill="white", width=2)
                desenha(no.direita, x_dir, y_novo, espacamento / 2, (cor_index + 1) % len(cores))

            cor = cores[cor_index]
            self.canvas.create_oval(x - self.raio_no, y - self.raio_no,
                                    x + self.raio_no, y + self.raio_no,
                                    fill=cor, outline="white", width=2)
            self.canvas.create_text(x, y, text=str(no.chave), fill="white", font=("Arial", 14, "bold"))

        desenha(self.arvore.raiz, largura / 2, 50, largura / 4)
        bbox = self.canvas.bbox("all")
        if bbox:
            x0, y0, x1, y1 = bbox
            self.canvas.configure(scrollregion=(0, 0, largura, y1))

if __name__ == "__main__":
    app = InterfaceABB()
    app.mainloop()
