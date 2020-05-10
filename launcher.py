import os
import os.path as osp
from doodad import mount, mode
from doodad.launch import launch_api

def command():
    return """sh /code/install.sh""" #&& run_example_local examples.development \
    #--algorithm SAC \
    #--universe gym \
    #--domain HalfCheetah \
    #--task v3 \
    #--exp-name my-sac-experiment-1 \
    #--checkpoint-frequency 1000  # Save the checkpoint to resume training later\
    #--log-dir /output"""

def run(run_mode='local', output_mode='local'):

    local_mount = mount.MountLocal(
        local_dir="/home/ashwin/Research/uber-robotics/softlearning",
        mount_point='/code',
        output=False
    )

    local_mount2 = mount.MountLocal(
        local_dir="/home/ashwin/.mujoco",
        mount_point='/root/.mujoco',
        output=False
    )



    # you can either run code on your machine or in the cloud

    if run_mode == 'local':
        launcher = mode.LocalMode()
    elif run_mode == 'ec2':
        launcher = mode.EC2Autoconfig(
             s3_bucket="doodad-ashwin-redone2",
             s3_log_path='test_doodad/softlearning_test',
             instance_type='c4.large',
             spot_price=0.03,
             region='us-west-1',
             ami_name='ami-874378e7',
        )


    results_mount_point = '/root/ray_results'

    if output_mode == 'local':
        output_mount = mount.MountLocal(
                local_dir="/home/ashwin/Research/results/",
                mount_point=results_mount_point,
                output=True
            )
    elif output_mode == 's3':
        output_mount = mount.MountS3(
             s3_path='softlearning_output',
             mount_point=results_mount_point,
             output=True
         )


    mounts = [local_mount, local_mount2, output_mount]

    print(mounts)
    if True:
        launch_api.run_command(
            #command     = "cat /code/secret.txt > /root/ray_results/secret.txt",
            command     = "source /code/install.sh",
            cli_args    = "",
            mode        = launcher,
            mounts      = mounts,
            verbose     = True,
            docker_image = "abhiguptaberk/softlearningashwin:latest"
        )

if __name__ == '__main__':
    run('ec2', 's3')
