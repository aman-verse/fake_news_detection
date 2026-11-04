from functools import lru_cache

import numpy as np
from PIL import Image

@lru_cache(maxsize=1)
def _get_reader():
    import easyocr

    return easyocr.Reader(["en"], gpu=False)

def extract_text_from_image(image_file) -> str:
    if image_file is None:
        return ""

    try:
        image_file.seek(0)
        image = Image.open(image_file).convert("RGB")
        image_array = np.asarray(image)
        extracted_lines = _get_reader().readtext(
            image_array,
            detail=0,
            paragraph=False,
        )

        return "\n".join(
            text.strip()
            for text in extracted_lines
            if text and text.strip()
        )
    except Exception as error:
        raise RuntimeError(f"OCR failed: {error}") from error
