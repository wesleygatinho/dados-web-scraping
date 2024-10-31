from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

#Configuração do WebDriver
driver_path = "./chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(driver_path), options=options)

try:
    #Acessar o site
    url = "https://sigaa.ufma.br/sigaa/public/curso/alunos_curso.jsf?lc=pt_BR&id=10816685"
    driver.get(url)

    time.sleep(5)
    # Localizar a tabela de alunos concluídos
    table = driver.find_element(By.CLASS_NAME, "table_lt")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Extrair dados da tabela
    data = []
    for i in range(1, len(rows) - 1):  # Ignorar cabeçalho e última linha
        row = rows[i]
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) >= 2:  # Linha padrão com informações principais
            matricula = cols[0].text.strip()
            aluno = cols[1].text.strip()        
        
        
        # Adicionando dados à lista
            data.append([matricula, aluno])

    # Converter para DataFrame
    df = pd.DataFrame(data, columns=["Matrícula", "Aluno"])

    # Exibe os dados no console de forma tabulada
    print(df.to_string(index=False))

    # Salvar como CSV 
    df.to_excel("alunos_ativos_bict.xlsx", index=False)

finally:
    # Fechar o navegador
    driver.quit()