import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuracion
URL_PRODUCTO = 'https://www.pcfactory.cl/producto/52424-logitech-teclado-gamer-inalambrico-pro-x-tkl-lightspeed-rgb-mecanico--negro?origin=PCF'
# Usamos la clase que encontraste en la inspeccion
CLASE_PRECIO = "detail__prices__cash" 

def rastrear_precio_selenium():
    print(f"Iniciando navegador para: {URL_PRODUCTO}")
    
    # Configuracion del navegador
    options = Options()
    # options.add_argument("--headless") # Descomentar esto despues para que no abra la ventana
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Inicializar Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(URL_PRODUCTO)
        
        # Espera explicita: Le decimos al script "Espera hasta 10 segundos a que aparezca el precio"
        # Esto es crucial porque PC Factory carga lento
        elemento_precio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, CLASE_PRECIO))
        )
        
        # Si llegamos aqui, encontro el elemento
        texto_precio = elemento_precio.text
        
        # Limpieza ($199.990 -> 199990)
        precio_limpio = int(texto_precio.replace('$', '').replace('.', '').replace('CLP', '').strip())
        
        print(f"EXITO - Precio detectado: {precio_limpio}")
        
        # Guardar datos
        nuevo_dato = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tienda": "PC Factory",
            "precio": precio_limpio,
            "url": URL_PRODUCTO
        }
        
        df = pd.DataFrame([nuevo_dato])
        escribir_header = not pd.io.common.file_exists("precios.csv")
        df.to_csv("precios.csv", mode='a', header=escribir_header, index=False)
        print("Datos guardados en CSV.")

    except Exception as e:
        print(f"Error durante la ejecucion: {e}")
        # Tip de depuracion: Si falla, toma un screenshot para ver que vio el bot
        driver.save_screenshot("debug_error.png")
        print("Se guardo una captura de pantalla del error como debug_error.png")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    rastrear_precio_selenium()