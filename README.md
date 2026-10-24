# 🛡️ Network Security MLOps Pipeline

An end-to-end Machine Learning project focused on network security and phishing-related data classification, developed using Python and essential MLOps tools.

The project demonstrates a structured machine learning workflow, including data ingestion, data validation, data drift detection, preprocessing, model training, model evaluation, and experiment tracking.

The goal is to build a **reproducible, modular, and maintainable ML pipeline** that can be extended toward automated prediction and cloud deployment.

---

## 📌 Project Overview

Machine learning applications require more than training a model. Reliable systems also need structured data ingestion, data quality checks, consistent preprocessing, model evaluation, and reproducible experiments.

This project implements these stages through modular Python components.

### Key Objectives

* Automate the machine learning training workflow.
* Ingest and manage data using MongoDB.
* Validate data quality and detect statistical changes in datasets.
* Build reusable preprocessing pipelines.
* Train and compare classification models.
* Evaluate model performance using classification metrics.
* Track experiments and save model artifacts.
* Extend the pipeline toward production-oriented deployment.

---

## 🚀 Features

### 1. Data Ingestion

* Reads structured data from MongoDB.
* Converts CSV records into JSON-compatible documents for database insertion.
* Retrieves data for subsequent processing.
* Splits the dataset into training and testing subsets.
* Stores intermediate datasets for downstream pipeline components.

### 2. Data Validation

* Validates the dataset against a predefined schema.
* Checks the expected columns and numerical features.
* Detects statistical differences between training and testing data.
* Uses the Kolmogorov–Smirnov (KS) two-sample test for numerical feature drift detection.
* Maintains logging and exception handling for improved traceability.

### 3. Data Transformation

* Separates input features from the target variable.
* Handles missing values using `KNNImputer`.
* Uses a Scikit-learn preprocessing pipeline.
* Fits preprocessing transformations on training data and applies them to testing data.
* Saves transformed datasets as NumPy arrays.
* Persists the preprocessing object for reuse during inference.

### 4. Model Training

* Trains and evaluates multiple classification algorithms.
* Uses `GridSearchCV` for hyperparameter tuning.
* Evaluates models using precision, recall, and F1-score.
* Supports model comparison and selection.
* Saves trained model artifacts for subsequent pipeline stages.
* Integrates MLflow for experiment tracking where configured.

---

## 🏗️ Project Architecture

The pipeline follows a modular architecture:

```text
                    ┌──────────────────────┐
                    │   Source Dataset      │
                    │  Phishing/Network Data│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Data Ingestion     │
                    │      MongoDB         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Data Validation    │
                    │  Schema + Drift      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Transformation  │
                    │ KNN Imputation       │
                    │ Feature Processing   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Model Training     │
                    │ Hyperparameter Tuning│
                    │ Model Evaluation     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Saved Artifacts    │
                    │ Model + Preprocessor │
                    └──────────────────────┘
```

---

## 🧰 Tech Stack

| Category                  | Technologies         |
| ------------------------- | -------------------- |
| Programming Language      | Python               |
| Data Processing           | Pandas, NumPy        |
| Machine Learning          | Scikit-learn         |
| Missing Value Imputation  | KNN Imputer          |
| Statistical Analysis      | SciPy                |
| Database                  | MongoDB Atlas        |
| Experiment Tracking       | MLflow               |
| Environment Configuration | Python dotenv        |
| Development Tools         | Git, GitHub, VS Code |

**Deployment technologies under development:** Docker, GitHub Actions, Amazon ECR, and Amazon EC2.

These deployment technologies are part of the planned workflow and should not be considered fully configured or deployed until implementation and testing are complete.

---

## 📂 Project Structure

```text
Network-Security-MLops-Pipeline/
│
├── networksecurity/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── constant/
│   │   └── training_pipeline.py
│   │
│   ├── entity/
│   │   ├── artifact_entity.py
│   │   └── config_entity.py
│   │
│   ├── exception/
│   │   └── exception.py
│   │
│   ├── logging/
│   │   └── logger.py
│   │
│   ├── pipeline/
│   │
│   └── utils/
│
├── Network_Data/
│   └── phisingData.csv
│
├── data_schema/
│   └── schema.yaml
│
├── .github/
│   └── workflows/
│       └── main.yml
│
├── .env.example
├── .gitignore
├── Dockerfile
├── main.py
├── push_data.py
├── requirements.txt
├── setup.py
└── README.md
```

*Note: This structure represents the intended organization. Keep only files and directories that actually exist in your repository, and update the tree as the project evolves.*

---

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the pipeline:

