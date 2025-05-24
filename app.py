from scripts import detect_frame


import gradio as gr


with gr.Blocks() as demo:
    gr.Markdown("# Detect Image")
    with gr.Accordion("Choose a Filter", open=False):
        class_checkboxes = gr.Checkboxgroup(detect_frame.get_model_class_names(), label="Classes", info="Filter")
    detect_btn = gr.Button("Process", variant="primary")
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Input Image")
            confidence_value = gr.Slider(label="Confidence Threshold", minimum=0.1, maximum=1.0, step=0.05, value=0.5, interactive=True)
        with gr.Column():
            output_image = gr.Image(label="Output Image", interactive=False)

    detected_objects = gr.Dataframe(
                            headers=["ID", "Class", "Locations", "Confidence"],
                            datatype=["str", "str", "str", "str"],
                            row_count=1,
                            col_count=(4, "fixed")
                        )

    detect_btn.click(
        fn=detect_frame.detect_image,
        inputs=[input_image, confidence_value, class_checkboxes],
        outputs=[output_image, detected_objects]
    )


if __name__ == "__main__":
    demo.launch(inbrowser=True, debug=True)