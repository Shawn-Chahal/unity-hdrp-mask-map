import os
from PIL import Image
import numpy as np

input_dir = "textures_input"
output_dir = "textures_output"


def generate_mask_map(prefix, metallic=None, occlusion=None, detail=None, smoothness=None,
                      smoothness_from_metallic_alpha=True, output_file_format="png"):
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
        img_metallic = Image.open(os.path.join(input_dir, f"{prefix}{metallic}.{input_file_format}"))
        if smoothness_from_metallic_alpha:
            img["R"] = Image.fromarray(np.array(img_metallic.convert("RGBA"))[:, :, 0])
        else:
            img["R"] = Image.open(img_metallic.convert("L"))
        img_zero = Image.fromarray(np.zeros_like(np.array(img["R"]))).convert("L")
    else:
        skipped.append("R")

    if occlusion is not None:
        img["G"] = Image.open(os.path.join(input_dir, f"{prefix}{occlusion}.{input_file_format}")).convert("L")
        img_zero = Image.fromarray(np.zeros_like(np.array(img["G"]))).convert("L")
    else:
        skipped.append("G")

    if detail is not None:
        img["B"] = Image.open(os.path.join(input_dir, f"{prefix}{detail}.{input_file_format}")).convert("L")
        img_zero = Image.fromarray(np.zeros_like(np.array(img["B"]))).convert("L")
    else:
        skipped.append("B")

    if smoothness is not None:
        img_smoothness = Image.open(os.path.join(input_dir, f"{prefix}{smoothness}.{input_file_format}"))
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
    rgba.save(os.path.join(output_dir, f"{prefix}mask_map.{output_file_format}"))

    print(f"Created {prefix} mask map.")


input_file_format = "psd"

generate_mask_map("Table_6_", metallic="MetallRough", occlusion="AO", smoothness="MetallRough")
generate_mask_map("Tables_2_", metallic="MetallRough", occlusion="AO", smoothness="MetallRough")
generate_mask_map("Tables_", metallic="MetallRough", occlusion=None, smoothness="MetallRough")
