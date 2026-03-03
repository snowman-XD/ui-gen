import pytesseract  # tool that can read texts from the image 
import io
from PIL import Image

class ocr_service:             #optical_charecter_recognition 
    @staticmethod               # also with this u can call this fuction without creating the obeject
    def text_extraction(file_content: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(file_content))                   # to store the uploaded image in ram temporarily 
            extracted_text = pytesseract.image_to_string(image) # extracting the text 
            return extracted_text                   
        
        except Exception as e :
            print("OCR ERROR:", str(e))
            raise e
            #return ""  # to not show this to user if any error arrives 
        

 #this basically tries to extract the text content from the user's uploaded image 