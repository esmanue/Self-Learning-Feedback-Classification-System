# %%
import pandas as pd
import random
import nltk
from nltk.corpus import wordnet
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# %%
# NLTK kaynaklarını indir
nltk.download('wordnet')

# Augmentation: Synonym Replacement
def synonym_replacement(sentence, n=1):
    words = sentence.split()
    new_words = words.copy()
    random_word_list = list(set([word for word in words if wordnet.synsets(word)]))
    random.shuffle(random_word_list)
    
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = wordnet.synsets(random_word)
        if not synonyms:
            continue
        synonym_words = set()
        for syn in synonyms:
            for lemma in syn.lemmas():
                synonym_words.add(lemma.name())
        synonym_words.discard(random_word)
        if synonym_words:
            synonym = random.choice(list(synonym_words))
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break

    return ' '.join(new_words)

# %%
# Veri yükleme (TEMİZLEME YOK)
df = pd.read_csv("amazon.csv")

# Augmentasyon uygulayalım
augmented_texts = []
augmented_labels = []

for text, label in zip(df['Text'], df['label']):
    augmented_texts.append(text)
    augmented_labels.append(label)
    
    augmented_sentence = synonym_replacement(text, n=2)
    augmented_texts.append(augmented_sentence)
    augmented_labels.append(label)

aug_df = pd.DataFrame({'text': augmented_texts, 'label': augmented_labels})
print(aug_df.head())

# Eğitim ve test bölme
X_train, X_test, y_train, y_test = train_test_split(aug_df['text'], aug_df['label'], test_size=0.2, random_state=42)

# TF-IDF vektörleştirme (ngram ile)
vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# GridSearch için parametreler
param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear']
}

grid = GridSearchCV(SVC(), param_grid, cv=3, scoring='accuracy', verbose=2)
grid.fit(X_train_vec, y_train)

# En iyi parametreleri göster
print("En iyi parametreler:", grid.best_params_)
print("En iyi doğruluk (cross-validation):", grid.best_score_)

# Test seti üzerinde değerlendirme
y_pred = grid.predict(X_test_vec)
test_accuracy = accuracy_score(y_test, y_pred)
print("Test seti doğruluğu:", test_accuracy)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
