import gradio as gr

def hello(name):
    return "Hello1, " + name + "!"

iface = gr.Interface(fn=hello, inputs="text", outputs="text")
iface.launch()
