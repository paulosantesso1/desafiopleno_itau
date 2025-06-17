import wx

class Produto:
    def __init__(self, nome, preco, opcoes=None):
        self.nome = nome
        self.preco = preco
        self.opcoes = opcoes or []

class Ingresso:
    def __init__(self, tipo, preco):
        self.tipo = tipo
        self.preco = preco

class MudancasPersonalizadasFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 800))
        panel = wx.Panel(self)

        self.ingressos = [
            Ingresso("Inteira", 30.0),
            Ingresso("Meia", 15.0)
        ]
        self.produtos = [
            Produto("Pipoca", 10.0, ["Pipoca doce", "Pipoca salgada", "Pipoca gourmet", "Pipoca pipocada", "Pipoca doce caramelada"]),
            Produto("Chocolate", 7.0, ["Suflair", "Diamante Negro", "Laka", "Chokito", "Prestígio"]),
            Produto("Refrigerante", 8.0, ["Coca-cola", "Guaraná Antártica", "Pepsi", "Fanta laranja", "Fanta uva"])
        ]

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Quantidade de ingressos
        vbox.Add(wx.StaticText(panel, label="Quantidade de ingressos:"), 0, wx.ALL, 5)
        self.qtd_choices = ["1", "2", "3", "4", "5", "Outro"]
        self.qtd_choice = wx.Choice(panel, choices=self.qtd_choices)
        self.qtd_choice.SetSelection(0)
        vbox.Add(self.qtd_choice, 0, wx.ALL | wx.EXPAND, 5)

        self.qtd_text = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.qtd_text.Hide()
        vbox.Add(self.qtd_text, 0, wx.ALL | wx.EXPAND, 5)

        # Tipo de ingresso
        self.tipo_box = wx.BoxSizer(wx.HORIZONTAL)
        self.tipo_label = wx.StaticText(panel, label="Tipo de ingresso:")
        self.tipo_box.Add(self.tipo_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.tipo_choice = wx.Choice(panel, choices=["Todos Inteira", "Todos Meia", "Personalizado"])
        self.tipo_choice.SetSelection(0)
        self.tipo_box.Add(self.tipo_choice, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.tipo_box, 0, wx.EXPAND)

        # Personalizado: quantidade de cada tipo
        self.personalizado_box = wx.BoxSizer(wx.HORIZONTAL)
        self.int_label = wx.StaticText(panel, label="Inteiras:")
        self.int_text = wx.TextCtrl(panel, value="0", size=(40, -1))
        self.meia_label = wx.StaticText(panel, label="Meias:")
        self.meia_text = wx.TextCtrl(panel, value="0", size=(40, -1))
        self.personalizado_box.Add(self.int_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.personalizado_box.Add(self.int_text, 0, wx.ALL, 5)
        self.personalizado_box.Add(self.meia_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.personalizado_box.Add(self.meia_text, 0, wx.ALL, 5)
        vbox.Add(self.personalizado_box, 0, wx.EXPAND)
        self.personalizado_box.ShowItems(False)

        # Produtos adicionais com quantidade e sabores
        vbox.Add(wx.StaticText(panel, label="Produtos adicionais (quantidade e sabores):"), 0, wx.ALL, 5)
        self.produto_sabor_qtds = []
        self.produto_sabor_checks = []
        for prod in self.produtos:
            box = wx.StaticBox(panel, label=f"{prod.nome} (R$ {prod.preco:.2f} cada)")
            sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
            sabor_qtds = []
            sabor_checks = []
            for sabor in prod.opcoes:
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                check = wx.CheckBox(panel, label=sabor)
                qtd = wx.SpinCtrl(panel, min=0, max=100, initial=0, size=(50, -1))
                qtd.Enable(False)
                hbox.Add(check, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
                hbox.Add(qtd, 0, wx.ALL, 5)
                sbox.Add(hbox, 0, wx.EXPAND)
                sabor_qtds.append(qtd)
                sabor_checks.append(check)
                check.Bind(wx.EVT_CHECKBOX, self.make_on_sabor_check(qtd))
            self.produto_sabor_qtds.append(sabor_qtds)
            self.produto_sabor_checks.append(sabor_checks)
            vbox.Add(sbox, 0, wx.EXPAND | wx.ALL, 5)

        vbox.AddSpacer(20)
        self.btn_reservar = wx.Button(panel, label="Reservar")
        self.btn_comprar = wx.Button(panel, label="Comprar")
        vbox.Add(self.btn_reservar, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.btn_comprar, 0, wx.ALL | wx.EXPAND, 5)

        self.resultado = wx.StaticText(panel, label="", style=wx.ST_ELLIPSIZE_END)
        vbox.Add(self.resultado, 0, wx.ALL, 10)

        panel.SetSizer(vbox)

        # Eventos
        self.qtd_choice.Bind(wx.EVT_CHOICE, self.on_qtd_choice)
        self.qtd_text.Bind(wx.EVT_TEXT_ENTER, self.on_qtd_text_enter)
        self.qtd_text.Bind(wx.EVT_TEXT, self.on_total_changed)
        self.tipo_choice.Bind(wx.EVT_CHOICE, self.on_tipo_choice)
        self.int_text.Bind(wx.EVT_TEXT, self.on_total_changed)
        self.btn_reservar.Bind(wx.EVT_BUTTON, self.on_reservar)
        self.btn_comprar.Bind(wx.EVT_BUTTON, self.on_comprar)

    def make_on_sabor_check(self, qtd_ctrl):
        def on_check(event):
            qtd_ctrl.Enable(event.IsChecked())
            if event.IsChecked():
                qtd_ctrl.SetValue(1)
            else:
                qtd_ctrl.SetValue(0)
        return on_check

    def on_qtd_choice(self, event):
        escolha = self.qtd_choice.GetStringSelection()
        if escolha == "Outro":
            self.qtd_text.Show()
            self.qtd_text.SetFocus()
        else:
            self.qtd_text.Hide()
            self.tipo_choice.Enable(True)
            self.tipo_choice.SetSelection(0)
            self.personalizado_box.ShowItems(False)
            self.Layout()

    def on_qtd_text_enter(self, event):
        self.tipo_choice.Enable(True)
        self.tipo_choice.SetSelection(0)
        self.personalizado_box.ShowItems(False)
        self.Layout()

    def on_tipo_choice(self, event):
        if self.tipo_choice.GetStringSelection() == "Personalizado":
            self.personalizado_box.ShowItems(True)
        else:
            self.personalizado_box.ShowItems(False)
        self.Layout()

    def on_total_changed(self, event):
        if self.tipo_choice.GetStringSelection() != "Personalizado":
            return
        try:
            total = self.get_quantidade()
            inteiras = int(self.int_text.GetValue())
            if inteiras < 0:
                inteiras = 0
            if inteiras > total:
                inteiras = total
            meias = total - inteiras
            if meias < 0:
                meias = 0
            self.meia_text.SetValue(str(meias))
        except ValueError:
            self.meia_text.SetValue("0")

    def get_quantidade(self):
        escolha = self.qtd_choice.GetStringSelection()
        if escolha == "Outro":
            try:
                qtd = int(self.qtd_text.GetValue())
                if qtd < 1:
                    return 1
                return qtd
            except ValueError:
                return 1
        else:
            return int(escolha)

    def get_tipo_ingressos(self):
        qtd = self.get_quantidade()
        tipo = self.tipo_choice.GetStringSelection()
        if tipo == "Todos Inteira":
            return qtd, 0
        elif tipo == "Todos Meia":
            return 0, qtd
        elif tipo == "Personalizado":
            try:
                inteiras = int(self.int_text.GetValue())
                if inteiras < 0:
                    inteiras = 0
                if inteiras > qtd:
                    inteiras = qtd
                meias = qtd - inteiras
                if meias < 0:
                    meias = 0
                return inteiras, meias
            except ValueError:
                return qtd, 0
        return qtd, 0

    def get_produtos(self):
        produtos_selecionados = []
        for prod, sabor_checks, sabor_qtds in zip(self.produtos, self.produto_sabor_checks, self.produto_sabor_qtds):
            for check, qtd_ctrl, sabor in zip(sabor_checks, sabor_qtds, prod.opcoes):
                if check.IsChecked():
                    qtd = qtd_ctrl.GetValue()
                    if qtd > 0:
                        produtos_selecionados.append((prod, sabor, qtd))
        return produtos_selecionados

    def on_reservar(self, event):
        self.exibir_resultado(reserva=True)

    def on_comprar(self, event):
        self.exibir_resultado(reserva=False)

    def exibir_resultado(self, reserva):
        qtd = self.get_quantidade()
        inteiras, meias = self.get_tipo_ingressos()
        produtos = self.get_produtos()
        total = inteiras * self.ingressos[0].preco + meias * self.ingressos[1].preco
        produtos_str = []
        for prod, sabor, qtd_prod in produtos:
            total += qtd_prod * prod.preco
            produtos_str.append(f"{qtd_prod}x {prod.nome} ({sabor})")
        msg = (
            f"{'Reserva feita' if reserva else 'Compra realizada'}!\n"
            f"Ingressos: {inteiras} Inteira(s), {meias} Meia(s)\n"
            f"Produtos: {', '.join(produtos_str) if produtos_str else 'Nenhum'}\n"
            f"Total: R$ {total:.2f}"
        )
        self.resultado.SetLabel(msg)
        self.resultado.SetFocus()
        wx.CallAfter(self.resultado.SetFocus)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MudancasPersonalizadasFrame(None, "Sistema de Bilhetagem - Personalizado")
    frame.Show()
    app.MainLoop()
