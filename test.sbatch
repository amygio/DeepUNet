#!/bin/bash
#SBATCH --job-name=TEST
#SBATCH --output=gpu.out 
#SBATCH --error=gpu.err    
#SBATCH --nodes=1        
#SBATCH --partition=xgpu
#SBATCH --ntasks=1       
#SBATCH --gres=gpu:tesla:4     

# Set stack size (to avoid warning message)
ulimit -s 10240
module load anaconda/3
module load cuda/11.0
source /home/al.giordano/.bashrc
eval "$(/home/al.giordano/miniconda3/bin/conda shell.bash hook)"
conda activate mypy3711
~/miniconda3/envs/mypy3711/bin/python eval.py --data_path dataset --load_from_checkpoint ./checkpoint/unet_examplemodel-0 --batch_size 11
