# BullBot

BullBot is an AI-driven stock prediction platform that employs sophisticated machine learning algorithms to generate precise buy, sell, and hold alerts for various equities. It leverages historical stock data, performs extensive feature engineering, trains predictive models, and delivers actionable insights directly to users. BullBot's core objective is to alleviate the inherent complexity of trading decision-making by providing timely and data-backed information, thus enabling users to maintain a competitive edge in the financial markets and make informed investment decisions. Whether you are a seasoned investor or a novice in financial markets, BullBot equips you with the critical tools needed to navigate the complexities of the stock market confidently and precisely.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Data Loading](#data-loading)
  - [Data Preprocessing](#data-preprocessing)
  - [Data Behavior Preprocessing](#data-behavior-preprocessing)
  - [Feature Engineering](#feature-engineering)
  - [Model Training](#model-training)
  - [Model Evaluation](#model-evaluation)
  - [Making Predictions](#making-predictions)
- [Testing](#testing)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

BullBot is designed to empower traders and investors by utilizing advanced machine learning methodologies to predict stock price trajectories. By analyzing large datasets of historical market data and deriving meaningful features, BullBot constructs sophisticated predictive models that inform trading decisions. The application delivers buy, sell, and hold alerts through real-time data analysis, aiding investors in executing strategic actions in a dynamic and volatile market environment. BullBot is equipped to seamlessly process massive datasets and employs advanced analytical techniques to discover nuanced patterns that are often imperceptible to human traders. This capacity provides users with data-driven decision support that optimizes returns while mitigating risks, irrespective of market volatility.

## Features

- **Data Acquisition**: Utilizes Yahoo Finance to retrieve a comprehensive historical dataset of stock prices. The data acquisition ensures that users are provided with an expansive array of historical data points, facilitating the model's learning across diverse market conditions. Access to a comprehensive data corpus is critical for understanding stock behavior under varying economic scenarios, enhancing model robustness and accuracy.
- **Data Preprocessing**: Cleans and refines raw data for analysis, ensuring consistency, reliability, and noise reduction. This phase involves handling missing values, standardizing data formats, and calculating important metrics such as moving averages to make the dataset suitable for downstream analysis. Effective data preprocessing is foundational, as the quality of data directly impacts the efficacy of the predictive model and ensures enhanced model performance.
- **Data Behavior Preprocessing**: Extracts and categorizes stock price behaviors, including short-term spikes, short-term dips, sustained uptrends, and sustained downtrends. This step is instrumental in extracting data segments leading up to significant price movements, allowing the model to focus on precursors that signal such events. This capability allows BullBot to anticipate upcoming movements rather than react retrospectively, providing foresight for users. This kind of behavior-based data extraction is critical for building targeted models that can effectively capture unique price patterns and behaviors.
- **Feature Engineering**: Generates derived features and technical indicators to enrich the dataset. Feature engineering is pivotal in constructing a robust predictive model. By synthesizing informative features such as moving averages, volatility indices, and trend oscillators, the model gains a more comprehensive understanding of underlying patterns within stock price dynamics. This ultimately leads to enhanced predictive accuracy and the ability to generalize effectively across different market conditions.
- **Model Training**: Trains a diverse set of machine learning models to forecast future stock prices. The training process employs the historical and behavior-processed data to build models capable of providing accurate predictions regarding future market movements. BullBot supports various algorithms—including Random Forest, XGBoost, and deep learning models such as neural networks—allowing users to experiment and determine the optimal approach based on their unique trading strategies and preferences. This adaptability makes BullBot suitable for a broad spectrum of trading styles, from high-frequency to long-term investing.
- **Model Evaluation**: Assesses model performance using multiple quantitative metrics, such as Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R-squared. The model evaluation phase provides insights into model accuracy and reliability, guiding further refinement and optimization. Evaluation metrics are computed over training, validation, and test splits, and cross-validation techniques are employed to verify the model's ability to generalize to unseen data. A rigorous evaluation process ensures that the final model is robust and capable of delivering reliable predictions under real-world conditions.
- **Real-time Prediction**: Delivers near-instantaneous predictions based on the latest available market data. Real-time prediction enables users to make informed decisions in response to rapidly changing market conditions. By offering timely insights, users can capitalize on emergent opportunities and mitigate the risk of adverse market moves, thereby maintaining a proactive stance in their trading activities.
- **Alerts System**: (Planned) Implements an alert mechanism to send buy, sell, or hold recommendations directly to the user's device. This feature aims to provide actionable insights with minimal delay, ensuring users do not miss key trading opportunities. Alerts are generated based on model output and delivered promptly to enable immediate action in a highly competitive trading environment.
- **Unit Testing**: Validates the reliability and correctness of the codebase through comprehensive unit tests. Each module of the application is rigorously tested to ensure its functionality meets expected standards. Unit testing plays a crucial role in identifying bugs and maintaining the overall stability of the system, thereby ensuring that the deployed model performs as intended in real-world scenarios.

## Project Structure

```plaintext
BullBot/
├── config/
│   └── config.yaml            # Configuration file
├── data/
│   ├── raw/                   # Raw data files
│   ├── processed/             # Processed data files, categorized by behavior type
│   ├── features/              # Feature-engineered data files
├── models/                    # Trained models
├── notebooks/
│   └── exploratory_analysis.ipynb  # Exploratory data analysis
├── results/                   # Evaluation results
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # Data loading script
│   ├── data_preprocessing.py  # Data preprocessing script
│   ├── data_behavior_preprocessing.py # Behavior identification and categorization script
│   ├── feature_engineering.py # Feature engineering script
│   ├── model_training.py      # Model training script
│   ├── model_evaluation.py    # Model evaluation script
│   └── predict.py             # Prediction script
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py         # Tests for data loading
│   ├── test_data_preprocessing.py  # Tests for data preprocessing
│   └── test_feature_engineering.py # Tests for feature engineering
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## Installation

### Prerequisites

- **Python 3.11**: Required to run the application and its dependencies.
- **pip**: Package manager used to install necessary Python libraries and dependencies.
- **Git** (Optional): Useful for cloning the repository and managing version control.

### Steps

1. **Clone the Repository**

   Clone the repository from GitHub to create a local copy of the project.

   ```bash
   git clone https://github.com/yourusername/BullBot.git
   cd BullBot
   ```

2. **Set Up Virtual Environment**

   Create a virtual environment to manage project dependencies.

   ```bash
   python -m venv BullBot_env
   ```

3. **Activate Virtual Environment**

   - On Windows:

     ```bash
     BullBot_env\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source BullBot_env/bin/activate
     ```

4. **Install Dependencies**

   Install the dependencies listed in `requirements.txt`.

   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

## Usage

### Data Loading

Retrieve historical stock data for specified tickers using the data loader script.

```bash
python src/data_loader.py
```

### Data Preprocessing

Perform initial data cleaning to prepare raw data for subsequent analysis.

```bash
python src/data_preprocessing.py
```

### Data Behavior Preprocessing

Identify and categorize specific stock price behaviors (e.g., short-term spike, sustained uptrend). This step extracts data preceding major price movements and saves it to behavior-specific folders for training.

```bash
python src/data_behavior_preprocessing.py
```

### Feature Engineering

Generate additional features, such as technical indicators, to enrich the dataset for model training.

```bash
python src/feature_engineering.py
```

### Model Training

Train the machine learning models using the engineered features and preprocessed behavior data.

```bash
python src/model_training.py
```

### Model Evaluation

Evaluate the performance of trained models using metrics like MSE, RMSE, and R-squared.

```bash
python src/model_evaluation.py
```

### Making Predictions

Generate predictions for new stock data using trained models.

```bash
python src/predict.py
```

## Testing

Execute unit tests to ensure the integrity and functionality of the codebase.

```bash
python -m unittest discover tests
```

## Configuration

Edit `config/config.yaml` to adjust data sources, model parameters, and file paths.

```yaml
# config/config.yaml
data:
  start_date: '2015-01-01'
  end_date: '2023-01-01'
  tickers:
    - AAPL
    - MSFT
    - GOOG

model:
  type: 'RandomForestRegressor'
  parameters:
    n_estimators: 100
    random_state: 42

paths:
  raw_data: 'data/raw'
  processed_data: 'data/processed/preprocessed'
  features_data: 'data/features'
  models: 'models'
  results: 'results'
  behavior_data:
    Short_Spike: 'data/processed/behaviors/Short_Spike'
    Short_Dip: 'data/processed/behaviors/Short_Dip'
    Long_Uptrend: 'data/processed/behaviors/Long_Uptrend'
    Long_Downtrend: 'data/processed/behaviors/Long_Downtrend'
```

The configuration file provides a centralized way to manage various parameters without altering the core code.

## Contributing

Contributions are welcome! Please adhere to the following guidelines:

1. **Fork the Repository**: Create a fork to make changes without affecting the main branch.
2. **Create a Feature Branch**: `git checkout -b feature/YourFeature`.
3. **Commit Changes**: `git commit -m 'Add new feature'`.
4. **Push to Branch**: `git push origin feature/YourFeature`.
5. **Open a Pull Request**: Submit for review.

Ensure your code follows project standards and passes all unit tests.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- **Author**: Allen J Chandler
- **Email**: allenjchandler@gmail.com, allen@shiftedorigin.com
- **GitHub**: [wonmorewave](https://github.com/wonmorewave)

For any inquiries, feedback, or suggestions, please reach out via email or GitHub. Contributions and feature requests are always welcome as we strive to enhance BullBot for both novice and expert traders alike.

