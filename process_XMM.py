import format_TraP_data
import plotting_tools
import generic_tools
import numpy as np
import sys
import os

# Obtain input parameters from the command line
if len(sys.argv) != 3:
    print 'python process_TraP.py <sigma1> <sigma2>'
    exit()
sigma1 = float(sys.argv[1])
sigma2 = float(sys.argv[2])

# get TraP data from the database and sort it into the required array which is then loaded
trans_data=generic_tools.extract_data('xmm_processed_trans_data.txt')
# make first array for the scatter_hist plot: [log10(eta_nu), log10(V_nu), nu]
data=[[trans_data[n][0],np.log10(float(trans_data[n][1])),np.log10(float(trans_data[n][2])),'xmm', 2] for n in range(len(trans_data)) if float(trans_data[n][1]) > 0 if float(trans_data[n][2]) > 0]
# Find the thresholds for a given sigma (in log space)
sigcutx,paramx,range_x = generic_tools.get_sigcut([a[1] for a in data],sigma1)
sigcuty,paramy,range_y = generic_tools.get_sigcut([a[2] for a in data],sigma2)
if sigma1 ==0:
    sigcutx=0
if sigma2==0:
    sigcuty=0

print 'Eta_nu threshold='+str(10.**sigcutx)+', V_nu threshold='+str(10.**sigcuty)

# Get the different frequencies in the dataset
frequencies = generic_tools.get_frequencies(data)

# Create the scatter_hist plot
IdTrans = plotting_tools.create_scatter_hist(data,sigcutx,sigcuty,paramx,paramy,range_x,range_y,'xmm',frequencies)

print 'Identified variables:'
print np.sort(list(set(IdTrans)))

# make second array for the diagnostic plot: [eta_nu, V_nu, maxflx_nu, flxrat_nu, nu, trans_type]
data2=[[trans_data[n][0],float(trans_data[n][1]),float(trans_data[n][2]),float(trans_data[n][3]),float(trans_data[n][4]), 'xmm', 2] for n in range(len(trans_data)) if float(trans_data[n][1]) > 0 if float(trans_data[n][2]) > 0] 

# Create the diagnostic plot
plotting_tools.create_diagnostic(data2,sigcutx,sigcuty,frequencies,'xmm')

