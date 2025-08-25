from PIL import Image
import io
import torch
from torchvision.transforms import v2
from django_app.upscalers.convolutional_model import UnetUpscaler


def conv_upscaling(image):
    pil_image = Image.open(image)
    transform = v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])
    input_tensor = transform(pil_image)
    print(input_tensor.shape)

    model = UnetUpscaler()
    state_dict = torch.load(
        "./upscalers/weights/convolutional_model_weights.pt",
        map_location="cpu",
    )
    model.load_state_dict(state_dict)
    print(model)
