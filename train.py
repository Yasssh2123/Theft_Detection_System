import sys
sys.path.append("./")
from ultralytics import YOLO

ROOT_DIR = "C:/Users/yashc/Downloads/"
PROJECT_DIR = f"{ROOT_DIR}Theft_Detection"

name_ver = "Theft_Detection_e200_smallModel_FYP_Dataset"
weight = f"{PROJECT_DIR}/yolo11s.pt"
model_yaml = f"{PROJECT_DIR}/yolo11s.yaml"
hyp_yaml = f"{PROJECT_DIR}/hyp2.yaml"
dataset_yaml = f"{PROJECT_DIR}/data.yaml"

model = YOLO(model_yaml).load(weight)
results = model.train(cfg=hyp_yaml,data=dataset_yaml, 
    epochs=200, imgsz=640, batch=16, device=[0],patience=25,
    workers=0, project=f"{PROJECT_DIR}", name=name_ver, exist_ok=True,optimizer="AdamW")