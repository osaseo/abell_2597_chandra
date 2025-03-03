import ciao_contrib.runtool as ciao
from sherpa.astro import ui as sherpa
import numpy as np
import logging
import matplotlib.pyplot as plt
import glob
import json
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
import astropy.units as u
import os

fit_image_folder = 'fit_images'
extract_folder_name = 'extracted_spectra'

if not os.path.exists(fit_image_folder):
    os.makedirs(fit_image_folder)
    print(f'Made directory {fit_image_folder}')
else:
    print(f'Directory {fit_image_folder} already exists')

obsids = [ # '922', # 922 is in FAINT mode and has a terrible flare, let's just ditch it
          '6934', # 56.0 ksec, Clarke ACIS-S3 VFAINT
          '7329', # 60.11 ksec, Clarke ACIS-S3 VFAINT
          '19596', # 69.39 ksec, Tremblay ACIS S3 VFAINT
          '19597', # 44.52
          '19598', # 14.34
          '20626', # 24.73
          '20627', # 20.85
          '20628', # 10.92
          '20629', # 56.36
          '20805', # 53.4
          '20806', # 37.62
          '20811', # 79.85
          '20817'] # 62.29

name = 'Abell 2597'
rah, decd = '23h25m19.7s', '-12d07m27s'
coord = SkyCoord(rah, decd, frame='icrs')
ra = coord.ra.degree
dec = coord.dec.degree
radius = Angle(20, u.arcsec)

z = 0.0821
zh = 0.0821
nH = 2.252e+20 # % (HI4PI)   DL,LAB: 2.500e+20 2.515e+20
kT_guess = 4.0 # keV
abundance_guess = 0.4
r500 = 904.8 # kpc This is R_500_Y from Vikhlinin et al.
r500_err = 2.4 #
m500 = 2.279e14 # Msol This is M_500_Y from Vikhlinin et al.
m500_err = 1.797e12

acis_pixel_scale = 0.4920 * u.arcsec

def fit_contbin_spectra(region_file, obsids):

    basename = region_file.split('.')[0]
    
    sherpa_log = logging.getLogger("Sherpa")
    sherpa_log.setLevel(logging.ERROR)

    print(f'Fitting region {basename}')

    for i, obsid in enumerate(obsids):
        pi_file_name = f'{extract_folder_name}/{obsid}_{basename}_grp.pi'
        bkg_pi_file_name = f'{extract_folder_name}/{obsid}_{basename}_bkg.pi'
        sherpa.load_pha(i, pi_file_name)
        sherpa.load_bkg(i, bkg_pi_file_name) # 
        sherpa.set_areascal(id=i, bkg_id=1, area=1.0)
        sherpa.subtract(i) # subtract the background
        sherpa.set_source(i, sherpa.xsphabs.phabs * sherpa.xsapec.apec)

    sherpa.set_analysis('energy')

    # usually the data is rather noisey below 0.7 keV and above 8.0 keV.
    # For low signal to noise regions, the high energy cutoff may need to
    # be lowered down (to 5 keV for example, look at the data).
    low_energy_cutoff = 0.5  # [units: keV]
    high_energy_cutoff = 7.0  # [units: keV]
    sherpa.notice(lo=low_energy_cutoff, hi=high_energy_cutoff) 

    total_counts = np.sum(sherpa.get_data().y)
    print("\n********************************************************")
    print(f'Number of counts in region {basename}: {total_counts}')
    print("********************************************************\n")


    # Define the model
    phabs.nH = nH / 1e22
    apec.kT = kT_guess
    apec.Abundanc = abundance_guess
    apec.redshift = z
    apec.norm = 1.0

    sherpa.freeze(phabs.nH, apec.redshift, apec.Abundanc)
    sherpa.thaw(apec.kT, apec.norm) #, apec.Abundanc)

    sherpa.fit()
    
    basic_fit_results = sherpa.get_fit_results()
    print(basic_fit_results)


    try:
        #print("trying")
        sherpa.calc_stat_info()
        rstat = sherpa.get_stat_info()[0].rstat
    except Exception as e:
        print(f'Error in sherpa.calc_stat_info(): {e}')
    

    if rstat < 3.0:
        print("\n********************************************************")
        print("successful fit") 
        print("********************************************************\n")
        # then good enough 
    
        sherpa.covar()
        sherpa.conf()

        fit_results = sherpa.get_conf_results()
        # covar_results = sherpa.get_covar_results()
        # confidence_fit_results = sherpa.get_conf_results()

        fit_results_to_export = fit_results

        # Make a dictionary of the results
        tmp0 = zip(fit_results_to_export.parvals, 
                    fit_results_to_export.parmins, 
                    fit_results_to_export.parmaxes)

        tmp1 = [(v, l, h) for (v, l, h) in tmp0]


        final_results_dict = dict(zip(fit_results_to_export.parnames, tmp1))

        # Save that results dict as a JSON for later parsing
        with open(f'{basename}_fit.json', 'w') as jdict:
            json.dump(final_results_dict, jdict, indent=4)

        print(f'Wrote {basename}_fit.json')

        sherpa.get_data_plot_prefs()['ylog'] = True
        sherpa.plot_fit_delchi(0)
        sherpa.plot_fit_delchi(1, overplot=True)

        # hijack the plot axes to override title
        fig = plt.gcf()
        fig.set_size_inches(12, 8)
        fig.get_axes()[0].set_title(f'{basename} | kT = {np.round(basic_fit_results.parvals[0],3)} keV | Stat = {np.round(rstat,3)}')
        plt.savefig(f'{fit_image_folder}/{basename}_good_fit.png', dpi=150)

    elif rstat > 3.0:

        #print("\n********************************************************")
        print("\nBAD fit") 
        #print("********************************************************\n")
        
        sherpa.plot_fit_delchi(0)
        sherpa.plot_fit_delchi(1, overplot=True)
        fig = plt.gcf()
        fig.set_size_inches(12, 8)
        plt.gcf().get_axes()[0].set_title(f'{basename} | Bad Fit | Stat = {rstat}')

        plt.savefig(f'{fit_image_folder}/{basename}_bad_fit.png')
        
    sherpa.clean()


region_list = glob.glob('ciao*xaf*.reg')

error_regions = []
good_regions = []
for idr, region_file in enumerate(region_list):
    print(f"region {idr+1}/{len(region_list)}: {region_file}")
    try:
        fit_contbin_spectra(region_file, obsids)
        good_regions.append(region_file)
    except:
        error_regions.append(region_file)
        print(f'Error with {region_file}')
        continue
print(f"{len(good_regions)} Final good regions: {good_regions}")
print(f"{len(error_regions)} Final bad regions: {error_regions}")
print("everything else good!")
