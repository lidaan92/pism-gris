#!/usr/bin/env python
# Copyright (C) 2016-17 Andy Aschwanden

import itertools
from collections import OrderedDict
import numpy as np
import os, sys, shlex
from os.path import join, abspath, realpath, dirname

try:
    import subprocess32 as sub
except:
    import subprocess as sub

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys

def current_script_directory():
    import inspect
    filename = inspect.stack(0)[0][1]
    return realpath(dirname(filename))

script_directory = current_script_directory()

sys.path.append(join(script_directory, "../resources"))
from resources import *

def map_dict(val, mdict):
    try:
        return mdict[val]
    except:
        return val

grid_choices = [18000, 9000, 6000, 4500, 3600, 3000, 2400, 1800, 1500, 1200, 900, 600, 450, 300, 150]

# set up the option parser
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.description = "Generating scripts for warming experiments."
parser.add_argument("FILE", nargs=1,
                    help="Input file to restart from", default=None)
parser.add_argument("-n", '--n_procs', dest="n", type=int,
                    help='''number of cores/processors. default=140.''', default=140)
parser.add_argument("-w", '--wall_time', dest="walltime",
                    help='''walltime. default: 100:00:00.''', default="100:00:00")
parser.add_argument("-q", '--queue', dest="queue", choices=list_queues(),
                    help='''queue. default=long.''', default='long')
parser.add_argument("--calving", dest="calving",
                    choices=['float_kill', 'vonmises_calving'],
                    help="calving", default='vonmises_calving')
parser.add_argument("-d", "--domain", dest="domain",
                    choices=['gris', 'gris_ext'],
                    help="sets the modeling domain", default='gris')
parser.add_argument("--exstep", dest="exstep",
                    help="Writing interval for spatial time series", default=10)
parser.add_argument("-f", "--o_format", dest="oformat",
                    choices=['netcdf3', 'netcdf4_parallel', 'pnetcdf'],
                    help="output format", default='netcdf4_parallel')
parser.add_argument("-g", "--grid", dest="grid", type=int,
                    choices=grid_choices,
                    help="horizontal grid resolution", default=9000)
parser.add_argument("--i_dir", dest="input_dir",
                    help="input directory", default=abspath(join(script_directory, "..")))
parser.add_argument("--o_dir", dest="output_dir",
                    help="output directory", default='.')
parser.add_argument("--o_size", dest="osize",
                    choices=['small', 'medium', 'big', 'big_2d', 'custom'],
                    help="output size type", default='custom')
parser.add_argument("-s", "--system", dest="system",
                    choices=list_systems(),
                    help="computer system to use.", default='pleiades_broadwell')
parser.add_argument("-b", "--bed_type", dest="bed_type",
                    choices=list_bed_types(),
                    help="output size type", default='no_bath')
parser.add_argument("--spatial_ts", dest="spatial_ts",
                    choices=['basic', 'standard', 'none'],
                    help="output size type", default='basic')
parser.add_argument("--forcing_type", dest="forcing_type",
                    choices=['ctrl', 'e_age'],
                    help="output size type", default='ctrl')
parser.add_argument("--hydrology", dest="hydrology",
                    choices=['null', 'diffuse', 'routing'],
                    help="Basal hydrology model.", default='diffuse')
parser.add_argument("-p", "--params", dest="params_list",
                    help="Comma-separated list with params for sensitivity", default=None)
parser.add_argument("--stable_gl", dest="float_kill_calve_near_grounding_line", action="store_false",
                    help="Stable grounding line", default=True)
parser.add_argument("--stress_balance", dest="stress_balance",
                    choices=['sia', 'ssa+sia', 'ssa'],
                    help="stress balance solver", default='ssa+sia')
parser.add_argument("--topg_delta", dest="topg_delta_file",
                    help="end of initialization detla=(topg-topg_initial) file", default=None)
parser.add_argument("--dataset_version", dest="version",
                    choices=['2', '3', '3a'],
                    help="input data set version", default='3a')
parser.add_argument("--vertical_velocity_approximation", dest="vertical_velocity_approximation",
                    choices=['centered', 'upstream'],
                    help="How to approximate vertical velocities", default='upstream')
parser.add_argument("--start_year", dest="start_year", type=int,
                    help="Simulation start year", default=0)
