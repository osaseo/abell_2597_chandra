# **Code, Calculations, and Notes for Omoruyi et al. (2025), submitted to ApJ**  
DOI  

This repository houses all of the codes and calculations (contained in Jupyter Python notebooks as well as standalone Python scripts) associated with our paper on **Chandra X-ray observations** of the **cool core galaxy cluster Abell 2597**, complemented by **archival ALMA, SINFONI and GMRT data**.  

## **AGN Feedback and ICM Evolution in Abell 2597**  
A2597 is a well-studied cool-core cluster exhibiting multiple **AGN-driven X-ray cavities**, potential **cocoon shocks**, and a **multiphase gas reservoir** spanning from X-ray-emitting plasma to cold molecular gas. Our deep **~600 ks Chandra dataset** allows us to:  
- Map **temperature, pressure, and entropy profiles** across key ICM structures.  
- Identify **potential weak shocks** (\( \mathcal{M} \sim 1.07–1.14 \)) at **~150 kpc scales**.  
- Examine how **AGN feedback regulates cooling** and fuels black hole accretion via **chaotic cold accretion (CCA)**.  

---

## **📂 Jupyter Notebooks (Main Analysis)**
These notebooks contain the **full step-by-step data analysis**, including data reduction and spectral fitting!  

- **`1_download_clean_data.ipynb`** | Download and clean Chandra data for A2597.  
  - Requires **CIAO 4.16**; data reduction follows standard **ACIS-S procedures**.  
- **`2_spectral_fitting.ipynb`** | Extract **temperature, density, pressure, entropy** from surface brightness profiles.  
- **`3_spectral_maps.ipynb`** | Generate **high-resolution spectral maps** using [Jeremy Sanders' contour binning code](https://github.com/jeremysanders/contbin).  
- **`4_pyproffit_profiles.ipynb`** | Extract and fit **spectral profiles** with [`pyproffit`](https://github.com/domeckert/pyproffit).  
- **`5_spectral_profiles.ipynb`** |  
  - **CCCPIV Spectral Profiles** → Spectral fits for large-scale cluster analysis (\( M_{500}, R_{500} \)).  
  - **By-Hand Spectral Profiles** → Custom fits for **central 200 arcseconds**.  
- **`6_xray_analysis.ipynb`** | General analysis of **all identified cluster features** in prior notebooks.  

---

## **📂 `scripts/` – Spectral Extraction & Fitting Codes**  
Standalone Python scripts used for **extracting spectra, fitting spectral models, and generating maps** used in the notebooks.  

- **`create_spectral_maps_noabundance.py`** → Generate spectral maps (**\( kT, n_e \)**) without fitting abundance.  
- **`create_spectral_maps.py`** → Generate spectral maps including **\( Z \) (metallicity)**.  
- **`extract_contbin_spectra.py`** → Extract spectra from **contour-binned regions**.  
- **`extract_spectra.py`** → Extract spectra from **regions of interest** (e.g., **linear annuli, cocoon shocks**).  
- **`fit_contbin_spectra_noabundance.py`** → Fit spectra from contour-binned regions, **without abundance fitting**.  
- **`fit_contbin_spectra.py`** → Fit spectra from contour-binned regions, **including abundance fitting**.  

---

## **📂 `archival_data/` – ALMA Data**
Contains **archival ALMA observations** relevant to A2597's CCA analysis.  

- **`abell297_vel.fits`** → ALMA Velocity map.  
- **`abell_2597_vdisp.fits`** → ALMA Velocity dispersion map.  

---

## **📂 `spectral_profiles/` – Spectral Fitting Outputs**  
Data products from **spectral fitting**.  

- **`accept_main_table.txt`** | Cavagnolo et al. (2008) data for nearby cool-core clusters.  
- **`byhand_020125_fine_Iss_annuli_abundance.npy`** | Fitted spectra results from **notebooks 2 & 3**.  
- **`byhand_timescales.npy`** | Derived timescales from **notebook 5**.  
- **`masses.par`** | Output from **CCCPIV spectral fitting** by Vikhlinin & Tremblay (in prep).  
- **`.flat` and `.flat.spec` files** | Spectral fitting outputs from CCCPIV.  

---

## **📩 Contact**
For questions or access to reduced data products not provided here, don't hesistate to email **Osase Omoruyi** at **osase.omoruyi@gmail.com**.  