import subprocess


def exec_timeout(exec_args, timeout=600, **popen_kwargs):
    child = subprocess.Popen(
        exec_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        **popen_kwargs
    )

    return *child.communicate(timeout=timeout), child.returncode
