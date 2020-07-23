"""Retrieve Orbita Zero hardware and write it to the specified config file.

This tool must be run while Orbita is fixed at the Zero Position using a specific 3D part.

"""

import os
import pathlib
import argparse
import numpy as np

from glob import glob

from pyluos import Device
from reachy.io.luos import OrbitaDisk


import reachy


def main():
    """Get the Zero hardware from Orbita."""
    bp = pathlib.Path(reachy.__file__).parent
    filename = 'orbita_head_hardware_zero.npy'
    output_filename = os.path.join(bp, filename)

    parser = argparse.ArgumentParser()
    parser.add_argument('--luos_port', default='/dev/ttyUSB*', help='Orbita gate luos port (default: %(default)s)')
    parser.add_argument('--output_filename', default=output_filename, help='output file where to store the zero (default: %(default)s)')
    args = parser.parse_args()

    ports = glob(args.luos_port)
    if len(ports) == 0:
        ports = [args.luos_port]

    device = Device(ports[0])
    disks = [OrbitaDisk(d.alias, d) for d in [device.disk_top, device.disk_middle, device.disk_bottom]]
    hardware_zero = [d._wait_for_update() for d in disks]

    print(f'Find Orbita Hardware Zero at {hardware_zero}')
    np.save(args.output_filename, hardware_zero)


if __name__ == '__main__':
    main()