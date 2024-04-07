# Text-to-Image and Image-to-Image with ControlNet Generation for Stable Diffusion

This project uses the Stable Diffusion API to generate images from text prompts and apply styles to images. It provides a user interface with two tabs: "Create Image" and "Style Image".

## Create Image

In the "Create Image" tab, you can input a positive prompt and a negative prompt to generate an image. You can also adjust the number of steps for the image generation process. After clicking the "Generate" button, the generated image will be displayed.

## Style Image

In the "Style Image" tab, you can upload an image and apply a style to it. The available styles are fetched from the Stable Diffusion API. You can also adjust the denoising strength and the number of steps for the image-to-image process. Additionally, you can select a ControlNet module and model to further refine the image-to-image process. After clicking the "Convert" button, the styled image will be displayed.

## Dependencies

This project requires the following dependencies:

- `requests`
- `gradio`
- `python-dotenv`

To install all dependencies:
``bash
pip install -r requirements.txt
```

## Usage

To run the project, simply execute the script using a Python interpreter:

```bash
python style-photo.py
```

This will launch the Gradio interface in your web browser. You can then interact with the interface to generate images from text prompts and apply styles to images.

## Notes

- The `url` variable in the script should be set to the address of your Stable Diffusion API instance.
- The `controlnetModule` and `controlnetModel` variables in the "Style Image" tab can be adjusted to use different ControlNet modules and models.
- The `denoising_strength` and `img2imgSteps` variables in the "Style Image" tab can be adjusted to control the denoising strength and number of steps for the image-to-image process.