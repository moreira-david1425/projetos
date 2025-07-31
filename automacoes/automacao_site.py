from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pyautogui

# Inicia o navegador Chrome
driver = webdriver.Chrome()
driver.get("https://precos-de-produtos.netlify.app/")
sleep(5)

# Rolar a página inteira para baixo para carregar os produtos
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(2)

# Clicar em "carregar mais" para vizualizar o restante dos produtos
botao_carregar_mais = driver.find_element(By.XPATH, "//button[@id='loadMoreButton']")
botao_carregar_mais.click()
sleep(2)

# Rolar a página totalmente para baixo
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(1)

# Subir totalmente de volta para o topo da página
driver.execute_script("window.scrollTo(0, 0);")
sleep(2)

# Clicar em Subir planilha de preços
botao_carregar_planilha_de_produtos = driver.find_element(By.XPATH, "//button[@class='btn btn-primary btn-custom']")
sleep(3)
botao_carregar_planilha_de_produtos.click()
sleep(3)
# Carregar a planilha "precos_produtos_atualizados.xlsx"
pyautogui.write(r'C:\Users\giras\Downloads\precos-produtos-atualizados.xlsx')
sleep(2)
pyautogui.press('enter')
input("Digite enter ")