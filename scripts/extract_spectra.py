import sys
import os
import glob

import ciao_contrib.runtool as ciao
from sherpa.astro import ui as sherpa

#---------------------------------------
#To call the script, use the following command:
# python extract_spectra.py file_region_name  ####run_name
#---------------------------------------


file_region_name = str(sys.argv[1])
run_name='run_020425_'
# run_name = str(sys.argv[2])


who_is_running_this_notebook = "Osase"
if who_is_running_this_notebook == "Grant":
    starting_dir = '/Users/grant/Science/ChandraA2597'
elif who_is_running_this_notebook == "Osase":
    starting_dir = '/Users/osaseomoruyi/research/a2597/chandra/careful_analysis/'

sb_path = starting_dir  + 'joint_analysis/'
file_region_path = starting_dir + 'regions/'

os.chdir(sb_path)


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


print(f'Now working in directory {os.getcwd()}')


def extract_spectra(file_region_name, file_region_path, run_name='run1'):

    #create folder to store xtraction in
    rname = file_region_name.split('.')[0]
    extract_folder_name = f'{rname}_extract'
    if not os.path.exists(extract_folder_name):
        os.makedirs(extract_folder_name)
        print(f'Made directory {extract_folder_name}')
    else:
        print(f'Directory {extract_folder_name} already exists')


    save_name = run_name + rname
    unique_run_name = save_name

    #open annuli
    with open(file_region_path + file_region_name) as f:
        list_of_annuli_strings = [ line.strip() for line in f ]

    print(f'Running {len(list_of_annuli_strings)} annuli: {list_of_annuli_strings}')
    
    # Clean up existing files that conflict with this run name
    existing_run_files = glob.glob(f'{extract_folder_name}/*{unique_run_name}*')
    for f in existing_run_files:
        os.remove(f)


    # First, extract the spectra. This'll take a while :( 
    for i, annulus_string in enumerate(list_of_annuli_strings):
        
        for obsid in obsids:

            print(f'Extracting spectra from region {i} for {obsid}...') 
            ciao.specextract.punlearn()
            basename = f'{extract_folder_name}/{unique_run_name}_{obsid}_{i}'

            ciao.specextract(infile=f'{obsid}_repro_flarecleaned_evt2.fits[sky={annulus_string}]',
                        outroot=basename,
                        bkgfile=f'{obsid}_blanksky_evt.fits[sky={annulus_string}]',
                        bkgresp='no',
                        clobber=True,
                        parallel='yes',
                        )
            
            #*NOTE*: Since we are using the blank sky image, we need to reset the AREASCAL keyword in
            # the extracted background file to 1.0 to avoid over-subtraction
            sherpa.load_pha(f"{extract_folder_name}/{unique_run_name}_{obsid}_{i}_bkg.pi")
            sherpa.set_areascal(id=1, area=1.0)
            sherpa.save_pha(filename=f"{extract_folder_name}/{unique_run_name}_{obsid}_{i}_bkg.pi",
                clobber=True, id=1)
            #now reset sherpa
            sherpa.delete_data(1)
    
    print("**********************************")
    print(f'Whew! Finished extracting spectra and respones files: {extract_folder_name}/{unique_run_name}*')
    print("**********************************")


extract_spectra(file_region_name, file_region_path, run_name=run_name)