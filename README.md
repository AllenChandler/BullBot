# BullBot Data Processing Pipeline

## Overview

The **BullBot Data Processing Pipeline** is designed to streamline the preprocessing, analysis, and preparation of stock market data for machine learning models. This repository provides tools to fetch, clean, calculate metrics, and identify pre-spike and non-spike data patterns across multiple ticker symbols and timelines.

The goal is to create high-quality datasets for training, validation, and testing stock market prediction models.

### Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Directory Structure](#directory-structure)  
4. [Installation](#installation)  
   - [Prerequisites](#prerequisites)  
   - [Setup](#setup)  
5. [Usage](#usage)  
   - [Fetch Data](#fetch-data)  
   - [Clean Data](#clean-data)  
   - [Calculate Metrics](#calculate-metrics)  
   - [Detect Spikes](#detect-spikes)  
   - [Detect Non-Spikes](#detect-non-spikes)  
   - [Combine Tickers](#combine-tickers)  
6. [Example Workflow](#example-workflow)  
7. [Configuration](#configuration)  
8. [Next Steps](#next-steps)  
   - [Model Training](#1-model-training)  
   - [Validation & Testing](#2-validation--testing)  
   - [Real-Time Prediction](#3-real-time-prediction)  
9. [Issues & Resolutions](#issues--resolutions)  
10. [License](#license)  
11. [Contribution](#contribution)  

---

## Features

- **Automated Data Fetching**:
  - Downloads minute-by-minute stock market data from an S3 bucket.
  - Supports decompression of `.gz` files into `.csv` format.
  
- **Comprehensive Data Cleaning**:
  - Handles missing values, invalid timestamps, and non-numeric data.
  - Validates and filters essential columns like `close` and `window_start`.

- **Metric Calculation**:
  - Adds advanced technical indicators (e.g., VWAP, RSI, MACD, Bollinger Bands).
  - Prepares data for detailed analysis.

- **Spike and Non-Spike Detection**:
  - Identifies pre-spike patterns with adjustable thresholds and back-off times.
  - Finds non-spike patterns for realistic model training.

- **Ticker-Specific Continuous Timelines**:
  - Merges daily CSVs into continuous datasets for each ticker symbol.

---

## Directory Structure

E:/projects/BullBot/
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   │   ├── kaggle/
│   │   ├── polygon/
│   │   └── store/
│   └── polygon/
│       ├── clean/
│       │   └── store/
│       ├── continuous/
│       │   └── store/
│       ├── metrics/
│       │   └── store/
│       ├── processed/
│       │   ├── live_test/
│       │   │   ├── non_spikes/
│       │   │   └── spikes/
│       │   ├── test/
│       │   │   ├── non_spikes/
│       │   │   └── spikes/
│       │   ├── train/
│       │   │   ├── non_spikes/
│       │   │   └── spikes/
│       │   └── val/
│       │       ├── non_spikes/
│       │       └── spikes/
│       └── raw/
│           └── store/
│
├── models/
│   ├── live_test/
│   ├── test/
│   ├── train/
│   └── val/
│
├── notebooks/
│
├── results/
│   ├── test_results/
│   └── validation_results/
│
├── src/
│   ├── preprocessing/
│   │   ├── clean_polygon.py
│   │   ├── continuous_polygon.py
│   │   ├── delete_csv_polygon.py
│   │   ├── fetch_polygon.py
│   │   ├── metrics_polygon.py
│   │   └── spikes_polygon.py
│   ├── testing/
│   │   ├── short_spike_live_test.py
│   │   └── spike_test_polygon.py
│   ├── training/
│   │   └── spike_train_polygon.py
│   ├── validation/
│   │   └── spike_val_polygon.py
│   ├── api_test.py
│   ├── delete_behavior_csvs.py
│   ├── reset_model.py
│   ├── utils.py
│   └── __init__.py
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_data_preprocessing.py
│   ├── test_feature_engineering.py
│   └── __init__.py
│
└── README.md


---

## Installation

### Prerequisites

- Python 3.10+
- `pip` or `conda` for dependency management

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/BullBot.git
   cd BullBot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv BullBot_env
   source BullBot_env/bin/activate  # Linux/Mac
   BullBot_env\Scripts\activate    # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up directory structure**:
   Ensure the `data/polygon` folder and its subdirectories exist before running the scripts.

---

## Usage

### Fetch Data
Fetch stock market data from S3 and decompress it:
```bash
python src/fetch_data.py
```

### Clean Data
Clean and validate the raw data:
```bash
python src/clean_polygon.py
```

### Calculate Metrics
Generate advanced technical metrics:
```bash
python src/metrics_polygon.py
```

### Detect Spikes
Identify pre-spike patterns:
```bash
python src/spikes_polygon.py
```

### Detect Non-Spikes
Identify non-spike patterns:
```bash
python src/non_spikes_polygon.py
```

### Combine Tickers
Create continuous timelines for each ticker:
```bash
python src/combine_tickers.py
```

---

## Example Workflow

1. Fetch raw stock market data:
   ```bash
   python src/fetch_data.py
   ```
2. Clean the downloaded data:
   ```bash
   python src/clean_polygon.py
   ```
3. Calculate metrics for analysis:
   ```bash
   python src/metrics_polygon.py
   ```
4. Identify pre-spike datasets:
   ```bash
   python src/spikes_polygon.py
   ```
5. Identify non-spike datasets:
   ```bash
   python src/non_spikes_polygon.py
   ```
6. Combine tickers into continuous datasets:
   ```bash
   python src/combine_tickers.py
   ```

---

## Configuration

- Adjust parameters in the individual scripts:
  - `spike_threshold` (default: `0.30`) in `spikes_polygon.py`.
  - `spike_window_minutes` (default: `120`) in `spikes_polygon.py` and `non_spikes_polygon.py`.

- Update file paths in `src/` scripts if needed.

---

## Next Steps

### 1. Model Training
- Prepare the training pipeline to use pre-spike and non-spike datasets.
- Incorporate machine learning frameworks like TensorFlow or PyTorch.

### 2. Validation & Testing
- Use continuous ticker timelines for robust validation.
- Test the model on unseen data.

### 3. Real-Time Prediction
- Connect the trained model to live API feeds for real-time spike predictions.

---

## Issues & Resolutions

1. **Incomplete Spike Data**:
   - Solution: Added logic to include rows from the previous day if spikes occurred early.

2. **Handling Non-Numeric Columns**:
   - Solution: Validation checks for required columns (`ticker`, `close`, `window_start`) in every script.

3. **Heavy Computation**:
   - Solution: Modularized scripts to allow targeted execution.

---

## License

[MIT License](LICENSE)

---

## Contribution

We welcome contributions to the BullBot Data Processing Pipeline! Whether it's reporting issues, suggesting features, or submitting pull requests, your input is valuable.

How to Contribute
Report Bugs: Use the GitHub Issues page to report bugs or feature requests.
Fork and Submit PRs: Fork the repository, make your changes, and submit a pull request for review.
Suggest Enhancements: Contact us directly with your ideas or feedback.
Contact Information
GitHub: @AllenChandler
X: @WonMoreWave
LinkedIn: https://www.linkedin.com/in/allenjchandler
Email: allenjchandler@gmail.com
       allen@shiftedorigin.com
Feel free to reach out with any questions or suggestions. Thank you for helping make BullBot even better!
