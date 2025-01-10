from ultralytics import YOLO

import gradio as gr
import numpy as np
import supervision as sv

import cv2

model_path = "./models/yolov8n.pt"
model = YOLO(model_path)


def detect_image(input_img):
    #img = cv2.imread(input_img)
    result = model(input_img)[0]
    bbox_annotation = sv.BoxAnnotator()
    label_annotation = sv.LabelAnnotator()

    detections = sv.Detections.from_ultralytics(result)

    labels = [
        f"{model.names[class_id]} {confidence}"
        for class_id, confidence in zip(detections.class_id, detections.confidence)
    ]

    annotated_img = bbox_annotation.annotate(scene=input_img.copy(), detections=detections)
    annotated_img = label_annotation.annotate(scene=annotated_img, detections=detections, labels=labels)
    return annotated_img


with gr.Blocks() as interface:
    gr.Markdown("# Detect Image")
    gr.Interface(
        fn=detect_image,
        inputs=gr.Image(),
        outputs="image"
    )


if __name__ == "__main__":
    interface.launch(inbrowser=True)