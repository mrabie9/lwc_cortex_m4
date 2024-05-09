# Uppdated Luciano Ost 02/11/23
#!/bin/bash

ocddir="C:/OpenOCD/share/openocd/scripts"
wdir="C:/Git/lwc_cortex_m4/Build" # directory of project folder
elf_file="$app_name.elf"


echo
#$SHELL #(prevent shell from auto closing)
opt="Os"
for app in ascon128 ascon128Armv7 ascon128a ascon128aArmv7 isapa128v20 isapa128v20Armv7 isapa128av20 isapa128av20Armv7 schwaemm256128v2 schwaemm256128v2Armv7 schwaemm256256v2 schwaemm256256v2Armv7 tinyjambu tinyjambuOpt giftcofb128v1 xoodyak romulusn romulusnOpt elephant160v2  grain128aeadv2   photonbeetleaead128rate128v1; do
	echo "=============================== "$app"_"$opt".elf ===============================" 
	elf_file=""$app"_Pwr_"$opt".elf"
	while true; do
		read -n 1 -t 10000 input   
			if [[ $input = "[" ]] || [[ $input = "/" ]]; then
				openocd -f C:/Git/lwc_cortex_m4/Board/board.cfg -f C:/Git/lwc_cortex_m4/Board/stm32l4discovery.cfg -c "program $wdir/$elf_file verify reset exit"
			break 
		fi
	done
	
	
done
$SHELL #(prevent shell from auto closing)
