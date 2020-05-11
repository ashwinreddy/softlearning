cp /code/mjkey.txt /root/.mujoco/mjkey.txt
ls /root/.mujoco
pip install -r /code/requirements.txt
git clone --recursive https://github.com/ashwinreddy/mj_envs.git /code/mj_envs
cd /code/mj_envs
git submodule update --remote
cd ~
export PYTHONPATH=/code/:/code/mj_envs/:$PYTHONPATH
python /code/examples/development/main.py  \
	--algorithm SAC \
	--universe gym \
	--domain $1 \
	--task "${2}-v0" \
	--trial-gpus 1 \
	--gpus 1 \
	--exp-name $3 \
