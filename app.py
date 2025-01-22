from ultralytics import YOLO

import gradio as gr
import numpy as np
import supervision as sv


model_path = "./models/yolov8n.pt"
model = YOLO(model_path)
classes_names = {name: id for id, name in model.names.items()}
model_classes_name = [name for name in classes_names.keys()]


def detect_image(input_img, conf, filter=None):
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


with gr.Blocks() as interface:
    gr.Markdown("# Detect Image")
    with gr.Accordion("Choose a Filter", open=False):
        class_checkboxes = gr.Checkboxgroup(model_classes_name, label="Classes", info="Filter")
    detect_button = gr.Button("Process")
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Input Image")
            confidence_value = gr.Slider(label="Confidence Threshold", minimum=0.1, maximum=1.0, step=0.05, value=0.5, interactive=True)
        with gr.Column():
            output_image = gr.Image(label="Output Image", interactive=False)
            with gr.Row():
                img_flag_button = gr.Button("Image Flag", interactive=False)
                data_flag_button = gr.Button("Data Flag", interactive=False)

    detected_objects = gr.Dataframe(
                            headers=["ID", "Class", "Locations", "Confidence"],
                            datatype=["str", "str", "str", "str"],
                            row_count=1,
                            col_count=(4, "fixed")
                        )

    detect_button.click(
        fn=detect_image,
        inputs=[input_image, confidence_value, class_checkboxes],
        outputs=[output_image, detected_objects]
    )


if __name__ == "__main__":
    interface.launch(inbrowser=True)