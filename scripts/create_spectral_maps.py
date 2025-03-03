import os
import glob
import json

#----------------------------------------------------------------------------------------------------------------------------
#CREATE SPECTRAL MAPS
#----------------------------------------------------------------------------------------------------------------------------


#about contbin creation
sn = 100 
smooth_sn = 15
constrain_value = 2
region_scale = 'lss' #large scale structure
dir_name = f'{sn}_constrain{constrain_value}_smooth{smooth_sn}_{region_scale}_region'


#convert json files to contbin files
def convert_json_results_to_contbin_files(json_file):
    with open(json_file) as f:
        fit = json.load(f)

    contbin_fit_filename = json_file.split('.')[0] + '_out.txt'

    contbin_string = f'''kT {fit['apec.kT'][0]}\nkT_uerr {fit['apec.kT'][2]}\nkT_lerr {fit['apec.kT'][1]}\nAbundanc {fit['apec.Abundanc'][0]}\nAbundanc_uerr {fit['apec.Abundanc'][2]}\nAbundanc_lerr {fit['apec.Abundanc'][1]}\nNorm {fit['apec.norm'][0]}\nNorm_uerr {fit['apec.norm'][2]}\nNorm_lerr {fit['apec.norm'][2]}'''.replace('None', '9999') # replace None with 9999 so paint_output_images doesn't freak out
    with open(contbin_fit_filename, 'w') as f:
        f.write(contbin_string)
    print(f'Wrote {contbin_fit_filename}')


json_files = glob.glob('*.json')
error_files = []
good_files = []
good_regions = []

for json_file in json_files:
    try:
        convert_json_results_to_contbin_files(json_file)
        good_files.append(json_file[:-5] + '_out.txt')
        good_regions.append(json_file[:-9] + '.reg')
    except:
        print("\n********************************************************")
        print(f'Error with {json_file}')
        error_files.append(json_file)
        print("********************************************************")
        continue

region_list = good_regions 

with open('region_list.txt', 'w') as f:
    for region in region_list:
        f.write(region.replace('.reg','')+ ' ' + region + '\n')


#Paint the Temperature, Abundance, and Norm maps

os.system(f'''
          paint_output_images --binmap=contbin_out{dir_name}.fits
            ''')

    