from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from index import get_multihop_rag_model

app = FastAPI()
chat = get_multihop_rag_model()

# CORS POLICY
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_rag_inference")
async def get_rag_inference( prompt: str):
    try:
        chat_model_inference= chat.get_inference(prompt=prompt)
        return {"status": "200", 
                "message": "Successfully fetched the inference from the multi-hop rag model",
                 "success": True,
                 "data" : chat_model_inference
                 }
    except Exception as exp:
        print(exp)
        return {"status": "500", "message": "Internal Server Error", "success": False }
