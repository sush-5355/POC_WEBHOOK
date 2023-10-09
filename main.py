import asyncio
import json
from fastapi import FastAPI
import uvicorn
app = FastAPI()


@app.post('/logs')
async def logs(data:dict):
    print(json.dumps(data))
    return data

@app.get('/')
async def home():
    return dict(status = True,ms = 'Ek No')

if __name__ == "__main__":
    asyncio.run(uvicorn.run(app='main:app',host='localhost',port=8000,reload=True,ssl_keyfile='ss_webhook_key.pem',ssl_certfile='ss_webhook_cert.crt'))