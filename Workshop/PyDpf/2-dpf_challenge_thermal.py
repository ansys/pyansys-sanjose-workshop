
# =========================================================================================
# Workshop : "Plot Element Volume" and "Extract Data from Contacts"
# =========================================================================================

"""
-  The provided analysis is a Transient Thermal Mechanical model.
-  This workshop does not require any specific knowledge in Mechanical discipline
"""

# =========================================================================================
# Challenge 1
# =========================================================================================


"""
***
### Aim of this Challenge 1 : "Plot Element Volume"
### To use PyDPF to extract Elemental Volumes from results  and plot them using the DpfPlotter (based on PyVista library) and a custom legend output
***



-  Hints for Challenge 1: 
    - Import the necessary Modules (already done in Challenge 1)
    - Create a DPF model from the "transient_thermal.rth" file in the "inputs" folder  (already done in Chalenge 1)
    - Select the Named Selection named PCB_CONT_2 and Scope it  to corresponding Mesh
    - Choose Results Property – elemental_volume . Scope to Any time point.
    - Generate Contour Plot
    - Calculate and Print Min & Max Volume in the DPF Field 


Expected Outcomes:

a) Refer to 'challenges-reference.png'  in 'inputs' folder

b) 
Smallest Element's Volume:  7.74578318152308e-11  m3
Largest Element's Volume:  1.046723738795663e-07  m3

"""

# =========================================================================================
# Challenge 2
# =========================================================================================

"""

Aim of this Challenge 2 : "Extract Data from Contacts"
To use PyDPF to extract available Contact Results and plot them using the DpfPlotter (based on PyVista library) and a custom legend output


-  Hints for Challenge 2: 
You will have to use  nmisc (Nonsummablle Miscellaneous Qty)  operator for heatflow : dpf.operators.result.nmisc 
Search for 'Contact Element Heat flow' on the below page (pdf is in inputs folder) to get the item_index for the quantity

https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v241/en/ans_elem/Hlp_E_CONTA174.html?q=conta174
Also refer to challenges-reference.png  in 'inputs' folder


    -  Create an NMISC operator for Extracting Contact Results : use help(dpf.operators.result.nmisc) to understand the arguments
    -  Get Heat Flow through Contact
    -  Plot HEAT FLOW Contour through the contact pair
    -  Calculate Total(Sum) Heat Flow through the Contact (Use Numpy)

Expected Results:

a) Refer to 'challenges-reference.png'  in 'inputs' folder

b) Total Heat Flow:  1.76  [W]
"""


# =========================================================================================
# The Code
# =========================================================================================


# =========================================================================================
# Import Modules
# =========================================================================================
from ansys.dpf import core as dpf
from ansys.dpf.core.plotter import DpfPlotter
import numpy as np


# =========================================================================================
# Load result file and create model database
# =========================================================================================
# Define Datasource using result file
# Define Model using this datasource
# your code


# =========================================================================================
### 1. List Contents of Model and Plot Elemental Volume for Named Selection named "PCB"
# =========================================================================================
# your code


# =========================================================================================
### 2. Contact post processing  
# =========================================================================================
# your code


# =========================================================================================
### 2B.  Plot HEAT FLOW Contour through the contact pair
# =========================================================================================
# your code


# =========================================================================================
### 2C. Sum up (using numpy) and Print TOTAL HEAT FLOW through a contact pair 
# =========================================================================================
# your code





