#!/bin/bash
module load qbic/anaconda2/2.1.0
module load qbic/strelka/1.0.14
module load qbic/vcflib/0.1
module load qbic/samtools/1.3

workflowDir=$(cat wfdir)
#parse using CTDopts and run workflow
python runWorkflow.py $workflowDir
cp wfdir wfdir2
