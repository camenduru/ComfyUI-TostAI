import os

import numpy as np
import requests
from PIL import Image

import folder_paths

class SendToTostAIWebhook:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "webhook_url": ("STRING", {"default": "https://tost.ai/api/webhook"}),
                "webhook_key": ("STRING", {"default": "YOUR_WEBHOOK_KEY_HERE"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True
    CATEGORY = "TostAI"
    FUNCTION = "send_to_tost_ai_webhook"

    def send_to_tost_ai_webhook(self, images, webhook_url: str, webhook_key: str,):
        (full_output_folder, filename, counter, subfolder, _,) = folder_paths.get_save_image_path("final_tost", folder_paths.get_temp_directory())
        tost_file_path = os.path.join(full_output_folder, f"{filename}_.png")
        tost_image = 255.0 * images[0].cpu().numpy()
        tost_image_pil = Image.fromarray(tost_image.astype(np.uint8))
        tost_image_pil.save(tost_file_path)
        response = requests.post(f"{webhook_url}/{webhook_key}", files={"file": open(tost_file_path, "rb")})
        if response.status_code == 204:
            print("Successfully uploaded file to TostAI.")
        else:
            print(f"Failed to upload file. Status code: {response.status_code}:{response.text}")
        return (f"{response.status_code}:{response.text}", )

NODE_CLASS_MAPPINGS = {
    "SendToTostAIWebhook": SendToTostAIWebhook,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SendToTostAIWebhook": "Send To Tost AI Webhook",
}