parser.add_argument("--duration", dest="duration", type=int,
                    help="Years to simulate", default=1000)
parser.add_argument("--step", dest="step", type=int,
                    help="Step in years for restarting", default=1000)
parser.add_argument("--test_climate_models", dest="test_climate_models", action="store_true",
                    help="Turn off ice dynamics and mass transport to test climate models", default=False)
parser.add_argument("-e", "--ensemble_file", dest="ensemble_file",
                    help="File that has all combinations for ensemble study", default=None)

options = parser.parse_args()

nn = options.n
input_dir = abspath(options.input_dir)
output_dir = abspath(options.output_dir)
spatial_tmp_dir = abspath(options.output_dir + '_tmp')

oformat = options.oformat
osize = options.osize
queue = options.queue
walltime = options.walltime
system = options.system

spatial_ts = options.spatial_ts

bed_type = options.bed_type
calving = options.calving
climate = 'warming'
exstep = options.exstep
float_kill_calve_near_grounding_line = options.float_kill_calve_near_grounding_line
forcing_type = options.forcing_type
frontal_melt = True
grid = options.grid
hydrology = options.hydrology
stress_balance = options.stress_balance
topg_delta_file = options.topg_delta_file
test_climate_models = options.test_climate_models
vertical_velocity_approximation = options.vertical_velocity_approximation
version = options.version

ensemble_file = options.ensemble_file

domain = options.domain
pism_exec = generate_domain(domain)

save_times = [92, 192, 492, 992]

if options.FILE is None:
    print('Missing input file')
    import sys
    sys.exit()
else:
    input_file = options.FILE[0]

if domain.lower() in ('greenland_ext', 'gris_ext'):
    pism_dataname = '$input_dir/data_sets/bed_dem/pism_Greenland_ext_{}m_mcb_jpl_v{}_{}.nc'.format(grid, version, bed_type)
else:
    pism_dataname = '$input_dir/data_sets/bed_dem/pism_Greenland_{}m_mcb_jpl_v{}_{}.nc'.format(grid, version, bed_type)

climate_file = '$input_dir/data_sets/climate_forcing/DMI-HIRHAM5_GL2_ERAI_2001_2014_YDM_BIL_EPSG3413_{}m.nc'.format(grid)

regridvars = 'litho_temp,enthalpy,age,tillwat,bmelt,ice_area_specific_volume,thk'

dirs = {"output": "$output_dir", "spatial_tmp": "$spatial_tmp_dir"}
for d in ["performance", "state", "scalar", "spatial", "snap", "jobs", "basins"]:
    dirs[d] = "$output_dir/{dir}".format(dir=d)

if spatial_ts == 'none':
    del dirs["spatial"]

# use the actual path of the run scripts directory (we need it now and
# not during the simulation)
scripts_dir = join(output_dir, "run_scripts")
if not os.path.isdir(scripts_dir):
    os.makedirs(scripts_dir)

# generate the config file *after* creating the output directory
pism_config = 'init_config'
pism_config_nc = join(output_dir, pism_config + ".nc")

cmd = "ncgen -o {output} {input_dir}/config/{config}.cdl".format(output=pism_config_nc,
                                                                 input_dir=input_dir,
                                                                 config=pism_config)
sub.call(shlex.split(cmd))

# these Bash commands are added to the beginning of the run scrips
run_header = """# stop if a variable is not defined
set -u
# stop on errors
set -e

# path to the config file
config="{config}"
# path to the input directory (input data sets are contained in this directory)
input_dir="{input_dir}"
# output directory
output_dir="{output_dir}"
# temporary directory for spatial files
spatial_tmp_dir="{spatial_tmp_dir}"

# create required output directories
for each in {dirs};
do
  mkdir -p $each
done

""".format(input_dir=input_dir,
           output_dir=output_dir,
           spatial_tmp_dir=spatial_tmp_dir,
           config=pism_config_nc,
           dirs=" ".join(dirs.values()))

# ########################################################
# set up model initialization
# ########################################################

ssa_n    = 3.25
ssa_e    = 1.0
tefo     = 0.020
phi_min  = 5.0
phi_max  = 40.
topg_min = -700
topg_max = 700

