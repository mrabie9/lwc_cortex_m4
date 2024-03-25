# Jonas Gava 
# updated Luciano Ost
# 2023-24 update by Mohamed Rabie

##### Project setup #####
# Name of your current project
PROJ_NAME = $(shell basename $(CURDIR))
BUILD_DIR = ../../Build
#~ PROJ_NAME = ascon128

# Linker script for STM32xx Device 
LINKER_SCRIPT = ../../Board/STM32L496ZGTxP_FLASH.ld

# Directory containing drivers source code
CMSIS_DIR = ../../Drivers/CMSIS
HAL_DIR = ../../Drivers/STM32L4xx_HAL_Driver

##### Arm Toolchain #####
TRIPLE  = arm-none-eabi
CC      = ${TRIPLE}-gcc
CLANG	= /soft64/cross/llvm/mitigation/clang_6.0.1/bin/clang
LD      = ${TRIPLE}-ld
AS      = ${TRIPLE}-as
GDB 	= ${TRIPLE}-gdb
OBJCOPY = ${TRIPLE}-objcopy
SZ 		= $(TRIPLE)-size

##### Compiler options #####
CFLAGS = -g -T$(LINKER_SCRIPT) -w
CFLAGS += -mlittle-endian -mthumb -mcpu=cortex-m4
CFLAGS += -mfloat-abi=hard --specs=nosys.specs

##### Project specific libraries #####
SRC_FILES += $(wildcard Src/*.c)
CFLAGS += -IInc

##### Drivers libraries and source code #####
CFLAGS += -I$(CMSIS_DIR)/Include
CFLAGS += -I$(CMSIS_DIR)/Device/ST/STM32L4xx/Include

SRC_FILES += ../../Startup/*
SRC_FILES += $(HAL_DIR)/Src/*
SRC_FILES += ../Common/Src/*
CFLAGS += -I$(HAL_DIR)/Inc
CFLAGS += -I../Common/Inc

all: $(PROJ_NAME).elf 
#$(PROJ_NAME).bin $(PROJ_NAME).hex

##### Flash code to board #####
flash:
	STM32_Programmer_CLI -c port=SWD -w $(shell pwd)/$(PROJ_NAME).hex -v -ob displ -rst

##### Print out disassembly of specified function using GDB #####
##### USAGE EXAMPLE: 	make disass FUNC=main 		    #####
disass: $(PROJ_NAME).elf
	$(GDB) $^ -batch -ex 'disass /r $(FUNC)'

clean:
	rm -f $(BUILD_DIR)/$(PROJ_NAME).bin $(BUILD_DIR)/$(PROJ_NAME).hex $(BUILD_DIR)/$(PROJ_NAME).elf $(BUILD_DIR)/$(PROJ_NAME).o

$(PROJ_NAME).elf: $(SRC_FILES) 
	$(CC) $(CFLAGS) -o $(BUILD_DIR)/$@ $^ -DSTM32L496xx -Wl,--print-memory-usage
	$(SZ) $(BUILD_DIR)/$@
	
assembly: 
	$(CC) -S -fverbose-asm $(CFLAGS) Src/aead.c -o $(BUILD_DIR)/Assembly/asconaead.s # output verbose assembly
	
#$(PROJ_NAME).elf: $(SRC_FILES) $(PROJ_NAME).o
#	$(CC) $(CFLAGS) -o $@ $^ #Src/$(PROJ_NAME)-$(SUFIX).o

#$(PROJ_NAME).o: $(PROJ_NAME).c
#	$(CLANG) --target=arm-none-eabi -mcpu=cortex-m4 -mfloat-abi=soft -mthumb -mlittle-endian -IInc -I/soft64/cross/gcc/gcc-arm-none-eabi-10.3/arm-none-eabi/include/ -fshort-enums -DKEY=$(KEY) -DDEBUG $(EXTRA_FLAGS) -c -o $@ $<

#~ $(PROJ_NAME).hex: $(PROJ_NAME).elf
#~ 	$(OBJCOPY) -O ihex $(PROJ_NAME).elf $@

#~ $(PROJ_NAME).bin: $(PROJ_NAME).elf
#~ 	$(OBJCOPY) -O binary $^ $@