* Python 3.12, subject to dependency compatibility.
* Git.
* MongoDB Atlas account and a configured database.
* A code editor such as Visual Studio Code.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Harshitraj123/Network-Security-MLops-Pipeline.git
```

Navigate to the project directory:

```bash
cd Network-Security-MLops-Pipeline
```

### Step 2: Create a Virtual Environment

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project's dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

The project uses environment variables to configure the MongoDB connection.

Create a `.env` file in the project root:

```env
MONGO_DB_URL=mongodb+srv://<username>:<password>@<cluster-host>/?retryWrites=true&w=majority
```

Replace the placeholders with your actual MongoDB Atlas connection details.

Before connecting, ensure that your MongoDB database user, network access rules, and cluster configuration permit the connection.

### Important Security Practices

* Never commit your actual `.env` file.
* Keep database credentials out of source code and logs.
* Commit `.env.example` with placeholder values instead of real credentials.
* Rotate credentials if they have been exposed.
* Never upload virtual environments or unnecessary generated artifacts to GitHub.

---

## ▶️ Running the Project

### Step 1: Prepare the Dataset

Ensure the dataset is available at the configured path:

```text
Network_Data/phisingData.csv
```

The filename and path must match those used in your code.

### Step 2: Upload Data to MongoDB

If your collection has not already been populated, run:

```bash
python push_data.py
```

This script reads the CSV file and inserts its records into the configured MongoDB collection.

**Important:** Avoid inserting the same dataset repeatedly, as doing so can create duplicate records unless duplicate prevention is implemented.

### Step 3: Execute the Training Pipeline

Run:

```bash
python main.py
```

The main script orchestrates the pipeline components:

1. Data Ingestion
2. Data Validation
3. Data Transformation
4. Model Training

Check the terminal output and application logs to confirm that each stage completes successfully.

---

## 📊 Model Evaluation

The model training component supports model comparison and hyperparameter tuning.

The evaluation metrics include:

| Metric    | Purpose                                                           |
| --------- | ----------------------------------------------------------------- |
| Precision | Measures the proportion of positive predictions that are correct. |
| Recall    | Measures the proportion of actual positive cases identified.      |
| F1-score  | Combines precision and recall using their harmonic mean.          |

The final model should be selected using appropriate evaluation metrics and validation results rather than accuracy alone.

Actual performance metrics should be added to this section after completing a verified training run.

---

## 🔄 MLOps Workflow

The project is being developed incrementally toward a more complete MLOps workflow.

| Stage               | Purpose                                             | Status                      |
| ------------------- | --------------------------------------------------- | --------------------------- |
| Data Ingestion      | Retrieve and split source data                      | Implemented                 |
| Data Validation     | Schema checks and drift detection                   | Implemented                 |
| Data Transformation | Missing-value handling and preprocessing            | Implemented                 |
| Model Training      | Model comparison and evaluation                     | Implemented                 |
| Experiment Tracking | Track model experiments with MLflow                 | Integrated where configured |
| Batch Prediction    | Generate predictions from new input data            | Planned / in progress       |
| Docker Packaging    | Package the application and dependencies            | Planned / in progress       |
| Automated CI/CD     | Automate builds and deployment using GitHub Actions | Planned / in progress       |
| Cloud Deployment    | Deploy the application using AWS services           | Planned / in progress       |

*Update the status of each component as implementation and testing are completed.*

---

## 🛣️ Future Enhancements

Planned improvements include:

* Complete the batch prediction pipeline.
* Improve model artifact management and inference consistency.
* Add automated testing and code-quality checks.
* Containerize the application using Docker.
* Configure continuous integration and deployment workflows.
* Store container images in Amazon Elastic Container Registry (ECR).
* Deploy the application on Amazon EC2.
* Improve monitoring, logging, and reproducibility.

---

## 🔒 Security Considerations

This project uses database credentials and may eventually use cloud credentials.

To reduce security risks:

* Store secrets in environment variables or an appropriate secrets manager.
* Use least-privilege database and cloud permissions.
* Exclude `.env`, virtual environments, and sensitive files from version control.
* Validate incoming data before using it for model inference.
* Do not publish real credentials, private connection strings, or sensitive dataset records.

---

## 🎯 Learning Outcomes

This project provides practical experience with:

* Modular Python application design.
* Data ingestion and database integration.
* Schema validation and statistical drift detection.
* Reusable Scikit-learn preprocessing pipelines.
* Classification model selection and hyperparameter tuning.
* Model evaluation and experiment tracking.
* ML pipeline orchestration and artifact management.
* The foundations of production-oriented MLOps.

---

## 👨‍💻 Author

**Harshit Raj**

Computer Science & Engineering | Machine Learning | Data Science | MLOps

* GitHub: [Harshitraj123](https://github.com/Harshitraj123)
* LinkedIn: [harshitraj010204](https://www.linkedin.com/in/harshitraj010204)

---

## 📜 License

This project is available for learning and demonstration purposes. A formal open-source license can be added to the repository when the licensing terms have been decided.

---

⭐ If you find this project interesting, consider exploring the repository and following its development.
