

# AgriVision AI

AgriVision AI is an end-to-end machine learning and data science
platform for agricultural intelligence.

The project combines computer vision, tabular machine learning,
data analysis, explainable AI, APIs, and eventually IoT/robotics
integration.

> Project status: Active development

---

## Vision

The goal of AgriVision AI is to create a unified agricultural
intelligence platform capable of:

- Detecting plant diseases from leaf images
- Predicting agricultural yield
- Analyzing environmental and agricultural data
- Providing explainable predictions
- Exposing ML models through APIs
- Providing an interactive analytics dashboard
- Eventually communicating with agricultural robotics and IoT devices

---

## Current Development

The project is being developed incrementally.

### Completed

- Project repository structure
- PlantVillage dataset setup
- PlantVillage metadata pipeline
- Image validation
- Dataset validation

### In Progress

- PlantVillage exploratory data analysis

### Planned

- Plant disease classification
- Transfer learning
- Model evaluation
- Explainable AI
- FAOSTAT data pipeline
- Weather data pipeline
- Agricultural yield prediction
- FastAPI backend
- Database integration
- React dashboard
- MLflow experiment tracking
- Automated testing
- Docker deployment
- Arduino/IoT integration

---

# Project Architecture

The planned architecture is:

```text
                    AgriVision AI
                         |
          +--------------+--------------+
          |                             |
          v                             v
   Computer Vision                 Tabular ML
          |                             |
   PlantVillage                  FAOSTAT + Weather
          |                             |
          v                             v
 Disease Classification            Yield Prediction
          |                             |
          +--------------+--------------+
                         |
                         v
                  ML/API Layer
                         |
          +--------------+--------------+
          |                             |
          v                             v
      Web Dashboard                 IoT/Robotics
                                      |
                                      v
                              Arduino / Sensors