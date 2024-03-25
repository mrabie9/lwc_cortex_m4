/*
 * aead.h
 *
 *  Created on: Oct 29, 2023
 *      Author: mdrab
 */

#ifndef INC_ASCON_128_AEAD_H_
#define INC_ASCON_128_AEAD_H_

#include <ASCON-128/api.h>
#include <ASCON-128/ascon.h>
#include <ASCON-128/permutations.h>
#include <ASCON-128/printstate.h>
#include <ASCON-128/word.h>


int crypto_aead_encrypt(unsigned char* c, unsigned long long* clen,
                        const unsigned char* m, unsigned long long mlen,
                        const unsigned char* ad, unsigned long long adlen,
                        const unsigned char* nsec, const unsigned char* npub,
                        const unsigned char* k);

int crypto_aead_decrypt(unsigned char* m, unsigned long long* mlen,
                        unsigned char* nsec, const unsigned char* c,
                        unsigned long long clen, const unsigned char* ad,
                        unsigned long long adlen, const unsigned char* npub,
                        const unsigned char* k);

#endif /* INC_ASCON_128_AEAD_H_ */
