from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

playlist = "https://open.spotify.com/playlist/"
username = ""
password = ""


#--- Chrome WebDriver Options
options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")

#--- download the file directly to the specified path without pop-up window
prefs = {"profile.default_content_settings.popups": 0,"download.default_directory": r"C:\Users\sasuk\Downloads", 
         "profile.default_content_setting_values.notifications" : 2,"directory_upgrade": True,
         "profile.default_content_setting_values.automatic_downloads": 1}
options.add_experimental_option("prefs", prefs)

#--- Launching a Browser Session    
driver = webdriver.Chrome(service=Service(r'C:\SeleniumDrivers\chromedriver.exe'), options=options)
driver.get('https://www.tunemymusic.com/es/transfer?mode=tidal#step1')
driver.set_page_load_timeout(10)
driver.implicitly_wait(10)

# Loggearse
wait = WebDriverWait(driver, 10)
driver.current_window_handle #--- store the window 
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/nav/button[2]'))).click()
driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div/div[3]/div/div/div/div/div[2]/input').send_keys(username)
driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div/div[3]/div/div/div/div/div[3]/input').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div/div/div/div/button').click()
driver.implicitly_wait(10) 

# Localizar el primer boton
driver.current_window_handle #--- store the current window handle
# Almacenar la ventana principal
main_window_handle = driver.current_window_handle
# Hacer clic en el botón que potencialmente abre la ventana emergente
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[5]/main/div/main/div[4]/button[1]'))).click()
# Obtener todas las ventanas abiertas (manejadores)
all_window_handles = driver.window_handles
# Cambiar a la ventana emergente (asumiendo que es la nueva pestaña)
for window_handle in all_window_handles:
    if window_handle != main_window_handle:
        driver.switch_to.window(window_handle)

        # Cerrar la pestaña emergente
        driver.close()
        break

driver.switch_to.window(main_window_handle)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[5]/main/div/main/div[4]/button[1]'))).click()
driver.implicitly_wait(10) 

# Localiza el input usando el atributo 'placeholder' o cualquier otro atributo relevante.
input_field = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[5]/main/div/main/div[4]/div/div/div/form/input')
input_field.send_keys(playlist)
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[5]/main/div/main/div[4]/div/div/div/form/button').click()
driver.implicitly_wait(10)

# Localiza el elemento usando XPATH.
element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[5]/main/div/main/div[4]/div/div/div[1]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[2]/div[2]')
# Extrae el texto del elemento.
text = element.text

# Procesa el texto para obtener el número antes del "/".
playlist_lenght = int(text.split('/')[0].strip())
# Obtener el tiempo de espera esperado
time_threshold = playlist_lenght * 0.053 

time.sleep(20)
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[5]/main/div/main/div[4]/div/div/div[3]/div/button').click()
time.sleep(20)
time.sleep(time_threshold)
driver.close()
