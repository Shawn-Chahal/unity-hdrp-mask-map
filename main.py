import os
from PIL import Image
import numpy as np

input_dir = "textures_input"
output_dir = "textures_output"


def generate_mask_map(prefix, metallic=None, occlusion=None, detail=None, smoothness=None,
                      smoothness_from_metallic_alpha=True):
    """
    • Red: Stores the metallic map.
    • Green: Stores the ambient occlusion map.
    • Blue: Stores the detail mask map.
    • Alpha: Stores the smoothness map.
    """

    skipped = []
    img = {}
    img_zero = None

    if metallic is not None:
        img_metallic = Image.open(os.path.join(input_dir, f"{prefix}{metallic}.{file_format}"))
        if smoothness_from_metallic_alpha:
            img["R"] = Image.fromarray(np.array(img_metallic.convert("RGBA"))[:, :, 0])
        else:
            img["R"] = Image.open(img_metallic.convert("L"))
        img_zero = Image.fromarray(np.zeros_like(np.array(img["R"]))).convert("L")
    else:
        skipped.append("R")

    if occlusion is not None:
        img["G"] = Image.open(os.path.join(input_dir, f"{prefix}{occlusion}.{file_format}")).convert("L")
        img_zero = Image.fromarray(np.zeros_like(np.array(img["G"]))).convert("L")
    else:
        skipped.append("G")

    if detail is not None:
        img["B"] = Image.open(os.path.join(input_dir, f"{prefix}{detail}.{file_format}")).convert("L")
        img_zero = Image.fromarray(np.zeros_like(np.array(img["B"]))).convert("L")
    else:
        skipped.append("B")

    if smoothness is not None:
        img_smoothness = Image.open(os.path.join(input_dir, f"{prefix}{smoothness}.{file_format}"))
        if smoothness_from_metallic_alpha:
            img["A"] = Image.fromarray(np.array(img_smoothness.convert("RGBA"))[:, :, -1])
        else:
            img["A"] = Image.open(img_smoothness.convert("L"))
        img_zero = Image.fromarray(np.zeros_like(np.array(img["A"]))).convert("L")
    else:
        skipped.append("A")

    for channel in skipped:
        img[channel] = img_zero

    max_size = 0

    for channel in img.keys():
        img_dim = img[channel].size[0]
        if img_dim > max_size:
            max_size = img_dim

    for channel in img.keys():
        img_dim = img[channel].size[0]

        if img_dim != max_size:
            img[channel] = img[channel].resize((max_size, max_size))
            print(f"Resized {prefix} channel {channel} from {img_dim} to {max_size}.")

    rgba = Image.merge("RGBA", (img["R"], img["G"], img["B"], img["A"]))
    rgba.save(os.path.join(output_dir, f"{prefix}mask_map.{file_format}"))

    print(f"Created {prefix} mask map.")


file_format = "png"

generate_mask_map("Skeleton_LowRes_phong1_", metallic="MetallicSmoothness", occlusion=None, smoothness="MetallicSmoothness")
