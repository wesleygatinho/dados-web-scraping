import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from nltk.tokenize import TreebankWordTokenizer

nltk.download('rslp')
nltk.download('punkt')
nltk.download('stopwords')

# Caminho do arquivo Excel
file_path = r'C:\Users\User\Downloads\alunos_bict_migracoes_apenas_2.xlsx'

# Lendo o arquivo Excel
df = pd.read_excel(file_path)

# Mapeando as engenharias
mapa_engenharias = {
    'ENGENHARIA CÍVIL': 1,
    'ENGENHARIA DA COMPUTAÇÃO': 2,
    'ENGENHARIA MECÂNICA': 3,
    'ENGENHARIA AEROESPACIAL': 4,
    'ENGENHARIA AMBIENTAL E SANITÁRIA': 5,
    'ENGENHARIA DE TRANSPORTES': 6,
    'Não migrou': 0
}
df['Engenharia'] = df['Engenharia'].map(mapa_engenharias)

# Salvando como CSV (opcional)
df.to_csv('planilha_mod_csv.csv', index=False)

# Lendo o CSV e extraindo os títulos
classificacoes = pd.read_csv('planilha_mod_csv.csv')
titulos = classificacoes['Título']

# Preparando stop words e stemmer
stop_words = set(stopwords.words('portuguese'))
stemmer = RSLPStemmer()
tokenizer = TreebankWordTokenizer()

# Processamento de texto: remoção de stop words e aplicação do stemmer
def preprocess_text(text):
    tokens = tokenizer.tokenize(text)
    filtered_tokens = [stemmer.stem(word) for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_tokens)

# Aplicando o pré-processamento em cada título
titulos_processados = [preprocess_text(titulo) for titulo in titulos]

# Exibindo as palavras transformadas (após remoção de stop words e stemming)
print("\nPalavras transformadas:")
for i, (original, transformado) in enumerate(zip(titulos[:5], titulos_processados[:5])):
    print(f"Titulo original {i + 1}: {original}")
    print(f"Titulo processado {i + 1}: {transformado}\n")

# Vetorização com TF-IDF
tfidf_vectorizer = TfidfVectorizer()
x = tfidf_vectorizer.fit_transform(titulos_processados)

# Exibindo o texto vetorizado com TF-IDF (primeiras 5 linhas)
print("\nTexto vetorizado com TF-IDF (primeiras 5 linhas):")
tfidf_array = x.toarray() 
tfidf_df = pd.DataFrame(tfidf_array, columns=tfidf_vectorizer.get_feature_names_out())
print(tfidf_df.head()) 

y = np.array(classificacoes['Engenharia'])

# Definindo variáveis de treino e validação
porcentagem_de_treino = 0.8
tamanho_de_treino = int(porcentagem_de_treino * len(y))
treino_dados = x[:tamanho_de_treino]
treino_marcacoes = y[:tamanho_de_treino]
validacao_dados = x[tamanho_de_treino:]
validacao_marcacoes = y[tamanho_de_treino:]

# Função para treinar e avaliar os modelos com StratifiedKFold
def predict(nome, modelo, treino_dados, treino_marcacoes):
    kfold = StratifiedKFold(n_splits=10)
    scores = cross_val_score(modelo, treino_dados, treino_marcacoes, cv=kfold)
    taxa_de_acerto = np.mean(scores)
    print(f"Taxa de acerto do {nome}: {taxa_de_acerto}")
    return taxa_de_acerto

# Testando diferentes classificadores
resultados = {}

# Modelo OneVsRest
modeloOneVsRest = OneVsRestClassifier(LinearSVC(random_state=0))
resultadoOneVsRest = predict("OneVsRest", modeloOneVsRest, treino_dados, treino_marcacoes)
resultados[resultadoOneVsRest] = modeloOneVsRest

# Modelo OneVsOne
modeloOneVsOne = OneVsOneClassifier(LinearSVC(random_state=0))
resultadoOneVsOne = predict("OneVsOne", modeloOneVsOne, treino_dados, treino_marcacoes)
resultados[resultadoOneVsOne] = modeloOneVsOne

# Modelo Multinomial Naive Bayes
modeloMultinomial = MultinomialNB()
resultadoMultinomial = predict("MultinomialNB", modeloMultinomial, treino_dados, treino_marcacoes)
resultados[resultadoMultinomial] = modeloMultinomial

# Modelo AdaBoost
modeloAdaBoost = AdaBoostClassifier(algorithm='SAMME')
resultadoAdaBoost = predict("AdaBoostClassifier", modeloAdaBoost, treino_dados, treino_marcacoes)
resultados[resultadoAdaBoost] = modeloAdaBoost

# Modelo Random Forest
modeloRandomForest = RandomForestClassifier(random_state=0)
resultadoRandomForest = predict("RandomForest", modeloRandomForest, treino_dados, treino_marcacoes)
resultados[resultadoRandomForest] = modeloRandomForest

# Modelo Gradient Boosting
modeloGradientBoosting = GradientBoostingClassifier(random_state=0)
resultadoGradientBoosting = predict("GradientBoosting", modeloGradientBoosting, treino_dados, treino_marcacoes)
resultados[resultadoGradientBoosting] = modeloGradientBoosting

# Modelo XGBoost
modeloXGBoost = XGBClassifier(eval_metric='mlogloss', random_state=0)
resultadoXGBoost = predict("XGBoost", modeloXGBoost, treino_dados, treino_marcacoes)
resultados[resultadoXGBoost] = modeloXGBoost

# Exibindo o modelo com melhor precisão
melhor_modelo = max(resultados)
print(f"\nMelhor modelo: {resultados[melhor_modelo]} com precisao de {melhor_modelo}")