#This makefile is desing to run worker.py on enggrid.bu.edu.
#To run this file, run 'make' command.
#This also calls appStore.sh file which sets up the environment on remote computer

queue ?= bme.q
example ?= worker.py
all: appStore
        qstat


appStore:
        qsub -q $(queue) $@.sh $(example)
clean:
        rm -rf rllab/
        rm -f appStore.{o,e,po,pe}
        rm -f core.*
