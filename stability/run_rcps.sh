#!/bin/bash


./warming_restart.py --o_dir 2017_07_rcps --exstep 1 --params rcp,lapse,precip_scaling -n 72 -w 8:00:00 -g 3600 -s chinook -q t2standard --step 1000 ../calibration/2017_06_vc/state/gris_g3600m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc 
_calving_vonmises_calving_0_100.nc

./warming_restart.py --o_dir 2017_07_rcps --exstep 1 --params rcp,lapse,precip_scaling,ocean_f -n 72 -w 8:00:00 -g 3600 -s chinook -q t2standard --step 1000 ../calibration/2017_06_vc/state/gris_g3600m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc 
_calving_vonmises_calving_0_100.nc



for lapse in 6; do
    for ps in 0.05; do
        end_year=2100
        /Volumes/79n/data/gris-analysis/plotting/plotting.py -o lapse_${lapse}_ps_${ps}_2009_${end_year} --title lapse_${lapse}_ps_${ps} --time_bounds 2009 ${end_year} --bounds 0 0.15 --plot rcp_mass 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_${lapse}_ps_${ps}_rcp_*_bd_off_calving_vonmises_calving_0_1000.nc
        /Volumes/79n/data/gris-analysis/plotting/plotting.py -o lapse_${lapse}_ps_${ps}_2009_${end_year} --title lapse_${lapse}_ps_${ps} --time_bounds 2009 ${end_year} --bounds 0 0.15 --plot rcp_d 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_${lapse}_ps_${ps}_rcp_*_bd_off_calving_vonmises_calving_0_1000.nc
        end_year=2200
        /Volumes/79n/data/gris-analysis/plotting/plotting.py -o lapse_${lapse}_ps_${ps}_2009_${end_year} --title lapse_${lapse}_ps_${ps} --time_bounds 2009 ${end_year} --bounds 0 0.75 --plot rcp_mass 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_${lapse}_ps_${ps}_rcp_*_bd_off_calving_vonmises_calving_0_1000.nc
        /Volumes/79n/data/gris-analysis/plotting/plotting.py -o lapse_${lapse}_ps_${ps}_2009_${end_year} --title lapse_${lapse}_ps_${ps} --time_bounds 2009 ${end_year} --bounds 0 0.75 --plot rcp_d 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_${lapse}_ps_${ps}_rcp_*_bd_off_calving_vonmises_calving_0_1000.nc
        end_year=3000
        /Volumes/79n/data/gris-analysis/plotting/plotting.py -o lapse_${lapse}_ps_${ps}_2009_${end_year} --title lapse_${lapse}_ps_${ps} --time_bounds 2009 ${end_year} --bounds 0 5 --plot rcp_mass 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_${lapse}_ps_${ps}_rcp_*_bd_off_calving_vonmises_calving_0_1000.nc
        /Volumes/79n/data/gris-analysis/plotting/plotting.py -o lapse_${lapse}_ps_${ps}_2009_${end_year} --title lapse_${lapse}_ps_${ps} --time_bounds 2009 ${end_year} --bounds 0 5 --plot rcp_d 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_${lapse}_ps_${ps}_rcp_*_bd_off_calving_vonmises_calving_0_1000.nc
    done
done

# FIX OF_ON/OF_OFF
ps=0.05
end_year=2100
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o ps_${ps}_2009_${end_year} --title "\$\psi_w\$=${ps}" --time_bounds 2009 ${end_year} --bounds 0 0.25 --plot rcp_lapse_mass 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_of_on_0_1000.nc 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_0_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_0_1000.nc
end_year=2200
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o ps_${ps}_2009_${end_year}  --title "\$\psi_w\$=${ps}" --time_bounds 2009 ${end_year} --bounds 0 1 --plot rcp_lapse_mass 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_of_on_0_1000.nc 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_0_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_0_1000.nc
end_year=3000
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o ps_${ps}_2009_${end_year}  --title "\$\psi_w\$=${ps}" --time_bounds 2009 ${end_year} --bounds -0.1 7 --plot rcp_lapse_mass 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_of_on_0_1000.nc 2017_07_rcps/scalar/cumsum_ts_gris_g3600m_warming_v3a_no_bath_lapse_0_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_0_1000.nc


cdo divc,1e12 -timmean -selyear,71/90 -selvar,surface_ice_flux ts_gris_g3600m_warming_v3a_no_bath_lapse_0_ps_0.05_rcp_45_bd_off_calving_vonmises_calving_0_1000.nc  ts_gris_g3600m_warming_v3a_no_bath_lapse_0_ps_0.05_rcp_45_bd_off_calving_vonmises_calving_2080-2100_mean.nc
cdo divc,1e12 -timmean -selyear,71/90 -selvar,surface_ice_flux ts_gris_g3600m_warming_v3a_no_bath_lapse_0_ps_0.05_rcp_85_bd_off_calving_vonmises_calving_0_1000.nc  ts_gris_g3600m_warming_v3a_no_bath_lapse_0_ps_0.05_rcp_85_bd_off_calving_vonmises_calving_2080-2100_mean.nc

