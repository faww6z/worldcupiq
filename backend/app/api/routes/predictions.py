from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PredictionResponse
from app.services.prediction_service import get_prediction_for_match, regenerate_prediction_for_match

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("/{match_id}", response_model=PredictionResponse)
def get_prediction(match_id: int, db: Session = Depends(get_db)) -> PredictionResponse:
    prediction = get_prediction_for_match(db, match_id)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return prediction


@router.post("/generate/{match_id}", response_model=PredictionResponse)
def generate_prediction(match_id: int, db: Session = Depends(get_db)) -> PredictionResponse:
    prediction = regenerate_prediction_for_match(db, match_id)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return prediction
