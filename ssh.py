import subprocess


def ssh_into(vm_name: str, command: str):
    """Execute a command inside a Multipass instance."""
    result = subprocess.run(
        ["multipass", "exec", vm_name, "--", "bash", "-c", command],
        capture_output=True,
        text=True,
    )
    return result.stdout, result.stderr, result.returncode