for basin in CW NE NO NW SE SW; do
    for rcp in ctrl 26 45 85; do
        /Volumes/79n/data/gris-analysis/basins/extract_basins.py --o_dir ../basins --basins $basin ex_gris_g3600m_v3a_no_bath_lapse_6_ps_0_rcp_${rcp}_bd_off_calving_vonmises_calving_0_1000.nc       
    done
done

for basin in CW NE NO NW SE SW; do
    for file in ex_g*.nc; do
        /Volumes/79n/data/gris-analysis/basins/extract_basins.py --o_dir ../basins --basins $basin $file
    done
done

end_year=3000
lapse=6
ps=0.05
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o 2009_${end_year}  --time_bounds 2009 ${end_year} --plot rcp_area_cold 2017_07_rcps_ps/scalar/rel_ts_gris_g2400m_warming_v3a_no_bath_lapse_${lapse}_ps_${ps}_rcp_*_bd_off_calving_vonmises_calving_of_on_0_1000.nc
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o 2009_${end_year}  --time_bounds 2009 ${end_year} --plot rcp_volume_cold 2017_07_rcps_ps/scalar/rel_ts_gris_g2400m_warming_v3a_no_bath_lapse_${lapse}_ps_${ps}_rcp_*_bd_off_calving_vonmises_calving_of_on_0_1000.nc


for basin in CW NE NO NW SE SW; do
    for rcp in 26 45 85; do
        extract_interface.py --step 20 -t ice_ocean -o 2017_07_rcps_ps/ice_ocean/ice_ocean_g2400m_lapse_6_rcp_${rcp}_${basin}.shp 2017_07_rcps_ps/basins/b_${basin}_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_${rcp}_bd_off_calving_vonmises_calving_of_on_0_1000/b_${basin}_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_${rcp}_bd_off_calving_vonmises_calving_of_on_0_1000.nc
        dissolve_by_attribute.py -o  2017_07_rcps_ps/ice_ocean/ice_ocean_g2400m_lapse_6_rcp_${rcp}_${basin}_ds.shp  2017_07_rcps_ps/ice_ocean/ice_ocean_g2400m_lapse_6_rcp_${rcp}_${basin}.shp
    done
done


# Extract basins
for basin in CW NE NO NW SE SW; do
    for rcp in 26 45 85; do
        for lapse in 6; do
            /Volumes/79n/data/gris-analysis/basins/extract_basins.py --o_dir ../basins --basins $basin  ex_gris_g2400m_warming_v3a_no_bath_lapse_${lapse}_ps_0.05_rcp_${rcp}_bd_off_calving_vonmises_calving_of_on_0_1000.nc
        done
    done
done

~/base/pypismtools/scripts/extract_interface.py -o 2017_07_rcps_ps/ice_ocean/ice_ocean_g2400m_lapse_6_rcp_26_GRIS.shp  -t ice_ocean 2017_07_rcps_ps/spatial/ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_26_bd_off_calving_vonmises_calving_of_on_0_1000.nc
dissolve_by_attribute.py -o 2017_07_rcps_ps/ice_ocean_g2400m_lapse_6_rcp_26_GRIS_ds.shp 2017_07_rcps_ps/ice_ocean_g2400m_lapse_6_rcp_26_GRIS.shp
~/base/pypismtools/scripts/extract_interface.py -o 2017_07_rcps_ps/ice_ocean/ice_ocean_g2400m_lapse_6_rcp_45_GRIS.shp  -t ice_ocean 2017_07_rcps_ps/spatial/ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_45_bd_off_calving_vonmises_calving_of_on_0_1000.nc 
dissolve_by_attribute.py -o 2017_07_rcps_ps/ice_ocean_g2400m_lapse_6_rcp_45_GRIS_ds.shp 2017_07_rcps_ps/ice_ocean_g2400m_lapse_6_rcp_45_GRIS.shp
~/base/pypismtools/scripts/extract_interface.py -o 2017_07_rcps_ps/ice_ocean/ice_ocean_g2400m_lapse_6_rcp_85_GRIS.shp  -t ice_ocean 2017_07_rcps_ps/spatial/ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_85_bd_off_calving_vonmises_calving_of_on_0_1000.nc 
dissolve_by_attribute.py -o 2017_07_rcps_ps/ice_ocean/ice_ocean_g2400m_lapse_6_rcp_85_GRIS_ds.shp 2017_07_rcps_ps/ice_ocean_g2400m_lapse_6_rcp_85_GRIS.shp

