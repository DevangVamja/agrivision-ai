# Data

This directory contains data-related documentation and processed
artifacts for the AgriVision AI project.

Large datasets are intentionally not stored in the Git repository.

---

## Current Data Sources

### 1. PlantVillage

**Purpose:** Plant disease classification and computer vision.

Source:

https://github.com/spMohanty/PlantVillage-Dataset

The official PlantVillage repository is maintained separately from
the AgriVision AI repository.

For the current computer vision pipeline, we use:

- Color images
- 54,304 images
- 38 classes
- 14 crop types

The current dataset contains no missing image paths.

### Dataset structure

```text
PlantVillage-Dataset/
└── raw/
    └── color/
        ├── Apple___Apple_scab/
        ├── Apple___Black_rot/
        ├── Apple___healthy/
        └── ...