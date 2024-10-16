import requests
import warnings
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

def cargar_urls(archivo):
    """ Cargar URLs desde un archivo de texto y devolverlas en una lista """
    try:
        with open(archivo, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]  # Elimina líneas vacías
        return urls
    except FileNotFoundError:
        print(Colors.red, Center.XCenter("El archivo {archivo} no fue encontrado."))
        return []

def main():

    os.system("cls")
    os.system(f"title Views Bot -  Viewer Bot @marto-nieto-g16 ")

    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""           

            ██╗░░░██╗██╗███████╗░██╗░░░░░░░██╗ ██████╗░░█████╗░████████╗
            ██║░░░██║██║██╔════╝░██║░░██╗░░██║ ██╔══██╗██╔══██╗╚══██╔══╝
            ╚██╗░██╔╝██║█████╗░░░╚██╗████╗██╔╝ ██████╦╝██║░░██║░░░██║░░░
            ░╚████╔╝░██║██╔══╝░░░░████╔═████║░ ██╔══██╗██║░░██║░░░██║░░░
            ░░╚██╔╝░░██║███████╗░░╚██╔╝░╚██╔╝░ ██████╦╝╚█████╔╝░░░██║░░░
            ░░░╚═╝░░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░░ ╚═════╝░░╚════╝░░░░╚═╝░░░                                             
                             
                             Github  github.com/kichi779    """)))
    
    print("")
    
    # Cargar las URLs desde un archivo de texto
    urls = cargar_urls('urls.txt')
    
    if not urls:
        print(Colors.red, Center.XCenter("No se encontraron URLs para cargar."))
        return

    proxy_servers = ['https://www.blockaway.net', 'https://www.croxyproxy.com', 'https://www.croxyproxy.rocks', 
                     'https://www.croxy.network', 'https://www.croxy.org', 'https://www.youtubeunblocked.live', 
                     'https://www.croxyproxy.net']
    
    def selectRandom(lista):
        """ Selecciona un elemento aleatorio de una lista """
        return random.choice(lista)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(Colors.red, Center.XCenter(f"Error al iniciar el navegador: {str(e)}"))
        return  # Si el navegador no se inicia, termina el programa

    def abrir_pestanas_y_buscar(driver, proxy_count, urls):
        for i in range(proxy_count):
            try:
                random_proxy_url = selectRandom(proxy_servers)  # Seleccionar proxy aleatorio
                driver.execute_script("window.open('" + random_proxy_url + "')")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(random_proxy_url)
                
                # Seleccionar una URL aleatoria del archivo de texto
                random_url = selectRandom(urls)

                # Intentar encontrar la caja de texto e ingresar la URL
                try:
                    text_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'url'))
                    )
                    text_box.send_keys(random_url)
                    text_box.send_keys(Keys.RETURN)
                except Exception as e:
                    print(Colors.red, Center.XCenter((f"Error al encontrar la caja de texto o enviar la URL: {str(e)}")))
                
                time.sleep(30)  # Esperar un poco antes de abrir la siguiente pestaña
            except Exception as e:
                print(Colors.red, Center.XCenter((f"Error al abrir una pestaña o realizar la búsqueda: {str(e)}")))

    def cerrar_todas_menos_una(driver):
        try:
            # Mantén la pestaña principal (primer handle)
            handles = driver.window_handles
            for handle in handles[1:]:
                driver.switch_to.window(handle)
                driver.close()
            driver.switch_to.window(handles[0])  # Vuelve a la pestaña principal
        except Exception as e:
            print((Colors.red, Center.XCenter(f"Error al cerrar pestañas: {str(e)}")))

    while True:
        try:
            proxy_count = random.choice([1, 2, 3, 4, 5])
            abrir_pestanas_y_buscar(driver, proxy_count, urls)
            
            # Espera antes de cerrar pestañas
            time.sleep(10)

            # Cerrar todas las pestañas excepto la primera
            cerrar_todas_menos_una(driver)
            time.sleep(5)  # Espera antes de repetir el ciclo
        except KeyboardInterrupt:
            print(Colors.green, Center.XCenter(f"El proceso fue interrumpido por el usuario."))
            break  # Rompe el ciclo cuando el usuario presiona Ctrl+C
        except Exception as e:
            print(Colors.red, Center.XCenter((f"Error en el ciclo principal: {str(e)}")))
            break

    
    driver.quit()

if __name__ == '__main__':
    main()
