import json
import requests
import io
import base64
from PIL import Image, ImageOps
import gradio as gr

url = "http://127.0.0.1:7860"

def pil_to_base64(pil_image):
    with io.BytesIO() as stream:
        pil_image.save(stream, "PNG")
        base64_str = str(base64.b64encode(stream.getvalue()), "utf-8")
        return "data:image/png;base64," + base64_str

def prompt2img(pPrompt, nPrompt, steps):
    payload = {
        "prompt": pPrompt,
        "negative_prompt": nPrompt,
        "steps": steps,
        "width": 512,
        "height": 512
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    image_data = base64.b64decode(r['images'][0])
    output_image = Image.open(io.BytesIO(image_data))
    return output_image

def img2img(input_image, selected_style, denoising_strength, steps, controlnetModule, controlnetModel):
    
    input_image = input_image.convert("RGB")
    pil_image = pil_to_base64(input_image)
    
    payload = {
        "init_images": [pil_image],
        "styles": [selected_style],
        "width": 512,
        "height": 512,
        "steps": steps,
        "resize_mode": 2,
        "denoising_strength": denoising_strength,
        "cfg_scale": 7,
        "sampler_name": "Euler a",
        "alwayson_scripts": {
            "controlnet": {
                "args": [{
                    "controlnet_module": controlnetModule,
                    "model": controlnetModel
                }]
            }
        }
    }

    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    r = response.json()
    image_data = base64.b64decode(r['images'][0])
    output_image = Image.open(io.BytesIO(image_data))
    return output_image

with gr.Blocks() as app:
    
    with gr.Tab("Create Image"):
        prompt2img_output_image = gr.Image(type="pil", label="Output Image")
        pPrompt = gr.Textbox(label="Positive Prompt")
        nPrompt = gr.Textbox(label="Negative Prompt")
        prompt2imgSteps = gr.Slider(15, 50, value=25, step=5, label="Steps", info="Choose between 15 and 50")

        genImage = gr.Button("Generate")

    with gr.Tab("Style Image"):
        with gr.Row():
            input_image = gr.Image(type="pil", label="Input Image")
            img2img_output_image = gr.Image(type="pil", label="Output Image")

            styles_response = requests.get(f'{url}/sdapi/v1/prompt-styles')
            style_names = [style['name'] for style in styles_response.json()]

        styleImage = gr.Button("Convert")
        selected_style = gr.Dropdown(label="Style", choices=style_names, value=style_names[0])

        with gr.Accordion("Open for More!", open=False):
            denoising_strength = gr.Slider(0.2, 0.7, value=0.4, step=0.01, label="Effect", info="Choose between 0.2 and 0.7")
            img2imgSteps = gr.Slider(15, 50, value=25, step=5, label="Steps", info="Choose between 15 and 50")

            contronlnet_module_response = requests.get(f'{url}/controlnet/module_list')
            module_list = json.loads(contronlnet_module_response.text)['module_list']

            contronlnet_model_response = requests.get(f'{url}/controlnet/model_list')
            model_list = json.loads(contronlnet_model_response.text)['model_list']
                
            controlnetModule = gr.Dropdown(label="ControlNet Module", choices=module_list, value="openpose_full")
            controlnetModel = gr.Dropdown(label="ControlNet Model", choices=model_list, value="control_v11p_sd15_openpose [cab727d4]")
            

    genImage.click(prompt2img, inputs=[pPrompt, nPrompt, prompt2imgSteps], outputs=prompt2img_output_image)
    styleImage.click(img2img, inputs=[input_image, selected_style, denoising_strength, img2imgSteps, controlnetModule, controlnetModel], outputs=img2img_output_image)
    
if __name__ == "__main__":
    app.launch()
