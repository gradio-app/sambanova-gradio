import gradio as gr
import sambanova

from typing import Callable

def get_fn(model_name: str, preprocess: Callable, postprocess: Callable):
    def fn(*args):
        args = preprocess(*args)
        outputs = sambanova.run(model_name, args)
        return postprocess(outputs)
    return fn

# Implemented manually for now, but could we parse the openapi spec to get the interface args?
def get_interface_args(pipeline):
    if pipeline == "text-to-image":
        inputs = [gr.Textbox()]
        outputs = [gr.Image()]
        preprocess = lambda x: {"prompt": x}
        postprocess = lambda x: x[0]
    return inputs, outputs, preprocess, postprocess

def get_pipeline(model):
    pipeline = "text-to-image"
    return pipeline

def registry(name: str, token: str | None, inputs=None, outputs=None, **kwargs) -> gr.Interface:
    """
    Create a Gradio Interface for a model on sambanova.
    Parameters:
        - name (str): The name of the model on sambanova.
        - token (str, optional): The API token for the model on sambanova. Not used for now.
        - inputs (List[gr.Component], optional): The input components to use instead of the default.
        - outputs (List[gr.Component], optional): The output components to use instead of the default.
    """
    pipeline = get_pipeline(name)
    inputs_, outputs_, preprocess, postprocess = get_interface_args(pipeline)
    inputs, outputs = inputs or inputs_, outputs or outputs_

    # construct a gr.Interface object
    fn = get_fn(name, preprocess, postprocess)
    return gr.Interface(fn, inputs, outputs, **kwargs)

__version__ = "0.0.1"
