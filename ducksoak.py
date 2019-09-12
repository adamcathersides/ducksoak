#!/usr/bin/env python3

import click
import yaml
import docker
import os
import pwd
import getpass
import sys
from time import sleep


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


def tidy_up(ctx, param, value):

    if not value or ctx.resilient_parsing:
        return
    for stream in cfg['inputs']:
        mc_ip = stream.split(':')[0]
        port = stream.split(':')[1]
        client.remove(name=mc_ip.replace('.', '-'))

    for stream in cfg['outputs']:
        mc_ip = stream.split(':')[0]
        port = stream.split(':')[1]
        client.remove(name=mc_ip.replace('.', '-'))
    ctx.exit()


@click.command()
@click.argument('config', required=True)
# @click.option('--tidyup', is_flag=True, is_eager=True, expose_value=False, callback=tidy_up)
def run(config):
    """Run a bunch of tsduck tsp instances and log results"""

    client = docker.from_env()
    cfg = parse_config(config)
    uid = int(pwd.getpwnam(getpass.getuser()).pw_uid)
    print(uid)

    try:
        os.mkdir(cfg['logs'])
    except FileExistsError:
        print('Log dir already exists')
    except OSError as e:
        print(f'Log dir creation error : {e}')

    for stream in cfg['inputs']:
        print(f'Testing: {stream}')
        mc_ip = stream.split(':')[0]
        port = stream.split(':')[1]
        # cmd = f'bash -c "tsp -I ip {mc_ip}:{port} -P continuity -O drop > {cfg["logs"]}/{mc_ip}.log"'
        cmd = f'bash -c "while true; do sleep 1; echo thing; done > {cfg["logs"]}/{mc_ip}.log"'
        print(cmd)
        client.containers.run(
                cfg['image'],
                detach=True,
                command=cmd,
                network_mode='host',
                auto_remove=True,
                name=mc_ip.replace('.', '-'),
                tty=True,
                volumes={cfg['logs']: {'bind': cfg['logs'], 'mode': 'rw'}},
                user=uid
                )


if __name__ == '__main__':
    run()
