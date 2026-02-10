import subprocess

cmd = subprocess.run(["dir"], shell=True, capture_output=True)

print(cmd.stdout.decode())