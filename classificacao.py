# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.cluster import KMeans
# import numpy as np
# import re
# from unidecode import unidecode
# import nltk
# from nltk.corpus import stopwords

# # Download de recursos do NLTK
# nltk.download('stopwords')

# # Carregar o arquivo com títulos e engenharia
# file_path = 'C:/Users/User/Documents/dados-web-scraping/bict/alunos_bict_migracoes_atualizado.xlsx'
# df = pd.read_excel(file_path)

# # Verificar se as colunas necessárias existem
# if 'Título' not in df.columns or 'Engenharia' not in df.columns:
#     raise ValueError("O arquivo deve conter as colunas 'Título' e 'Engenharia'.")

# # Função para limpar e padronizar os títulos
# def preprocess_text(text):
#     text = unidecode(text) 
#     text = re.sub(r'\W+', ' ', text)  
#     text = text.lower().strip()  
#     tokens = text.split() 
#     tokens = [word for word in tokens if word not in stopwords.words('portuguese')] 
#     return ' '.join(tokens)

# # Aplicar pré-processamento aos títulos
# df['Título'] = df['Título'].dropna().apply(preprocess_text)

# # Stopwords adicionais específicas
# additional_stopwords = [
#      "de", "da", "do", "para", "com", "em", "uma", "um", "por", "sobre", 
#     "como", "que", "na", "no", "das", "dos", "as", "os", "e", "ou", "a", "o", "uso", "ma", "sao", "luis", "ufma", "estudo", "centro", "caso", "custo", "baixo", "baseado", "viabilidade", "federal", "maranhao", "universidade", "campus", "analise", "sobre", "avaliacao", "gestao"
# ]

# # Transformação com TF-IDF, incluindo bigramas e trigramas
# vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese') + additional_stopwords, ngram_range=(1, 3), max_df=0.85)
# X = vectorizer.fit_transform(df['Título'])

# # Aplicação do clustering K-Means com número de clusters ajustado para refletir melhor a distribuição
# num_clusters = min(df['Engenharia'].nunique(), 10)  # Limite superior para evitar excesso de granularidade
# kmeans = KMeans(n_clusters=num_clusters, random_state=42)
# kmeans.fit(X)

# # Adiciona os clusters ao DataFrame original
# df_clusters = df[['Título', 'Engenharia']].copy()
# df_clusters['Cluster'] = kmeans.labels_

# # Palavras mais representativas em cada cluster para análise
# top_n_words = 10
# terms = np.array(vectorizer.get_feature_names_out())
# top_words_per_cluster = {}

# for cluster_num in range(num_clusters):
#     centroid = kmeans.cluster_centers_[cluster_num]
#     top_term_indices = centroid.argsort()[-top_n_words:][::-1]
#     top_words = terms[top_term_indices]
#     top_words_per_cluster[cluster_num] = top_words.tolist()

# # Exibir as palavras principais por cluster, associando com a engenharia
# cluster_to_engineering = df_clusters.groupby('Cluster')['Engenharia'].first().to_dict()

# distribuicao_titulos = df['Engenharia'].value_counts()

# for cluster, words in top_words_per_cluster.items():
#     engenharia = cluster_to_engineering.get(cluster, "Engenharia Desconhecida")
#     print(f"Cluster {cluster} ({engenharia}): {', '.join(words)}")

# # Exibir a distribuição de títulos por engenharia
# print("\nDistribuição de Títulos por Engenharia:")
# print(distribuicao_titulos)

# # Salvar o resultado em um arquivo Excel
# output_path = 'titulos_classificados_por_engenharia.xlsx'
# df_clusters.to_excel(output_path, index=False)

# print(f"Arquivo salvo em: {output_path}")

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import re
from unidecode import unidecode
import nltk
from nltk.corpus import stopwords

# Download de recursos do NLTK
nltk.download('stopwords')

# Carregar o arquivo com títulos e engenharia
file_path = 'C:/Users/User/Documents/dados-web-scraping/bict/alunos_bict_migracoes_atualizado.xlsx'
df = pd.read_excel(file_path)

# Verificar se as colunas necessárias existem
if 'Título' not in df.columns or 'Engenharia' not in df.columns:
    raise ValueError("O arquivo deve conter as colunas 'Título' e 'Engenharia'.")

# Função para limpar e padronizar os títulos
def preprocess_text(text):
    text = unidecode(text)  # Remove acentuação
    text = re.sub(r'\W+', ' ', text)  # Remove caracteres especiais
    text = text.lower().strip()  # Converte para minúsculas e remove espaços desnecessários
    tokens = text.split()  # Divide o texto em palavras de forma simples
    tokens = [word for word in tokens if word not in stopwords.words('portuguese')]  # Remove stopwords
    return ' '.join(tokens)

# Aplicar pré-processamento aos títulos
df['Título'] = df['Título'].dropna().apply(preprocess_text)

# Rebalancear os dados de entrada para igualar o número de títulos por engenharia
min_titulos = min(df['Engenharia'].value_counts())
df_balanced = pd.concat([df[df['Engenharia'] == eng].sample(min_titulos, random_state=42) for eng in df['Engenharia'].unique() if len(df[df['Engenharia'] == eng]) >= min_titulos])

# Stopwords adicionais específicas
additional_stopwords = [
    "uso", "ma", "sao", "luis", "ufma", "estudo", "centro",
]

# Transformação com TF-IDF, incluindo bigramas e trigramas com ponderação
vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese') + additional_stopwords, ngram_range=(1, 3), max_df=0.8, min_df=2)
X = vectorizer.fit_transform(df_balanced['Título'])

# Aplicação do clustering K-Means com número de clusters igual ao número de engenharias únicas
num_clusters = df_balanced['Engenharia'].nunique()
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Adiciona os clusters ao DataFrame original

df_clusters = df_balanced[['Título', 'Engenharia']].copy()
df_clusters['Cluster'] = kmeans.labels_

# Palavras mais representativas em cada cluster para análise
top_n_words = 10
terms = np.array(vectorizer.get_feature_names_out())
top_words_per_cluster = {}

for cluster_num in range(num_clusters):
    centroid = kmeans.cluster_centers_[cluster_num]
    top_term_indices = centroid.argsort()[-top_n_words:][::-1]
    top_words = terms[top_term_indices]
    top_words_per_cluster[cluster_num] = top_words.tolist()

# Exibir as palavras principais por cluster, associando com a engenharia
cluster_to_engineering = df_clusters.groupby('Cluster')['Engenharia'].first().to_dict()

distribuicao_titulos = df_balanced['Engenharia'].value_counts()

for cluster, words in top_words_per_cluster.items():
    engenharia = cluster_to_engineering.get(cluster, "Engenharia Desconhecida")
    print(f"Cluster {cluster} ({engenharia}): {', '.join(words)}")

# Exibir a distribuição de títulos por engenharia
print("\nDistribuição de Títulos por Engenharia (Amostrada):")
print(distribuicao_titulos)

# Salvar o resultado em um arquivo Excel
output_path = 'titulos_classificados_por_engenharia.xlsx'
df_clusters.to_excel(output_path, index=False)

print(f"Arquivo salvo em: {output_path}")
