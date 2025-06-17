import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);  // dikkat: null başlangıç
  const [feedbackuser, setFeedbackUser] = useState("");
  const [loading, setLoading] = useState(false); // loading state

  const handleSubmit = async () => {
    if (!text.trim()) {
      alert("Please enter some text first.");
      return;
    }
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/api/predict/", { text });
      setResult(response.data.prediction);
    } catch (error) {
      console.error("Tahmin yapılırken hata oluştu:", error);
    }
    setLoading(false);
  };

  const resetForm = () => {
    setText("");
    setResult(null);
    setFeedbackUser("");
  };

  const handleFeedback = async () => {
    try {
      let label;

      if (feedbackuser === "True") {
        label = result;
      } else if (feedbackuser === "False") {
        label = result === 1 ? 0 : 1;
      } else {
        alert("Please select feedback.");
        return;
      }

      await axios.post("http://localhost:8000/api/feedback/", {
        text: text,
        label: label
      });

      alert("Feedback sisteme eklendi.");
      resetForm();
    } catch (error) {
      console.error("Feedback eklenirken hata:", error);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '600px', margin: 'auto' }}>
      <h2>Self-Learning-Feedback-Classification-System
</h2>

      <textarea
        rows="5"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Please enter your feedback here..."
      />
      <br />

      <button onClick={handleSubmit} disabled={loading || !text.trim()}>
        {loading ? "Predicting..." : "Predict Sentiment"}
      </button>

      <h3>
        Model Prediction: {result === null ? "" : (result === 1 ? "Positive" : "Negative")}
      </h3>

      {result !== null && (
        <div>
          <h4>Was the prediction correct?</h4>
          <select value={feedbackuser} onChange={(e) => setFeedbackUser(e.target.value)}>
            <option value="">Select</option>
            <option value="True">Correct</option>
            <option value="False">Wrong</option>
          </select>
          <button onClick={handleFeedback} disabled={!feedbackuser}>Submit Feedback</button>
        </div>
      )}
    </div>
  );
}

export default App;
