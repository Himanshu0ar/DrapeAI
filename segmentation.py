from rembg import remove
from PIL import Image
import numpy as np

input_path = "input_images/test1.jpeg"
output_path = "output_images/test1_nobg.png"
mask_path = "output_images/test1_mask.png"

input_image = Image.open(input_path)
output_image = remove(input_image)
output_image.save(output_path)

print("Background removed! Saved to:", output_path)

output_array = np.array(output_image)
alpha_channel = output_array[:, :, 3]

mask_image = Image.fromarray(alpha_channel)
mask_image.save(mask_path)

print("Mask save ho gaya:", mask_path)
