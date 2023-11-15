from flask import Flask, render_template, request
import PySimpleGUI as sg
import requests

app = Flask(__name__)

def cotacoes():
    r = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")
    cotacao = r.json()
    dolar = cotacao["USDBRL"]["bid"] 
    euro = cotacao["EURBRL"]["bid"] 
    bit = cotacao["BTCBRL"]["bid"] 
    return dolar, euro, bit

def converter_moeda(valor, cotacao):
    return valor * cotacao

def abre_form(dolar, euro, bit, layout):

   valor_d_form = None
   valor_e_form = None
   valor_b_form = None
   
   # Abre a janela com o formulário de conversão
   window = sg.Window('Pick a color', layout, element_justification="center", size=(500, 500))

   def valor_dolar():
      valor = values["-VALOR-"]
      valor_d_form = float(valor.replace(',', '.'))
      dolar_form = float(dolar)
      conversao_dolar = valor_d_form/dolar_form
      window["saida"].update('{:.2f}'.format(conversao_dolar))

   def valor_euro():
      valor = values["-VALOR-"]
      valor_e_form = float(valor.replace(',', '.'))
      euro_form = float(euro)
      conversao_euro = valor_e_form/euro_form
      window["saida"].update('{:.2f}'.format(conversao_euro))

   def valor_bitcoin():
      valor = values["-VALOR-"]
      valor_b_form = float(valor.replace(',', '.'))
      bit_form = float(bit)
      conversao_bit = valor_b_form/bit_form
      window["saida"].update('{:.2f}'.format(conversao_bit))

   def limpar():
      valor = values["-VALOR-"]
      limpar = float(valor.replace(',', '.'))
      limpar_form = float(limpar)
      limpa_conversao = limpar_form*valor_d_form*valor_e_form*valor_b_form
      window["saida"].update('{:.2f}'.format(limpa_conversao)) 

   while True:
      event, values = window.read()
      if event == "Dólar":
         valor_dolar()
      elif event == "Euro":
         valor_euro()
      elif event == "Bitcon":
         valor_bitcoin()
      elif event == "limpar":
         limpar()
      elif event == sg.WIN_CLOSED or event == "Sair":
         break
   return 'Código executado com sucesso!'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        valor = float(request.form['valor'])
        moeda = request.form['moeda']
        dolar, euro, bit = cotacoes()

        if moeda == 'Dólar':
            resultado = converter_moeda(valor, float(dolar))
        elif moeda == 'Euro':
            resultado = converter_moeda(valor, float(euro))
        elif moeda == 'Bitcon':
            resultado = converter_moeda(valor, float(bit))
        else:
            resultado = 0

        return render_template('index.html', resultado=resultado)

    return render_template('index.html', resultado=None)

@app.route('/exec_conversor')
def exec_conversor():
   sg.theme("Dark Grey 13")
   sg.popup_non_blocking("Os valores apresentados podem variar de acordo com final de semana e fériados", title = "Aviso")
   dolar, euro, bit = cotacoes()

   layout = [  
   [sg.Text("Conversor de Moedas", font="Any 24")],
   [sg.Text("Informe o valor para o cambio", font="Any 24")],
   [sg.Text("")],
   [sg.Text("")],
   [sg.Text("")],
   [sg.Push(), sg.Text("Digite o Valor em Real R$", font="Any 14"), sg.Push(), sg.Input(font="Any 14", size=15, key="-VALOR-")],
   [sg.Text("")],
   [sg.Push(), sg.Text("Converter Para", font="Any 14"),sg.Push()],
   [sg.Text("")],
   [sg.Button('Dólar', font="Anya 14"), sg.Button('Euro', font="Anya 14"), sg.Button('Bitcon', font="Anya 14")],
   [sg.Text("")],
   [sg.Text("R$", font="Any 16"), sg.Input("", font="Any 14", key = "saida", size = 14, justification="center")],
   [sg.Button("Sair", font='Any 16')]	  		
]

   abre_form(dolar, euro, bit, layout)

if __name__ == '__main__':
    app.run(debug=True)
