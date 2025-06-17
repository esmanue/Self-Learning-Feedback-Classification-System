from rest_framework.views import APIView
from rest_framework.response import Response
import pickle
from .utils import clean_data
import os

model = pickle.load(open("classifier.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


class PredictOverview(APIView):
    def post(self, request):
        text = request.data.get("text")
        cleaned = clean_data(text)
        vectorized = vectorizer.transform([cleaned])
        prediction = model.predict(vectorized)[0]
        label = "Positive" if prediction == 1 else "Negative"
        return Response({"prediction": label})

class CorrectLabel(APIView):
    def post(self,request):
        text = request.data.get("text")
        feedbackuser =request.data.get("feedbackuser")

        if feedbackuser=="Positive":
            label=1
        else:
            label=0

        with open("amazon.csv", "a", encoding="utf-8") as f:
            f.write(f'"{text}",{label}\n')
        
        return Response({"text": text,"label":label})
