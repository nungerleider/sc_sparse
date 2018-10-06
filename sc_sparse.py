import numpy as np
import pandas as pd
import sys
import os

'''

   Takes a single cell sequencing matrix as input
   Columns should be cell barcodes and rows should be gene names
   Returns three files - an ordered list of barcodes, genes, and a marketmatrix file

'''

script = sys.argv.pop(0)

if len(sys.argv) != 1 or sys.argv[0] in ['-h','--help']:
    sys.exit('\tUsage:\n\t {script} /path/to/input/tsv')
 
path = sys.argv[0]

if not os.path.exists(path):
    sys.exit("{path} was not found. Make sure the path is accurate.")

print ("\n\tInputting data...\n")

# Use the right delimiter.
df = pd.read_table(path, index_col=0)
if df.shape[1] <= 1:
    df = pd.read_csv(path, index_col=0)
    if df.shape[1] <= 1:
        sys.exit("\tInput file should have more than one column and be tab or comma delimited.")

print("\tSaving barcodes to file...\n")
with open("{path}_barcodes".format(path=path),"w") as bar_out:                                         
    for barcode in df.columns:                                                 
        bar_out.write("%s\n" % barcode)   

print("\tSaving genes to file...\n")
with open("{path}_genes".format(path=path),"w") as gene_out:                                            
    for gene in df.index:                                                   
        gene_out.write("%s\n" % gene)  

gt_zero = pd.DataFrame(np.where(df > 0)[0]) 
gt_zero[1] = np.where(df > 0)[1] 
df_mat = np.matrix(df) 
gt_zero_mat = np.matrix(gt_zero)

final_matrix = np.zeros(len(gt_zero.index)) 

print("\tConverting to sparse matrix...\n")
for ind, value in enumerate(gt_zero_mat):
    final_matrix[ind] = df_mat[value[0,0], value[0,1]]

gt_zero[2] = final_matrix  

# 1-based index
gt_zero += 1

print("\tSaving marketmatrix file...\n")
gt_zero.to_csv('{path}_marketmatrix'.format(path=path), index=None, header=None, sep='\t')

directory = os.path.dirname(path)
print("\tDone! Files saved in {path}.\n".format(path=directory))
