from fastapi import FastAPI, Request, Query, HTTPException , APIRouter, UploadFile, File
import json
import os
import uuid
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
#from dotenv import load_dotenv
import uvicorn
import httpx
import cv2
import base64
import asyncio
import numpy as np
import shutil
import logging
from bs4 import BeautifulSoup
from services.image_service import images # importing the class 
from services.ocr_text import ocr_service
from services.llm_service import lLM_work
from services.github_service import github_class
from services.cheating import lLM_cheat
from configs import settings


class DeploymentResponse(BaseModel): # pydantic schemas this all will be returned finally as json
    repo_url : str
    pages_url : str
    status :str

class ErrorResponse(BaseModel): #how errors shall be coming 
    err : str


app = FastAPI(title = "UI generator and deployer")
api_url = ""
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) # to ensure if the uploaded directory is there to hold uploads
logger = logging.getLogger('Ui_generator_deployer..')


router = APIRouter()


# sanitizer function 
def sanitizer(html_content: str) -> str :
    soup = BeautifulSoup(html_content, "html.parser")
      #to remove the scripts and tags froms the raw html
    for tags in soup(["script", "iframe", "object", "embed"]):  #removing the these tags to avoid xss attacks
        tags.decompose()

    # removing the event handelers
    for tags in soup.find_all(True):
        attrs = dict(tags.attrs) #stores event attributes into the dictionary like Example: <button onclick="alert(1)"> → {"onclick": "alert(1)"}.
        for attr in attrs:
            if attr.startswith("on"): #Examples: onclick, onload, onmouseover are potential javascript event handelers
                del tags[attr]  # deleting such tags thus deleting inline execution
    
    # Ensure <head> tags exists in the biggining
    head = soup.find("head")
    if not head:
        head = soup.new_tag("head")
        soup.insert(0, head)

    # ensuring if the tailwind css cdn exists in the file first
    tailwind = soup.new_tag("script", src="https://cdn.tailwindcss.com")
    head.append(tailwind)
    return str(soup)


# validator function to make sure our llm output is not gibbrish 

def validation(stuff: str) -> bool:
    if not stuff or len(stuff) < 150: # Increased min-length for a full HTML file
        return False
        
    soop = BeautifulSoup(stuff, "html.parser")
    
    # Check for body OR at least a div (sometimes models skip body in snippets)
    has_structure = bool(soop.find("body")) or bool(soop.find("div"))
    
    # Check for any common Tailwind CDN pattern (v3 or v4)
    has_tailwind = any(term in stuff.lower() for term in ["tailwindcss", "cdn.tailwindcss", "@tailwindcss/browser"])
    
    return has_structure and has_tailwind





@app.get("/")
async def health():
    return {"status":"jinda hai"}

@app.post("/generate" , response_model= None)
async def generate_ui(figma: UploadFile = File(...)):  # File(...). for user input or upload 

    if not figma.content_type.startswith('image/'): #checks the uploaded figma image type 
        raise HTTPException(400, "the file must be a image type")
    
    content = await figma.read() # to store the contents of the file 

    # processing the image by using the image process function
    bs64image =images.process_and_encode(content)

    

    # optical charecter recognition service for extracting the useful texts 
    extraction = ocr_service.text_extraction(content)

    # llm generating the page contents
    ai = lLM_work()
    figma_html = await ai.llm_generation(bs64image, extraction)

    # cleaning the raw html code into proper format , basically sanitization and validation
    sanitized = sanitizer(figma_html)

    #if not validation(sanitized) :
        #raise HTTPException(500,"generated html not looking good king :( ")



    # deploying the page on github

    repo_name = f"ui-gen-{uuid.uuid4().hex[:8]}" # to generate unique name for ui code repo like  ui-gen-blahblah 
    github = github_class()
    result = await github.deploye(repo_name, sanitized)
    
    #can be seen in jason response body in postman or fastapi docs not on terminal
    return {
        "repo_url": result["repo_url"],
        "pages_url": result["pages_url"],
        "ocr_text": extraction
    }
    


@app.delete("/delete_repo/{repo_name}")
async def delete_repo(repo_name: str):
    github = github_class()
    return await github.delete(repo_name)


# api endpoint for testing the ocr from the uploaded file 
@app.post("/ocrtext")    
async def ocr_text(img : UploadFile = File(...)):
    if not img.content_type.startswith('image/'): #checks the uploaded figma image type 
        raise HTTPException(400, "the file must be a image type")
    
    content = await img.read() # to store the contents of the file 
    

    # optical charecter recognition service for extracting the useful texts 
    extraction = ocr_service.text_extraction(content)
    
    
    cheating_ai = lLM_cheat()
    answer = await cheating_ai.answered( extraction)

    return {
        "ocr_text": extraction,
        "answer": answer
    }



