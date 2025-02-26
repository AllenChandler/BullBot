"""
=============================================
 BullBot Pipeline Runner
=============================================

USAGE:
------
This script allows you to run one, multiple, or all preprocessing & deep learning scripts in sequence.

RUN ALL STEPS:
--------------
To execute the **entire pipeline** (from data fetching to deep learning prediction), run:
    python run_pipeline.py all

RUN SPECIFIC STEPS:
-------------------
You can specify **only the steps you want to run**, for example:
    python run_pipeline.py fetch clean preprocess_dl train_dl

AVAILABLE STEPS:
---------------
1. fetch         → Fetch raw data from Polygon API.
2. clean         → Clean the raw Polygon data.
3. metrics       → Add advanced trading metrics.
4. continuous    → Organize data into continuous time-series per ticker.
5. spikes        → Identify price spikes (for ML model training).
6. preprocess_dl → Convert continuous data to `.npy` format for deep learning.
7. train_dl      → Train the deep learning model.
8. predict_dl    → Use the trained model to make predictions.

EXAMPLES:
---------
Run only preprocessing:
    python run_pipeline.py fetch clean metrics continuous

Run deep learning only:
    python run_pipeline.py preprocess_dl train_dl predict_dl

Run training & prediction only:
    python run_pipeline.py train_dl predict_dl

NOTES:
------
- This script loads paths from `config.yaml`, so ensure it's correctly configured.
- The steps must match the keys listed in the script (see `scripts` dictionary).
- If a step fails, check the printed error message for debugging.

=============================================
"""


import os
import argparse
import yaml

# Load config
CONFIG_PATH = "E:/projects/BullBot_backup/config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Define script paths
scripts = {
    "fetch": config["script_paths"]["fetch_polygon"],
    "clean": config["script_paths"]["clean_polygon"],
    "metrics": config["script_paths"]["metrics_polygon"],
    "continuous": config["script_paths"]["continuous_polygon"],
    "spikes": config["script_paths"]["spikes_polygon"],
    "preprocess_dl": config["script_paths"]["preprocess_dl"],
    "train_dl": config["script_paths"]["train_dl"],
    "predict_dl": config["script_paths"]["predict_dl"],
}

# Define execution order
default_order = [
    "fetch", "clean", "metrics", "continuous", "spikes",  # Preprocessing steps
    "preprocess_dl", "train_dl", "predict_dl"  # Deep Learning pipeline
]

# Argument parser setup
parser = argparse.ArgumentParser(description="Run BullBot Pipeline.")
parser.add_argument(
    "steps", nargs="*", choices=scripts.keys() + ["all"],
    help="Specify which steps to run (or use 'all')."
)
args = parser.parse_args()

# Determine which steps to run
steps_to_run = default_order if "all" in args.steps else args.steps

# Execute selected steps
for step in steps_to_run:
    script_path = scripts[step]
    print(f"🚀 Running {step}: {script_path}")
    os.system(f"python {script_path}")

print("✅ Pipeline execution complete!")
