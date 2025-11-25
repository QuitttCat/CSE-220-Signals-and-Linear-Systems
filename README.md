# CSE 220 – Signals and Linear Systems
[![Stars](https://img.shields.io/github/stars/QuitttCat/CSE-220-Signals-and-Linear-Systems?style=flat-square&logo=github)](https://github.com/QuitttCat/CSE-220-Signals-and-Linear-Systems/stargazers)
[![Forks](https://img.shields.io/github/forks/QuitttCat/CSE-220-Signals-and-Linear-Systems?style=flat-square&logo=github)](https://github.com/QuitttCat/CSE-220-Signals-and-Linear-Systems/network/members)
![Repo Size](https://img.shields.io/github/repo-size/QuitttCat/CSE-220-Signals-and-Linear-Systems?style=flat-square)
[![License](https://img.shields.io/github/license/QuitttCat/CSE-220-Signals-and-Linear-Systems?style=flat-square)](LICENSE)
![Last Commit](https://img.shields.io/github/last-commit/QuitttCat/CSE-220-Signals-and-Linear-Systems?style=flat-square&logo=git)
## 🚀 Tech Stack
### Languages
![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
### Frameworks & Libraries
![NumPy](https://img.shields.io/badge/NumPy-1.x-lightgrey?style=flat-square&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-blue?style=flat-square)
![SciPy](https://img.shields.io/badge/SciPy-1.x-green?style=flat-square&logo=scipy)
### Developer Tools
![VS Code](https://img.shields.io/badge/VSCode-Editor-blue?style=flat-square&logo=visualstudiocode)
![Git](https://img.shields.io/badge/Git-VersionControl-orange?style=flat-square&logo=git)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat-square&logo=jupyter)
---
## 📚 Table of Contents
- [Overview](#overview)
- [Offline 1 – Convolution](#offline-1--convolution)
- [Offline 2 – Fourier Series Approximation](#offline-2--fourier-series-approximation)
- [Offline 3 – Fourier Transform](#offline-3--fourier-transform)
- [Offline 4 – Discrete Fourier Transform & FFT](#offline-4--discrete-fourier-transform--fft)
- [Installation & Running](#installation--running)
- [Folder Structure](#folder-structure)
- [Author](#author)
- [Star & Support](#star--support)
---
## 🧠 Overview
This repository contains full implementations and reports for
**CSE 220 – Signals and Linear Systems (BUET, Level 2 Term 2)**.
These assignments cover:
- Convolution in discrete and continuous signals
- Fourier Series approximation for periodic functions
- Fourier Transform and Inverse Fourier Transform
- Discrete Fourier Transform (DFT), Fast Fourier Transform (FFT), and applications like cross-correlation and denoising
---
## Offline 1 – Convolution
- Discrete and continuous signal representations
- Linear Time-Invariant (LTI) systems
- Impulse response and decomposition
- Visualization of inputs, impulses, and outputs
---
## Offline 2 – Fourier Series Approximation
- Fourier Series from scratch
- Coefficients calculation (a0, an, bn) using numerical integration
- Approximation for square, sawtooth, triangle, sine, cosine waves
- Plotting original vs. approximated functions
---
## Offline 3 – Fourier Transform
- Custom Fourier Transform (FT) and Inverse FT (IFT)
- Approximation of parabolic, triangular, sawtooth, rectangular functions
- Frequency spectrum analysis
- Audio denoising using FT (buzzjc.wav → denoised_audio.wav)
---
## Offline 4 – Discrete Fourier Transform & FFT
- DFT-based cross-correlation for signal lag detection
- Custom DFT, IDFT, FFT, IFFT implementations
- Runtime comparison (DFT vs. FFT, IDFT vs. IFFT)
- Plots for signals, spectra, correlations, and runtimes
---
## ⚙ Installation & Running
### Clone Repository
```bash
git clone https://github.com/QuitttCat/CSE-220-Signals-and-Linear-Systems.git
cd CSE-220-Signals-and-Linear-Systems
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Run Assignments
```bash
python Offline\ 1\ -\ Convolution/2105044.py # Offline 1
jupyter notebook Offline\ 2\ -\ Fourier\ Series\ Approximation/offline.ipynb # Offline 2
jupyter notebook Offline\ 3\ -\ Fourier\ Transform/task1.ipynb # Offline 3 Task 1
jupyter notebook Offline\ 3\ -\ Fourier\ Transform/task2.ipynb # Offline 3 Task 2
jupyter notebook Offline\ 4\ -\ Discrete\ Fourier\ Transform\ \&\ FFT/Task1.ipynb # Offline 4 Task 1
jupyter notebook Offline\ 4\ -\ Discrete\ Fourier\ Transform\ \&\ FFT/Task2.ipynb # Offline 4 Task 2
```
---
## 📁 Folder Structure
```
CSE-220-Signals-and-Linear-Systems/
│
├── Offline 1 - Convolution/
│   ├── 2105044.py
│   └── CSE220_offline_1.pdf
│
├── Offline 2 - Fourier Series Approximation/
│   ├── Offline Description.pdf
│   ├── offline.ipynb
│   └── template.py
│
├── Offline 3 - Fourier Transform/
│   ├── buzzjc.wav
│   ├── denoised_audio.wav
│   ├── Offline_CSE220_FT.pdf
│   ├── task1.ipynb
│   └── task2.ipynb
│
├── Offline 4 - Discrete Fourier Transform & FFT/
│   ├── task 1 plots/
│   ├── task 2 plots/
│   ├── offline_4.pdf
│   ├── Task1.ipynb
│   └── Task2.ipynb
│
└── README.md
```
---
## 👤 Author
**Niloy Kumar Mondal**  
Student ID: **2105044**  
GitHub: https://github.com/QuitttCat  
---
## ⭐ Star & Support
If you found this repository helpful, please ⭐ star it on GitHub.  
Your support motivates future contributions! ❤️
