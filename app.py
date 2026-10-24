import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

# Project root
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables before importing project modules
load_dotenv(BASE_DIR / ".env")

# Use the same variable name as Data Ingestion
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    raise RuntimeError(
        "MONGO_DB_URL is missing. Check your .env configuration."
    )

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


app = FastAPI()

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
def train_route():
    """
    Run the complete training pipeline.
    """
    try:
        logging.info("Starting the training pipeline")

        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()

        logging.info("Training pipeline completed successfully")

        return {"message": "Training completed successfully"}

    except Exception as e:
        logging.exception("Training pipeline failed")
        raise NetworkSecurityException(e, sys) from e


@app.post("/predict")
async def predict_route(
    request: Request,
    file: UploadFile = File(...)
):
    """
    Read a CSV file and generate predictions.
    """
    try:
        # Read uploaded CSV
        df = pd.read_csv(file.file)

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="The uploaded CSV file is empty."
            )

        # Load saved preprocessing object and trained model
        preprocessor_path = BASE_DIR / "final_model" / "preprocessor.pkl"
        model_path = BASE_DIR / "final_model" / "model.pkl"

        if not preprocessor_path.is_file():
            raise HTTPException(
                status_code=503,
                detail="Preprocessor not found. Train the model first."
            )

        if not model_path.is_file():
            raise HTTPException(
                status_code=503,
                detail="Trained model not found. Train the model first."
            )

        preprocessor = load_object(str(preprocessor_path))
        final_model = load_object(str(model_path))

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=final_model
        )

        # Generate predictions
        predictions = network_model.predict(df)

        df["predicted_column"] = predictions

        # Save prediction output
        output_dir = BASE_DIR / "prediction_output"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / "output.csv"

        df.to_csv(output_path, index=False)

        logging.info("Prediction completed successfully")

        # Display results in the HTML template
        table_html = df.to_html(
            classes="table table-striped",
            index=False
        )

        return templates.TemplateResponse(
            request=request,
            name="table.html",
            context={"table": table_html}
        )

    except HTTPException:
        raise

    except Exception as e:
        logging.exception("Prediction failed")
        raise NetworkSecurityException(e, sys) from e

    finally:
        await file.close()


if __name__ == "__main__":
    app_run(
        app,
        host="127.0.0.1",
        port=8000
    )