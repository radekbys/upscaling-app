from PIL import Image
import os
from django.conf import settings
import torch
from torchvision.transforms import v2
from datetime import datetime

from django_app.upscalers.convolutional_model import UnetUpscaler
from django_app.upscalers.tiling import run_model_on_patch, tile_image, merge_patches

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device is {device}")


def run_model_on_patch(model, patch):
    """Run model on a single patch"""
    with torch.no_grad():
        return model(patch)


def conv_upscaling(image):
    pil_image = Image.open(image).convert("RGB")
    transform = v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])
    input_tensor = transform(pil_image)
    input_tensor = input_tensor.unsqueeze(0)

    model = UnetUpscaler()
    weights_path = os.path.join(
        settings.BASE_DIR,
        "django_app",
        "upscalers",
        "weights",
        "convolutional_model_weights.pt",
    )
    state_dict = torch.load(
        weights_path,
        map_location="cpu",
    )
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    print(f"model prepared {datetime.now()}")

    # Split into patches
    patches, positions, full_size = tile_image(input_tensor)
    patches = [p.to(device) for p in patches]
    print(f"data split into patches {datetime.now()}")

    # Run inference
    outputs = [run_model_on_patch(model, p) for p in patches]
    print(f"inference complete {datetime.now()}")

    # Merge back
    result_tensor = merge_patches(outputs, positions, full_size)
    print(f"patches merged {datetime.now()}")

    # Convert back to image
    result_tensor = result_tensor.squeeze(0).clamp(0, 1).cpu()
    result_image = v2.ToPILImage()(result_tensor)
    result_image.save("temp.png", format="PNG")
    print(f"image saved as temp.png")

    return result_image
