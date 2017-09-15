# In general it would make sense to use /mnt/nokrb/$USER, but in this case
# we'll use this example directory to keep things self-contained.
export HOME_ORIG="$HOME"
export HOME=./conda-home/

hostname
date

module load anaconda

if [ -d $HOME/.conda/envs/venv ]
then
        echo "Environment directory already exists; skipping install."
else
        echo "Installing to $HOME"
        conda env create --file environment.yml
fi

# Install complete!  Now we can load our custom environment for use.
source activate venv


# A few points about how the examples run:
#  * PYTHONPATH is given manually since we should be sure to working environment.
#	After all that run the code on virtual environmnet
PYTHONPATH="." python "worker.py"
