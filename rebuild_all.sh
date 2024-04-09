#!/bin/sh
filename=$1
wdir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/Software
output_file=$filename.txt
echo $output_file
echo > $output_file # Overwrite once 

for app in ascon128 ascon128a elephant160v2 giftcofb128v1 grain128aeadv2 isapa128av20 isapa128v20 photonbeetleaead128rate128v1 romulusn schwaemm256128v2 schwaemm256256v2 tinyjambu xoodyak; do
	echo "=============================== $app ===============================" >> $output_file
	# echo "Cleaning $app"
	make clean -C $wdir/"$app"
	# echo "Building $app"
	make -C $wdir/"$app" >> $output_file
	echo >> $output_file
	echo >> $output_file
done

#$SHELL #(prevent shell from auto closing)