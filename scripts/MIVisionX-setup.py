__author__      = "Kiriti Nagesh Gowda"
__copyright__   = "Copyright 2018, AMD Radeon MIVisionX setup"
__license__     = "MIT"
__version__     = "0.9.9"
__maintainer__  = "Kiriti Nagesh Gowda"
__email__       = "Kiriti.NageshGowda@amd.com"
__status__      = "beta"

import os
import getopt
import sys
import subprocess
 

opts, args = getopt.getopt(sys.argv[1:], 's:d:l:m:')
 
sudoPassword = ''
setupDir = ''
MIOpenVersion = ''
linuxSystemInstall = ''

for opt, arg in opts:
    if opt == '-s':
        sudoPassword = arg
    elif opt =='-d':
    	setupDir = arg
    elif opt =='-m':
    	MIOpenVersion = arg
    elif opt == '-l'
    	linuxSystemInstall = arg

if sudoPassword == '':
    print('Invalid command line arguments.\n \t\t\t\t-s [sudo password - required]\n '\
                                            '\t\t\t\t-d [setup directory - optional]\n '\
                                            '\t\t\t\t-l [Linux system install - optional (default:apt-get options:apt-get/yum)]\n '\
                                            '\t\t\t\t-m [MIOpen Version - optional (default:1.6.0)]\n')
    exit()

if setupDir == '':
	setupDir_deps = '~/deps'
else:
	setupDir_deps = setupDir+'/deps'

if MIOpenVersion == '':
	MIOpenVersion = '1.6.0'

if linuxSystemInstall == '':
	linuxSystemInstall = 'apt-get'

from subprocess import call
deps_dir = os.path.expanduser(setupDir_deps)

# MIVisionX setup
if(os.path.exists(deps_dir)):
	print("\nMIVisionX Dependencies Installed\n")
else:
	print("\nMIVisionX Dependencies Installation\n")
	cmd='sudo -S '+linuxSystemInstall+' -y --allow-unauthenticated install cmake git wget unzip'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd '+setupDir+'; mkdir deps)');
	os.system('(cd '+deps_dir+'; git clone https://github.com/RadeonOpenCompute/rocm-cmake.git )');
	os.system('(cd '+deps_dir+'; git clone https://github.com/ROCmSoftwarePlatform/MIOpenGEMM.git )');
	os.system('(cd '+deps_dir+'; wget https://github.com/ROCmSoftwarePlatform/MIOpen/archive/'+MIOpenVersion+'.zip )');
	os.system('(cd '+deps_dir+'; unzip '+MIOpenVersion+'.zip )');
	os.system('(cd '+deps_dir+'; wget https://github.com/protocolbuffers/protobuf/archive/v3.5.2.zip )');
	os.system('(cd '+deps_dir+'; unzip v3.5.2.zip )');
	os.system('(cd '+deps_dir+'; wget https://github.com/opencv/opencv/archive/3.3.0.zip )');
	os.system('(cd '+deps_dir+'; unzip 3.3.0.zip )');
	os.system('(cd '+deps_dir+'; mkdir build )');
	os.system('(cd '+deps_dir+'/build; mkdir rocm-cmake MIOpenGEMM MIOpen OpenCV )');
	os.system('(cd '+deps_dir+'/build/rocm-cmake; cmake ../../rocm-cmake )');
	os.system('(cd '+deps_dir+'/build/rocm-cmake; make -j8 )');
	cmd='(cd '+deps_dir+'/build/rocm-cmake; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd '+deps_dir+'/build/MIOpenGEMM; cmake ../../MIOpenGEMM )');
	os.system('(cd '+deps_dir+'/build/MIOpenGEMM; make -j8 )');
	cmd='(cd '+deps_dir+'/build/MIOpenGEMM; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/MIOpen-'+MIOpenVersion+'; sudo -S cmake -P install_deps.cmake )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/build/MIOpen; sudo -S '+linuxSystemInstall+' -y --allow-unauthenticated install libssl-dev libboost-dev libboost-system-dev libboost-filesystem-dev  )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd '+deps_dir+'/build/MIOpen; cmake -DMIOPEN_BACKEND=OpenCL ../../MIOpen-'+MIOpenVersion+' )');
	os.system('(cd '+deps_dir+'/build/MIOpen; make -j8 )');
	os.system('(cd '+deps_dir+'/build/MIOpen; make MIOpenDriver )');
	cmd='(cd '+deps_dir+'/build/MIOpen; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/build/MIOpen; sudo -S apt autoremove )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/build/MIOpen; sudo -S apt autoclean )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf-3.5.2; sudo -S '+linuxSystemInstall+' -y --allow-unauthenticated install autoconf automake libtool curl make g++ unzip )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf-3.5.2; sudo -S apt autoremove )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf-3.5.2; sudo -S apt autoclean )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd '+deps_dir+'/protobuf-3.5.2; git submodule update --init --recursive )');
	os.system('(cd '+deps_dir+'/protobuf-3.5.2; ./autogen.sh )');
	os.system('(cd '+deps_dir+'/protobuf-3.5.2; ./configure )');
	os.system('(cd '+deps_dir+'/protobuf-3.5.2; make -j16 )');
	os.system('(cd '+deps_dir+'/protobuf-3.5.2; make check -j16 )');
	cmd='(cd '+deps_dir+'/protobuf-3.5.2; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf-3.5.2; sudo -S ldconfig )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf-3.5.2; sudo -S '+linuxSystemInstall+' -y --allow-unauthenticated install python-pip )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf-3.5.2; sudo -S yes | pip install protobuf )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf-3.5.2; sudo -S yes | pip install pytz )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf-3.5.2; sudo -S yes | pip install numpy )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='sudo -S '+linuxSystemInstall+' -y --allow-unauthenticated install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='sudo -S '+linuxSystemInstall+' -y --allow-unauthenticated install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd '+deps_dir+'/build/OpenCV; cmake -DWITH_OPENCL=OFF -DWITH_OPENCLAMDFFT=OFF -DWITH_OPENCLAMDBLAS=OFF -DWITH_VA_INTEL=OFF -DWITH_OPENCL_SVM=OFF ../../opencv-3.3.0 )');
	os.system('(cd '+deps_dir+'/build/OpenCV; make -j8 )');
	cmd='(cd '+deps_dir+'/build/OpenCV; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/build/OpenCV; sudo -S ldconfig )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='sudo -S '+linuxSystemInstall+' -y --allow-unauthenticated install inxi aha libboost-python-dev build-essential'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='sudo -S '+linuxSystemInstall+' -y --allow-unauthenticated install python-matplotlib python-numpy python-pil python-scipy python-skimage cython'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='sudo -S '+linuxSystemInstall+' -y --allow-unauthenticated install qt5-default qtcreator'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
