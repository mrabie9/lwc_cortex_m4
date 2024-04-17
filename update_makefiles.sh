#!/bin/bash

wdir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/Software
# Define the file to be copied
file_to_copy="$wdir/common/Makefile"

for app in ascon128 ascon128a elephant160v2 giftcofb128v1 grain128aeadv2 isapa128av20 isapa128v20 photonbeetleaead128rate128v1 romulusn schwaemm256128v2 schwaemm256256v2 tinyjambu xoodyak; do
    # Check if the folder exists
	cp "$file_to_copy" "$wdir/$app/"
	echo "Copied $file_to_copy to $app"
done

file_to_copy="$wdir/ascon128Armv7/Makefile"
for app in ascon128aArmv7 isapa128av20Armv7 isapa128v20Armv7 schwaemm256128v2Armv7 schwaemm256256v2Armv7 tinyjambuOpt; do
    # Check if the folder exists
	cp "$file_to_copy" "$wdir/$app/"
	echo "Copied $file_to_copy to $app"
done
