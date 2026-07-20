import cv2
import numpy as np
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

MODEL_NAME = "microsoft/trocr-base-handwritten"

processor = TrOCRProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

def prep_ocr(image_input):
    if image_input is None:
        raise ValueError("No image provided")

    if isinstance(image_input, str):
        img = cv2.imread(image_input)
        if img is None:
            raise ValueError(f"Could not read image path: {image_input}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    elif isinstance(image_input, Image.Image):
        img = np.array(image_input.convert("RGB"))

    else:
        img = np.array(image_input)
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("Expected an RGB image")

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    gray = cv2.equalizeHist(gray)

    h, w = gray.shape
    new_h = 384
    new_w = max(1, int(w * (new_h / h)))
    gray = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(rgb)

def clean_text(text):
    return " ".join(text.strip().split())

def recognize_text(image_input):
    image = prep_ocr(image_input)
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)

    with torch.no_grad():
        generated_ids = model.generate(
            pixel_values,
            max_new_tokens=32,
            num_beams=5,
            early_stopping=True
        )

    text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )[0]

    return clean_text(text)
