from ultralytics import YOLO

# Load a model
model = YOLO('')  # load a partially trained model

# Resume training
results = model.train(resume=True)