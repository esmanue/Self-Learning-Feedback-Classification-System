from rest_framework.views import APIView
from rest_framework.response import Response
import pickle
from .utils import clean_data
import os

model = pickle.load(open("classifier.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predictions(text):
    cleaned=clean_data(text)
    vectorized = vectorizer.transform([cleaned])
    prediction=model.predict(vectorized)[0]
    return prediction   
    
class PredictOverview(APIView):
    def post(self, request):
        text = request.data.get("text")
        prediction=predictions(text)
        label = "Positive" if prediction == 1 else "Negative"
        return Response({"prediction": label})

class CorrectLabel(APIView):
    def post(self,request):
        text = request.data.get("text")
        feedbackuser =request.data.get("feedbackuser")
        prediction=predictions(text)

        if feedbackuser=="Positive":
            label=1
        else:
            label=0

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #abspathle kodun olduğu dosyanı dirname ile bir üst pathe cıkıyoruz
        csv_path = os.path.join(BASE_DIR, 'predict', 'amazon.csv') #bir üst pathdeki dosyanın yolunu alıyor

        with open(csv_path, "a", encoding="utf-8") as f:
            f.write(f'"{text}",{label}\n')
        
        with open("compare.csv","a",encoding="utf-8") as f:
            f.write(f'"{text}","yanlis tahmin:"{prediction}","dogrusu: {label}"')
        
        
        return Response({"text": text,"label":label})
