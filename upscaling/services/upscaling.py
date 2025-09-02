from PIL import Image
import os
from django.conf import settings
import torch
from torchvision.transforms import v2
from datetime import datetime

from upscaling.services.convolutional_model import UnetUpscaler
from upscaling.services.ViT_model import ViT_model
from upscaling.services.tiling import (
    run_model_on_patch,
    tile_image,
    merge_patches,
    pad_to_grid,
    crop_output,
)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device is {device}")


def load_image_to_tensor(image):
    pil_image = Image.open(image).convert("RGB")
    transform = v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])
    input_tensor = transform(pil_image)
    input_tensor = input_tensor.unsqueeze(0)
    return input_tensor


def conv_upscaling(image):
    input_tensor = load_image_to_tensor(image)

    model = UnetUpscaler()
    weights_path = os.path.join(
        settings.BASE_DIR,
        "upscaling",
        "services",
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

    # Split into patches
    patches, positions, full_size = tile_image(input_tensor)
    patches = [p.to(device) for p in patches]

    # Run inference
    outputs = [run_model_on_patch(model, p) for p in patches]

    # Merge back
    result_tensor = merge_patches(outputs, positions, full_size)

    # Convert back to image
    result_tensor = result_tensor.squeeze(0).clamp(0, 1).cpu()
    result_image = v2.ToPILImage()(result_tensor)
    result_image.save("temp.png", format="PNG")

    return result_image


def trans_upscaling(image):
    input_tensor = load_image_to_tensor(image)

    model = ViT_model

    weights_path = os.path.join(
        settings.BASE_DIR,
        "upscaling",
        "services",
        "weights",
        "ViT_model_weights.pt",
    )
    state_dict = torch.load(
        weights_path,
        map_location="cpu",
    )
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    # Pad once
    input_padded, orig_size, _ = pad_to_grid(input_tensor)

    # Split into patches
    patches, positions, full_size = tile_image(input_padded)
    patches = [p.to(device) for p in patches]

    # Run inference
    outputs = [run_model_on_patch(model, p) for p in patches]

    # Merge back
    result_tensor = merge_patches(outputs, positions, full_size)

    # Crop back to original scaled size
    final = crop_output(result_tensor, orig_size, scale=2)

    # Convert back to image
    final = final.squeeze(0).clamp(0, 1).cpu()
    result_image = v2.ToPILImage()(final)
    result_image.save("temp.png", format="PNG")

    return result_image
