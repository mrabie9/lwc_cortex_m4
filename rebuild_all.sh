#!/bin/sh
filename=$1
wdir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/Software
output_file=$filename.txt
echo $output_file
echo > $output_file # Overwrite once 

for app in Base ascon128 ascon128Armv7 ascon128a ascon128aArmv7 isapa128v20 isapa128av20Armv7 isapa128av20 isapa128v20Armv7 schwaemm256128v2 schwaemm256128v2Armv7 schwaemm256256v2 schwaemm256256v2Armv7 tinyjambu tinyjambuOpt giftcofb128v1 xoodyak romulusn romulusnOpt elephant160v2  grain128aeadv2   photonbeetleaead128rate128v1; do
	echo "=============================== $app ===============================" >> $output_file
	# echo "Cleaning $app"
	make clean -C $wdir/"$app"
	# echo "Building $app"
	make -C $wdir/"$app" >> $output_file
	echo >> $output_file
	echo >> $output_file
done

#for app in ascon128aArmv7 isapa128av20Armv7 isapa128v20Armv7 schwaemm256128v2Armv7 schwaemm256256v2Armv7 tinyjambuOpt; do
	#echo "=============================== $app ===============================" >> $output_file
	## echo "Cleaning $app"
	#make clean -C $wdir/"$app"
	### echo "Building $app"
	#make -C $wdir/"$app" >> $output_file
	#echo >> $output_file
	#echo >> $output_file
# done
#$SHELL #(prevent shell from auto closing)