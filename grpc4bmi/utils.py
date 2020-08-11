import os
import shutil
from genericpath import exists
from os.path import abspath, expanduser


def stage_config_file(filename, input_dir, input_mount_point, home_mounted=False):
    """Stage config file inside container

    Args:
        filename (str): Path to config file
        input_dir (str): The input directory outside the container
        input_mount_point (str): The input directory inside the container
        home_mounted (bool): True if home directory is mounted inside container
    """
    fn = filename
    is_filename_inside_input_dir = input_dir and abspath(filename).startswith(abspath(input_dir))
    is_filename_inside_home_dir = home_mounted and abspath(filename).startswith(expanduser('~'))
    filename_exists = exists(filename)
    if is_filename_inside_input_dir:
        # Replace input dir outside container by input dir inside container
        fn = abspath(filename).replace(abspath(input_dir), input_mount_point)
    elif is_filename_inside_home_dir:
        # Singularity has home dir mounted, so valid filename should be available inside container
        # Make absolute because current working dir can be different inside image
        fn = abspath(filename)
    elif filename_exists:
        if input_dir is not None:
            # Copying filename inside input dir
            shutil.copy(filename, input_dir)
            fname = os.path.basename(filename)
            fn = os.path.join(input_mount_point, fname)
        else:
            raise Exception(f'Unable to copy {filename}, without a input_dir')
    else:
        # Assume filename exists inside container or model does not need a file to initialize
        pass
    return fn


# grpc max message size is 4Mb
GRPC_MAX_MESSAGE_LENGTH = 4 * 1024 * 1024
