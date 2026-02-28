from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class CommentRequest(BaseModel):
    comment: str

positive_words = [
    "good", "great", "excellent", "amazing", "love",
    "awesome", "fantastic", "perfect", "happy"
]

negative_words = [
    "bad", "terrible", "awful", "hate", "worst",
    "poor", "disappointed", "angry", "horrible"
]

@app.post("/comment")
async def analyze_comment(request: CommentRequest):
    text = request.comment.lower().strip()

    if not text:
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    pos_score = sum(word in text for word in positive_words)
    neg_score = sum(word in text for word in negative_words)

    if pos_score > neg_score:
        sentiment = "positive"
        rating = min(5, 3 + pos_score)
    elif neg_score > pos_score:
        sentiment = "negative"
        rating = max(1, 3 - neg_score)
    else:
        sentiment = "neutral"
        rating = 3

    return JSONResponse(
        content={
            "sentiment": sentiment,
            "rating": rating
        },
        media_type="application/json"
    )