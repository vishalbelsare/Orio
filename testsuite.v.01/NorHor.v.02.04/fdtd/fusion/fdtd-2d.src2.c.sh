#!/bin/bash
#PBS -l nodes=1
#PBS -l walltime=300:00:00
#PBS -j oe
#PBS -m abe
#PBS -N fdtd-2d.src2.c

cd $PBS_O_WORKDIR

orcc -v fdtd-2d.src2.c > fdtd-2d.src2.c.rs.data

