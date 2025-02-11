// src/App.js
import React, { useState } from 'react';

function App() {
  const [feedback, setFeedback] = useState('');
  const [videoFile, setVideoFile] = useState(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      setVideoFile(file);
      setFeedback('Uploading video...');
      
      // Create a FormData object and append the video file
      const formData = new FormData();
      formData.append('video', file);
      
      try {
        const response = await fetch("https://squatbuddy-app-a8afe5b7d5f8.herokuapp.com/api/upload", {
          method: "POST",
          body: formData,
        });
        
        if (!response.ok) {
          // If the response is not ok, try to get the error message
          const errorText = await response.text();
          setFeedback(`Upload failed: ${errorText}`);
        } else {
          // Parse the JSON response and update feedback
          const result = await response.json();
          setFeedback(`Video uploaded successfully! Feedback: ${result.message}`);
        }
      } catch (error) {
        // Catch any network or unexpected errors
        setFeedback(`Upload error: ${error.message}`);
      }
    }
  };
  

  return (
    <div
      style={{
        margin: '20px',
        backgroundColor: 'deeppink',
        fontFamily: 'Consolas, monospace',
        minHeight: '100vh',
        padding: '20px',
        textAlign: 'center'
      }}
    >
      <h1>SquatBuddy</h1>
      <p>> Welcome to SquatBuddy!</p>
      <p>> The purpose of this app is to help people who are scared of squatting get some computer-vision assisted advice to let you know if you're performing a squat safely.</p>
      <p>> To get started, upload a video of yourself performing a squat!</p>
      <p>> Some things to keep in mind when you record:</p>
      <ul style={{ listStyleType: 'none', padding: 0, textAlign: 'center' }}>
        <li>1. Make sure your entire body is visible in the video.</li>
        <li>2. Record from a front-side view to get the best feedback.</li>
        <li>3. Ensure the lighting is good so your form is clearly visible.</li>
      </ul>
      <p>happy lifting! :-)</p>
      <input
        type="file"
        accept="video/*"
        onChange={handleFileChange}
        style={{ marginTop: '10px' }}
      />
      <div
        style={{
          marginTop: '20px',
          padding: '10px',
          border: '1px solid #ccc',
          backgroundColor: '#f9f9f9'
        }}
      >
        {feedback ? <p>{feedback}</p> : <p>No feedback yet.</p>}
      </div>

      <p>
        Some fun info about how this app works:
      </p>
      <p>
        This app uses a combination of <a href="https://github.com/tensorflow/tfjs-models/tree/master/posenet" target="_blank" rel="noopener noreferrer">Google's PoseNet model</a> and a custom trained model to analyze your squat form. I am currently experimenting with various kinds of models which balance speed and accuracy.
      </p>
      <p>
        Obviously, using some huge deep learning models seems a bit unfeasable for a web-app, nor is calling openAI 4o a bunch of times seem cost/time effective. This more a fun app/ML building exercise, but hopefully you can squat safely and soundly! :)
      </p>

      <p>
        to learn more about this project, check this out, also feel free to check out my other stuff <a href="https://pranavramachandra1.github.io/projects/squat_buddy" target="_blank" rel="noopener noreferrer">here</a> :D
      </p>

    </div>
  );
}

export default App;
