# Self-Learning-Feedback-Classification-System

This project is a web-based application that classifies text using a machine learning model and allows users to send feedback when the prediction is incorrect. The aim is to create a system that improves over time through real user input.

---

## 🔧 Features

## 🔧 Features

- Text classification using a trained machine learning model
- Feedback mechanism to correct wrong predictions
- Backend with Django REST Framework  
  > ⚠️ Before running the backend or frontend, make sure to run the training script (e.g. `overview.py`) to generate the `classifier.pkl` and `vectorizer.pkl` files.
- Simple frontend built with React
- Cleaned and vectorized text using TF-IDF
- Feedback stored for future model updates


---

## 💻 Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: React (JavaScript)
- **Machine Learning**: scikit-learn, Pickle
- **Vectorizer**: TF-IDF
- **Text Cleaning**: Custom Python function (`clean_data`)
- **Database**: Django ORM (e.g. SQLite)

---

## 📡 API Endpoints

### 1. `POST /api/predict/`

Predicts the label of a given text.

**Request:**
```json
{
  "text": "This product is very good."
}
```

**Response:**
```json
{
  "prediction": 1
}
```

---

### 2. `POST /api/correct-label/`

Allows user to send the correct label if prediction is wrong.

**Request:**
```json
{
  "text": "This product is very good.",
  "label": 0
}
```

**Response:**
```json
{
  "message": "Feedback received."
}
```

---

## ⚙️ How It Works

1. User submits a text through the interface.
2. Text is cleaned and transformed using TF-IDF.
3. The model predicts a class label (e.g. 0 or 1).
4. If the prediction is wrong, user sends the correct label.
5. Feedback is saved to the database for review and future retraining.

---

## 📁 Project Structure

```
project/
│
├── predict/
│   ├── views.py           # API logic
│   ├── utils.py           # Text cleaning function
│   ├── classifier.pkl     # Trained ML model
│   └── vectorizer.pkl     # TF-IDF vectorizer
│
├── manage.py
├── settings.py
└── urls.py
```

---

## 🚀 How to Run

1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Django backend:
   ```
   python manage.py runserver
   ```
4. (Optional) Start the React frontend if needed.



