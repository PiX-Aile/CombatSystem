
import subprocess
import _thread


# Source - https://stackoverflow.com/a/72101287
# Posted by ibarrond
# Retrieved 2026-03-16, License - CC BY-SA 4.0

def run_command(port):
    """Run a command while printing the live output"""
    process = subprocess.Popen(
        "ngrok tcp {port}",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    while True:   # Could be more pythonic with := in Python3.8+
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        print(line.decode(), end='')




_thread.start_new_thread(run_command, (8000,))
