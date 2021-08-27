import os
from PIL import Image
import numpy as np
import pandas as pd

input_dir = "paintings_input"
output_dir = "paintings_output"

output_dim = (4096, 2618)
output_aspect_ratio = output_dim[0] / output_dim[1]

logs_index = 1

painting_paths = os.listdir(input_dir)

img_base = np.array(Image.open(os.path.join("painting_base_color", "Painting_BaseColor.png")))

my_dict = {
    "input": [],
    "aspect ratio": [],
    "output": []
}

for i, painting_path in enumerate(painting_paths):
    my_dict["input"].append(painting_path)

    img = Image.open(os.path.join(input_dir, painting_path))
    if img.height > img.width:
        rotation = 90
    else:
        rotation = 180

    img = img.rotate(rotation, expand=True)
    input_aspect_ratio = img.width / img.height
    aspect_ratio = np.around(input_aspect_ratio / output_aspect_ratio, 3)
    my_dict["aspect ratio"].append(aspect_ratio)

    img = img.resize(output_dim)
    img = np.array(img)
    img_out = img_base.copy()
    img_out[-output_dim[1]:, :, :] = img
    img_out = Image.fromarray(img_out)

    painting_tag = ".".join(painting_path.split(".")[:-1])

    output_name = f"Painting_BaseColor_{painting_tag}.png"
    my_dict["output"].append(output_name)
    img_out.save(os.path.join(output_dir, output_name))

    print(f"Progress: {(i + 1) / len(painting_paths):.0%}")

pd.DataFrame.from_dict(my_dict).to_csv(os.path.join("paintings_logs", f"painting_logs_{logs_index:04d}.csv"))
