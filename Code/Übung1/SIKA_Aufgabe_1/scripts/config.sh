#! /bin/bash
#This file sets some variables that are used in multiple scripts
#The other scripts can include this file so that all scripts use the same variables

export PREFIX=$HOME/SIKA/avr
export PATH=$PATH:$PREFIX/bin
export AVR_PATH=$PREFIX/bin/
export UTIL_PATH="../utils"
export CODE_DIR="../code"
export DEFAULT_C_FILE="${CODE_DIR}/student.c"
export DEFAULT_ELF_FILE="${CODE_DIR}/student.elf"
export DEFAULT_HEX_FILE="${CODE_DIR}/student.hex"
export DEFAULT_ASM_FILE="${CODE_DIR}/student.asm"
export DEFAULT_REPORT_FILE="../report/SIKA_AES_Report.pdf"
export ARCH=$(uname -m)
