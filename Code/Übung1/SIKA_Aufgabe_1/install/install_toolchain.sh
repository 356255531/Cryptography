#! /bin/bash
#AVR Toolchain ( http://www.nongnu.org/avr-libc/user-manual/install_tools.html )
#
#Ubuntu 10.04 and 13.04

#Include all common variables
. ../utils/config.sh

updated=0
dpkg -s build-essential > /dev/null
if [ $? == 1 ]
then
	sudo apt-get update
	updated=1
	sudo apt-get install build-essential
fi

#coreutils contains md5sum, which we use in the submission script
dpkg -s coreutils > /dev/null
if [ $? == 1 ]
then
        sudo apt-get update
        updated=1
        sudo apt-get install coreutils
fi

dpkg -s texinfo > /dev/null
if [ $? == 1 ]
then
        sudo apt-get update
        updated=1
        sudo apt-get install texinfo
fi

dpkg -s timeout > /dev/null
if [ $? == 1 ]
then
        sudo apt-get update
        updated=1
        sudo apt-get install timeout
fi

dpkg -s mawk > /dev/null
if [ $? == 1 ]
then
	sudo apt-get update
	updated=1
	sudo apt-get install mawk
fi

dpkg -s binutils-dev > /dev/null
if [ $? == 1 ]
then
        sudo apt-get update
        updated=1
        sudo apt-get install binutils-dev 
fi

dpkg -s texinfo > /dev/null
if [ $? == 1 ]
then
	if [ $updated == 0 ]
	then
		sudo apt-get update
	fi
	sudo apt-get install texinfo
fi

dpkg -s libncurses5-dev > /dev/null
if [ $? == 1 ]
then
	if [ $updated == 0 ]
	then
		sudo apt-get update
	fi
	sudo apt-get install libncurses5-dev
fi


dpkg -s libexpat1-dev > /dev/null
if [ $? == 1 ]
then
	if [ $updated == 0 ]
	then
		sudo apt-get update
	fi
	sudo apt-get install libexpat1-dev
fi

dpkg -s curl > /dev/null
if [ $? == 1 ]
then
        if [ $updated == 0 ]
        then
                sudo apt-get update
        fi
        sudo apt-get install curl
fi

if lsb_release -r | grep "1[3-4]\..\+"
then
	dpkg -s python2.7-dev > /dev/null
	if [ $? == 1 ]
	then
		if [ $updated == 0 ]
		then
			sudo apt-get update
		fi
		sudo apt-get install python2.7-dev
	fi
	dpkg -s openjdk-7-jre > /dev/null
	if [ $? == 1 ]
	then
	        if [ $updated == 0 ]
	        then
	                sudo apt-get update
	        fi
	        sudo apt-get install openjdk-7-jre
	fi
	sudo apt-get install libiberty-dev
elif lsb_release -r | grep 10.04
then
	dpkg -s python2.6-dev > /dev/null
	if [ $? == 1 ]
	then
		if [ $updated == 0 ]
		then
			sudo apt-get update
		fi
		sudo apt-get install python2.6-dev
	fi
        dpkg -s oracle-java7-installer > /dev/null
        if [ $? == 1 ]
        then
        	sudo apt-add-repository ppa:webupd8team/java
		sudo apt-get update
		sudo apt-get install oracle-java7-installer
        fi
else
	echo "Unsupported Ubuntu release. Please consider using Ubuntu 10.04, 13.04 or 14.04"
	exit 1
fi

#Binutils
if lsb_release -r | grep 10
then
    export binutils_name=binutils-2.23.2
elif lsb_release -r | grep 13
then
    export binutils_name=binutils-2.23.2
elif lsb_release -r | grep 14
then #binutils-2.23.2 doesn't compile on Ubuntu 14
    export binutils_name=binutils-2.24
fi

if [[ ! -e ./packages/$binutils_name.tar.bz2 ]]
then
	wget --no-check-certificate -O ./packages/$binutils_name.tar.bz2 http://ftp.gnu.org/gnu/binutils/$binutils_name.tar.bz2
fi
echo "Unpacking binutils..."
bunzip2 -c ./packages/$binutils_name.tar.bz2 | tar xf -
cd $binutils_name
mkdir obj-avr
cd obj-avr
../configure --prefix=$PREFIX --target=avr --disable-nls
make

if [[ $? != 0 ]]
then
    echo "Error compiling binutils! Exiting..."
    exit
fi

make install

if [[ $? != 0 ]]
then
    echo "Error installing binutils! Exiting..."
    exit
fi

cd ..
cd ..
rm -rf $binutils_name

#GCC
if [[ ! -e ./packages/gcc-4.8.1.tar.bz2 ]]
then
	wget --no-check-certificate -O ./packages/gcc-4.8.1.tar.bz2 ftp://ftp.fu-berlin.de/unix/languages/gcc/releases/gcc-4.8.1/gcc-4.8.1.tar.bz2
