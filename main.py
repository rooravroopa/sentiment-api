from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CommentRequest(BaseModel):
    comment: str

response_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "sentiment_response",
        "schema": {
            "type": "object",
            "properties": {
                "sentiment": {
                    "type": "string",
                    "enum": ["positive", "negative", "neutral"]
                },
                "rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5
                }
            },
            "required": ["sentiment", "rating"],
            "additionalProperties": False
        }
    }
}

@app.post("/comment")
async def analyze_comment(req: CommentRequest):
    if not req.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
Classify sentiment as positive, negative, or neutral.
Return rating 1–5:
5 = highly positive
4 = positive
3 = neutral
2 = negative
1 = highly negative

Comment: {req.comment}
""",
            response_format=response_schema
        )

        return response.output_parsed

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))