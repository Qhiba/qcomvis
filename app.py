from ultralytics import YOLO

import gradio as gr
import numpy as np
import supervision as sv


model_path = "./models/yolov8n.pt"
model = YOLO(model_path)
classes_names = {name: id for id, name in model.names.items()}
model_classes_name = [name for name in classes_names.keys()]

def detect_image(input_img):
    result = model(input_img)[0]
    bbox_annotation = sv.BoxAnnotator()
    label_annotation = sv.LabelAnnotator()

    detections = sv.Detections.from_ultralytics(result)

    detected_objects = []
    for object_class, object_loc, object_conf in zip(detections.class_id, detections.xyxy, detections.confidence):
        detected_objects.append([model.names[object_class], object_loc, round(object_conf, 2)])

    labels = [
        f"{model.names[class_id]} {confidence:.2f}"
        for class_id, confidence in zip(detections.class_id, detections.confidence)
    ]

    annotated_img = bbox_annotation.annotate(scene=input_img.copy(), detections=detections)
    annotated_img = label_annotation.annotate(scene=annotated_img, detections=detections, labels=labels)
    print
    return annotated_img, detected_objects


with gr.Blocks() as interface:
    gr.Markdown("# Detect Image")
    class_checkboxes = gr.Checkboxgroup(model_classes_name, label="Classes", info="Filter")
    input_image = gr.Image(label="Input Image")
    detect_button = gr.Button("Process")

    output_image = gr.Image(label="Output Image", interactive=False)
    detected_objects = gr.Dataframe(
                            headers=["Class", "Locations", "Confidence"],
                            datatype=["str", "str", "str"],
                            row_count=1,
                            col_count=(3, "fixed")
                        )


if __name__ == "__main__":
    interface.launch(inbrowser=True)