import pandas as pd

# Carregar dados dos alunos do BICT e das engenharias
df_bict = pd.read_excel("./bict/alunos_concluidos_bict_2019_2024.xlsx")
df_engenharias_ativos = pd.read_excel("./engenharias/alunos_ativos_engenharias.xlsx")
df_engenharias_concluidos = pd.read_excel("./engenharias/alunos_concluidos_engenharias.xlsx")

# Normalizar os nomes dos alunos para evitar discrepâncias
df_bict["Aluno"] = df_bict["Aluno"].str.strip().str.upper()
df_bict["Titulo"] = df_bict["Titulo"].str.strip().str.upper()
df_engenharias_ativos["Aluno"] = df_engenharias_ativos["Aluno"].str.strip().str.upper()
df_engenharias_concluidos["Aluno"] = df_engenharias_concluidos["Aluno"].str.strip().str.upper()

# Unir os DataFrames das engenharias (ativos e concluídos) em um só
df_engenharias = pd.concat([df_engenharias_ativos, df_engenharias_concluidos])

# Criar a coluna "Engenharia" no DataFrame do BICT e preencher como "Não migrou" por padrão
df_bict["Engenharia"] = "Não migrou"

# Atualizar a coluna "Engenharia" para indicar a migração com base nos dados das engenharias
df_bict["Engenharia"] = df_bict["Aluno"].map(
    lambda aluno: df_engenharias.loc[df_engenharias["Aluno"] == aluno, "Engenharia"].values[0]
    if aluno in df_engenharias["Aluno"].values else "Não migrou"
)

# Exibir ou salvar o DataFrame atualizado
print(df_bict)
df_bict.to_excel("alunos_bict_migracoes_coore.xlsx", index=False)
