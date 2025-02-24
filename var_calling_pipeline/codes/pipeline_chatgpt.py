import os
import subprocess
import argparse
import datetime #to save running time of the pipeline


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


# Register start time
start_time = datetime.datetime.now()
print(f"Inicio: {start_time}")

# Step 1: Perform BWA alignment
 subprocess.run(['bwa', 'mem', '-M', '/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_GRCh38.p14.noMT.names.fasta', fastq_file_read1, fastq_file_read2], stdout=open(output_sam, 'w'), check=True)

# Step 2: Convert SAM to BAM and sort
 subprocess.run(['samtools', 'view', '-Sb', output_sam, '-o', output_bam], check=True)
 subprocess.run(['samtools', 'sort', output_bam, '-o', output_sorted_bam], check=True)

# Step 3: Index the sorted BAM file
 subprocess.run(['samtools', 'index', output_sorted_bam], stdout=open(output_sorted_bam_index, 'w'), check=True)

# Step 4: Perform GATK variant calling
################## Here the variant calling with GATK starts #####################

# Step 1: AddOrReplaceReadGroups
 subprocess.run(["gatk", "AddOrReplaceReadGroups",
                "-I", output_sorted_bam,
                "-O", output_read_groups,
                "-RGPU", "M04871",
                "-RGLB", name_file,
                "-RGPL", "ILLUMINA",
                "-RGSM", name_file], check=True)

# Step 2: MarkDuplicates with Spark (optimized for parallel execution)
subprocess.run(["gatk", "MarkDuplicatesSpark",
                "-I", output_read_groups,
                "-O", output_marksDuplicate,
                "-M", output_metrics,
                "--conf", "spark.executor.cores=8"], check=True)

# Step 3: BaseRecalibrator (optimized for speed)
subprocess.run(["gatk", "BaseRecalibrator",
                "-I", output_marksDuplicate,
                "-O", output_table,
                "-R", "/path/to/reference.fasta",
               "-R", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_GRCh38.p14.noMT.names.fasta",
                "--known-sites" ,"/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_assembly38.dbsnp138_no_chr.vcf",
                "--known-sites", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_assembly38.known_indels_no_chr.vcf.gz",
                "--known-sites", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Mills_and_1000G_gold_standard.indels.hg38_no_chr.vcf.gz",
                "--num-threads", "8"], check=True)
        

# Step 4: ApplyBQSR
subprocess.run(["gatk", "ApplyBQSR",
                "-I", output_marksDuplicate,
                "-O", output_base_recalibrator,
                "-R", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_GRCh38.p14.noMT.names.fasta",
                "--bqsr-recal-file", output_table], check=True)

# Step 5: HaplotypeCaller (optimized for multithreading)
subprocess.run(["gatk", "HaplotypeCaller",
                "-I", output_base_recalibrator,
                "-O", output_vcf,
                "-R", "/mnt/Timina/cgonzaga/resources/GRCh38.14/prueba/Homo_sapiens_GRCh38.p14.noMT.names.fasta",
                "--native-pair-hmm-threads", "8"], check=True)

# Register end time
end_time = datetime.datetime.now()
print(f"Final: {end_time}")

# Calculate and print elapsed time
elapsed_time = end_time - start_time
print(f"Tiempo total de ejecución: {elapsed_time}")

# Save execution times to a log file
log_file = os.path.join(output_dir, "execution_time.log")
with open(log_file, "w") as log:
    log.write(f"Inicio: {start_time}\n")
    log.write(f"Final: {end_time}\n")
    log.write(f"Tiempo total de ejecución: {elapsed_time}\n")

