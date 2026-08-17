# Loewe Additivity & Isobologram Calculator

A comprehensive toolkit for computing the **Loewe Combination Index (CI)** and plotting **Isobolograms** for drug combination synergy/antagonism assays.

---

## 📁 Package Contents

* **`index.html`** – Standalone, zero-install web application with interactive sliders, real-time CI computation, and a dynamic 2D Isobologram scatter plot.
* **`loewe_analysis.py`** – Python module using NumPy, SciPy, and Matplotlib to invert 4PL Hill dose-response curves, calculate CI, and export publication-grade PNG plots.
* **`server.js` & `package.json`** – Node.js Express REST API backend for batch or web integration.

---

## 🧮 Mathematical Model

The Loewe Combination Index is calculated as:

$$\text{CI} = \frac{d_A}{D_A} + \frac{d_B}{D_B}$$

* **$CI < 0.9$** : Synergism (lower doses needed than expected)
* **$0.9 \le CI \le 1.1$** : Loewe Additivity (drugs act without pharmacodynamic interaction)
* **$CI > 1.1$** : Antagonism (higher doses needed than expected)

---

## 🚀 Getting Started

### 1. Web App
Simply open `index.html` in any web browser.

### 2. Python Script
```bash
pip install numpy scipy matplotlib
python loewe_analysis.py
```

### 3. Node.js API Server
```bash
npm install
npm start
```
Test with curl:
```bash
curl -X POST http://localhost:3000/api/calculate-loewe \
  -H "Content-Type: application/json" \
  -d '{"DA": 100, "DB": 50, "dA": 30, "dB": 15}'
```
