#look for the documentation on the github automation in python how to push pull or commit repos   and how to cook these payloads 

import httpx
import base64
from configs import settings # settings class
from helpers_decorator.retry import async_retry

class github_class:
    def __init__(self):    #  the purpose was to setup header for every github api call    read github header docs ..
        self.header = { "Authorization": f"token {settings.GITHUB_TOKEN}", 
                       "Accept": "application/vnd.github+json",  # to tell github that we expec json response
                       "X-GitHub-Api-Version": "2022-11-28"   # for stablity remove if cause trouble 
                       }
    @async_retry(retries = 1, base_delay = 2) #custom decorater to retry this process
    async def deploye(self, repo_name: str, figma_html: str) -> str:
            github_baseAPI = settings.GITHUB_API_BASE
            github_username = settings.GITHUB_USERNAME
            async with httpx.AsyncClient() as client:   # my browser robot to interact with websites and carry out tasks as "client"

                # step1  creating the repository 
               
                repo_response = await client.post(
                    f"{github_baseAPI}/user/repos",
                    json= {"name": repo_name, "auto_init": True, "private": False}, 
                    headers=self.header
                )
                print(repo_response.status_code)
                print(repo_response.text)

                #step2 push code 
                file_url = f"{github_baseAPI}/repos/{github_username}/{repo_name}/contents/index.html" # basically uploads on this repo link
                content_b64 = base64.b64encode(figma_html.encode()).decode() #converts the html file to base64 encode for github
                await client.put( #put for uploading the file
                    file_url,
                    json={"message": "Initial UI generation", "content": content_b64},
                    headers =self.header 
                    )
                
                

                #step3 enable pages
                await client.post(
                    f"{github_baseAPI}/repos/{github_username}/{repo_name}/pages",
                    json={"source": {"branch": "main", "path": "/"}},
                    headers=self.header
                    )
                
                return {
                "repo_url": f"https://github.com/{github_username}/{repo_name}",  #github code repo link 
                "pages_url": f"https://{github_username}.github.io/{repo_name}/" # website url
            }
    async def delete(self, repo_name: str) -> str:
        async with httpx.AsyncClient() as client:
            respons = await client.delete(
            f"https://api.github.com/repos/{settings.GITHUB_USERNAME}/{repo_name}",
            headers= self.header
        )
        print(respons.status_code, respons.text)
        print("repo deleted sucessfully")

             

