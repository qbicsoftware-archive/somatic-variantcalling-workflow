#!/bin/bash
module load qbic/anaconda2
module load qbic/strelka/1.0.14

workflowDir=$(cat wfdir)
#parse using CTDopts and run workflow
python runWorkflow.py $workflowDir
cp wfdir wfdir2
