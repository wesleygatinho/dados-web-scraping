from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import sys

#Configuração do WebDriver
driver_path = "./chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(driver_path), options=options)

try:
    #Acessar o site
    url = "https://sigaa.ufma.br/sigaa/public/curso/concluidos_curso.jsf?lc=false&id=17150698"
    driver.get(url)

    #Clicando no botão de busca no site
    wait = WebDriverWait(driver, 20)
    search_button = wait.until(EC.element_to_be_clickable((By.ID, "form:buscarTurmas")))
    search_button.click()

    # Aguardando a tela carregar
    time.sleep(5)

    # Localizar a tabela de alunos concluídos
    table = driver.find_element(By.CLASS_NAME, "table_lt")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Extrair dados da tabela
    data = []
    for i in range(1, len(rows) - 1):
        row = rows[i]
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) >= 2:
            matricula = cols[0].text.strip()
            aluno = cols[1].text.strip()
            
        
    
        
        # Adicionando dados à lista
            data.append([matricula, aluno])

   
    df = pd.DataFrame(data, columns=["Matrícula", "Aluno"])

    
    sys.stdout.reconfigure(encoding='utf-8')

    
    print(df.to_string(index=False))

    # Salvar como arquivo Excel (formato xlsx)
    df.to_excel("alunos_concluidos_amb_2018.xlsx", index=False, engine='openpyxl')


finally:
    # Fechar o navegador
    driver.quit()
