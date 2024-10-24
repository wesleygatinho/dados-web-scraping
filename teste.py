from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configuração do WebDriver (atualize o caminho do chromedriver)
driver_path = "./chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(driver_path), options=options)

try:
    # Acessar o site
    url = "https://sigaa.ufma.br/sigaa/public/curso/monografias_curso.jsf?lc=pt_BR&lc=pt_BR&id=10816685"
    driver.get(url)

    # Clicar no botão de busca
    wait = WebDriverWait(driver, 20)
    search_button = wait.until(EC.element_to_be_clickable((By.ID, "form:buscar")))
    search_button.click()

    # Aguarde a tabela carregar
    time.sleep(5)

    # Localizar a tabela de alunos concluídos
    table = driver.find_element(By.CLASS_NAME, "table_lt")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Extrair dados da tabela
    data = []
    for row in rows[1:-1]:  # Ignorar cabeçalho e última linha
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 2:
            ano = cols[0].text.strip()
            date = cols[1].text.strip()
            aluno = cols[2].text.strip()
            orientador = cols[3].text.strip()
            curso = cols[4].text.strip()
            data.append([ano, date, aluno, orientador, curso])

    # Converter para DataFrame
    df = pd.DataFrame(data, columns=["Ano", "Data", "Aluno", "Orientador", "Curso"])

    # Exibir os dados no console de forma tabular
    print(df.to_string(index=False))

    # Salvar como CSV com vírgula como delimitador
    df.to_csv("alunos_concluidos.csv", index=False, sep="\t")  # Delimitador padrão é vírgula

finally:
    # Fechar o navegador
    driver.quit()
