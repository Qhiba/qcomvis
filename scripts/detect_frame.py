from ultralytics import YOLO


import numpy as np
import supervision as sv


model_path = "./models/yolov8n.pt"
model = YOLO(model_path)
classes_names = {name: id for id, name in model.names.items()}
model_class_names = [name for name in classes_names.keys()]


def get_model_class_names():
    return model_class_names


def detect_image(input_img, conf=0.5, filter=None):
    tracker = sv.ByteTrack()
    result = model(input_img)[0]
    filtered_class = [classes_names[name] for name in filter]
    bbox_annotation = sv.BoxAnnotator()
    label_annotation = sv.LabelAnnotator()

    detections = sv.Detections.from_ultralytics(result)
    detections = detections[detections.confidence >= conf]
    if len(filtered_class) != 0:
        detections = detections[np.isin(detections.class_id, filtered_class)]
    detections = tracker.update_with_detections(detections)

    detected_objects = []
    for tracker_id, object_class, object_loc, object_conf in zip(detections.tracker_id, detections.class_id, detections.xyxy, detections.confidence):
        detected_objects.append([f"#{tracker_id}", model.names[object_class], object_loc, round(object_conf, 2)])

    labels = [
        f"#{tracker_id} {model.names[class_id]} {confidence:.2f}"
        for tracker_id, class_id, confidence in zip(detections.tracker_id, detections.class_id, detections.confidence)
    ]

    annotated_img = bbox_annotation.annotate(scene=input_img.copy(), detections=detections)
    annotated_img = label_annotation.annotate(scene=annotated_img, detections=detections, labels=labels)
    return annotated_img, detected_objects
