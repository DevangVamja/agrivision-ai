import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from src.inference.plant_disease_predictor import (
    PlantDiseasePredictor,
)


MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "plantvillage_efficientnetb0.keras"
)

CLASS_MAPPING_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "plantvillage"
    / "class_mapping.csv"
)

TEST_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "plantvillage"
    / "test.csv"
)

def main():
    predictor = PlantDiseasePredictor(
        model_path=MODEL_PATH,
        class_mapping_path=CLASS_MAPPING_PATH,
    )

    print("Model loaded successfully.")
    print(
        f"Number of classes: "
        f"{len(predictor.class_names)}"
    )

    test_df = pd.read_csv(TEST_DATA_PATH)

    sample = test_df.iloc[0]

    image_path = (
        PROJECT_ROOT / sample["image_path"]
    )

    result = predictor.predict(image_path)

    print("\nInference result:")
    print(f"True class:      {sample['class_name']}")
    print(f"Predicted class: {result['class_name']}")
    print(f"Confidence:      {result['confidence']:.4f}")


if __name__ == "__main__":
    main()