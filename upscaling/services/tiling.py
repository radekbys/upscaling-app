import torch
from PIL import Image
from torchvision.transforms import v2
import torch.nn.functional as F

# Fixed config
TILE_SIZE = (360, 640)  # (height, width)
OVERLAP = (36, 64)  # (height, width)
SCALE_FACTOR = 2  # change if your model scales differently
GRAY_VALUE = 0.5  # neutral gray in [0,1]


def run_model_on_patch(model, patch):
    """Run model on a single patch"""
    with torch.no_grad():
        return model(patch)


def pad_to_grid(tensor, tile_size=TILE_SIZE, overlap=OVERLAP, value=GRAY_VALUE):
    """
    Pad input image so it divides evenly into tiles.
    Returns padded_tensor, original_size, padding_added
    """
    b, c, h, w = tensor.shape
    tile_h, tile_w = tile_size
    stride_h = tile_h - overlap[0]
    stride_w = tile_w - overlap[1]

    # Compute how many tiles we need
    n_tiles_h = max(1, (h - overlap[0] + stride_h - 1) // stride_h)
    n_tiles_w = max(1, (w - overlap[1] + stride_w - 1) // stride_w)

    padded_h = n_tiles_h * stride_h + overlap[0]
    padded_w = n_tiles_w * stride_w + overlap[1]

    pad_h = padded_h - h
    pad_w = padded_w - w

    tensor_padded = F.pad(tensor, (0, pad_w, 0, pad_h), value=value)
    return tensor_padded, (h, w), (pad_h, pad_w)


def tile_image(tensor, tile_size=TILE_SIZE, overlap=OVERLAP):
    """Split tensor [B, C, H, W] into equally sized overlapping tiles."""
    b, c, h, w = tensor.shape
    tile_h, tile_w = tile_size
    stride_h, stride_w = tile_h - overlap[0], tile_w - overlap[1]

    patches, positions = [], []

    for y in range(0, h - overlap[0], stride_h):
        for x in range(0, w - overlap[1], stride_w):
            patch = tensor[:, :, y : y + tile_h, x : x + tile_w]
            patches.append(patch)
            positions.append((y, y + tile_h, x, x + tile_w))

    return patches, positions, (h, w)


def merge_patches(patches, positions, full_size):
    """Reconstruct full image from upscaled patches"""
    device = patches[0].device
    b, c, h, w = (
        1,
        patches[0].shape[1],
        full_size[0] * SCALE_FACTOR,
        full_size[1] * SCALE_FACTOR,
    )

    output = torch.zeros((b, c, h, w), device=device)
    count_map = torch.zeros((b, c, h, w), device=device)

    for patch, (y1, y2, x1, x2) in zip(patches, positions):
        # Scale coordinates
        y1s, y2s = y1 * SCALE_FACTOR, y2 * SCALE_FACTOR
        x1s, x2s = x1 * SCALE_FACTOR, x2 * SCALE_FACTOR

        output[:, :, y1s:y2s, x1s:x2s] += patch
        count_map[:, :, y1s:y2s, x1s:x2s] += 1

    output /= count_map
    return output


def crop_output(output, orig_size, scale=1):
    """Crop back to original size (scaled)."""
    orig_h, orig_w = orig_size
    return output[:, :, : orig_h * scale, : orig_w * scale]
