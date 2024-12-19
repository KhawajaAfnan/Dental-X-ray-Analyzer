from ultralytics import YOLO

   # Load a model
model = YOLO("diseases.pt")  # load an official yolov8* model

   # Export the model
model.export(format="onnx", imgsz=[800,800])