# AI-Enhanced-Grid-Resilience-using-OpenDSS-with-HIL


# GridGuard – AI-Powered Smart Grid Resilience Platform

**GridGuard** is an AI-powered smart grid resilience platform designed to **predict faults**, **minimize blackout time**, and **enhance disaster recovery** in power distribution systems.  


---

## Problem Statement
Extreme weather events and unpredictable demand cause **frequent power outages** and **slow recovery** in distribution grids.  
There is a need for a **low-cost, real-time, AI-based fault detection and recovery system** to improve grid resilience, especially in disaster-prone regions.

---

## Proposed Solution – 6 Steps

1. **OpenDSS Grid Simulation**  
   Simulate the IEEE 123-bus power distribution network in OpenDSS, incorporating generators, loads, renewable sources, and realistic operating conditions.

![Step 1 – OpenDSS Grid Simulation]( )

2. **Spectral Clustering for Zone Partitioning**  
   Apply spectral clustering to divide the grid into smaller, manageable zones for **localized fault detection**, **faster recovery**, and **efficient resource allocation**.

3. **Zone-wise Fault Injection**  
   Introduce fault scenarios such as **line-to-ground faults**, **voltage sags**, and **equipment failures** in each zone. Record simulation data for training.

4. **AI-based Fault Prediction**  
   Train machine learning models (e.g., **XGBoost**) to predict **fault location**, **type**, and **recovery time**. Assign resilience scores for quick decision-making.

5. **Real-time Monitoring Dashboard**  
   Build an interactive **Streamlit** dashboard to display **grid status**, **predicted fault zones**, and **recovery timelines**.  
   Integrate **Power BI** for advanced analytics and historical trend analysis.

6. **Hardware-in-the-Loop (HIL) Validation**  
   Deploy AI models on **Raspberry Pi / FPGA** connected to the simulated grid for real-time testing and validation.

   ![Step 1 – OpenDSS Grid Simulation]( ![WhatsApp Image 2025-08-08 at 13 23 19_7687567e](https://github.com/user-attachments/assets/c2055c37-8873-4e6a-8e46-a333c7d553cf)
)

---

## Technical Approach

- **OpenDSS Grid Simulation** → IEEE 123-bus model with renewable integration  
- **Spectral Clustering** → Grid partitioning for localized analysis  
- **Fault Injection** → Simulated per-zone faults for training data  
- **ML Models** → Predict recovery time & resilience score  
- **Visualization** → Streamlit + Power BI  
- **HIL Testing** → Raspberry Pi / FPGA integration

---

## Tech Stack

**Languages:** Python, MATLAB  
**Tools:** OpenDSS, Streamlit, Power BI  
**Libraries:** scikit-learn, XGBoost, pandas, numpy  
**Hardware:** Raspberry Pi / FPGA (HIL setup)

---

## Key Features

- Real-time **AI-driven fault prediction**
- Zone-wise **grid clustering** for faster recovery
- Hardware-validated for **real-world deployment**
- **Low-cost** and scalable for distribution grids

---

##

