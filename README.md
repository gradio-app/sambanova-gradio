# `sambanova_gradio`

is a Python package that makes it very easy for developers to create machine learning apps that are powered by sambanova's Inference API.

# Installation

```bash
pip install sambanova-gradio
```

That's it! 

# Basic Usage

Just like if you were to use the `sambanova` API, you should first save your sambanova API token to this environment variable:

```
export SAMBANOVA_API_KEY=<your token>
```

Then in a Python file, write:

```python
import gradio as gr
import sambanova_gradio

gr.load(
    name='Meta-Llama-3.1-405B-Instruct',
    src=sambanova_gradio.registry,
).launch()
```

or simply without setting the environment variable
```
# text only chatbot
import gradio as gr
import sambanova_gradio

gr.load("Meta-Llama-3.1-70B-Instruct-8k", src=sambanova_gradio.registry, accept_token=True).launch()
```

```
# multimodal chatbot
import gradio as gr
import sambanova_gradio

gr.load("Llama-3.2-11B-Vision-Instruct", src=sambanova_gradio.registry, accept_token=True, multimodal = True).launch()
```

Run the Python file, and you should see a Gradio Interface connected to the model on sambanova!

![ChatInterface](chatinterface.png)

# Customization 

Once you can create a Gradio UI from a sambanova endpoint, you can customize it by setting your own input and output components, or any other arguments to `gr.Interface`. For example, the screenshot below was generated with:

```py
import gradio as gr
import sambanova_gradio

gr.load(
    name='Meta-Llama-3.1-405B-Instruct',
    src=sambanova_gradio.registry,
    title='Sambanova-Gradio Integration',
    description="Chat with Meta-Llama-3.1-405B-Instruct model.",
    examples=["Explain quantum gravity to a 5-year old.", "How many R are there in the word Strawberry?"]
).launch()
```
![ChatInterface with customizations](chatinterface_with_customization.png)

# Composition

Or use your loaded Interface within larger Gradio Web UIs, e.g.

```python
import gradio as gr
import sambanova_gradio

with gr.Blocks() as demo:
    with gr.Tab("405B"):
        gr.load('Meta-Llama-3.1-405B-Instruct', src=sambanova_gradio.registry)
    with gr.Tab("70B"):
        gr.load('Meta-Llama-3.1-70B-Instruct-8k', src=sambanova_gradio.registry)

demo.launch()
```

# Under the Hood

The `sambanova-gradio` Python library has two dependencies: `openai` and `gradio`. It defines a "registry" function `sambanova_gradio.registry`, which takes in a model name and returns a Gradio app.

# Supported Models in Sambanova Cloud

Access Meta’s Llama 3.2 and 3.1 family of models at **full precision** via the SambaNova Cloud API!

**Model details for Llama 3.2 family**:
1. Llama 3.2 1B:
   - Model ID: `Meta-Llama-3.2-1B-Instruct`
   - Context length: 4,096 tokens
2. Llama 3.2 3B:
   - Model ID: `Meta-Llama-3.2-3B-Instruct`
   - Context length: 4,096 tokens
3. Llama 3.2 11B Vision:
   - Model ID: `Llama-3.2-11B-Vision-Instruct`
   - Context length: 4096 tokens
4. Llama 3.2 90B Vision:
   - Model ID: `Llama-3.2-90B-Vision-Instruct`
   - Context length: 4096 tokens

**Model details for Llama 3.1 family**:
1. Llama 3.1 8B:
   - Model ID: `Meta-Llama-3.1-8B-Instruct`
   - Context length: 4k, 8k, 16k
2. Llama 3.1 70B:
   - Model ID: `Meta-Llama-3.1-70B-Instruct`
   - Context length: 4k, 8k, 16k, 32k, 64k
3. Llama 3.1 405B:
   - Model ID: `Meta-Llama-3.1-405B-Instruct`
   - Context length: 4k, 8k

-------

Note: if you are getting a 401 authentication error, then the sambanova API Client is not able to get the API token from the environment variable. This happened to me as well, in which case save it in your Python session, like this:

```py
import os

os.environ["SAMBANOVA_API_KEY"] = ...
```
