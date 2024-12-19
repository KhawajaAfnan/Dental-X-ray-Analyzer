from ultralytics import YOLO
from flask import request, Response, Flask
from waitress import serve
from PIL import Image
from matplotlib import pyplot as plt
import json
from flask_cors import CORS
#python3 object_detector.py
#http://localhost:8080

#cd Z:\Desktop\ngrok-v3-stable-windows-amd64
#./ngrok.exe config add-authtoken 2fMqCXdkHIg8mDs55TfT7IpMlsB_7DQ3qjZKd1eVx2m5T7di
#./ngrok.exe http http://localhost:8080

app = Flask(__name__)
CORS(app)
@app.route("/")
def root():
    """
    Site main page handler function.
    :return: Content of index.html file
    """
    with open("index.html") as file:
        return file.read()


@app.route("/detect", methods=["POST"])
def detect():
    """
       
        :return: a JSON array of objects bounding 
        boxes in format 
        [[x1,y1,x2,y2,object_type,probability],..]
    """
    buf = request.files["image_file"]
    
    boxes = detect_objects_on_image(Image.open(buf.stream))
    return Response(
      json.dumps(boxes),  
      mimetype='application/json'
    )


def detect_objects_on_image(buf):
    """
    :param buf: Input image file stream
    :return: Array of bounding boxes in format 
    [[x1,y1,x2,y2,object_type,probability],..]
    """
    
    model = YOLO("diseases.pt")
    results = model.predict(buf, conf=0.5)
    result = results[0]
    
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output.append([x1, y1, x2, y2, result.names[class_id], prob])
    
    model1 = YOLO("species.pt")
    results1 = model1.predict(buf, conf=0.5)
    result1 = results1[0]
    
    output1 = []
    for box in result1.boxes:
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output1.append([x1, y1, x2, y2, result1.names[class_id], prob])
    
    output2 = []

    # Flag to check if any bounding box from output intersects with a bounding box from output1
    intersects = False

    # Iterate through each bounding box in output
    for box1 in output:
        x1_1, y1_1, x2_1, y2_1, object_type_1, prob_1 = box1
        
        # Check if the bounding box in output1 is contained within the bounding box in output
        for box2 in output1:
            x1_2, y1_2, x2_2, y2_2, object_type_2, prob_2 = box2
            
            # If box2 is inside box1
            # Define leeway
            leeway = 40  # You can adjust this value as needed

            # If box2 is inside box1 with leeway
            if x1_1 - leeway <= x1_2 and y1_1 - leeway <= y1_2 and x2_1 + leeway >= x2_2 and y2_1 + leeway >= y2_2:
                intersects = True
                output2.append([
                    x1_1, y1_1, x2_1, y2_1, object_type_1, prob_1,
                    object_type_2, prob_2
                ])
        
      
    
    # If there's no intersection after iterating through all bounding boxes in output, append all bounding boxes from both output and output1 to output2
    if not intersects:
        for box2 in output1:
            x1_2, y1_2, x2_2, y2_2, object_type_2, prob_2 = box2
        # Append object_type_2 and prob_2 to box2
            box2.extend([object_type_2, prob_2])
        # Extend output2 with the modified output1
        output2.extend(output1)

    return output2




serve(app, host='0.0.0.0', port=8080)