fi
echo "Unpacking gcc..."
bunzip2 -c ./packages/gcc-4.8.1.tar.bz2 | tar xf -
cd gcc-4.8.1
./contrib/download_prerequisites
mkdir obj-avr
cd obj-avr
../configure --prefix=$PREFIX --target=avr --enable-languages=c,c++ --disable-nls --disable-libssp --with-dwarf2
make

if [[ $? != 0 ]]
then
    echo "Error compiling gcc! Exiting..."
    exit
fi


make install

if [[ $? != 0 ]]
then
    echo "Error compiling gcc! Exiting..."
    exit
fi


cd ..
cd ..
rm -rf gcc-4.8.1

#AVR libc
if [[ ! -e ./packages/avr-libc-1.8.0.tar.bz2 ]]
then
	wget --no-check-certificate -O ./packages/avr-libc-1.8.0.tar.bz2 http://download.savannah.gnu.org/releases/avr-libc/avr-libc-1.8.0.tar.bz2
fi
echo "Unpacking avr-libc..."
bunzip2 -c ./packages/avr-libc-1.8.0.tar.bz2 | tar xf -
cd avr-libc-1.8.0
./configure --prefix=$PREFIX --build=`./config.guess` --host=avr
make

if [[ $? != 0 ]]
then
    echo "Error compiling avr-libc! Exiting..."
    exit
fi

make install

if [[ $? != 0 ]]
then
    echo "Error installing avr-libc! Exiting..."
    exit
fi

cd ..
rm -rf avr-libc-1.8.0

#GDB for avr
if [[ ! -e ./packages/gdb-7.6.1.tar.bz2 ]]
then
	wget --no-check-certificate -O ./packages/gdb-7.6.1.tar.bz2 http://ftp.gnu.org/gnu/gdb/gdb-7.6.1.tar.bz2
fi
echo "Unpacking gdb..."
bunzip2 -c ./packages/gdb-7.6.1.tar.bz2 | tar xf -
cd gdb-7.6.1
mkdir obj-avr
cd obj-avr
../configure --prefix=$PREFIX --target=avr --with-python
make

if [[ $? != 0 ]]
then
    echo "Error compiling gdb! Exiting..."
    exit
fi

make install

if [[ $? != 0 ]]
then
    echo "Error installing gdb! Exiting..."
    exit
fi

cd ..
cd ..
rm -rf gdb-7.6.1

#simulavr
if [[ ! -e ./packages/simulavr-1.0.0.tar.gz ]]
then
	wget --no-check-certificate -O ./packages/simulavr-1.0.0.tar.gz http://download.savannah.gnu.org/releases/simulavr/simulavr-1.0.0.tar.gz
fi
echo "Unpacking simulavr..."
gunzip -c ./packages/simulavr-1.0.0.tar.gz | tar xf -
cd simulavr-1.0.0
patch -p0 < ../simulavr_patch.diff
mkdir obj-avr
cd obj-avr

if lsb_release -r | grep 10
then
    ../configure --prefix=$PREFIX
elif lsb_release -r | grep 13
    ../configure --prefix=$PREFIX
elif lsb_release -r | grep 14
then
    if [ "${ARCH}" == "i686" ]; then
        LIBIBERTY_PATH="/usr/lib/i386-linux-gnu"
    else
        LIBIBERTY_PATH="/usr/lib/${ARCH}-linux-gnu"
    fi
    ../configure --prefix=$PREFIX --with-libiberty="/usr/lib/${LIBIBERTY_PATH}"
fi

make

if [[ $? != 0 ]]
then
    echo "Error compiling simulavr! Exiting..."
    exit
fi

make install

if [[ $? != 0 ]]
then
    echo "Error installing simulavr! Exiting..."
    exit
fi

cd ..
cd ..
rm -rf simulavr-1.0.0
rm simulavr_patch.diff

#Avrora
if [[ ! -e ./packages/avrora-beta-1.7.117-with-timeout.jar ]]
then
	wget --no-check-certificate -O ./packages/avrora-beta-1.7.117.jar http://netcologne.dl.sourceforge.net/project/avrora/avrora-beta-1.7.117.jar
	cp -rf ./packages/avrora-beta-1.7.117.jar $PREFIX/bin/avrora-beta-1.7.117.jar
else
        cp -rf ./packages/avrora-beta-1.7.117-with-timeout.jar $PREFIX/bin/avrora-beta-1.7.117.jar
fi

#Pycrypto
if [[ ! -e ./packages/pycrypto-2.6.tar.gz ]]
then
	wget --no-check-certificate -O ./packages/pycrypto-2.6.tar.gz https://pypi.python.org/packages/source/p/pycrypto/pycrypto-2.6.tar.gz
fi
echo "Unpacking pycrypto..."
gunzip -c ./packages/pycrypto-2.6.tar.gz | tar xf -
cd pycrypto-2.6
python setup.py build
python setup.py install --user
cd ..
rm -rf pycrypto-2.6

if [[ ! -e ~/.bash_login ]]
then
    echo "source ~/.bashrc" >> ~/.bash_login
elif [[ ! $(grep "source ~/.bashrc" ~/.bash_login) ]]
then
    echo "source ~/.bashrc" >> ~/.bash_login
fi

echo "export PATH=$PREFIX/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc
