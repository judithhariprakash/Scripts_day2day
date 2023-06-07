import os
import glob

sample_list = "/lustre/data/t-tcga/Judith/LUNG_CANCER/samples.tsv"
cram_location = '/lustre/data/t-tcga/bcbio_analysis/bcbio_done'
cram_dir = '/lustre/data/t-tcga/Judith/LUNG_CANCER/'

def get_file(pattern):
    try:
        return glob.glob(pattern)[0]
    except IndexError:
        return False

def make_pattern(uid, suffix, ext='cram'):
    return f"{cram_location}/{uid}/final/*/*_{suffix}.{ext}"

def merge_crams(uid, sample_type):
    partial_cram_files = ""
    for i in ['ready', 'disc', 'sr']:
        fn = get_file(make_pattern(uid, f"{sample_type}-{i}"))
        if fn is False:
            fn2 = get_file(make_pattern(uid, f"{sample_type}-{i}", 'bam'))
            if fn2 is False:
                fn2 = get_file(make_pattern(uid, f"{sample_type}"))
                if fn2 is False:
                    print ("Skipping due to unknown reason", uid, sample_type)
                else:
                    print ("Skipping because already merged", uid, sample_type)
            else:
                 print ("Skipping because in BAM", uid, sample_type)
            return False
        else:
            partial_cram_files += f"{fn} "
    out_fn = cram_dir+ fn.rsplit('/', 1)[1].rsplit('-', 1)[0] + '.cram'
    cmd = f"samtools cat -o {out_fn} {partial_cram_files}"
    print (cmd)
    os.system(cmd)
    return out_fn


with open (sample_list) as handle:
    for sample in handle:
        sample = sample.rstrip('\n')
        print (sample)
       
        tumor_cram = merge_crams(sample, 'T*')
        break
