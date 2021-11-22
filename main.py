import os
import time
import json
from urllib import parse
import uvicorn
from typing import Optional
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()


ZOOM_OAUTH_AUTHORIZE_API = 'https://zoom.us/oauth/authorize?response_type=code'

ZOOM_TOKEN_API = 'https://zoom.us/oauth/token?grant_type=authorization_code'


@app.get("/")
def get_token(code: Optional[str] = None):
    try:
        if code:
            redirect_url = os.environ.get("redirectURL")
            url = ZOOM_TOKEN_API + "&code=" + code + "&redirect_uri=" + parse.quote_plus(redirect_url)

            response = requests.post(url=url, auth=(os.environ.get("clientID"), os.environ.get('clientSecret')))

            if response.status_code == 200:
                response_json = response.json()
                with open('credential.json', 'w') as f:
                    json.dump(response_json, f)
                return response_json
            else:
                return HTTPException(status_code=500, detail="fail to get auth code")
        else:
            return RedirectResponse(ZOOM_OAUTH_AUTHORIZE_API + '&client_id=' + os.environ.get(
                "clientID") + '&redirect_uri=' + os.environ["redirectURL"])

    except Exception as e:
        return HTTPException(status_code=500, detail=e.__str__())

def main():
    uvicorn.run(
            "main:app",
            port=8000
    )

if __name__ == "__main__":
    main()
