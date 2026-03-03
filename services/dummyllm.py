import html
from helpers_decorator.retry import async_retry
from configs import settings

class LLM_work():
    async def llm_generation(self, bs64_image, ocr_text : str="") -> str :
        safetext = html.escape(ocr_text)
        print(safetext)
        return f"""
    <html>
      <head><script src="https://cdn.tailwindcss.com"></script></head>
      <body class="bg-gray-100 flex items-center justify-center h-screen">
        <h1 class="text-4xl font-bold text-blue-600">AI Pipeline Test Successful!</h1>
        <p class="text-lg text-gray-700 whitespace-pre-wrap">
                {safetext}
              </p>
        <h1 class="text-4xl font-bold text-blue-600"> extracted from image !</h1>
      </body>
    </html>
    """
            