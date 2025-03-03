import sys
import os
import glob

import ciao_contrib.runtool as ciao
from sherpa.astro import ui as sherpa


obsids = [ # '922', # 922 is in FAINT mode and has a terrible flare, let's just ditch it M01
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


def extract_contbin_spectra(region_file, dir='extracted_spectra/'):
    
    for obsid in obsids:
        basename = obsid + '_' + region_file.split('.')[0]
        try:
            ciao.specextract.punlearn()

            ciao.specextract(infile=f'{obsid}_repro_flarecleaned_evt2.fits[sky=region({region_file})]',
                            outroot=dir+basename,
                            bkgfile=f'{obsid}_blanksky_evt.fits[sky=region({region_file})]',
                            clobber=True,
                            bkgresp='no',
                            parallel='yes')
        except OSError as e:
            print(f'{e}')

working_dir = 'extracted_spectra'
if not os.path.exists(working_dir):
    os.makedirs(working_dir)
    print(f'Made directory {working_dir}')
else:
    print(f'Directory {working_dir} already exists')

region_files = glob.glob('ciao*xaf*.reg') 

for idr, region_file in enumerate(region_files):

    print(f'.......... Extracting region ({idr+1}/{len(region_files)}..........')
    extract_contbin_spectra(region_file)