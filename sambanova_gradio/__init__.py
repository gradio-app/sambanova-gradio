import os
from openai import OpenAI
import gradio as gr
from typing import Callable

__version__ = "0.0.1"

def get_fn(model_name: str, preprocess: Callable, postprocess: Callable):
    def fn(message, history):
        # Preprocess the inputs
        inputs = preprocess(message, history)

        # Initialize the OpenAI client for Sambanova
        client = OpenAI(
            base_url="https://api.sambanova.ai/v1/",
            api_key=os.environ.get("SAMBANOVA_API_KEY"),
        )

        # Call the Sambanova API with streaming enabled
        completion = client.chat.completions.create(
            model=model_name,
            messages=inputs['messages'],
            stream=True,
        )

        # Streaming response to Gradio ChatInterface UI
        response_text = ""
        for chunk in completion:
            delta = chunk.choices[0].delta.content or ""
            response_text += delta
            yield postprocess(response_text)
    return fn

def get_interface_args(pipeline):
    if pipeline == "chat":
        # Using the default ChatInterface for chat models
        inputs = None
        outputs = None
        def preprocess(message, history):
            # Constructing the messages list from the conversation history
            messages = []
            for user_msg, assistant_msg in history:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})
            messages.append({"role": "user", "content": message})
            return {'messages': messages}

        postprocess = lambda x: x  # No post-processing needed
    else:
        # Add other pipeline types when they will be needed
        raise ValueError(f"Unsupported pipeline type: {pipeline}")
    return inputs, outputs, preprocess, postprocess

def get_pipeline(model_name):
    # Determine the pipeline type based on the model name
    # For simplicity, assuming all models are chat models at the moment
    return "chat"

def registry(name: str, api_key: str = None, **kwargs):
    """
    Create a Gradio Interface for a model on Sambanova.

    Parameters:
        - name (str): The name of the model on Sambanova.
        - api_key (str, optional): The API key for Sambanova.
    """
    # Set the Sambanova API key
    if api_key is not None:
        os.environ["SAMBANOVA_API_KEY"] = api_key

    # Ensure the API key is set
    api_key = os.environ.get("SAMBANOVA_API_KEY")
    if not api_key:
        raise ValueError("SAMBANOVA_API_KEY environment variable is not set.")

    # Determine the pipeline type
    pipeline = get_pipeline(name)
    inputs, outputs, preprocess, postprocess = get_interface_args(pipeline)
    fn = get_fn(name, preprocess, postprocess)

    if pipeline == "chat":
        # Create a Gradio ChatInterface
        interface = gr.ChatInterface(fn=fn, **kwargs)
    else:
        # For other pipelines, create a standard Interface
        interface = gr.Interface(fn=fn, inputs=inputs, outputs=outputs, **kwargs)

    return interface
