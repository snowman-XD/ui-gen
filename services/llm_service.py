import httpx
from helpers_decorator.retry import async_retry
from configs import settings
 # find a free tier llm that can handel text +image  this groq is only for text based work ocr
class lLM_work():
    def __init__(self):
        self.model = "gemini-2.5-flash" # Best vision model for free tier
        self.api_key = settings.GEMINI_API_KEY
        self.llm_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
       
    @async_retry(retries = 1, base_delay= 60) # calling the retry helper from outside class as the decorator here rather than hardcoding custom retry for each service
    
    async def llm_generation(self, bs64_image: str, ocr_text : str) -> str : 
        headers = {
            "Content-Type": "application/json"
        }
        prompt2= ("You are a Senior Frontend Developer. Convert this UI screenshot into a professional "
    "single-file responsive HTML using Tailwind CSS. \n"
    "REQUIREMENTS:\n"
    "- Include a full <!DOCTYPE html> structure with <html>, <head>, and <body> tags.\n"
    "- Use this Tailwind CDN in the <head>: <script src='https://cdn.tailwindcss.com'></script>\n"
    f"- Use the following text for content: {ocr_text}\n"
    "- Return ONLY the raw code starting with <!DOCTYPE html>.")
        
        prompt1= (f"""
You are a Senior Product Engineer and UI/UX Specialist. 
I have uploaded a hand-drawn whiteboard sketch of a web dashboard.

CONTEXTUAL DATA (OCR):
The following text was extracted from the sketch: {ocr_text}

YOUR TASK:
1. INTERPRET LAYOUT: Identify rectangles as containers/cards, circles as user avatars, and horizontal lines as dividers or navigation items.
2. DATA MAPPING: Match the OCR text to the UI elements. For example, if 'Total Sales' is near a box, turn that box into a KPI metric card.
3. DESIGN SYSTEM: 
   - Use Tailwind CSS for styling.
   - Use Lucide-React icons for any drawn icons.
   - Implement a clean "Modern SaaS" aesthetic (rounded corners, subtle shadows, plenty of whitespace).
4. LOGIC: If the sketch shows a graph, use Chart.js to create a functional chart with mock data.

TECHNICAL REQUIREMENTS:
- Output a SINGLE FILE responsive HTML with Tailwind via CDN.
- Ensure the code includes <!DOCTYPE html>, <html>, <head>, and <body> tags.
- The UI must be high-fidelity (make it look like a finished product, not a sketch).
- RETURN ONLY THE CODE. NO PROSE. NO MARKDOWN BACKTICKS.
""")
        prompt = (f"""You are a Senior Frontend Developer.

Your task is to convert a provided UI screenshot into a professional, single-file, responsive HTML document using Tailwind CSS.

IMPORTANT IMAGE RULE:
- If the screenshot contains ANY images, avatars or logos:
  - DO NOT attempt to recreate the image.
  - DO NOT generate <img> tags.
  - Instead, create an empty placeholder block that preserves the layout structure.
  - The placeholder must be a <div> with appropriate width/height and Tailwind utility classes.
  - Use a subtle gray background (e.g., bg-gray-200) and keep it completely empty (no text inside).

TEXT CONTENT RULE:
- Use ONLY the following extracted text for all textual content:
  {ocr_text}
- Do NOT invent, modify, or add extra text.
- If text is missing or unclear, leave that section empty.

STRUCTURE REQUIREMENTS:
- Include a complete <!DOCTYPE html> document.
- Include <html>, <head>, and <body> tags.
- Include this Tailwind CDN inside <head>:
  <script src="https://cdn.tailwindcss.com"></script>
- Ensure the layout is responsive.
- Use clean semantic structure.
- Preserve spacing, alignment, and hierarchy based on the screenshot.

OUTPUT RULE:
- Return ONLY raw HTML code.
- The response must start with <!DOCTYPE html>.
- Do NOT include explanations, comments, or markdown formatting.""")
        
        
        clean_bs64 = bs64_image.replace("\n", "").replace("\r", "")
        image_data_url = f"data:image/jpeg;base64,{clean_bs64}"
        #each llm has its own diffrent payload format check respectively and temperature sets the creativity. here gemini
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": bs64_image.strip() # No 'data:image/jpeg' prefix needed here!
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.1,
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
            raw_html = data['candidates'][0]['content']['parts'][0]['text']
            return raw_html.replace("```html", "").replace("```", "").strip()#cleaning the extra markdowns





    