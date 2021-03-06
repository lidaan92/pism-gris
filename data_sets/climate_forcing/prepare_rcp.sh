#!/bin/bash

var=tas
box="-73,-12,59,84"
data_dir=nasa-giss
for rcp in 26 45 85; do
    for ens in r1i1p1 r1i1p2 r1i1p3; do
        cdo -O mergetime ${data_dir}/${var}_Amon_GISS-E2-H_rcp${rcp}_${ens}_*01-*12.nc  ${var}_Amon_GISS-E2-H_rcp${rcp}_ens_${ens}_2006-2300.nc
        cdo -O fldmean -sellonlatbox,$box ${var}_Amon_GISS-E2-H_rcp${rcp}_ens_${ens}_2006-2300.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ens_${ens}_GRIS_2006-2300.nc
    done
    cdo -O ensmean ${var}_Amon_GISS-E2-H_rcp${rcp}_ens_*_GRIS_2006-2300.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_GRIS_2006-2300.nc
    cdo -O sub -timmean -selyear,2091/2100 ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_GRIS_2006-2300.nc -timmean -selyear,2006,2015 ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_GRIS_2006-2300.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_GRIS_2006-2015_2091-2100_rel_warming.nc
    cdo -O yearmean ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_GRIS_2006-2300.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_GRIS_2006-2300.nc
    cdo -O sub ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_GRIS_2006-2300.nc -timmean -selyear,2006/2015  ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_GRIS_2006-2300.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2006-2300.nc
    cdo selyear,2008/2300 ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2006-2300.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-2300.nc
    cdo -O trend -selyear,2201/2300 ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-2300.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-2300_a.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-2300_b.nc
    ncks -O ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-2300.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-7008.nc
    python extend_cmip5.py ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-7008.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-2300_a.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-2300_b.nc
    ncrename -O -v tas,delta_T  ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-7008.nc  ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-7008.nc
    ncwa -a lat,lon -O ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-7008.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-7008.nc
    cdo settaxis,01-01-01,12:00:00,1year ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_2008-7008.nc ${var}_Amon_GISS-E2-H_rcp${rcp}_ensmean_ym_anom_GRIS_0-5000.nc
done
