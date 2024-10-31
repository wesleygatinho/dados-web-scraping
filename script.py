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
    url = "https://sigaa.ufma.br/sigaa/public/curso/monografias_curso.jsf?lc=pt_BR&lc=pt_BR&id=10816685"
    driver.get(url)

    #Clicando no botão de busca no site
    wait = WebDriverWait(driver, 20)
    search_button = wait.until(EC.element_to_be_clickable((By.ID, "form:buscar")))
    search_button.click()

    # Aguardando a tela carregar
    time.sleep(5)

    # Localizar a tabela de alunos concluídos
    table = driver.find_element(By.CLASS_NAME, "table_lt")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Extrair dados da tabela
    data = []
    for i in range(1, len(rows) - 1):  # Ignorar cabeçalho e última linha
        row = rows[i]
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) >= 5:  # Linha padrão com informações principais
            ano = cols[0].text.strip()
            date = cols[1].text.strip()
            aluno = cols[2].text.strip()
            orientador = cols[3].text.strip()
            curso = cols[4].text.strip()
        
        # Verifica se a próxima linha contém o título
            next_row = rows[i + 1]
            next_cols = next_row.find_elements(By.TAG_NAME, "td")
        
        # Verificar se o <td> possui "colspan" e contém o texto "Título:"
            titulo = ""
            if len(next_cols) == 1 and "Título:" in next_cols[0].text:
                titulo = next_cols[0].text.split("Título:")[1].strip()
        
        # Adicionando dados à lista
            data.append([ano, date, aluno, orientador, curso, titulo])

    # Converter para DataFrame
    df = pd.DataFrame(data, columns=["Ano", "Data", "Aluno", "Orientador", "Curso", "Titulo"])

    # Exibe os dados no console de forma tabulada
    print(df.to_string(index=False))

    # Salvar como CSV 
    df.to_csv("alunos_concluidos.csv", index=False, sep="\t")

finally:
    # Fechar o navegador
    driver.quit()
