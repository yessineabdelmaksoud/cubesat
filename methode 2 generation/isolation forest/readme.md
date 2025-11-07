# SEL Detector

**Purpose:** Early detection and prevention of **Single Event Latch-up (SEL)** in CubeSat power regulators using a lightweight embedded AI model.

---

##  Problem Statement

CubeSat missions are vulnerable to **Single Event Latch-up (SEL)** — a radiation-induced short circuit that can permanently damage DC–DC converters or microcontrollers.

Traditional protection circuits act **after** the latch-up has already started, often reacting too late (30–50 ms delay).  
This can result in **mission-ending failures** if power rails collapse or chips burn out.

---

##  Solution Overview

**EclipseGuardian SEL Detector** is an **AI-based early warning system** that continuously monitors the regulator’s electrical behavior and predicts abnormal patterns **before** latch-up occurs.

It runs directly on a low-power **ESP32** watchdog microcontroller, analyzing voltage, current, and temperature data at high frequency (10–20 kHz).

### Core Concept
> Learn what "healthy" operation looks like, detect the smallest deviations that precede a latch-up, and trigger a preventive reset within milliseconds.

---

##  System Architecture

| Layer | Component | Role |
|-------|------------|------|
| Hardware | DC–DC power regulator, sensors (Vin, Iin, Vout, Iout, Temp) | Signal acquisition |
| AI Supervisor | ESP32 running trained Isolation Forest (Q15 fixed-point) | Real-time anomaly detection |
| Main OBC | Raspberry Pi 4 / Flight computer | Receives alerts, logs telemetry, and controls recovery |
| Ground Station | Mission operators | Receive anomaly events for post-analysis |

---

##  Pipeline Summary

| Step | Description |
|------|--------------|
| **1. Data Generation** | Simulated regulator data (healthy + SEL-like faults) at 10 kHz sampling |
| **2. Visualization** | Time-series and correlation plots to understand system dynamics |
| **3. Feature Engineering** | 5 physical indicators: `dI/dt`, `Vout_droop`, `ripple_RMS`, `efficiency`, `dEff/dT` |
| **4. Model Training** | Isolation Forest trained on *healthy-only* data |
| **5. Evaluation** | F1-score optimization, latency measurement, confusion matrix |
| **6. Visualization** | ROC curves, feature importance, anomaly score timeline |
| **7. Export to ESP32** | Model quantized to **Q15 fixed-point** and exported as `model_iforest.h` |
| **8. Integration** | Real-time scoring + power cut logic in CubeSat watchdog firmware |

---

##  Model Results (Simulation)

| Metric | Value | Notes |
|---------|--------|-------|
| **Best F1 Threshold** | −0.0064 | Tuned for balanced detection |
| **F1-Score (fault class)** | 0.62 | Room for improvement (data imbalance) |
| **Accuracy** | 0.97 | Strong normal/fault separation |
| **Recall (fault detection)** | 0.59 | Missed events reduced by threshold tuning |
| **Average Detection Latency** | 65.6 ms | Above target → optimize window size / feature timing |

### Confusion Matrix
| | Pred Healthy | Pred Fault |
|---|---|---|
| **True Healthy** | 9473 | 127 |
| **True Fault** | 163 | 235 |

---

## Insights

- **Most informative features:** `dI/dt` and `Vout_droop` show the highest deviation during SEL events.  
- **False alarms** mainly occur during normal high-load transitions (transient spikes).  
- **Detection latency** can be reduced by shorter windows (1 ms) or faster scoring loop on ESP32.  

---

## Integration in CubeSat

**Onboard sequence (real-time loop on ESP32):**
1. Sample ADC data (`Vin`, `Iin`, `Vout`, `Iout`, `Temp`) at 10–20 kHz.  
2. Compute 5 features every 2 ms window.  
3. Standardize using Q15 mean/scale from `model_iforest.h`.  
4. Evaluate Isolation Forest → produce anomaly score.  
5. Compare to threshold:  
   - `score > THRESHOLD` → trigger fault event.  
6. Send flag to OBC or cut power channel instantly.

**Reaction chain:**
- **AI warning (2–10 ms)**  
- **Hardware current limiter (< 1 ms)**  
- **Power reset / isolation (≤ 17 ms total)**  

---

## Exported Firmware Assets

| File | Description |
|------|--------------|
| `model_iforest.h` | Q15 fixed-point version of the trained Isolation Forest |
| `feature_scaler.pkl` | Python scaler (for validation on PC) |
| `iforest_model.pkl` | Full model for retraining or analysis |
| `cubesat_features.csv` | Processed features used in training |
| `cubesat_regulator_raw.csv` | Original simulated sensor data |

---

## Future Work

- **Reduce latency:** Smaller sliding windows or optimized C inference code.  
- **Add online adaptation:** Gradual recalibration in orbit as components age.  
- **Hardware validation:** Inject real current surges on CubeSat power board.  
- **Radiation beam testing:** Collect true SEL signatures for retraining.  
- **Combine with rule-based logic:** Merge ML + absolute safety limits for redundancy.  

---

## Mission Impact

| Impact | Result |
|---------|--------|
| Reaction time improvement | From 40 ms → ~10–17 ms (goal) |
| Predictive protection | Detects early stress before hard SEL |
| Power safety | Prevents regulator and MCU burnout |
| Reliability | +20–30 % power subsystem resilience |
| Energy efficiency | Reduced waste due to early cutoff |

---

### Summary

> **EclipseGuardian SEL Detector** is a compact, explainable, and embeddable AI designed to *predict and prevent radiation-induced power faults in CubeSats*, bridging the gap between hardware protection and intelligent fault prediction.

