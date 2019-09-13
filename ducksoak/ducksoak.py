#!/usr/bin/env python3

import click
import yaml
import docker
import os
import pwd
import getpass
import sys


def parse_config(config_file):

    """
    Get the stream info from config file
    """

    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as e:
            print(f'Erk that yaml is ugly: {e}')

def start_analysis_containers(client, stream_list, image, logs, uid):

    """
    Start an analysis container per stream
    """

    for stream in stream_list:
        print(f'Testing: {stream}')
        mc_ip = stream.split(':')[0]
        port = stream.split(':')[1]
        cmd = f'bash -c "tsp -I ip {mc_ip}:{port} -P continuity -O drop > {logs}/{mc_ip}.log"'
        # cmd = f'bash -c "while true; do sleep 1; echo thing; done > {logs}/{mc_ip}.log"'
        client.containers.run(
                image,
                detach=True,
                command=cmd,
                network_mode='host',
                auto_remove=True,
                name=mc_ip,
                tty=True,
                volumes={logs: {'bind': logs, 'mode': 'rw'}},
                user=uid
                )


def tidy_up(client, cfg):

    for c in client.containers.list():
        if c.name in cfg['inputs'] or cfg['outputs']:
            print(f'Killing : {c.name}')
            c.kill()


@click.command()
@click.argument('config', required=True)
@click.option('--tidyup', is_flag=True)
def run(config, tidyup):
    """Run a bunch of tsduck tsp instances and log results"""

    client = docker.from_env()
    cfg = parse_config(config)
    uid = int(pwd.getpwnam(getpass.getuser()).pw_uid)

    try:
        os.mkdir(cfg['logs'])
    except FileExistsError:
        pass
    except OSError as e:
        print(f'Log dir creation error : {e}')
        sys.exit(1)

    if tidyup:
        tidy_up(client, cfg)
    else:
        start_analysis_containers(client, cfg['inputs'], cfg['image'], cfg['logs'], uid)
        start_analysis_containers(client, cfg['outputs'], cfg['image'], cfg['logs'], uid)

if __name__ == '__main__':
    run()
