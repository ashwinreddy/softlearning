cp /code/mjkey.txt /root/.mujoco/mjkey.txt
ls /root/.mujoco
pip install -r /code/requirements.txt
export PYTHONPATH=/code/:$PYTHONAPTH
python /code/examples/development/main.py  \
	--algorithm SAC \
	--universe gym \
	--domain Sawyer \
	--task "${1}-v0" \
	--trial-gpus 1 \
	--gpus 1 \
	--exp-name $2 \
