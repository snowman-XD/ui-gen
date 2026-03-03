import httpx
from helpers_decorator.retry import async_retry
from configs import settings
 # find a free tier llm that can handel text +image  this groq is only for text based work ocr
class lLM_cheat():
    def __init__(self):
        self.model = "gemini-2.5-flash" # Best vision model for free tier
        self.api_key = settings.GEMINI_API_KEY
        self.llm_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
       
    @async_retry(retries = 1, base_delay= 60) # calling the retry helper from outside class as the decorator here rather than hardcoding custom retry for each service
    
    async def answered(self, ocr_text : str) -> str : 
        headers = {
            "Content-Type": "application/json"
        }
      
        prompt = (f""" Read the question "{ocr_text}"and answer the correct options given in the last """)
        
        
     
        #each llm has its own diffrent payload format check respectively and temperature sets the creativity. here gemini
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    
                ]
            }],
            "generationConfig": {
                "temperature": 0.5,
                "maxOutputTokens": 4096
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client : 
            #print(bs64_image[:50]) # sending request to ai by opening a temporary internet connection and waiting for only 60 sec max
            response = await client.post(self.llm_api_url, headers=headers ,json=payload)  # sends data to ai
            
            if response.status_code != 200:
                print(f"Gemini Error: {response.text}")
                response.raise_for_status()
                
            
            data = response.json()
            

            # each llm has diffrent default reponse format  here we try to extract the raw html from the json response of gemini .  change for any other llm
            anser = data['candidates'][0]['content']['parts'][0]['text']
            return anser.strip()





    