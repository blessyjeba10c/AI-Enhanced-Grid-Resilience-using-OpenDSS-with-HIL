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
<p align="center">
   <img width="462" height="386" alt="image" src="https://github.com/user-attachments/assets/3eb1e1d5-bfc8-46c1-904b-35e5db94cb2c" />
</p>

<p align="center">
   <img width="268" height="265" alt="image" src="https://github.com/user-attachments/assets/39f991ea-2859-4f81-aa0c-2001a623353e" />
</p>

<p align="center">
   <img width="293" height="287" alt="image" src="https://github.com/user-attachments/assets/dec4794d-224f-435a-b7ff-aa1137e1a96c" />
</p>

<p align="center">
   <img width="293" height="293" alt="image" src="https://github.com/user-attachments/assets/21e1d023-178b-405d-88e3-ca123f359ef3" />
</p>

<p align="center">
   <img width="274" height="268" alt="image" src="https://github.com/user-attachments/assets/246594f0-e91b-45ff-9385-725673ae751c" />
</p>

<p align="center">
   <img width="290" height="286" alt="image" src="https://github.com/user-attachments/assets/a6c31939-9dd6-4641-a1f6-1601b81539c8" />
</p>

<p align="center">
   <img width="267" height="268" alt="image" src="https://github.com/user-attachments/assets/7026b81b-0f20-492a-81f9-a22cf3b05b86" />
</p>

<p align="center">
   <img width="1271" height="713" alt="image" src="https://github.com/user-attachments/assets/0bc6e31c-3c2e-4198-ba01-fa5d94c87da7" />
</p>

<p align="center">
   <img width="517" height="362" alt="image" src="https://github.com/user-attachments/assets/4a368b49-781c-47b4-a8ce-66685b98d5e4" />
</p>


2. **Spectral Clustering for Zone Partitioning**  
   Apply spectral clustering to divide the grid into smaller, manageable zones for **localized fault detection**, **faster recovery**, and **efficient resource allocation**.


<p align="center">
   <img width="581" height="318" alt="image" src="https://github.com/user-attachments/assets/74ac14d2-152b-4983-8dfb-e41e089caf13" />
</p>

<p align="center">
   <img width="555" height="321" alt="image" src="https://github.com/user-attachments/assets/19b51e12-1260-4580-aa7e-cd8fdd63040c" />
</p>

<p align="center">
   <img width="551" height="414" alt="image" src="https://github.com/user-attachments/assets/ac5357bd-37e8-458a-96a1-4359b8ea9f25" />
</p>

<p align="center">
   <img width="541" height="303" alt="image" src="https://github.com/user-attachments/assets/337b7c01-d947-4a93-9b15-b3e249f71ac4" />
</p>

<p align="center">
   <img width="793" height="755" alt="image" src="https://github.com/user-attachments/assets/ea53c50c-2eb6-40f5-8359-05e0da8fb37d" />
</p>


3. **Zone-wise Fault Injection**  
   Introduce fault scenarios such as **line-to-ground faults**, **voltage sags**, and **equipment failures** in each zone. Record simulation data for training.

<p align="center">
   <img width="639" height="247" alt="image" src="https://github.com/user-attachments/assets/cb777fba-b8ef-4ad8-802f-1792411df7f1" />
</p>

<p align="center">
   <img width="547" height="413" alt="image" src="https://github.com/user-attachments/assets/bb7b2078-d46b-45fa-af95-ba18269f8f41" />
</p>

<p align="center">
   <img width="1109" height="477" alt="image" src="https://github.com/user-attachments/assets/56a47bd7-6517-4240-a049-48acd9c84325" />
</p>

4. **AI-based Fault Prediction**  
   Train machine learning models (e.g., **XGBoost**) to predict **fault location**, **type**, and **recovery time**. Assign resilience scores for quick decision-making.

<p align="center">
   <img width="734" height="329" alt="image" src="https://github.com/user-attachments/assets/e2e5253c-ce1f-4f12-b4d9-9654ad2b479b" />
</p>

<p align="center">
   <img width="595" height="171" alt="image" src="https://github.com/user-attachments/assets/634141d0-1e2e-4dfe-b271-5eec7da628b8" />
</p>

<p align="center">
   <img width="623" height="178" alt="image" src="https://github.com/user-attachments/assets/5962ce93-6704-4a0c-a672-a5344d9cb6d5" />
</p>

5. **Real-time Monitoring Dashboard**  
   Build an interactive **Streamlit** dashboard to display **grid status**, **predicted fault zones**, and **recovery timelines**.  
   Integrate **Power BI** for advanced analytics and historical trend analysis.

<p align="center">
   <img width="760" height="429" alt="image" src="https://github.com/user-attachments/assets/a79ad7ff-2c1b-42fa-9113-536667d8f0ef" />
</p>

<p align="center">
   <img width="754" height="423" alt="image" src="https://github.com/user-attachments/assets/d590a0a0-f801-4afa-bda2-9c50d00285ef" />
</p>

<p align="center">
   <img width="757" height="424" alt="image" src="https://github.com/user-attachments/assets/c600bc13-55d9-447e-a519-6caa4b80323e" />
</p>


6. **Hardware-in-the-Loop (HIL) Validation**  
   Deploy AI models on **Raspberry Pi / FPGA** connected to the simulated grid for real-time testing and validation.

<p align="center">
   <img width="1186" height="451" alt="image" src="https://github.com/user-attachments/assets/72bd6d5f-910e-422f-b8d2-b2aebc981b9c" />
</p>

<p align="center">
   <img width="428" height="346" alt="image" src="https://github.com/user-attachments/assets/4e9a1aef-c66c-4153-973f-59952115cbad" />
</p>

<p align="center">
   <img width="507" height="381" alt="image" src="https://github.com/user-attachments/assets/d5bdad1e-8899-4c62-94cc-c37336c03a5a" />
</p>

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

