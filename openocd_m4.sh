# Uppdated by Luciano Ost 02/11/23
# Updated by Mohamed Rabie 27/11/23
#!/bin/bash

ocddir="C:/OpenOCD/share/openocd/scripts"
app_name="$1" # pass app name on CLI
wdir=C:/Git/lwc_cortex_m4/Build
elf_file="$app_name.elf"

echo
openocd -f C:/Git/lwc_cortex_m4/Board/board.cfg -f C:/Git/lwc_cortex_m4/Board/stm32l4discovery.cfg -c "program $wdir/$elf_file verify reset exit"

echo
#$SHELL #(prevent shell from auto closing)