import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import re
from unidecode import unidecode

# Carregar o arquivo com títulos
file_path = 'C:/Users/User/Documents/dados-web-scraping/bict/alunos_concluidos_bict_2013_2024.xlsx'
df = pd.read_excel(file_path)

# Função para limpar e padronizar os títulos
def preprocess_text(text):
    text = unidecode(text)  # Remove acentuação
    text = re.sub(r'\W+', ' ', text)  # Remove caracteres especiais
    text = text.lower().strip()  # Converte para minúsculas e remove espaços desnecessários
    return text

# Aplicar pré-processamento aos títulos
df['Título'] = df['Título'].dropna().apply(preprocess_text)

# Stopwords em português (convertidas para lista)
portuguese_stopwords = list([
    "de", "da", "do", "para", "com", "em", "uma", "um", "por", "sobre", 
    "como", "que", "na", "no", "das", "dos", "as", "os", "e", "ou", "a", "o", "uso", "ma", "sao", "luis", "ufma", "estudo", "centro",
])

# Transformação com TF-IDF, incluindo bigramas e trigramas
vectorizer = TfidfVectorizer(stop_words=portuguese_stopwords, ngram_range=(1, 3), max_df=0.85)
X = vectorizer.fit_transform(df['Título'])

# Aplicação do clustering K-Means com 5 clusters
kmeans_5_clusters = KMeans(n_clusters=5, random_state=42)
kmeans_5_clusters.fit(X)

# Adiciona os clusters ao DataFrame original
df_clusters = df[['Título']].copy()
df_clusters['Cluster'] = kmeans_5_clusters.labels_

# Mapeamento dos 5 clusters para as engenharias especificadas
cluster_to_engineering_5 = {
    0: "Engenharia de Computação",
    1: "Engenharia Civil",
    2: "Engenharia Aeroespacial",
    3: "Engenharia Ambiental",
    4: "Engenharia Civil"  # Ajuste conforme necessário
}
df_clusters['Engenharia'] = df_clusters['Cluster'].map(cluster_to_engineering_5)

# Palavras mais representativas em cada cluster para análise
top_n_words = 10
terms = np.array(vectorizer.get_feature_names_out())
top_words_per_cluster_5 = {}

for cluster_num in range(5):
    centroid = kmeans_5_clusters.cluster_centers_[cluster_num]
    top_term_indices = centroid.argsort()[-top_n_words:][::-1]
    top_words = terms[top_term_indices]
    top_words_per_cluster_5[cluster_num] = top_words.tolist()

# Exibir as palavras principais por cluster
for cluster, words in top_words_per_cluster_5.items():
    print(f"Cluster {cluster} ({cluster_to_engineering_5[cluster]}): {', '.join(words)}")

# Salvar o resultado em um arquivo Excel
output_path_5_clusters = 'titulos_classificados_5_clusters.xlsx'
df_clusters.to_excel(output_path_5_clusters, index=False)

print(f"Arquivo salvo em: {output_path_5_clusters}")
