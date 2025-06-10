# app/api/v1/endpoints/models.py
from fastapi import APIRouter, Depends, UploadFile, File
from app.services.ml.inference import ModelInferenceService
from app.models.schemas.models import PredictionRequest, PredictionResponse

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_traffic_signals(
    request: PredictionRequest,
    inference_service: ModelInferenceService = Depends(get_inference_service)
):
    """Generate traffic light timing predictions using MARL-RNN model."""
    predictions = await inference_service.predict(
        traffic_data=request.traffic_data,
        intersection_ids=request.intersection_ids,
        prediction_horizon=request.prediction_horizon
    )
    
    return PredictionResponse(
        predictions=predictions,
        confidence_scores=predictions.confidence,
        timestamp=datetime.utcnow()
    )

@router.post("/model/upload")
async def upload_model(
    file: UploadFile = File(...),
    inference_service: ModelInferenceService = Depends(get_inference_service)
):
    """Upload and deploy a new trained model."""
    if not file.filename.endswith(('.pkl', '.pt', '.h5')):
        raise HTTPException(status_code=400, detail="Invalid model file format")
    
    model_id = await inference_service.deploy_model(file)
    return {"model_id": model_id, "status": "deployed"}


@app.post("/simulation/start")
async def start_simulation(config_id: str):
    config_path = f"configs/{config_id}.sumocfg"
    try:
        init_sumo_simulation(config_path)
        return {"status": "Simulation started", "config_id": config_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start simulation: {str(e)}")
    
    
    
    def load_marl_model(model_path: str = "models/marl_rnn.pt"):
    model = MARL_RNN_Model()  # Model class definition
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cuda" if torch.cuda.is_available() else "cpu")))
    model.eval()  # Set to inference mode
    return model


interface TrafficData {
  vehicleCount: number;
  queueLength: number;
}

const useTrafficWebSocket = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    const ws = new WebSocket('ws://backend-api/ws/traffic');
    ws.onmessage = (event) => {
      const data: TrafficData = JSON.parse(event.data);
      dispatch(updateTrafficState(data));
    };
    return () => ws.close();
  }, [dispatch]);
};

export default useTrafficWebSocket;