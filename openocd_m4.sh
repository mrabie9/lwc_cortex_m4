# Uppdated Luciano Ost 02/11/23
#!/bin/bash

ocddir="C:/OpenOCD/share/openocd/scripts"
app_name="$1" # pass app name on CLI
wdir="C:/WSD030/m7_board/m4_board/Build" # directory of project folder
elf_file="$app_name.elf"

echo
openocd -f C:/WSD030/m7_board/m4_board/Board/board.cfg -f C:/WSD030/m7_board/m4_board/Board/stm32l4discovery.cfg -c "program $wdir/$elf_file verify reset exit"

echo
#$SHELL #(prevent shell from auto closing)