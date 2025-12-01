# 🍱 BentoML - University Score

This repository contains a BentoML service that predicts the likelihood of student admission to a university based on various features.

## 📊 Data:

- **GRE Score**: Score obtained on the GRE test (scored out of 340)
- **TOEFL Score**: Score obtained on the TOEFL test (scored out of 120)
- **University Rating**: University rating (scored out of 5)
- **SOP**: Statement of Purpose (scored out of 5)
- **LOR**: Letter of Recommendation (scored out of 5)
- **CGPA**: Cumulative Grade Point Average (scored out of 10)
- **Research**: Research experience (0 or 1)
- **Chance of Admit**: Chance of admission (scored out of 1)

## 📦 Installation

1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
2. Get dependencies and activate the virtual environment:

   ````
    uv sync
    source .venv/bin/activate
   ````
 ## 🚀 Usage

Use the Makefile to prepare data, train the model, and start the BentoML API server:
- `make load_data`: downloads the raw data
- `make prepare_data`: prepares the data for training
- `make train_model`: trains the machine learning model
- `make start_api`: starts the BentoML API server (use a separate terminal)


## 🧪 Testing

Run `python tests/test_request.py` to test the API endpoints.