# On JETSON Nano

# export LD_PRELOAD='/home/user/.local/lib/python3.10/site-packages/torch.libs/libgomp-ee2ec4d2.so.1.0.0'
# export LD_PRELOAD=/home/user/.local/lib/python3.10/site-packages/torch/lib/../../torch.libs/libgomp-ee2ec4d2.so.1.0.0 

conda activate reach
sudo /home/user/miniconda3/envs/reach/bin/python ./src/main.py
