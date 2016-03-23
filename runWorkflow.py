from CTDopts.CTDopts import _InFile, CTDModel, args_from_file
import sys
import os
import subprocess
import shlex

wf_dir = sys.argv[1]
ctd_params = args_from_file(wf_dir + '/WORKFLOW-CTD')
ctd_files = args_from_file(wf_dir + '/IN-FILESTOSTAGE')

command = 'configureStrelkaWorkflow.pl'

data_path = os.path.join(wf_dir, 'data')
result_path = os.path.join(wf_dir, 'result')
db_path = os.path.join(wf_dir, 'ref')
log_path = os.path.join(wf_dir, 'logs')

path_to_config = '/lustre_cfc/software/qbic/strelka/1.0.14/etc/strelka_config_%s_default.ini'

tumorFile = os.path.join(data_path, ctd_files['Tumor'].split('/')[-1])
normalFile = os.path.join(data_path, ctd_files['Normal'].split('/')[-1])
reference = os.path.join(db_path, ctd_files['db'].split('/')[-1])

command += ' --tumor %s' % tumorFile
command += ' --normal %s' % normalFile
command += ' --ref %s' % reference
command += ' --config %s' % path_to_config % ctd_params['read_mapper']
command += ' --output-dir %s' % os.path.join(wf_dir, 'analysis')

commandSam = 'samtools index {f}'
commandSam2 = 'samtools faidx {f}'

logfilename = 'somaticvariantcalling_1_0_workflow.logs'
logfile = open(logfilename, 'w')

subprocess.call(shlex.split(commandSam.format(f=normalFile)), stdout=logfile, stderr=logfile)
subprocess.call(shlex.split(commandSam.format(f=tumorFile)), stdout=logfile, stderr=logfile)
subprocess.call(shlex.split(commandSam2.format(f=reference)), stdout=logfile, stderr=logfile)

output_folder = os.path.join(wf_dir, 'analysis')
subprocess.call(shlex.split(command), stderr=logfile, stdout=logfile)
#os.chdir(output_folder)
analysisCommand = 'make -j 16 -C {f}'
subprocess.call(shlex.split(analysisCommand.format(f=output_folder)), stdout=logfile, stderr=logfile)

#os.chdir(os.path.join(output_folder, 'results'))
vcfCommand = 'vcfoverlay {i} {s}'

with open(os.path.join(output_folder, 'results/somatic.variants.vcf'), 'w') as f:
    subprocess.call(shlex.split(vcfCommand.format(i=os.path.join(output_folder, 'results/all.somatic.snvs.vcf'), s=os.path.join(output_folder, 'results/all.somatic.indels.vcf'))), stdout=f,stderr=logfile)

subprocess.call(['cp', os.path.join(output_folder, 'results/somatic.variants.vcf'), result_path], stderr=logfile, stdout=logfile)

logfile.close()
subprocess.call(["mv", logfilename, log_path])
