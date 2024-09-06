import PySimpleGUI as sg
import pyautogui
import io, os, threading, pytesseract
from PIL import ImageGrab, Image
from time import sleep
from winotify import Notification, audio

# Função para caso nao exista o diretório "imagens", crie o dirotório
def criar_diretorio_imagem(pasta):
    if os.path.exists(pasta):
        pass
    else:
        os.mkdir(pasta)
        
        notificacao = Notification(app_id='App', title='OCR Program', msg=f'Pasta {pasta} criada com sucesso!', )
        notificacao.set_audio(audio.Reminder, loop=False)
        notificacao.show()

# Função para retornar a quantidade de imagens dentro do diretório "imagens"
def tamanho_diretorio(pasta):
    try:
        lista_imagens = [imagem for imagem in os.listdir(pasta) if imagem.endswith('.png', '.jpeg', '.jpg', '.bmp')]
        
        return len(lista_imagens)
    
    except Exception as e:
        sg.popup(e)

# Função para verificar as imagens dentro da pasta "imagens"
def verificar_diretorio(pasta, janela):
    while True:
        try:
            sleep(1)

            arquivos_imagens = [os.path.join(pasta, arquivo) for arquivo in os.listdir(pasta) if arquivo.endswith(('.png', '.jpeg', '.jpg', '.bmp'))]
            
            for imagem in arquivos_imagens:
                extrair_texto(imagem, janela)
            
        except FileNotFoundError as e:
            sg.popup(e)
            break

        except Exception as e:
            sg.popup(e, 'verificar diretorio')
            break


def encontrar_e_subtrair(imagem_referencia_path, pasta):
    try:
        sleep(1)
        
        imagem_referencia = pyautogui.locateOnScreen(imagem_referencia_path, confidence=0.5)

        if imagem_referencia:
            x,y,width,height = imagem_referencia
            imagem_capturada = pyautogui.screenshot(region=(x,y,width,height))
            imagem_capturada.save('imagem_capturada.png')

            for arquivo in os.listdir(pasta):
                if arquivo.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    caminho_imagem = os.path.join(pasta, arquivo)
                    os.remove(caminho_imagem)
                    imagem_capturada.save(caminho_imagem)
                    print(f'Imagem substituida {caminho_imagem}')
        else:
            print('Imagem de refencia não encontrada')            

    except FileNotFoundError as e:
        sg.popup(e, 'Função encontrar e substituir')


            
# Função para extrair o texto da imagem utilizando OCR, mandando o texto para a caixa de texto da tela principal
def extrair_texto(imagem, janela):
    try:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Exemplo para Windows
        
        img = Image.open(imagem)
        janela.write_event_value(f'-UPDATE-',pytesseract.image_to_string(img))
                
    except Exception as e:
        sg.popup(e, 'Extrair Texto')

# Função para tirar um print do que está atrás da janela, e convertendo a imagem para um formato compatível com PySimpleGui
def tirar_print(janela):
    try:
        x, y = janela.CurrentLocation()
        
        largura, altura = janela.size
        
        janela.hide()
        sleep(0.5)
        img = ImageGrab.grab(bbox=(x, y, x + largura, y + altura))
        janela.un_hide()

        # Converter a imagem para um formato compatível com PySimpleGUI
        bio = io.BytesIO()
        img.save(bio, format='PNG')

        return img, bio 
    
    except Exception as e:
        sg.popup(e)
        
# Função para salvar a imagem dentro da pasta "imagens" 
def salvarImagem1(imagem):
    try:
        caminho = r'.\imagens'
        
        num = tamanho_diretorio(caminho)
        num += 1

        if not os.path.exists(caminho):
            os.makedirs(caminho)
        
        caminho_completo = os.path.join(caminho, f'imagem{num}.png')
        imagem.save(caminho_completo)
        
    except Exception as e:
        sg.popup(e)


def salvarImagem2(caminho_imagem):
    try:
        caminho = caminho_imagem

        if not os.path.exists(caminho):
            os.makedirs(caminho)

    except Exception as e:
        sg.popup(e)

# Função para quando o usuario fechar o software, arquivos dentro da pasta "imagens" serão deletadas
def remover_imagens(pasta):
    try:
        for arquivo in os.listdir(pasta):
            caminho_completo = os.path.join(pasta, arquivo)
            os.remove(caminho_completo)
    
    except Exception as e:
        sg.popup(e)
