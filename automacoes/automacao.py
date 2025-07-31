import pyautogui # biblioteca para automação de tarefas 
import pandas # biblioteca para ajudar a obter os arquivos na mesma pasta, ler o csv, aplica as fórmulas que tem no excel
# a biblioteca pandas ajuda a ler dados de qualquer lugar como sites, blogs, arquivos com fontes diferentes, banco de dados, etc. 
import time # biblioteca que acompanha a pyautogui para automação, mas essa ajuda no tempo dos comandos 

pyautogui.PAUSE = 0.6
pyautogui.press('win') # o comando press vai pressionar a tecla que for digitada, no caso windows
pyautogui.write('chrome') # o comando write vai escrever onde tiver uma caixa de texto a palavra desejada
pyautogui.press('enter')
time.sleep(1) # comando que faz pausar por segundos determinados
pyautogui.click(x=518, y=409) # entrando no meu perfil no chrome 
pyautogui.click(x=298, y=19) # abrindo uma nova aba no chrome 
pyautogui.write('https://aula01.simplificapython.com.br') # digitando a url do site para iniciar os cadastros
pyautogui.press('enter')
time.sleep(1)
pyautogui.click(x=860, y=466) # posição para logar no site 
pyautogui.write('admin') # login do site 
pyautogui.press('tab')
pyautogui.write('simplificapython') # senha do site  
pyautogui.press('tab')
pyautogui.press('enter')
 
tabela = pandas.read_csv('alunos.csv') # responsável por ler o arquivo alunos.csv
# df = pd.read_excel("arquivo.xlsx") para ler arquivos xlsx
# df = pd.read_excel("arquivo.xls") para ler arquivos xls
# df = pd.read_json('arquivo.json')
# para ler banco de dados é necessário bibliotecas para cada tipo e passos específicos 
# from openpyxl import load_workbook
# wb = load_workbook('seuarquivo.xlsm')


for linha in tabela.index: # loop para preencher o cadastro de cada pessoa no alunos.csv
    pyautogui.click(x=507, y=346) # posição do site para início do cadastro

    nome = tabela.loc[linha, 'Nome'] # localiza a variável nome com o .loc, pegando as variáveis da pasta alunos.csv e armazenando
    # em variáveis
    pyautogui.write(nome)
    pyautogui.press('tab')
    email = tabela.loc[linha, 'Email']
    pyautogui.write(email)
    pyautogui.press('tab')
    endereco = tabela.loc[linha, 'Endereco']
    pyautogui.write(endereco)
    pyautogui.press('tab')
    telefone = tabela.loc[linha, 'Telefone']
    pyautogui.write(telefone)
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.scroll(5000)