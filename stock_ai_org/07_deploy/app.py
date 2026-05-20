from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import datetime

app = FastAPI(
    title="stock_ai_org - MVP Core API v1.1",
    description="エージェント制御およびパイプライン駆動用コアインターフェース"
)

class PaperRegistryRequest(BaseModel):
    paper_id: str
    title: str
    arxiv_url: str
    category: str

class SignalExecutionRequest(BaseModel):
    run_id: str
    ticker: str
    signal_type: str
    confidence_score: float

@app.post("/api/v1/research/register", status_code=201)
async def register_paper(payload: PaperRegistryRequest):
    return {
        "status": "success",
        "registered_id": payload.paper_id,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.post("/api/v1/pipeline/trigger")
async def trigger_reproduction_pipeline(paper_id: str, background_tasks: BackgroundTasks):
    return {
        "status": "pipeline_initiated",
        "target_paper_id": paper_id,
        "detail": "reproduce_agent & trainer_agent assigned."
    }

@app.post("/api/v1/trade/signal")
async def receive_trading_signal(payload: SignalExecutionRequest):
    if payload.confidence_score < 0.6:
        raise HTTPException(status_code=400, detail="Confidence score too low for execution.")
    return {
        "status": "signal_processed",
        "action": payload.signal_type,
        "kpi_check": "Sharpe > 1.5 Target evaluation triggered"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
