cp /code/mjkey.txt /root/.mujoco/mjkey.txt
ls /root/.mujoco
pip install -r /code/requirements.txt
export PYTHONPATH=/code/:$PYTHONAPTH
python /code/examples/development/main.py  --algorithm SAC --universe gym --domain HalfCheetah --task v3 --exp-name my-sac-experiment-1
