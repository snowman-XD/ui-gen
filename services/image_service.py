import io
from PIL import Image
import base64 # to encode  the binary data into the text strings 

class images:
    @staticmethod  
    def process_and_encode(file_content: bytes) -> str:
        # Load image from bytes
        image = Image.open(io.BytesIO(file_content))
        
        # Convert to RGB if necessary (required for JPEG)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # 1. AGGRESSIVE RESIZING
        # High-res images (1920px) consume massive tokens. 
        # For UI generation, 1024px is usually plenty for the AI to see buttons/text.
        max_dimension = 1024 
        if image.width > max_dimension or image.height > max_dimension:
            if image.width > image.height:
                ratio = max_dimension / float(image.width)
                new_width = max_dimension
                new_height = int(float(image.height) * float(ratio))
            else:
                ratio = max_dimension / float(image.height)
                new_height = max_dimension
                new_width = int(float(image.width) * float(ratio))
            
            # Use LANCZOS for quality, but at a smaller scale
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 2. FORMAT SWITCH & COMPRESSION
        # PNG is too heavy for free tier quotas. 
        # JPEG at 70% quality is the "sweet spot" for AI Vision.
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=70, optimize=True)
        
        return base64.b64encode(buffered.getvalue()).decode("utf-8")


 # open image frm byte and store in a variable --> resize the image if necessary -->  using the ram to hold it temporarily for faster accesiblity 