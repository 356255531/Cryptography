.PHONY: install
all: clean compile verify

clean:
	@echo "Cleaning up code directory ...\n"
	@cd code && rm -rf *.elf *.hex *.trace *.memtrace

compile:
	@echo "Compiling student.c ...\n"
	@cd scripts && ./compile.sh

verify:
	@echo "Verifying student.elf ...\n"
	@cd scripts && ./verify_code.sh -s 60 && ( ./measure_runtime.sh; ./measure_memusage.sh; ./measure_size.sh )

submit:
	@echo "Submitting student.c ...\n"
	@cd scripts && ./submit_code.sh

flash:
	@echo "Flashing code/student.hex to MCU ...\n"
	@avrdude -p m644 -c avrisp2 -B 5 -P usb -U flash:w:code/student.hex

install:
	@echo "Installing the Toolchain ...\n"
	@cd install && ( ./install_toolchain.sh 2>&1 | tee install_toolchain.log )
	@echo "Please run \"source ~.bashrc\"!"

remove:
	@echo "Removing the toolchain ...\n"
	@rm -Ir ~/SIKA
