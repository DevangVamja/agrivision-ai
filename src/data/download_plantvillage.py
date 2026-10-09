"""
PlantVillage dataset setup.

This script does NOT download the dataset if it is already available locally.

Expected local dataset:
    PlantVillage-Dataset/raw/color/

If the dataset is missing, the script prints the official
source and instructions.
"""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_DIR = PROJECT_ROOT / "PlantVillage-Dataset"
COLOR_DIR = DATASET_DIR / "raw" / "color"

REPOSITORY_URL = (
    "https://github.com/spMohanty/PlantVillage-Dataset.git"
)


def dataset_exists() -> bool:
    """Check whether the actual color images are available."""

    if not COLOR_DIR.exists():
        return False

    class_directories = [
        path for path in COLOR_DIR.iterdir()
        if path.is_dir()
    ]

    return len(class_directories) > 0


def count_images() -> int:
    """Count JPG/JPEG images in the color dataset."""

    extensions = {
        ".jpg",
        ".jpeg",
        ".JPG",
        ".JPEG",
    }

    return sum(
        1
        for path in COLOR_DIR.rglob("*")
        if path.is_file()
        and path.suffix in extensions
    )


def clone_dataset() -> None:
    """Clone the official PlantVillage repository."""

    print("\nPlantVillage dataset was not found.")
    print("The official repository will be cloned.")
    print(f"\nSource: {REPOSITORY_URL}\n")

    try:

        subprocess.run(
            [
                "git",
                "clone",
                REPOSITORY_URL,
                str(DATASET_DIR),
            ],
            check=True,
        )

    except subprocess.CalledProcessError:
        print("\nERROR: Git clone failed.")
        print(
            "Please clone the repository manually using:"
        )
        print(
            f"\ngit clone {REPOSITORY_URL}\n"
        )
        sys.exit(1)


def main():

    print("=" * 60)
    print("AgriVision AI - PlantVillage Dataset Setup")
    print("=" * 60)

    print(f"\nProject root:")
    print(PROJECT_ROOT)

    print("\nChecking local PlantVillage dataset...")

    if dataset_exists():

        image_count = count_images()

        print("\n✓ PlantVillage dataset already exists.")
        print(f"✓ Location: {COLOR_DIR}")
        print(f"✓ Color images found: {image_count:,}")

        print(
            "\nNo download required."
        )

        return

    print("\nLocal dataset not found.")

    clone_dataset()

    if dataset_exists():

        image_count = count_images()

        print("\n✓ Dataset successfully installed.")
        print(f"✓ Color images found: {image_count:,}")

    else:

        print(
            "\nERROR: Dataset repository was cloned, "
            "but raw/color was not found."
        )

        sys.exit(1)


if __name__ == "__main__":
    main()