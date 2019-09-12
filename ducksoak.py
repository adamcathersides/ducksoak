#!/usr/bin/env python3

import click
import yaml
import docker
from time import sleep


def get_stream_definitions(config_file):

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


client = docker.from_env()

@click.command()
@click.argument('config', required=True)
@click.option('--interface', required=False, default='eth0', help='The capture interfizzle fo shizzle (either ip or name)')
@click.option('--tidyup', is_flag=True, is_eager=True, expose_value=False, callback=tidy_up)
def run(config, interface):
    """Run a bunch of tsduck tsp instances and log results"""

    cfg = get_stream_definitions(config)

    for stream in cfg['inputs']:
        print(f'Testing: {stream}')
        mc_ip = stream.split(':')[0]
        port = stream.split(':')[1]
        cmd = f'bash -c "tsp -I ip {mc_ip}:{port} -P continuity -O drop > /tmp/{mc_ip}.log"'
        print(cmd)
        client.containers.run(
                'tsduck:1',
                detach=True,
                command=cmd,
                network_mode='host',
                auto_remove=True,
                name=mc_ip.replace('.', '-'),
                tty=True)


if __name__ == '__main__':
    run()
