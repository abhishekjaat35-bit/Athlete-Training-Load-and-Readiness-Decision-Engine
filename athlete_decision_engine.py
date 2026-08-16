import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


print("=" * 80)
print("             ATHLETE TRAINING LOAD + READINESS DECISION ENGINE")
print("=" * 80)


# ------------------------------------------
# Load Data
# ------------------------------------------

data = pd.read_csv(
    "athlete_monitoring_data.csv"
)

data["Date"] = pd.to_datetime(
    data["Date"]
)

data = data.sort_values(
    ["Athlete", "Date"]
).reset_index(drop=True)


# ------------------------------------------
# Data Validation
# ------------------------------------------

print("\n" + "=" * 80)
print("DATA VALIDATION")
print("=" * 80)

print(f"Rows           : {len(data)}")
print(f"Columns        : {len(data.columns)}")
print(
    f"Missing values : "
    f"{data.isnull().sum().sum()}"
)
print(
    f"Athletes       : "
    f"{data['Athlete'].nunique()}"
)


# ------------------------------------------
# Training Load
# ------------------------------------------

data["Training_Load"] = (
    data["Duration_min"]
    *
    data["sRPE"]
)


# ------------------------------------------
# Individual Training Load Baseline
# ------------------------------------------

data["Load_Baseline"] = (
    data.groupby("Athlete")["Training_Load"]
    .transform("mean")
)

data["Load_SD"] = (
    data.groupby("Athlete")["Training_Load"]
    .transform("std")
)


# ------------------------------------------
# Readiness Baseline
# ------------------------------------------

data["Readiness_Baseline"] = (
    data.groupby("Athlete")["Readiness_Score"]
    .transform("mean")
)

data["Readiness_SD"] = (
    data.groupby("Athlete")["Readiness_Score"]
    .transform("std")
)


# ------------------------------------------
# Z-Scores
# ------------------------------------------

data["Load_Z_Score"] = (
    (
        data["Training_Load"]
        -
        data["Load_Baseline"]
    )
    /
    data["Load_SD"]
)

data["Readiness_Z_Score"] = (
    (
        data["Readiness_Score"]
        -
        data["Readiness_Baseline"]
    )
    /
    data["Readiness_SD"]
)


# ------------------------------------------
# Clean Infinite Values
# ------------------------------------------

data["Load_Z_Score"] = (
    data["Load_Z_Score"]
    .replace(
        [np.inf, -np.inf],
        0
    )
    .fillna(0)
)

data["Readiness_Z_Score"] = (
    data["Readiness_Z_Score"]
    .replace(
        [np.inf, -np.inf],
        0
    )
    .fillna(0)
)


# ------------------------------------------
# Previous Training Load
# ------------------------------------------

data["Previous_Load"] = (
    data.groupby("Athlete")["Training_Load"]
    .shift(1)
)


# ------------------------------------------
# Load Change
# ------------------------------------------

data["Load_Change_%"] = np.where(
    data["Previous_Load"] > 0,

    (
        (
            data["Training_Load"]
            -
            data["Previous_Load"]
        )
        /
        data["Previous_Load"]
    )
    *
    100,

    0
)


# ------------------------------------------
# Load Status
# ------------------------------------------

def load_status(z):

    if abs(z) >= 2.0:
        return "HIGH"

    elif abs(z) >= 1.5:
        return "WATCH"

    else:
        return "NORMAL"


data["Load_Status"] = (
    data["Load_Z_Score"]
    .apply(load_status)
)


# ------------------------------------------
# Readiness Status
# ------------------------------------------

def readiness_status(z):

    # A strongly negative readiness
    # z-score is more concerning than
    # a strongly positive score.

    if z <= -2.0:
        return "LOW"

    elif z <= -1.5:
        return "WATCH"

    else:
        return "NORMAL"


data["Readiness_Status"] = (
    data["Readiness_Z_Score"]
    .apply(readiness_status)
)


# ------------------------------------------
# Load Change Status
# ------------------------------------------

def load_change_status(change):

    if abs(change) >= 20:
        return "HIGH"

    elif abs(change) >= 10:
        return "WATCH"

    else:
        return "NORMAL"


data["Load_Change_Status"] = (
    data["Load_Change_%"]
    .apply(load_change_status)
)


# ------------------------------------------
# Decision Score
# ------------------------------------------

def calculate_decision_score(row):

    score = 0

    if row["Load_Status"] == "HIGH":
        score += 2

    elif row["Load_Status"] == "WATCH":
        score += 1

    if row["Readiness_Status"] == "LOW":
        score += 3

    elif row["Readiness_Status"] == "WATCH":
        score += 2

    if row["Load_Change_Status"] == "HIGH":
        score += 2

    elif row["Load_Change_Status"] == "WATCH":
        score += 1

    return score


data["Decision_Score"] = (
    data.apply(
        calculate_decision_score,
        axis=1
    )
)


# ------------------------------------------
# Overall Decision
# ------------------------------------------

def overall_decision(score):

    if score >= 5:
        return "RED"

    elif score >= 2:
        return "YELLOW"

    else:
        return "GREEN"


data["Overall_Status"] = (
    data["Decision_Score"]
    .apply(overall_decision)
)


# ------------------------------------------
# Monitoring Priority
# ------------------------------------------

def monitoring_priority(status):

    if status == "RED":
        return "HIGH"

    elif status == "YELLOW":
        return "MODERATE"

    else:
        return "LOW"


