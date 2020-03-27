import subprocess


def exec_timeout(exec_args, timeout=600):
    stdout, _ = subprocess.Popen(
        exec_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    ).communicate(timeout=timeout)

    return stdout
