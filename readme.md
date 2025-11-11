# **Code, Calculations, and Notes for Omoruyi et al. (2025), submitted to ApJ**  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15383913.svg)](https://doi.org/10.5281/zenodo.15383913)

This repository houses all of the codes (contained in Jupyter Python notebooks as well as Python scripts) used in our newly published paper utilizing **Chandra X-ray observations** of the **cool core galaxy cluster Abell 2597**, complemented by **archival ALMA, SINFONI and GMRT data**, to analyze the impact of AGN feedback on the cluster's evolution.  

## **AGN Feedback and ICM Evolution in Abell 2597**  
A2597 is a well-studied cool-core cluster exhibiting  plentiful AGN activity: **X-ray bubbles, cavities**, potential **shock fronts**, and a **multiphase gas reservoir** spanning from X-ray-emitting plasma to cold molecular gas. Our deep **~600 ks Chandra dataset** allows us to:  
- Map **temperature, pressure, and entropy profiles** across the large-scale ICM and interest features within it  
- Identify **potential weak shocks** (\( \mathcal{M} \sim 1.05–1.14 \)) out to **~150 kpc scales**.  
- Examine how **AGN feedback regulates cooling** and fuels black hole accretion via **chaotic cold accretion (CCA)**.  

<div style="text-align:center;">
    <img src="a2597.png" alt="A multiphase look at the beautiful Abell 2597 cluster of galaxies :)" width="100%">
</div>
---

## **Jupyter Notebooks (Main Analysis)**
These notebooks contain the **full step-by-step data analysis**, including data reduction and spectral fitting!  

- **`1_download_clean_data.ipynb`** | Download and clean Chandra data for A2597.  
  - Requires **CIAO 4.16** or newer; data reduction follows standard **ACIS-S procedures**.  
- **`2_spectral_fitting.ipynb`** | Extract **temperature, density, pressure, entropy** from surface brightness profiles of the large-scale structure and features of interest.  
- **`3_spectral_maps.ipynb`** | Generate **high-resolution spectral maps** using [Jeremy Sanders' contour binning code](https://github.com/jeremysanders/contbin).  
- **`4_pyproffit_profiles.ipynb`** | Extract and fit **spectral profiles** with [`pyproffit`](https://github.com/domeckert/pyproffit).  
- **`5_spectral_profiles.ipynb`** |  
  - **Results from CCCPIV Spectral Profiles** → Spectral fits for large-scale cluster analysis (\( M_{500}, R_{500} \)).  
  - **By-Hand Spectral Profiles** → Straightforward fits for the **central 150 kpc**.  
- **`6_xray_analysis.ipynb`** | General analysis of **all identified cluster features** in prior notebooks.  

---

## ** `scripts/` – Spectral Extraction & Fitting Codes**  
Standalone Python scripts used for **extracting spectra, fitting spectra, and generating the spectral maps**. Follow the notebooks to learn how to use them.
- **`create_spectral_maps.py`** → Generate spectral maps of **temperature, entropy**, and **pressure**.  
- **`extract_contbin_spectra.py`** → Extract spectra from **contour-binned regions**.  
- **`extract_spectra.py`** → Extract spectra from **regions of interest** (e.g., **large scale linear annuli, shock fronts**).  
- **`fit_contbin_spectra.py`** → Fit spectra from contour-binned regions.  

---

## **`archival_data/` – ALMA Data**
Contains **archival ALMA observations** relevant to A2597's CCA analysis.  

- **`abell297_vel.fits`** → ALMA Velocity map.  
- **`abell_2597_vdisp.fits`** → ALMA Velocity dispersion map.  

---

## **`spectral_profiles/` – Spectral Fitting Outputs**  
Data products from **spectral fitting**.  

- **`accept_main_table.txt`** | Cavagnolo et al. (2008) data for nearby cool-core clusters.  
- **`byhand_020125_fine_Iss_annuli_abundance.npy`** | Fitted spectra results from **notebooks 2 & 3**.  
- **`byhand_timescales.npy`** | Derived timescales from **notebook 5**.  
- **`masses.par`** | Output from **CCCPIV spectral fitting** by Vikhlinin & Tremblay (in prep).  
- **`.flat` and `.flat.spec` files** | Spectral fitting outputs from CCCPIV.  

---

## **Contact**
For questions or access to reduced data products not provided here, don't hesistate to email me at **osase.omoruyi@gmail.com**!