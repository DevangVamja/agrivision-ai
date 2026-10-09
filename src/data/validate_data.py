"""
Validate the local AgriVision AI datasets.

Currently validates the PlantVillage color dataset.
"""

from pathlib import Path

import pandas as pd
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_DIR = (
    PROJECT_ROOT
    / "PlantVillage-Dataset"
    / "raw"
    / "color"
)

METADATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "plantvillage"
    / "metadata.csv"
)


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".JPG",
    ".JPEG",
}


def validate_directory():

    print("=" * 60)
    print("PlantVillage Dataset Validation")
    print("=" * 60)

    if not SOURCE_DIR.exists():

        print(
            "\n❌ Dataset not found."
        )

        print(
            f"\nExpected:\n{SOURCE_DIR}"
        )

        print(
            "\nRun:"
        )

        print(
            "python src/data/download_plantvillage.py"
        )

        return False

    class_directories = [
        path
        for path in SOURCE_DIR.iterdir()
        if path.is_dir()
    ]

    print(
        f"\nClasses found: "
        f"{len(class_directories)}"
    )

    total_images = 0

    for directory in class_directories:

        count = sum(
            1
            for path in directory.iterdir()
            if (
                path.is_file()
                and path.suffix
                in SUPPORTED_EXTENSIONS
            )
        )

        print(
            f"{directory.name}: "
            f"{count:,}"
        )

        total_images += count

    print(
        f"\nTotal images: "
        f"{total_images:,}"
    )

    return True


def validate_metadata():

    print("\nChecking processed metadata...")

    if not METADATA_PATH.exists():

        print(
            "⚠ Metadata file does not exist."
        )

        print(
            "\nRun:"
        )

        print(
            "python src/data/prepare_plantvillage.py"
        )

        return False

    df = pd.read_csv(
        METADATA_PATH
    )

    required_columns = {
        "image_path",
        "class_id",
        "class_name",
        "crop",
        "condition",
    }

    missing = (
        required_columns
        - set(df.columns)
    )

    if missing:

        print(
            f"❌ Missing columns: {missing}"
        )

        return False

    print(
        f"✓ Metadata rows: {len(df):,}"
    )

    print(
        f"✓ Classes: "
        f"{df['class_name'].nunique()}"
    )

    print(
        f"✓ Crops: "
        f"{df['crop'].nunique()}"
    )

    # Check paths
    missing_files = 0

    for relative_path in df["image_path"]:

        image_path = (
            PROJECT_ROOT
            / relative_path
        )

        if not image_path.exists():

            missing_files += 1

    print(
        f"✓ Missing image files: "
        f"{missing_files:,}"
    )

    if missing_files == 0:

        print(
            "✓ All metadata paths are valid."
        )

    else:

        print(
            "❌ Some metadata paths are invalid."
        )

        return False

    return True


def main():

    directory_ok = (
        validate_directory()
    )

    if not directory_ok:
        return

    metadata_ok = (
        validate_metadata()
    )

    print("\n" + "=" * 60)

    if directory_ok and metadata_ok:

        print(
            "✓ DATASET VALIDATION PASSED"
        )

    else:

        print(
            "❌ DATASET VALIDATION FAILED"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()