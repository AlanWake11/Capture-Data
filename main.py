from PySimpleGUI import popup

from apresentacao.tela import Programa
from os import system

def main():
    Programa(True)

if __name__ == '__main__':
    try:
        system('cls')
        main()
    except ImportError as e:
        popup(e)
    except Exception as e:
        popup(e)