from CTDopts.CTDopts import _InFile, CTDModel, args_from_file
import sys
import os
import subprocess

wf_dir = sys.argv[1]
ctd_params = args_from_file(wf_dir + '/WORKFLOW-CTD')
ctd_files = args_from_file(wf_dir + '/IN-FILESTOSTAGE')

command = 'configureStrelkaWorkflow.pl'

data_path = os.path.join(wfdir, 'data')
result_path = os.path.join(wfdir, 'result')
db_path = os.path.join(wfdir, 'ref')
log_path = os.path.join(wfdir 'log')

path_to_config = '/lustre_cfc/software/qbic/strelka/1.0.14/etc/strelka_config_%s_default.ini'

command += ' --tumor %s' % os.path.join(data_path, ctd_files['tumor'].split('/')[-1])
command += ' --normal %s' % os.path.join((data_path, ctd_files['normal'].split('/')[-1])
command += ' --ref %s' % os.path.join((db_path, ctd_files['db'][0].split('/')[-1])
command += ' --config %s' % path_to_config % ctd_params['read_mapper']
command += ' --output-dir %s' % os.path.join(wf_dir, 'analysis')

output_folder = os.path.join(wf_dir, 'analysis')
subprocess.call(command.split())
os.chdir(output_folder)

with open(os.path.join(log_path,'log.txt'),"wb") as out:
        subprocess.call(['make', '-j', '16'], stdout=out)


os.chdir(os.path.join(output_folder, 'results'))
subprocess.call(['/lustre_cfc/software/qbic/vcflib/bin/vcfoverlay', 'all.somatic.indels.vcf',  'all.somatic.snvs.vcf', '>', 'somatic.variants.vcf'])

subprocess.call(['cp', 'somatic.variants.vcf', result_path])
