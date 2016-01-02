#!/usr/bin/env python
# Copyright (C) 2015 Andy Aschwanden

import itertools
from collections import OrderedDict
import os
from argparse import ArgumentParser
from resources import *

grid_choices = [18000, 9000, 4500, 3600, 1800, 1500, 1200, 900, 600, 450, 300, 150]

# set up the option parser
parser = ArgumentParser()
parser.description = "Generating scripts for model initialization."
parser.add_argument("-n", '--n_procs', dest="n", type=int,
                    help='''number of cores/processors. default=64.''', default=64)
parser.add_argument("-w", '--wall_time', dest="walltime",
                    help='''walltime. default: 12:00:00.''', default="12:00:00")
parser.add_argument("-q", '--queue', dest="queue", choices=['standard_4', 'standard_16', 'standard', 'gpu', 'gpu_long', 'long', 'normal'],
                    help='''queue. default=standard_4.''', default='standard_4')
parser.add_argument("--climate", dest="climate",
                    choices=['const', 'paleo'],
                    help="Climate", default='paleo')
parser.add_argument("--calving", dest="calving",
                    choices=['float_kill', 'ocean_kill', 'eigen_calving'],
                    help="claving", default='ocean_kill')
parser.add_argument("-d", "--domain", dest="domain",
                    choices=['gris'],
                    help="sets the modeling domain", default='gris')
parser.add_argument("-f", "--o_format", dest="oformat",
                    choices=['netcdf3', 'netcdf4_parallel', 'pnetcdf'],
                    help="output format", default='netcdf4_parallel')
parser.add_argument("-g", "--grid", dest="grid", type=int,
                    choices=grid_choices,
                    help="horizontal grid resolution", default=9000)
parser.add_argument("--o_size", dest="osize",
                    choices=['small', 'medium', 'big', '2dbig'],
                    help="output size type", default='2dbig')
parser.add_argument("-s", "--system", dest="system",
                    choices=['pleiades', 'fish', 'pacman', 'debug'],
                    help="computer system to use.", default='pacman')
parser.add_argument("-b", "--bed_type", dest="bed_type",
                    choices=['ctrl', 'old_bed', 'ba01_bed', '970mW_hs', 'jak_1985', 'cresis'],
                    help="output size type", default='ctrl')
parser.add_argument("--bed_deformation", dest="bed_deformation",
                    choices=[None, 'lc', 'iso'],
                    help="Bed deformation model.", default=None)
parser.add_argument("--forcing_type", dest="forcing_type",
                    choices=['ctrl', 'e_age'],
                    help="output size type", default='ctrl')
parser.add_argument("--stress_balance", dest="stress_balance",
                    choices=['sia', 'ssa+sia', 'ssa'],
                    help="stress balance solver", default='ssa+sia')
parser.add_argument("--dataset_version", dest="version",
                    choices=['2'],
                    help="input data set version", default='2')


options = parser.parse_args()

nn = options.n
oformat = options.oformat
osize = options.osize
queue = options.queue
walltime = options.walltime
system = options.system

calving = options.calving
climate = options.climate
forcing_type = options.forcing_type
grid = options.grid
bed_deformation = options.bed_deformation
bed_type = options.bed_type
version = options.version
stress_balance = options.stress_balance

domain = options.domain
pism_exec = generate_domain(domain)
save_times = [-25000, -5000, -1500, -1000, -500, -200, -100]

    
infile = ''
pism_dataname = 'pism_Greenland_{}m_mcb_jpl_v{}_{}.nc'.format(grid, version, bed_type)


# ########################################################
# set up model initialization
# ########################################################

hydro = 'null'

sia_e = (3.0)
ssa_n = (3.25)
ssa_e = (1.0)

ppq_values = [0.25, 0.33, 0.60]
tefo_values = [0.020, 0.025, 0.030]
phi_min_values = [5.0]
phi_max_values = [40.]
topg_min_values = [-700]
topg_max_values = [700]
combinations = list(itertools.product(ppq_values, tefo_values, phi_min_values, phi_max_values, topg_min_values, topg_max_values))

tsstep = 'yearly'
exstep = '100'

scripts = []

start = -125000
end = 0

