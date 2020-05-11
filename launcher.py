import sys
import os
import os.path as osp
from doodad import mount, mode
from doodad.launch import launch_api

def command(args):
    return """source /code/install.sh""" + " ".join(args)

def run(args, run_mode='local', storage_mode='local', dry_run=False):
    
    
    local_mount = mount.MountLocal(
        local_dir="/home/ashwin/Research/playground/softlearning",
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
             #s3_log_path='test_doodad/softlearning_test',
             s3_log_path='softlearning_exps/',
             instance_type='c4.large',
             spot_price=0.03,
             region='us-west-1',
             ami_name='ami-874378e7',
        )


    results_mount_point = '/root/ray_results'

    if storage_mode == 'local':
        output_mount = mount.MountLocal(
                local_dir="/home/ashwin/Research/results/",
                mount_point=results_mount_point,
                output=True
            )
    elif storage_mode == 's3':
        output_mount = mount.MountS3(
             s3_path='softlearning_output',
             mount_point=results_mount_point,
             output=True
         )


    mounts = [local_mount, local_mount2, output_mount]


    kwargs = {
            #'command': "cat /code/secret.txt > /root/ray_results/secret.txt",
            'command': command(args),
            'cli_args': "",
            'mode': launcher,
            'mounts': mounts,
            'verbose': True,
            'docker_image': 'abhiguptaberk/softlearningashwin:latest'
    }

    print(kwargs)

    if not dry_run:
        launch_api.run_command(**kwargs)

if __name__ == '__main__':
    assert len(sys.argv) == 4, "Expects domain, environment and experiment name"
    run(run_mode='ec2',
        storage_mode='s3',
        args=sys.argv[1:],
        dry_run=False)
    #run('ec2', 's3')