# Plot RCP mass
end_year=2100
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o 2009_${end_year} --time_bounds 2009 ${end_year}  --plot rcp_ens_mass 2017_07_ocean/scalar/cumsum_ts_gris_g2400m_v3a_rcp*.nc
end_year=2200
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o 2009_${end_year} --time_bounds 2009 ${end_year}  --plot rcp_ens_mass 2017_07_ocean/scalar/cumsum_ts_gris_g2400m_v3a_rcp*.nc
end_year=3000
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o 2009_${end_year} --time_bounds 2009 ${end_year}  --plot rcp_ens_mass 2017_07_ocean/scalar/cumsum_ts_gris_g2400m_v3a_rcp*.nc
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o 2009_${end_year} --time_bounds 2009 ${end_year}  --plot rcp_ens_area 2017_07_ocean/scalar/rel_ts_gris_g2400m_v3a_rcp*.nc
/Volumes/79n/data/gris-analysis/plotting/plotting.py -o 2009_${end_year} --time_bounds 2009 ${end_year}  --plot rcp_ens_volume 2017_07_ocean/scalar/rel_ts_gris_g2400m_v3a_rcp*.nc

end_year=3000
ps=0.05
for rcp in 26 45 85; do
    /Volumes/79n/data/gris-analysis/plotting/plotting.py -o rcp_${rcp}_ps_${ps}_2009_${end_year} --title "RCP${rcp}" --time_bounds 2009 ${end_year}  --plot basin_discharge 2017_07_rcps_ps/basins/b_*_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_${rcp}_bd_off_calving_vonmises_calving_of_on_0_1000/scalar_fldsum_b_*_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_${rcp}_bd_off_calving_vonmises_calving_of_on_0_1000.nc
    /Volumes/79n/data/gris-analysis/plotting/plotting.py -o rcp_${rcp}_ps_${ps}_2009_${end_year} --title "RCP${rcp}" --time_bounds 2009 ${end_year}  --plot basin_mass_d 2017_07_rcps_ps/basins/b_*_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_${rcp}_bd_off_calving_vonmises_calving_of_on_0_1000/cumsum_b_*_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_${rcp}_bd_off_calving_vonmises_calving_of_on_0_1000.nc
done
  

for basin in CW NE NO NW SE SW; do
    /Volumes/79n/data/gris-analysis/plotting/plotting.py -o lapse_6 --basin ${basin} --bounds 0 250 --runmean 10 --plot rcp_flux_rel 2017_07_rcps_ps/basins/b_${basin}_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_of_on_0_1000/scalar_fldsum_b_${basin}_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_of_on_0_1000.nc
    # /Volumes/79n/data/gris-analysis/plotting/plotting.py -o lapse_6 --basin ${basin} --runmean 10 --plot rcp_flux 2017_07_rcps_ps/basins/b_${basin}_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_of_on_0_1000/scalar_fldsum_b_${basin}_ex_gris_g2400m_warming_v3a_no_bath_lapse_6_ps_0.05_rcp_*_bd_off_calving_vonmises_calving_of_on_0_1000.nc
done


# Basal enthalpy
odir=2017_07_ocean
grid=2400
mkdir -p $odir/enth_base
python /Volumes/79n/data/gris-analysis/enth_base/extract_basal_enthalpy.py ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc ${odir}/enth_base/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_of_on_0_100.nc
cd ${odir}/state
for file in gris_g${grid}*.nc; do
    python /Volumes/79n/data/gris-analysis/enth_base/extract_basal_enthalpy.py $file ../enth_base/$file
done
cd ../enth_base
for rcp in 26 45 85; do
    cdo -O ensmean gris_g${grid}m_v3a_rcp_${rcp}_*.nc ensmean_gris_g${grid}m_v3a_rcp_${rcp}.nc
    cdo mulc,100 -div -sub   ensmean_gris_g${grid}m_v3a_rcp_${rcp}.nc gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_of_on_0_100.nc gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_of_on_0_100.nc rel_diff_ensmean_gris_g${grid}m_v3a_rcp_${rcp}.nc
    gdal_translate -a_srs EPSG:3413 NETCDF:rel_diff_ensmean_gris_g${grid}m_v3a_rcp_${rcp}.nc:basal_enthalpy  rel_diff_ensmean_gris_g${grid}m_v3a_rcp_${rcp}.tif
done
cd ../../



for file in ts_*;do
    cdo mulc,100 -div -sub -seltimestep,-1 $file -seltimestep,1 $file -seltimestep,1 $file rel_diff_$file
done
for rcp in 26 45 85; do
    cdo -O ensmean rel_diff_ts_gris_g2400m_v3a_rcp_${rcp}_*.nc ensmean_rel_diff_ts_gris_g2400m_v3a_rcp_${rcp}.nc
    cdo -O ensmin rel_diff_ts_gris_g2400m_v3a_rcp_${rcp}_*.nc ensmin_rel_diff_ts_gris_g2400m_v3a_rcp_${rcp}.nc
    cdo -O ensmax rel_diff_ts_gris_g2400m_v3a_rcp_${rcp}_*.nc ensmax_rel_diff_ts_gris_g2400m_v3a_rcp_${rcp}.nc
done