data["Monitoring_Priority"] = (
    data["Overall_Status"]
    .apply(monitoring_priority)
)


# ------------------------------------------
# Coaching Recommendation
# ------------------------------------------

def recommendation(row):

    if row["Overall_Status"] == "RED":

        return (
            "Review training load, readiness, "
            "recovery and athlete context "
            "before progressing workload."
        )

    elif row["Overall_Status"] == "YELLOW":

        return (
            "Monitor athlete closely and "
            "review recent workload trends."
        )

    else:

        return (
            "Continue planned monitoring "
            "and training progression."
        )


data["Coaching_Recommendation"] = (
    data.apply(
        recommendation,
        axis=1
    )
)


# ------------------------------------------
# Latest Athlete Status
# ------------------------------------------

latest = (
    data.sort_values("Date")
    .groupby("Athlete")
    .tail(1)
    .copy()
)


print("\n" + "=" * 80)
print("CURRENT ATHLETE MONITORING STATUS")
print("=" * 80)


latest_display = latest[
    [
        "Athlete",
        "Date",
        "Training_Load",
        "Load_Z_Score",
        "Readiness_Score",
        "Readiness_Z_Score",
        "Load_Change_%",
        "Decision_Score",
        "Overall_Status",
        "Monitoring_Priority"
    ]
].copy()


for column in [
    "Load_Z_Score",
    "Readiness_Z_Score",
    "Load_Change_%"
]:

    latest_display[column] = (
        latest_display[column]
        .round(2)
    )


print(
    latest_display.to_string(
        index=False
    )
)


# ------------------------------------------
# Decision Summary
# ------------------------------------------

print("\n" + "=" * 80)
print("DECISION SUMMARY")
print("=" * 80)


for _, row in latest.iterrows():

    print(
        f"\nAthlete: {row['Athlete']}"
    )

    print(
        f"Status: "
        f"{row['Overall_Status']}"
    )

    print(
        f"Priority: "
        f"{row['Monitoring_Priority']}"
    )

    print(
        f"Recommendation: "
        f"{row['Coaching_Recommendation']}"
    )


# ------------------------------------------
# Athlete Summary
# ------------------------------------------

athlete_summary = (
    data.groupby("Athlete")
    .agg(
        Observations=(
            "Athlete",
            "count"
        ),

        Average_Load=(
            "Training_Load",
            "mean"
        ),

        Load_Baseline=(
            "Load_Baseline",
            "mean"
        ),

        Average_Readiness=(
            "Readiness_Score",
            "mean"
        ),

        Red_Alerts=(
            "Overall_Status",
            lambda x:
            (x == "RED").sum()
        ),

        Yellow_Alerts=(
            "Overall_Status",
            lambda x:
            (x == "YELLOW").sum()
        ),

        Green_Observations=(
            "Overall_Status",
            lambda x:
            (x == "GREEN").sum()
        )
    )
    .reset_index()
)


print("\n" + "=" * 80)
print("ATHLETE MONITORING SUMMARY")
print("=" * 80)


summary_display = athlete_summary.copy()

for column in [
    "Average_Load",
    "Load_Baseline",
    "Average_Readiness"
]:

    summary_display[column] = (
        summary_display[column]
        .round(1)
    )


print(
    summary_display.to_string(
        index=False
    )
)


# ------------------------------------------
# Dashboard
# ------------------------------------------

status_counts = (
    latest["Overall_Status"]
    .value_counts()
    .reindex(
        [
            "GREEN",
            "YELLOW",
            "RED"
        ],
        fill_value=0
    )
)


plt.figure(
    figsize=(8, 6)
)

plt.bar(
    status_counts.index,
    status_counts.values
)

plt.title(
    "Current Athlete Monitoring Status"
)

plt.xlabel(
    "Overall Status"
)

plt.ylabel(
    "Number of Athletes"
)

plt.tight_layout()

plt.savefig(
    "athlete_monitoring_dashboard.png",
    dpi=300
)

plt.show()


# ------------------------------------------
# Load vs Readiness
# ------------------------------------------

plt.figure(
    figsize=(10, 7)
)

plt.scatter(
    latest["Training_Load"],
    latest["Readiness_Score"],
    s=120
)

for _, row in latest.iterrows():

    plt.annotate(
        row["Athlete"],
        (
            row["Training_Load"],
            row["Readiness_Score"]
        ),
        xytext=(6, 6),
        textcoords="offset points"
    )


plt.title(
    "Training Load vs Readiness"
)

plt.xlabel(
    "Training Load (AU)"
)

plt.ylabel(
    "Readiness Score (%)"
)

plt.tight_layout()

plt.savefig(
    "load_vs_readiness.png",
    dpi=300
)

plt.show()


# ------------------------------------------
# Export Complete Results
# ------------------------------------------

data.to_csv(
    "athlete_decision_results.csv",
    index=False
)


# ------------------------------------------
# Final Output
# ------------------------------------------

print("\n" + "=" * 80)
print("ATHLETE DECISION ENGINE COMPLETE")
print("=" * 80)

print("Generated files:")

print(
    "1. athlete_decision_results.csv"
)

print(
    "2. athlete_monitoring_dashboard.png"
)

print(
    "3. load_vs_readiness.png"
)

print("\n" + "=" * 80)
print(
    "MONITOR • INTEGRATE • INTERPRET • DECIDE"
)
print("=" * 80)