from rest_framework.views import APIView
from rest_framework.response import Response
import pickle
import os
from .utils import clean_data
import pandas as pd
import re

model = pickle.load(open("classifier.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


def predictions(text):
    cleaned = clean_data(text)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]
    return prediction

class PredictOverview(APIView):
    def post(self, request):
        text = request.data.get("text")
        prediction = predictions(text)
        return Response({"prediction": int(prediction)})

class CorrectLabel(APIView):
    def post(self, request):
        text = request.data.get("text")
        label = int(request.data.get("label"))
        prediction = predictions(text)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(BASE_DIR, 'predict', 'amazon.csv')
        compare_path = os.path.join(BASE_DIR, 'predict', 'compare.csv')

        df = pd.read_csv(csv_path, names=["Text", "label"])

        text = re.sub(r'\s+', ' ', text).strip() #ortada bırakılan bosluklar icin stripe re ekledim.
        if text in df["Text"].values: #textin içinde arama yapıyor
            return Response({'message': 'Bu kayıt zaten mevcut.'} )
        
        else:
            with open(csv_path, "a", encoding="utf-8") as f:
                f.write(f'"{text}",{label}\n')

            if prediction != label:
             with open(compare_path, "a", encoding="utf-8") as f:
                f.write(f'"{text}","{prediction}","{label}"\n')

        return Response({'message': 'Feedback kaydedildi.'})
