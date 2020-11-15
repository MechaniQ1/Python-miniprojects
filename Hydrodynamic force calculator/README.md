# Hydrodynamic Force Calculator

## General info
This console based application is a part of my Master Thesis which will be defended at the Gdansk University of Technology. This program calculates hydrodynamic force acting on the submarine pipeline.
## How it works
This application gets data from the file 'dane.txt'. Next it calculates buoyancy force, wave-induced pore pressure oscillations in around the pipeline using two models (potential and diffusion model) and hydrodynamic force. 
Program also writes pressure values to file 'results.xlsx'. Calculations are performed only for finite thickness of seabed layer.

## Technologies
* Python 3.7
Libraries:
* openpyxl