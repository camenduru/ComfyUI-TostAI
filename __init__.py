import os

import numpy as np
import requests
from PIL import Image

import folder_paths

class SendToTostAI:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "api_key": ("STRING", {"default": "YOUR_API_KEY_HERE"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True
    CATEGORY = "TostAI"
    FUNCTION = "send_to_tost_ai"

    def send_to_tost_ai(self, images, api_key: str,):
        (full_output_folder, filename, counter, subfolder, _,) = folder_paths.get_save_image_path("final_tost", folder_paths.get_temp_directory())
        tost_file_path = os.path.join(full_output_folder, f"{filename}.png")
        tost_image = 255.0 * images[0].cpu().numpy()
        tost_image_pil = Image.fromarray(tost_image.astype(np.uint8))
        tost_image_pil.save(tost_file_path)
        response = requests.post(f"https://tost.ai/api/s1/{api_key}", files={"file": open(tost_file_path, "rb")})
        return (f"{response.status_code}:{response.text}", )

NODE_CLASS_MAPPINGS = {
    "SendToTostAI": SendToTostAI,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SendToTostAI": "Send To Tost AI",
}