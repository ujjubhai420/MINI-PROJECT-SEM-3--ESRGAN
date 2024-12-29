import os
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch


class ESRGAN:
    def __init__(self, model_path):

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {'cuda' if torch.cuda.is_available() else 'cpu'}")
        self.model = self.load_model(model_path)
        self.model.to(self.device)  # Move the model to the correct device here

    def load_model(self, model_path):
      
        model = arch.RRDBNet(3, 3, 64, 23, gc=32)
        model.load_state_dict(torch.load(model_path, map_location=self.device), strict=True)
        model.eval()
        print(f"Model loaded from {model_path}")
        return model

    def enhance_image(self, img_path):
     
        # Read and preprocess the image
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"Could not read image from {img_path}")

        img = img.astype(np.float32) / 255.0  # Normalize to [0, 1]
        img = img.transpose((2, 0, 1))  # Channel order (HWC -> CHW)
        img_LR = torch.from_numpy(img).unsqueeze(0).float().to(self.device)  # Add batch dimension

        # Inference
        with torch.no_grad():
            output = self.model(img_LR).data.squeeze().float().cpu().clamp(0, 1).numpy()

        # Post-process the output
        output = output.transpose((1, 2, 0))  # Channel order (CHW -> HWC)
        output = (output * 255.0).round().astype(np.uint8)  # Convert back to uint8
        return output

    def save_image(self, img, output_path):
    
        cv2.imwrite(output_path, img)
        print(f"Image saved to {output_path}")
