import PySimpleGUI as sg

from modelo.tarefas import *

class Programa:
    def __init__(self, tela):
        self.tela = tela

        pasta = r'.\imagens'


        criar_diretorio_imagem(pasta) # Criar diretório "imagens" caso não exista no projeto
        self.tela_principal() # Inicia a tela principal
            
        
        print('Programa encerrado')

    # Definindo as telas
    def tela_principal(self):
        menu = [
            ['Iniciar',['Criar', '---', 'Sair']],
            ['Ajuda']
        ]

        # Definindo as abas onde aparecerão os textos de cada imagem
        aba1_layout = [
            [sg.Text('Texto da imagem 1')],
            [sg.Multiline(size=(60,20), disabled=True, key='-OUTPUT1-')]
        ]
        
        aba2_layout = [
            [sg.Text('Texto da imagem 2')],
            [sg.Multiline(size=(60,20), disabled=True, key='-OUTPUT2-')]
        ]

        tab_group_layout = [
            [sg.Tab('Imagem 1', aba1_layout, key='-TAB1-'),
             sg.Tab('Imagem 2', aba2_layout, key='-TAB2-')]
        ]


        layout = [
            [sg.Menu(menu)],
            [sg.Text('Texto da imagem')],
            [sg.TabGroup(tab_group_layout)]
        ]

        janela = sg.Window('App', layout, element_justification='center', resizable=False)

        threading.Thread(target=verificar_diretorio, args=(r'.\imagens', janela), daemon=True).start()
        
        while True:
            evento, valor = janela.read()

            if evento in (sg.WIN_CLOSED, 'Sair'):
                janela.disable()

                resposta = sg.popup_yes_no('Tem certeza que quer fechar?')
                if resposta == 'Yes': 
                    break
                
            if evento == 'Criar':
                janela.disable()
                self.tela_criar_config()

            if evento == '-UPDATE-':
                janela['-OUTPUT1-'].update(valor['-UPDATE-'])
            
            janela.enable()
            janela.bring_to_front()
        
        janela.close()

    def tela_criar_config(self):
        opcoes = [1,2,3,4,5]

        layout = [
            [sg.Text('Quantas janelas capturar'),  sg.Combo(opcoes,size=(20,1), key='-NUMERO-', readonly=True, default_value=opcoes[0])],
            [sg.Radio('Selecionar imagem do computador', 'RADIOGROUP', key='-OPCAO1-', default=True)],
            [sg.Radio('Tirar print no programa', 'RADIOGROUP', key='-OPCAO2-')],
            [sg.Text('', expand_y=True)],

            [sg.Button('Ok'), sg.Button('Cancelar')]
        ]

        janela = sg.Window('Criar Janelas', layout, resizable=False)
        
        while True:
            evento, valor = janela.read()


            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                break
            
            if evento == 'Ok' and valor['-OPCAO1-']:
                janela.close()
                
                contador = 0

                while contador != valor['-NUMERO-']:
                    self.tela_escolher_imagem(contador)
                    repetir = True
                    contador += 1
                break

            elif evento == 'Ok' and valor['-OPCAO2-']:
                janelas = valor['-NUMERO-']
                
                janelas = int(janelas)
                contador = 0
                
                janela.close()
                
                repetir = True
                
                while contador != janelas and repetir:
                    self.tela_print(repetir)
                    contador +=1
        
        janela.close()

    def tela_escolher_imagem(self):
        layout = [
            [sg.Text('Selecione uma foto do seu computador')],
            [sg.Input(key='-FILE-', enable_events=True, disabled=True), sg.FileBrowse(file_types=(('Imagens','*.png;*.jpg;*.jpeg;*.bmp'),))],
            [sg.Text('', size=(0,0), expand_y=True)],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        janela = sg.Window('Escolha de imagem', layout, resizable=False, element_justification='center')

        while True:
            evento, valor = janela.read()

            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                break
            
            if evento == 'Confirmar' and valor['-FILE-'] != '':
                path_imagem = valor['-FILE-']
                salvarImagem2(path_imagem)
            
        janela.close()
        
    def tela_print(self, repetir):
        largura, altura = 360,240

        # Ajustar o tamanaho da janela de print para poder tirar um print mais precisa
        def mudar_tamanho_janela(evento, largura, altura):
            match evento:
                case '-AUMENTAR_LARGURA-':
                    return largura + 2, altura
                case '-DIMINUIR_LARGURA-':
                    return largura - 2, altura
                case '-AUMENTAR_ALTURA-':
                    return largura, altura + 2
                case '-DIMINUIR_ALTURA-':
                    return largura, altura - 2
  
          
        layout = [
            [sg.Text('Largura'), sg.Button('+', key='-AUMENTAR_LARGURA-', size=(3,1)), sg.Button('-', key='-DIMINUIR_LARGURA-', size=(3,1),)],
            [sg.Text('Altura'), sg.Button('+', key='-AUMENTAR_ALTURA-', size=(3,1)), sg.Button('-', key='-DIMINUIR_ALTURA-', size=(3,1))],
            [sg.Text('', size=(0,0), expand_y=True)],

            [sg.Button('Salvar posição'), sg.Button('Sair')]
        ]

        janela = sg.Window(f'Janela', layout, resizable= True, element_justification='center', size=(largura,altura), no_titlebar=True, grab_anywhere=True)

        while True:
            evento, valor = janela.read()

            if evento in (sg.WIN_CLOSED, 'Sair'):
                repetir = False
                break

            if evento == 'Salvar posição':
                imagem, bio = tirar_print(janela)
                self.tela_confirmar_print(imagem, bio)
                break
                
            # Ajustar a altura e a largura da janela de acordo com o usuario pressionar no botao - ou + 
            largura, altura = mudar_tamanho_janela(evento, largura, altura) 
            janela.size = (largura,altura)

        janela.close()
        
        # Encerra o looping de janelas
        if not repetir:
            return repetir        

    # Aqui o usuario vai confirmar se vai querer usar a print que acabou de tirar
    def tela_confirmar_print(self, imagem, bio):
        layout = [
            [sg.Image(key='-IMAGE-', data=(bio.getvalue()))],
            [sg.Button('Salvar'), sg.Button('Descartar')]
        ]

        janela = sg.Window('Confirmar', layout, resizable=True, element_justification='center')
        
        while True:
            evento, valor = janela.read()

            if evento in (sg.WIN_CLOSED,'Descartar'):
                break
            
            if evento == 'Salvar':
                try:
                    salvarImagem1(imagem)
                except Exception as e:
                    sg.popup(e, text_color='red')
                else:
                    sg.popup('Imagem salva com sucesso')
                    break
        
        janela.close()