for n, combination in enumerate(combinations):

    ppq, tefo, phi_min, phi_max, topg_min, topg_max = combination

    ttphi = '{},{},{},{}'.format(phi_min, phi_max, topg_min, topg_max)

    name_options = OrderedDict()
    name_options['sia_e'] = sia_e
    name_options['ppq'] = ppq
    name_options['tefo'] = tefo
    name_options['ssa_n'] = ssa_n
    name_options['ssa_e'] = ssa_e
    name_options['phi_min'] = phi_min
    name_options['phi_max'] = phi_max
    name_options['topg_min'] = topg_min
    name_options['topg_max'] = topg_max
    name_options['calving'] = calving
    if calving in ('eigen_calving'):
        name_options['calving_k'] = calving
        name_options['calving_thk_threshold'] = calving
    name_options['forcing_type'] = forcing_type
    
    vversion = 'v' + str(version)
    experiment =  '_'.join([climate, vversion, bed_type, '_'.join(['_'.join([k, str(v)]) for k, v in name_options.items()])])

        
    script = 'init_{}_g{}m_{}.sh'.format(domain.lower(), grid, experiment)
    scripts.append(script)
    
    for filename in (script):
        try:
            os.remove(filename)
        except OSError:
            pass

    pbs_header = make_pbs_header(system, nn, walltime, queue)
            
    with open(script, 'w') as f:

        f.write(pbs_header)

        outfile = '{domain}_g{grid}m_spinup_straight_{experiment}_0.nc'.format(domain=domain.lower(),grid=grid, experiment=experiment)

        prefix = generate_prefix_str(pism_exec)

        general_params_dict = OrderedDict()
        general_params_dict['i'] = pism_dataname
        general_params_dict['bootstrap'] = ''
        general_params_dict['ys'] = start
        general_params_dict['ye'] = end
        general_params_dict['o'] = outfile
        general_params_dict['o_format'] = oformat
        general_params_dict['o_size'] = osize
        general_params_dict['config_override'] = 'init_config.nc'
        general_params_dict['age'] = ''
        if bed_deformation is not None:
            general_params_dict['bed_def'] = bed_deformation
        if forcing_type in ('e_age'):
            general_params_dict['e_age_coupling'] = ''
        
        grid_params_dict = generate_grid_description(grid)

        sb_params_dict = OrderedDict()
        sb_params_dict['sia_e'] = sia_e
        sb_params_dict['ssa_e'] = ssa_e
        sb_params_dict['ssa_n'] = ssa_n
        sb_params_dict['pseudo_plastic_q'] = ppq
        sb_params_dict['till_effective_fraction_overburden'] = tefo
        sb_params_dict['topg_to_phi'] = ttphi

        stress_balance_params_dict = generate_stress_balance(stress_balance, sb_params_dict)
        climate_params_dict = generate_climate(climate)
        ocean_params_dict = generate_ocean(climate)
        hydro_params_dict = generate_hydrology(hydro)
        calving_params_dict = generate_calving(calving, ocean_kill_file=pism_dataname)

        exvars = "climatic_mass_balance_cumulative,tempsurf,diffusivity,temppabase,bmeltvelsurf_mag,mask,thk,topg,usurf,taud_mag,velsurf_mag,climatic_mass_balance,climatic_mass_balance_original,velbase_mag,tauc,taub_mag"
        spatial_ts_dict = generate_spatial_ts(outfile, exvars, exstep, start=start, end=end)
        scalar_ts_dict = generate_scalar_ts(outfile, tsstep, start=start, end=end)
        snap_shot_dict = generate_snap_shots(outfile, save_times)

        
        all_params_dict = merge_dicts(general_params_dict, grid_params_dict, stress_balance_params_dict, climate_params_dict, ocean_params_dict, hydro_params_dict, calving_params_dict, spatial_ts_dict, scalar_ts_dict, snap_shot_dict)
        all_params = ' '.join([' '.join(['-' + k, str(v)]) for k, v in all_params_dict.items()])
        
        cmd = ' '.join([prefix, all_params, '2>&1 | tee job.${PBS_JOBID}'])

        f.write(cmd)
        f.write('\n')

        if vversion in ('v2', 'v2_1985'):
            mytype = "MO14 2015-04-27"
        else:
            import sys
            print('TYPE {} not recognized, exiting'.format(vversion))
            sys.exit(0)        
    
scripts = uniquify_list(scripts)

submit = 'submit_{domain}_g{grid}m_{climate}_{bed_type}.sh'.format(domain=domain.lower(), grid=grid, climate=climate, bed_type=bed_type)
try:
    os.remove(submit)
except OSError:
    pass

with open(submit, 'w') as f:

    f.write('#!/bin/bash\n')

    for k in range(len(scripts)):
        f.write('JOBID=$(qsub {script})\n'.format(script=scripts[k]))

print("\nRun {} to submit all jobs to the scheduler\n".format(submit))

