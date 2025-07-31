import pyautogui
import time

time.sleep(5) # função que faz o sistema pausar por quantos segundos vc quiser
posicao = pyautogui.position() # função que fala as coordenadas x e y do mouse
print(posicao)