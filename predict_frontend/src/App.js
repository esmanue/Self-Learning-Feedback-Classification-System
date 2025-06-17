import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [feedbackuser, setFeedbackUser] = useState("");

  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/predict/", { text: text });
      setResult(response.data.prediction);
    } catch (error) {
      console.error("Tahmin yapılırken hata oluştu:", error);
    }
  };

  const handleFeedback = async () => {
    try {
      let label = 0;
      if (feedbackuser === 'Positive') {
        label = 1;
      }

      await axios.post("http://localhost:8000/api/feedback/", {
        text: text,
        label: label
      });

      alert("Feedback sisteme eklendi.");
    } catch (error) {
      console.error("Feedback eklenirken hata:", error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Student Feedback Sentiment Analysis</h2>

      <textarea
        rows="5"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Please enter your feedback here..."
      />
      <br />

      <button onClick={handleSubmit}>Predict Sentiment</button>

      <h3>Model Prediction: {result}</h3>

      <div>
        <h4>If prediction was wrong, give correct one:</h4>
        <select value={feedbackuser} onChange={(e) => setFeedbackUser(e.target.value)}>
          <option value="">Select</option>
          <option value="Positive">Positive</option>
          <option value="Negative">Negative</option>
        </select>
        <button onClick={handleFeedback}>Submit Feedback</button>
      </div>
    </div>
  );
}

export default App;
