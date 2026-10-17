from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model


IMG_SIZE = (256, 256)


class PlantDiseasePredictor:
    def __init__(self, model_path, class_mapping_path):
        self.model = load_model(model_path)

        class_mapping = pd.read_csv(
            class_mapping_path
        ).sort_values("class_id")

        self.class_names = (
            class_mapping["class_name"]
            .tolist()
        )

        if self.model.output_shape[-1] != len(
            self.class_names
        ):
            raise ValueError(
                "Model output classes do not match "
                "the class mapping."
            )

    def preprocess_image(self, image_path):
        image_bytes = tf.io.read_file(
            str(image_path)
        )

        image = tf.image.decode_jpeg(
            image_bytes,
            channels=3,
        )

        image = tf.image.resize(
            image,
            IMG_SIZE,
        )

        image = tf.cast(
            image,
            tf.float32,
        )

        return tf.expand_dims(
            image,
            axis=0,
        )

    def predict(self, image_path):
        image = self.preprocess_image(
            image_path
        )

        probabilities = self.model.predict(
            image,
            verbose=0,
        )[0]

        predicted_index = int(
            np.argmax(probabilities)
        )

        confidence = float(
            probabilities[predicted_index]
        )

        return {
            "class_id": predicted_index,
            "class_name": self.class_names[
                predicted_index
            ],
            "confidence": confidence,
        }