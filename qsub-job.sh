#!/bin/bash -l
#!/usr/bin/env python


# Specify the project name
#$-P dlearn

# Specify the time limit
#$-l h_rt=48:00:00 

# Job Name
#$-N appStore

# Send email at the end of the job
#$-m ae

# Join error and output streams
#$-j y

#gpu capability
#-l gpu_c=2.5

#Load modules:
module load anaconda/3.4

#Run the program
chmod +x deneme.py
python3 deneme.py $1