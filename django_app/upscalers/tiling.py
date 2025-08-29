import torch

# Fixed config
TILE_SIZE = (640, 360)  # (height, width)
OVERLAP = (64, 36)  # (height, width)
SCALE_FACTOR = 2  # change if your model scales differently


def run_model_on_patch(model, patch):
    """Run model on a single patch"""
    with torch.no_grad():
        return model(patch)


def tile_image(tensor):
    """Split tensor [1, C, H, W] into overlapping tiles"""
    b, c, h, w = tensor.shape
    tile_h, tile_w = TILE_SIZE
    overlap_h, overlap_w = OVERLAP
    stride_h = tile_h - overlap_h
    stride_w = tile_w - overlap_w

    patches = []
    positions = []

    for y in range(0, h, stride_h):
        for x in range(0, w, stride_w):
            y1, x1 = y, x
            y2, x2 = min(y + tile_h, h), min(x + tile_w, w)

            patch = tensor[:, :, y1:y2, x1:x2]
            patches.append(patch)
            positions.append((y1, y2, x1, x2))

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
