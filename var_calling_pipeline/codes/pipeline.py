import os
import subprocess
import argparse

# Initialize argument parser
parser = argparse.ArgumentParser(description="GATK variant calling")

# Add arguments
parser.add_argument("-n", "--name", type=str, help="Input name of the fasta file")
parser.add_argument("-f1", "--fasta1", type=str, help="Input file path to fasta file")
parser.add_argument("-f2", "--fasta2", type=str, help="Input file path to fasta file")

# Parse the arguments
args = parser.parse_args()

# Input files
name_file = args.name
fastq_file_read1 = args.fasta1
fastq_file_read2 = args.fasta2

# Define the output directory
output_dir = os.path.join(os.getcwd(), '{}_output'.format(name_file))

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define output files with the directory path
output_sam = os.path.join(output_dir, '{}.sam'.format(name_file))
output_bam = os.path.join(output_dir, '{}.bam'.format(name_file))
output_sorted_bam = os.path.join(output_dir, '{}.sorted.bam'.format(name_file))
output_sorted_bam_index = os.path.join(output_dir, '{}.sorted.bam.bai'.format(name_file))
output_read_groups = os.path.join(output_dir, '{}.read_groups.bam'.format(name_file))
output_marksDuplicate = os.path.join(output_dir, '{}.marks_duplicate.bam'.format(name_file))
output_metrics = os.path.join(output_dir, '{}.metrics.txt'.format(name_file))
output_table = os.path.join(output_dir, '{}.br.table'.format(name_file))
output_base_recalibrator = os.path.join(output_dir, '{}.base_recalibrator.bam'.format(name_file))
output_vcf = os.path.join(output_dir, '{}.output.vcf'.format(name_file))


# Step 1: Perform BWA alignment
subprocess.run (['bwa', 'mem', '-M', '/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_GRCh38.p14.noMT.names.fasta', fastq_file_read1, fastq_file_read2], stdout=open(output_sam, 'w'),check=True)

# Step 2: Convert SAM to BAM and sort
subprocess.run(['samtools', 'view', '-Sb', output_sam, '-o', output_bam], check=True)
subprocess.run(['samtools', 'sort', output_bam, '-o', output_sorted_bam], check=True)

# Step 3: Index the sorted BAM file
subprocess.run(['samtools', 'index', output_sorted_bam],stdout=open(output_sorted_bam_index, 'w'), check=True)

# Step 4: Perform GATK variant calling
##################Here the variant calling with GATK starts#####################
# Step 1: AddOrReplaceReadGroups
subprocess.run(["gatk", "AddOrReplaceReadGroups",
                    "-I", output_sorted_bam,
                    "-O",output_read_groups ,
                    "-RGPU", "M04871",
                    "-RGLB", '{}'.format(name_file),
                    "-RGPL", "ILLUMINA",
                    "-RGSM", '{}'.format(name_file)], check=True)
 #Step 2: MarksDuplicate   

subprocess.run(["gatk", "MarkDuplicatesSpark",
                    "-I", output_read_groups,
                    "-O", output_marksDuplicate,
                    "-M", output_metrics], check=True)
    
# Step 3: BaseRecalibrator  

subprocess.run(["gatk","BaseRecalibrator",
                    "-I", output_marksDuplicate,
                    "-O", output_table,
                    "-R", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_GRCh38.p14.noMT.names.fasta",
                    "--known-sites" ,"/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_assembly38.dbsnp138_no_chr.vcf",
                    "--known-sites", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_assembly38.known_indels_no_chr.vcf.gz",
                    "--known-sites", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Mills_and_1000G_gold_standard.indels.hg38_no_chr.vcf.gz" ])
# Step 4: ApplyBQSR

subprocess.run(["gatk", "ApplyBQSR",
                    "-I", output_marksDuplicate,
                    "-O", output_base_recalibrator,
                    "-R", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_GRCh38.p14.noMT.names.fasta",
                    "--bqsr-recal-file", output_table])

#Step 5: Haplotype caller
subprocess.run(["gatk", "HaplotypeCaller",
                    "-I", output_base_recalibrator,
                    "-O", output_vcf,
                    "-R", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_GRCh38.p14.noMT.names.fasta"])

