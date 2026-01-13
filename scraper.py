import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import os

# --- CONFIGURACION MASIVA ---
# Ahora usamos una lista de diccionarios. Puedes agregar cuantos quieras.
PRODUCTOS = [
    {
        "nombre": "Teclado Logitech",
        "url": "https://www.pcfactory.cl/producto/52424-logitech-teclado-gamer-inalambrico-pro-x-tkl-lightspeed-rgb-mecanico--negro?origin=PCF"
    },
    {
        "nombre": "Cable USB-C a Lightning 2m Blanco Apple", 
        "url": "https://www.pcfactory.cl/producto/43220-apple-cable-usb-c-a-lightning-2m-blanco-apple?origin=PCF" 
    },

]

CLASE_PRECIO = "detail__prices__cash"

# --- CONFIGURACION DE LOGGING ---
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/scraper_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()  # También muestra en consola
    ]
) 

def rastrear_todos():
    logging.info(f"=== INICIANDO RASTREO DE {len(PRODUCTOS)} PRODUCTOS ===")
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Abrimos el navegador UNA sola vez para todo el proceso (mas eficiente)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    listado_datos = []

    try:
        for item in PRODUCTOS:
            logging.info(f"Revisando: {item['nombre']}")
            
            driver.get(item['url'])
            
            try:
                # Esperamos a que cargue el precio
                elemento = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, CLASE_PRECIO))
                )
                
                precio_texto = elemento.text
                precio_limpio = int(precio_texto.replace('$', '').replace('.', '').replace('CLP', '').strip())
                
                logging.info(f"Precio obtenido: ${precio_limpio:,}")
                
                listado_datos.append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "tienda": "PC Factory",
                    "producto": item['nombre'],
                    "precio": precio_limpio,
                    "url": item['url']
                })
                
                # Pausa humana de 2 segundos para no parecer robot loco
                time.sleep(2)
                
            except Exception as e:
                logging.error(f"Error con {item['nombre']}: {e}")

        # Guardar todo junto al final
        if listado_datos:
            df = pd.DataFrame(listado_datos)
            escribir_header = not pd.io.common.file_exists("precios.csv")
            df.to_csv("precios.csv", mode='a', header=escribir_header, index=False)
            logging.info(f"{len(listado_datos)} registros guardados en precios.csv")
        else:
            logging.warning("No se obtuvieron datos para guardar")

    except Exception as e:
        logging.error(f"Error general: {e}", exc_info=True)
    finally:
        driver.quit()
        logging.info("=== RASTREO FINALIZADO ===\n")

if __name__ == "__main__":
    rastrear_todos()