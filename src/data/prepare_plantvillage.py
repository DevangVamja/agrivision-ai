"""
Prepare PlantVillage metadata for AgriVision AI.

The original PlantVillage images remain in:

    PlantVillage-Dataset/raw/color/

This script does NOT duplicate the images.

Instead, it creates metadata describing:
    - image path
    - crop
    - disease/health status
    - class name
    - class ID
"""

from pathlib import Path
import json

import pandas as pd
from PIL import Image


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_DIR = (
    PROJECT_ROOT
    / "PlantVillage-Dataset"
    / "raw"
    / "color"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "plantvillage"
)


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".JPG",
    ".JPEG",
}


# --------------------------------------------------
# Dataset discovery
# --------------------------------------------------

def get_class_directories():

    if not SOURCE_DIR.exists():

        raise FileNotFoundError(
            "\nPlantVillage color dataset was not found.\n"
            f"Expected location:\n{SOURCE_DIR}\n\n"
            "Run:\n"
            "python src/data/download_plantvillage.py"
        )

    directories = sorted(
        [
            path
            for path in SOURCE_DIR.iterdir()
            if path.is_dir()
        ]
    )

    if not directories:

        raise RuntimeError(
            f"No class directories found in {SOURCE_DIR}"
        )

    return directories


# --------------------------------------------------
# Parse class name
# --------------------------------------------------

def parse_class_name(class_name):

    """
    Example:

        Apple___Black_rot

    becomes:

        crop   = Apple
        status = Black_rot
    """

    parts = class_name.split("___")

    crop = parts[0]

    condition = (
        parts[1]
        if len(parts) > 1
        else "unknown"
    )

    return crop, condition


# --------------------------------------------------
# Find images
# --------------------------------------------------

def build_metadata():

    class_directories = get_class_directories()

    records = []

    classes = sorted(
        directory.name
        for directory in class_directories
    )
    
    class_to_id = {
        class_name: class_id
        for class_id, class_name
        in enumerate(classes)
    }

    print(
        f"Found {len(classes)} classes."
    )

    for class_directory in class_directories:

        class_name = class_directory.name

        crop, condition = parse_class_name(
            class_name
        )

        class_id = class_to_id[class_name]

        images = [
            path
            for path in class_directory.iterdir()
            if (
                path.is_file()
                and path.suffix in SUPPORTED_EXTENSIONS
            )
        ]

        for image_path in images:

            records.append(
                {
                    "image_path": str(
                        image_path.relative_to(
                            PROJECT_ROOT
                        )
                    ),
                    "class_id": class_id,
                    "class_name": class_name,
                    "crop": crop,
                    "condition": condition,
                }
            )

    return pd.DataFrame(records), class_to_id


# --------------------------------------------------
# Validate images
# --------------------------------------------------

def validate_images(df):

    valid_records = []
    corrupted_records = []

    total = len(df)

    print(
        f"\nValidating {total:,} images..."
    )

    for index, row in df.iterrows():

        image_path = (
            PROJECT_ROOT
            / row["image_path"]
        )

        try:

            with Image.open(image_path) as image:

                image.verify()

            valid_records.append(row)

        except Exception as error:

            corrupted_records.append(
                {
                    "image_path": row["image_path"],
                    "error": str(error),
                }
            )

        if (
            (index + 1) % 5000 == 0
            or index + 1 == total
        ):

            print(
                f"Progress: "
                f"{index + 1:,}/{total:,}"
            )

    valid_df = pd.DataFrame(
        valid_records
    )

    corrupted_df = pd.DataFrame(
        corrupted_records
    )

    return valid_df, corrupted_df


# --------------------------------------------------
# Statistics
# --------------------------------------------------

def create_statistics(df):

    statistics = {

        "total_images": int(len(df)),

        "total_classes": int(
            df["class_name"].nunique()
        ),

        "total_crops": int(
            df["crop"].nunique()
        ),

        "classes": sorted(
            df["class_name"].unique().tolist()
        ),

        "crops": sorted(
            df["crop"].unique().tolist()
        ),

        "images_per_class": {
            str(key): int(value)
            for key, value
            in df["class_name"]
            .value_counts()
            .to_dict()
            .items()
        },

        "images_per_crop": {
            str(key): int(value)
            for key, value
            in df["crop"]
            .value_counts()
            .to_dict()
            .items()
        },
    }

    return statistics


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("AgriVision AI")
    print("PlantVillage Preparation Pipeline")
    print("=" * 60)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ----------------------------------------------
    # Build metadata
    # ----------------------------------------------

    df, class_to_id = build_metadata()

    print(
        f"\nTotal images discovered: "
        f"{len(df):,}"
    )

    # ----------------------------------------------
    # Validate
    # ----------------------------------------------

    valid_df, corrupted_df = validate_images(df)

    print(
        f"\nValid images: "
        f"{len(valid_df):,}"
    )

    print(
        f"Corrupted images: "
        f"{len(corrupted_df):,}"
    )

    # ----------------------------------------------
    # Save metadata
    # ----------------------------------------------

    metadata_path = (
        OUTPUT_DIR / "metadata.csv"
    )

    valid_df.to_csv(
        metadata_path,
        index=False
    )

    print(
        f"\n✓ Metadata:"
        f"\n  {metadata_path}"
    )

    # ----------------------------------------------
    # Class mapping
    # ----------------------------------------------

    mapping_df = pd.DataFrame(
        [
            {
                "class_id": class_id,
                "class_name": class_name,
            }
            for class_name, class_id
            in sorted(
                class_to_id.items(),
                key=lambda item: item[1],
            )
        ]
    )

    mapping_path = (
        OUTPUT_DIR / "class_mapping.csv"
    )

    mapping_df.to_csv(
        mapping_path,
        index=False
    )

    print(
        f"✓ Class mapping:"
        f"\n  {mapping_path}"
    )

    # ----------------------------------------------
    # Corrupted images
    # ----------------------------------------------

    corrupted_path = (
        OUTPUT_DIR
        / "corrupted_images.csv"
    )

    corrupted_df.to_csv(
        corrupted_path,
        index=False
    )

    print(
        f"✓ Corrupted image report:"
        f"\n  {corrupted_path}"
    )

    # ----------------------------------------------
    # Statistics
    # ----------------------------------------------

    statistics = create_statistics(
        valid_df
    )

    statistics_path = (
        OUTPUT_DIR
        / "dataset_statistics.json"
    )

    with open(
        statistics_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            statistics,
            file,
            indent=4
        )

    print(
        f"✓ Dataset statistics:"
        f"\n  {statistics_path}"
    )

    print("\n" + "=" * 60)
    print("Preparation completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()