rcps            = ['cold', '26', '45', '85']
std_dev         = 4.23
firn            = 'ctrl'
lapse_rate      = 6
bed_deformation = 'ip'

try:
    combinations = np.loadtxt(ensemble_file, delimiter=',', skiprows=1)
except:
    combinations = np.genfromtxt(ensemble_file, dtype=None, delimiter=',', skip_header=1)

firn_dict = {-1.0: 'low', 0.0: 'off', 1.0: 'ctrl'}
ocs_dict  = {-2.0: 'off', -1.0: 'low', 0.0: 'mid', 1.0: 'high'}
ocm_dict  = {-1.0: 'low', 0.0: 'mid', 1.0: 'high', 2.0: 'm10', 3.0: 'm15'}
tct_dict  = {-1.0: 'low', 0.0: 'mid', 1.0: 'high'}
bd_dict   = {-1.0: 'off', 0.0: 'i0', 1.0: 'ip'}

tsstep = 'yearly'

scripts           = []
scripts_combinded = []
scripts_post      = []

simulation_start_year = options.start_year
simulation_end_year   = options.start_year + options.duration
restart_step          = options.step

if restart_step > (simulation_end_year - simulation_start_year):
    print('Error:')
    print('restart_step > (simulation_end_year - simulation_start_year): {} > {}'.format(restart_step, simulation_end_year - simulation_start_year))
    print('Try again')
    import sys
    sys.exit(0)

batch_header, batch_system = make_batch_header(system, nn, walltime, queue)
post_header = make_batch_post_header(system)

