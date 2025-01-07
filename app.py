import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

with gr.Blocks() as interface:
    gr.Markdown('# Greetings from Gradio!')
    inp = gr.Textbox(placeholder="What is your name?")
    out = gr.Textbox()

    inp.change(
        fn = lambda x: f"Welcome, {x}",
        inputs = inp,
        outputs = out
    )

    gr.Interface(
        fn=greet,
        inputs=['text', 'slider'],
        outputs=['text']
    )


if __name__ == "__main__":
    interface.launch(inbrowser=True)