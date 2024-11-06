# Web Scraping de Monografias da UFMA

Este projeto realiza a extração de dados de alunos ativos, alunos concluídos e monografias dos sites da Universidade Federal do Maranhão (UFMA) utilizando Selenium e Pandas.

## Descrição

O script acessa a página de alunos ativos, alunos concluídos e monografias concluídas das 6 engenharias da UFMA, clica no botão de busca e extrai os dados da tabela de alunos concluídos. Os dados são então convertidos para um DataFrame do Pandas e salvos em um arquivo XLSX.

## Requisitos

- Python 3.x

pip install{
        - Selenium
        - Pandas
        - ChromeDriver
        - openpyxl
}

## Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    ```
2. Instale as dependências:
    ```bash
    pip install selenium 
    pip install pandas
    pip install openpyxl
    ```
3. Baixe o ChromeDriver e atualize o caminho no script.

## Uso

1. Atualize o caminho do ChromeDriver no script:
    ```python
    driver_path = "./chromedriver.exe"
    ```
2. Execute o script:
    ```bash
    python script.py
    python engenharias.py
    python alunos-ativos.py
    ```
3. O script irá acessar o site, clicar no botão de busca e extrair os dados da tabela com os dados dos alunos. Os dados serão exibidos no console e salvos em um arquivo Excel com o nome desejado.