import os
import shutil
import subprocess

def install_dependencies():
    # Use the Go command-line tool to download and install the dependencies
    # This assumes you're in the directory with your Go module
    subprocess.run(['go', 'mod', 'download'], check=True)

def build_shared_object():
    # Use the Go command-line tool to build the shared object file
    # This assumes you're in the directory with your Go module
    subprocess.run(['go', 'build', '-o', 'libtls_client.so', '-buildmode=c-shared', 'tls_client.go'], check=True)

def move_shared_object():
    # Move the shared object file to the libraries directory
    shutil.move('libtls_client.so', '../glizzy_tls/libraries/')

def clean_installation():
    # Remove .h files
    os.remove('libtls_client.h')

def remove_compiled_file_if_exists():
    if os.path.exists('../glizzy_tls/libraries/libtls_client.so'):
        os.remove('../glizzy_tls/libraries/libtls_client.so')

if __name__ == "__main__":
    os.chdir('dependencies')  # Change to the directory with your Go module
    remove_compiled_file_if_exists()
    install_dependencies()
    build_shared_object()
    move_shared_object()
    clean_installation()