for n, combination in enumerate(combinations):

    for rcp in rcps:
        m_bd = None
        m_pdd = 0.0
        m_ohc = 0.0
        try:
            run_id, fice, fsnow, prs, rfr, ocm_v, ocs_v, tct_v, vcm, ppq, sia_e, m_bd, m_tlr, m_firn, m_pdd, m_ohc = combination
            bed_deformation = bd_dict[m_bd]
            firn = firn_dict[m_firn]
            lapse_rate = m_tlr
        except:
            run_id, fice, fsnow, prs, rfr, ocm_v, ocs_v, tct_v, vcm, ppq, sia_e = combination

        ocm = ocm_dict[ocm_v]
        ocs = ocs_dict[ocs_v]
        tct = ocs_dict[tct_v]

        ttphi = '{},{},{},{}'.format(phi_min, phi_max, topg_min, topg_max)

        name_options = {'rcp' : rcp}
        try:
            name_options['id'] = '{:03d}'.format(int(run_id))
        except:
            name_options['id'] = '{}'.format(run_id)
            

        vversion = 'v' + str(version)
        full_exp_name =  '_'.join([vversion, '_'.join(['_'.join([k, str(v)]) for k, v in name_options.items()])])
        full_outfile = 'g{grid}m_{experiment}.nc'.format(grid=grid, experiment=full_exp_name)

        forcing_files = {'cold' : 'pism_warming_climate_{tempmax}K.nc'.format(tempmax=-1),
                         'ctrl' : 'pism_warming_climate_{tempmax}K.nc'.format(tempmax=0),
                         '26'   : '$input_dir/data_sets/climate_forcing/tas_Amon_GISS-E2-H_rcp26_ensmean_ym_anom_GRIS_0-5000.nc',
                         '45'   : '$input_dir/data_sets/climate_forcing/tas_Amon_GISS-E2-H_rcp45_ensmean_ym_anom_GRIS_0-5000.nc',
                         '85'   : '$input_dir/data_sets/climate_forcing/tas_Amon_GISS-E2-H_rcp85_ensmean_ym_anom_GRIS_0-5000.nc'}

        climate_modifier_file = forcing_files[rcp]

        if m_ohc == 0:
            ocean_modifier_file = climate_modifier_file
        else:
            ocean_modifier_file = 'pism_step_climate_{}K.nc'.format(m_ohc)

        # All runs in one script file for coarse grids that fit into max walltime
        script_combined = join(scripts_dir, 'lhs_g{}m_{}_j.sh'.format(grid, full_exp_name))
        with open(script_combined, 'w') as f_combined:

            outfiles = []
            job_no = 0
            for start in range(simulation_start_year, simulation_end_year, restart_step):
                job_no += 1

                end = start + restart_step

                experiment =  '_'.join([vversion, '_'.join(['_'.join([k, str(v)]) for k, v in name_options.items()]), '{}'.format(start), '{}'.format(end)])

                script = join(scripts_dir, 'lhs_g{}m_{}.sh'.format(grid, experiment))
                scripts.append(script)

                for filename in (script):
                    try:
                        os.remove(filename)
                    except OSError:
                        pass

                if (start == simulation_start_year):
                    f_combined.write(batch_header)
                    f_combined.write(run_header)

                with open(script, 'w') as f:

                    f.write(batch_header)
                    f.write(run_header)

                    outfile = '{domain}_g{grid}m_{experiment}.nc'.format(domain=domain.lower(), grid=grid, experiment=experiment)

                    pism = generate_prefix_str(pism_exec)

                    general_params_dict = {
                        'profile':                     join(dirs["performance"], 'profile_${job_id}.py'.format(**batch_system)),
                        'ys':                          start,
                        'ye':                          end,
                        'calendar':                    '365_day',
                        'climate_forcing_buffer_size': 365,
                        'o':                           join(dirs["state"], outfile),
                        'o_format':                    oformat,
                        'config_override':             "$config"
                    }

                    if start == simulation_start_year:
                        general_params_dict['bootstrap'] = ''
                        general_params_dict['i'] = pism_dataname
                        general_params_dict['regrid_file'] = input_file
                        general_params_dict['regrid_vars'] = regridvars
                        general_params_dict['regrid_special'] = ''
                    else:
                        general_params_dict['i'] = regridfile

                    if (start == simulation_start_year) and (topg_delta_file is not None):
                        general_params_dict['topg_delta_file'] = topg_delta_file

                    if osize != 'custom':
                        general_params_dict['o_size'] = osize
                    else:
                        general_params_dict['output.sizes.medium'] = 'sftgif,velsurf_mag'
                        
                    if test_climate_models == True:
                        general_params_dict['test_climate_models'] = ''
                        general_params_dict['no_mass'] = ''

                    if bed_deformation != 'off':
                        general_params_dict['bed_def'] = 'lc'

                    if (bed_deformation == 'ip') and (start == simulation_start_year):
                        general_params_dict['bed_deformation.bed_uplift_file'] = '$input_dir/data_sets/uplift/uplift_g{}m.nc'.format(grid)

                    if forcing_type in ('e_age'):
                        general_params_dict['e_age_coupling'] = ''

                    if start == simulation_start_year:
                        grid_params_dict = generate_grid_description(grid, domain)
                    else:
                        grid_params_dict = generate_grid_description(grid, domain, restart=True)

                    sb_params_dict = {'sia_e':                              sia_e,
                                      'ssa_e':                              ssa_e,
                                      'ssa_n':                              ssa_n,
                                      'pseudo_plastic_q':                   ppq,
                                      'till_effective_fraction_overburden': tefo,
                                      'vertical_velocity_approximation':    vertical_velocity_approximation}

                    if start == simulation_start_year:
                        sb_params_dict['topg_to_phi'] = ttphi

                    stress_balance_params_dict = generate_stress_balance(stress_balance, sb_params_dict)

                    firn_files = {'off' : '$input_dir/data_sets/climate_forcing/firn_forcing_off.nc',
                                  'ctrl': '$input_dir/data_sets/climate_forcing/hirham_firn_depth_4500m_ctrl.nc'}

                    firn_file = firn_files[firn]

                    ice_density = 910.
                    climate_parameters = {'surface.pdd.factor_ice':                               fice / ice_density,
                                          'surface.pdd.factor_snow':                              fsnow / ice_density,
                                          'surface.pdd.refreeze':                                 rfr,
                                          'surface.pdd.std_dev':                                  std_dev,
                                          'atmosphere_given_file':                                climate_file,
                                          'atmosphere_given_period':                              1,
                                          'atmosphere_lapse_rate_file':                           climate_file,
                                          'atmosphere.precip_exponential_factor_for_temperature': prs / 100,
                                          'atmosphere_paleo_precip_file':                         climate_modifier_file,
                                          'atmosphere_delta_T_file':                              climate_modifier_file,
                                          'temp_lapse_rate':                                      lapse_rate}

                    if start == simulation_start_year:
                        climate_parameters['pdd_firn_depth_file'] = firn_file

                    climate_params_dict = generate_climate(climate, **climate_parameters)

                    if m_pdd == 1.0:
                        setattr(climate_params_dict, 'pdd_aschwanden', '')

                    ocean_files = {'low' : '$input_dir/data_sets/ocean_forcing/ocean_forcing_300myr_71n_10myr_80n.nc',
                                   'mid' : '$input_dir/data_sets/ocean_forcing/ocean_forcing_400myr_71n_20myr_80n.nc',
                                   'high': '$input_dir/data_sets/ocean_forcing/ocean_forcing_500myr_71n_30myr_80n.nc',
                                   'm10' : '$input_dir/data_sets/ocean_forcing/ocean_forcing_1000myr_71n_60myr_80n.nc',
                                   'm15' : '$input_dir/data_sets/ocean_forcing/ocean_forcing_1500myr_71n_90myr_80n.nc'}

                    ocean_file = ocean_files[ocm]

                    calving_thresholds = {'low' : '$input_dir/data_sets/ocean_forcing/tct_forcing_400myr_74n_50myr_76n.nc',
                                          'mid' : '$input_dir/data_sets/ocean_forcing/tct_forcing_500myr_74n_100myr_76n.nc',
                                          'high': '$input_dir/data_sets/ocean_forcing/tct_forcing_600myr_74n_150myr_76n.nc'}

                    tct_file = calving_thresholds[tct]

                    ocs_params = {'off': (1.0, 1.0),
                                  'low' : (0.5, 1.0),
                                  'mid' : (0.54, 1.17),
                                  'high': (0.85, 1.61)}

                    ocean_alpha, ocean_beta = ocs_params[ocs]

                    if ocs == 'off':
                        ocean_params_dict = generate_ocean('given',
                                                           **{'ocean_given_file': ocean_file})
                    else:
                        ocean_params_dict = generate_ocean('warming',
                                                           **{'ocean_given_file':                       ocean_file,
                                                              'ocean.runoff_to_ocean_melt_power_alpha': ocean_alpha,
                                                              'ocean.runoff_to_ocean_melt_power_beta':  ocean_beta,
                                                              'ocean_runoff_smb_file':                  ocean_modifier_file})

                    hydro_params_dict = generate_hydrology(hydrology)

                    calving_parameters = {'thickness_calving_threshold_file':     tct_file,
                                          'float_kill_calve_near_grounding_line': float_kill_calve_near_grounding_line,
                                          'frontal_melt':                         frontal_melt,
                                          'calving.vonmises.sigma_max':           vcm * 1e6}

                    calving_params_dict = generate_calving(calving, **calving_parameters)

                    scalar_ts_dict = generate_scalar_ts(outfile, tsstep,
                                                        start=simulation_start_year,
                                                        end=simulation_end_year,
                                                        odir=dirs["scalar"])
                    
                    all_params_dict = merge_dicts(general_params_dict,
                                                  grid_params_dict,
                                                  stress_balance_params_dict,
                                                  climate_params_dict,
                                                  ocean_params_dict,
                                                  hydro_params_dict,
                                                  calving_params_dict,
                                                  scalar_ts_dict)

                    if not spatial_ts == 'none':
                        if spatial_ts == 'basic':
                            exvars = basic_spatial_ts_vars()
                        else:
                            exvars = stability_spatial_ts_vars()
                        spatial_ts_dict = generate_spatial_ts(outfile, exvars, exstep, odir=dirs["spatial_tmp"], split=False)
                        snap_dict = generate_snap_shots(outfile, save_times, odir=dirs["snap"])

                        all_params_dict = merge_dicts(all_params_dict,
                                                      spatial_ts_dict,
                                                      snap_dict)

                    all_params = ' \\\n  '.join(["-{} {}".format(k, v) for k, v in all_params_dict.items()])

                    if system == 'debug':
                        redirect = ' 2>&1 | tee {jobs}/job_{job_no}.${job_id}'
                    else:
                        redirect = ' > {jobs}/job_{job_no}.${job_id} 2>&1'

                    template = "{mpido} {pism} {params}" + redirect

                    context = merge_dicts(batch_system,
                                          dirs,
                                          {"job_no" : job_no, "pism" : pism, "params" : all_params})
                    cmd = template.format(**context)

                    f.write(cmd)
                    f.write('\n')
                    f.write(batch_system.get("footer", ""))

                    f_combined.write(cmd)
                    f_combined.write('\n\n')

                    regridfile = join(dirs["state"], outfile)
                    outfiles.append(outfile)

            f_combined.write(batch_system.get("footer", ""))

        scripts_combinded.append(script_combined)

        script_post = join(scripts_dir, 'post_lhs_g{}m_{}.sh'.format(grid, full_exp_name))
        scripts_post.append(script_post)

        with open(script_post, 'w') as f:

            f.write(post_header)
            f.write(run_header)

            if exstep == 'monthly':
                mexstep = 1. / 12
            elif exstep == 'daily':
                mexstep = 1. / 365
            else:
                mexstep = int(exstep)

            real_start_year = 2008
            for start in range(simulation_start_year, simulation_end_year, restart_step):
                end = start + restart_step
                ts_file = join(dirs["scalar"], 'ts_{domain}_g{grid}m_{experiment}_{start}_{end}.nc'.format(domain=domain.lower(), grid=grid, experiment=full_exp_name, start=start, end=end))
                cmd = ' '.join(['adjust_timeline.py -i start -p yearly -a {}-1-1 -u seconds -d 2008-1-1'.format(real_start_year), '{}'.format(ts_file), '\n'])
                f.write(cmd)
                outfile = '{domain}_g{grid}m_{experiment}_{start}_{end}.nc'.format(domain=domain.lower(), grid=grid, experiment=full_exp_name, start=start, end=end)
                state_file = join(dirs["state"], outfile)
                cmd = ' '.join(['ncks -O -4 -L 9', state_file, state_file, '\n\n'])
                f.write(cmd)
                real_start_year += restart_step
            ts_files = join(dirs["scalar"], 'ts_{domain}_g{grid}m_{experiment}_*.nc'.format(domain=domain.lower(), grid=grid, experiment=full_exp_name))
            ts_file = join(dirs["scalar"], 'ts_{domain}_g{grid}m_{experiment}_{start}_{end}.nc'.format(domain=domain.lower(), grid=grid, experiment=full_exp_name, start=simulation_start_year, end=simulation_end_year))
            cmd = '#cdo -f nc4 -z zip_9 mergetime {} {}\n\n'.format(ts_files, ts_file)
            f.write(cmd)
            if not spatial_ts == 'none':
                for start in range(simulation_start_year, simulation_end_year, restart_step):
                    end = start + restart_step
                    extra_file_tmp = spatial_ts_dict['extra_file']
                    extra_file = '{}.nc'.format(os.path.split(extra_file_tmp)[-1].split('.nc')[0])
                    extra_file_wd = join(dirs["spatial"], extra_file)
                    cmd = ' '.join(['ncks -O -4 -L 9 ', extra_file_tmp, extra_file_tmp, '\n'])
                    f.write(cmd)
                    cmd = ' '.join(['nccopy ', extra_file_tmp, extra_file_wd, '\n'])
                    f.write(cmd)
                    cmd = ' '.join(['adjust_timeline.py -i start -p yearly -a 2008-1-1 -u seconds -d 2008-1-1', extra_file_wd, '\n'])
                    f.write(cmd)
                    cmd = ' '.join(['~/base/gris-analysis/scripts/nc_add_hillshade.py -z 1 ', extra_file_wd, '\n\n'])
                    f.write(cmd)
                    basin_dir = 'basins'
                    cmd = ' '.join(['cd', dirs['spatial'], '\n'])
                    f.write(cmd)
                    for basin in ('CW', 'NE', 'NO', 'NW', 'SE', 'SW'):
                        cmd = ' '.join(['~/base/gris-analysis/basins/extract_basins.py --basins ', basin, '--o_dir ../{}'.format(basin_dir),  extra_file, '\n'])
                        f.write(cmd)
                    f.write('cd ../../ \n')

scripts = uniquify_list(scripts)
scripts_combinded = uniquify_list(scripts_combinded)
scripts_post = uniquify_list(scripts_post)
print '\n'.join([script for script in scripts])
print('\nwritten\n')
print '\n'.join([script for script in scripts_combinded])
print('\nwritten\n')
print '\n'.join([script for script in scripts_post])
print('\nwritten\n')

