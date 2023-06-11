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

def move_shared_object(glizzy_tls_dir):
    if not os.path.exists(f'{glizzy_tls_dir}/libraries/'):
        os.mkdir(f'{glizzy_tls_dir}/libraries/')
    # Move the shared object file to the libraries directory
    shutil.move('libtls_client.so', f'{glizzy_tls_dir}/libraries/libtls_client.so')

def clean_installation():
    # Remove .h files
    os.remove('libtls_client.h')

def check_if_go_is_installed():
    try:
        subprocess.run(['go', 'version'], check=True)
    except:
        raise Exception("Go is not installed. Please install Go and try again.")

def build():
    original_dir = os.getcwd()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(f'{current_dir}')
    glizzy_tls_dir = current_dir.replace('/dependencies', '')

    if os.path.exists(f'{glizzy_tls_dir}/libraries/libtls_client.so'):
        os.chdir(original_dir)
        return
    print("Building the shared object file...")
    install_dependencies()
    build_shared_object()
    move_shared_object(glizzy_tls_dir)
    print("Successfully built the shared object file!")
    clean_installation()
    os.chdir(original_dir)