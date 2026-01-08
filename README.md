# Railway Calculator

## 📖 About the Project
This project is a robust web application designed for Transport Engineers and students. It combines a secure user authentication system with a specialized engineering suite for Railway Geometric and Structural Design.

The main goal is to automate the complex calculations required for railway engineering, validating parameters like Superelevation, Speed Limits, and Rail Structural Integrity according to standard engineering criteria (AREMA/CEFET-MG).

## ⚙️ Features

### 🔐 Core System
* User Authentication: Secure Login, Registration, and Logout system using password hashing.
* Responsive Interface: Clean UI built with Bootstrap 5, featuring tabbed navigation for easy access to tools.

### 📐 Module 1: Superelevation Calculator
Determines the required superelevation ($h$) based on four critical engineering criteria:
1.  Theoretical Criterion: Equilibrium of centrifugal force.
2.  Safety Criterion (Dynamic): Stability of the vehicle while in motion.
3.  Safety Criterion (Static): Stability of the vehicle when stopped on the curve.
4.  Comfort Criterion: Limits the uncompensated lateral acceleration for passengers.

### 🚂 Module 2: Speed & Geometry Calculator
Validates the operational limits of a curve based on track geometry:
1.  Maximum Speed ($V_{max}$): Calculates limits based on Safety and Comfort.
2.  Minimum Speed ($V_{min}$): Determines the minimum speed to prevent internal tipping.
3.  Minimum Radius ($R_{min}$): Calculates the strictest radius required for a desired speed.
4.  Gauge Widening (Superlargura): Calculates necessary gauge widening for tight curves.

### 🛤️ Module 3: Rail Dimensioning (New in v1.2.0)
Verifies if a specific rail profile is suitable for the operational load using structural mechanics:
1.  Dynamic Load Analysis: Calculates the Dynamic Coefficient ($C_d$) based on speed.
2.  Bending Moment ($M_{max}$): Compares results from Winkler's Method (Fixed Supports) and Zimmermann's Method (Elastic Foundation).
3.  Stress Verification: Checks if the working stress ($\sigma$) exceeds the steel's admissible limits ($\sigma_{adm}$).

### 🪵 Module 4: Sleeper Dimensioning (New in v1.3.0)
Validates the structural integrity of wooden sleepers (dormentes) under dynamic loads:
1.  Load Distribution: Calculates the effective load acting on a single sleeper ($P$) considering vehicle axle spacing ($d$) and sleeper spacing ($a$).
2.  Dynamic Analysis: Applies the Dynamic Coefficient ($C_d$) to the static wheel load.
3.  Stress Verification: Determines the maximum bending moment ($M_{max}$) and checks if the resulting flexural stress ($\sigma$) is within the timber's admissible limits ($\sigma_{adm}$).

### 🪨 Module 5: Ballast Dimensioning (New in v1.4.0)
Determines the required ballast layer thickness to protect the subgrade:
1.  Talbot's Analysis: Calculates the minimum ballast depth ($h$) required to reduce the pressure at the sleeper interface ($\sigma_0$) to the subgrade's admissible limit ($\sigma_{adm}$).
2.  Pressure Distribution: Generates an interactive chart to visualize how stress decreases with depth ($z$).
3.  Dynamic Load: Considers the vehicle's speed and dynamic impact ($C_d$) on the load distribution.

## 🛠️ Technologies Used
* Language: Python
* Web Framework: Flask
* Database: SQLite (via SQLAlchemy)
* Security: Flask-Bcrypt, Flask-Login, Flask-WTF
* Frontend: HTML5, CSS3, Bootstrap 5, Jinja2, Chart.js (for data visualization)
* Math: Custom engineering algorithms based on standard railway mechanics literature (e.g., BRINA, NABAIS).

## 🚀 Project Ambition
The ambition of this project is to become a handy, quick-reference tool for railway engineers to validate track parameters instantly. It aims to bridge the gap between theoretical formulas and practical, on-the-fly verification in the field or office.

## 📍 Current Stage
Status: Active (v1.4.0)
* v1.0: Superelevation Calculator & Auth System.
* v1.1: Added Speed & Geometry Calculator module.
* v1.2: Added Rail Dimensioning (Structural Analysis) module.
* v1.3: Added railroad tie Dimensioning module.
* v1.4: Added Ballast Dimensioning module with interactive charts.


The application is fully functional. Users can register, log in, and perform complex geometric and structural calculations using real-world variables.

## 🐛 Known Issues & Future Improvements
While the project is finished, there is always room for evolution:
* Unit Conversion: Currently accepts inputs in standard metric units (kgf, cm, km/h). Future updates could include unit conversion (SI/Imperial).
* Calculation History: We have a database for users, but currently, we do not save the calculation history. This is a planned feature.
* Formula Standards: The calculations are based on specific academic literature. Adding a toggle for different international standards (UIC, ABNT) would be a great addition.


---
*Developed by Luciano Faria - Transport Engineer*