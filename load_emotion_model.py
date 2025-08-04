import joblib
import numpy as np

# Correct file path
model_path = r"C:\Users\Dell\Desktop\aditi\Masters_IT\Sem4\MyProjects\melospeech\model\emotion_model.pkl"

# Load using joblib
emotion_model = joblib.load(model_path)

# Dummy input (make sure it matches the expected shape)
sample_input = np.random.rand(1, 40)

# Predict
prediction = emotion_model.predict(sample_input)
print("Predicted Emotion:", prediction[0])
