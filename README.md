# Athlete Training Load + Readiness Decision Engine

A Python-based athlete monitoring system that integrates training load, individual athlete baselines, readiness and workload changes into an automated monitoring signal.

## Objective

The goal of this project is to move from isolated metrics toward an integrated athlete decision-support system.

Instead of asking only:

> How much did the athlete train?

the system considers:

> How does the current training load compare with the athlete's normal load, how ready is the athlete, and how much has the workload changed?

## Data Flow

```text
Training Sessions
        ↓
Training Load
        ↓
Individual Baseline
        ↓
Load Z-Score
        ↓
Readiness Baseline
        ↓
Readiness Z-Score
        ↓
Load Change
        ↓
Decision Score
        ↓
GREEN / YELLOW / RED
        ↓
Monitoring Recommendation
```

## Dataset

The sample dataset contains 40 observations from four athletes.

Variables:

| Variable | Description |
|---|---|
| Athlete | Athlete identifier |
| Date | Observation date |
| Duration_min | Training duration in minutes |
| sRPE | Session rating of perceived exertion |
| Readiness_Score | Athlete readiness score |

## Training Load

Training load is calculated using:

```text
Training Load = Duration × sRPE
```

Example:

```text
80 minutes × RPE 9 = 720 AU
```

## Individual Baseline

Each athlete receives an individual training-load baseline based on their historical observations.

The system also calculates an individual readiness baseline.

## Z-Score

The system uses:

```text
z = (observed value - athlete mean) / athlete standard deviation
```

This allows observations to be interpreted relative to the athlete's own historical distribution.

## Readiness Interpretation

For readiness, negative deviations are considered more concerning.

```text
Readiness z > -1.5
NORMAL
```

```text
-2.0 < Readiness z ≤ -1.5
WATCH
```

```text
Readiness z ≤ -2.0
LOW
```

## Training Load Interpretation

```text
|Load z| < 1.5
NORMAL
```

```text
1.5 ≤ |Load z| < 2.0
WATCH
```

```text
|Load z| ≥ 2.0
HIGH
```

## Load Change

The system compares the current training load with the athlete's previous session:

```text
Load Change % =
(Current Load - Previous Load)
/
Previous Load × 100
```

## Decision Engine

Three components contribute to the decision score:

1. Training-load status
2. Readiness status
3. Load-change status

The resulting score produces:

```text
GREEN
YELLOW
RED
```

### GREEN

Normal monitoring signal.

### YELLOW

Moderate monitoring priority.

### RED

High monitoring priority requiring contextual review.

## Coaching Recommendations

### GREEN

Continue planned monitoring and training progression.

### YELLOW

Monitor the athlete closely and review recent workload trends.

### RED

Review training load, readiness, recovery and athlete context before progressing workload.

## Output Files

The system generates:

```text
athlete_decision_results.csv
athlete_monitoring_dashboard.png
load_vs_readiness.png
```

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Athlete monitoring
- Statistical normalization
- Decision rules
- Data visualization

## Installation

```bash
pip install pandas numpy matplotlib
```

## Running the Project

Place the Python script and CSV file in the same directory.

Run:

```bash
python athlete_decision_engine.py
```

## Sports Science Applications

Potential applications include:

- Strength and conditioning
- Athlete monitoring
- Training-load management
- Readiness monitoring
- Performance analytics
- Recovery monitoring
- Periodization support
- Coaching decision support

## Important Limitations

This is an educational decision-support system using synthetic data.

A RED signal does not automatically mean:

- Injury
- Overtraining
- Excessive fatigue
- Poor recovery
- Need to stop training

It indicates that the available variables warrant closer contextual review.

Real-world athlete monitoring should consider:

- Training phase
- Competition schedule
- Athlete history
- Recovery
- Sleep
- Wellness
- Injury status
- GPS workload
- Internal workload
- Performance data
- Measurement reliability
- Coaching context

The thresholds and scoring rules in this project are demonstration rules and are not validated clinical or injury-prediction thresholds.

## Future Development

Possible extensions include:

- GPS data
- Heart-rate data
- Wellness questionnaires
- Sleep data
- Jump testing
- Force-plate data
- Bar velocity
- Training monotony
- Training strain
- Forecasting
- Machine learning
- Time-series anomaly detection
- Automated alerts
- Athlete dashboards
- Explainable AI
- Agentic decision-support systems

## Skills Demonstrated

```text
Python
   ↓
Pandas
   ↓
NumPy
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Individual Baselines
   ↓
Z-Score Analysis
   ↓
Decision Rules
   ↓
Athlete Monitoring
   ↓
Decision Support
```

## Author

**Abhishek Tomar**

Strength & Conditioning | Sports Performance | Sports Analytics | Python

## License

MIT License