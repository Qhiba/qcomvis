import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)


interface = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"]
)


app = interface.app