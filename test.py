from vosk import Model

model_path = "in_en_model"  # Or the path to your model folder

try:
    model = Model(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")