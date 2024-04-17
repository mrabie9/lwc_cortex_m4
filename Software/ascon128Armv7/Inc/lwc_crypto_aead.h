// NEITHER REPRESENTS NOR WARRANTS THAT THE OPERATION OF THE SOFTWARE WILL BE
// UNINTERRUPTED OR ERROR-FREE, OR THAT ANY DEFECTS WILL BE CORRECTED. NIST
// DOES NOT WARRANT OR MAKE ANY REPRESENTATIONS REGARDING THE USE OF THE SOFTWARE
// OR THE RESULTS THEREOF, INCLUDING BUT NOT LIMITED TO THE CORRECTNESS, ACCURACY,
// RELIABILITY, OR USEFULNESS OF THE SOFTWARE.
//
// You are solely responsible for determining the appropriateness of using and
// distributing the software and you assume all risks associated with its use,
// including but not limited to the risks and costs of program errors, compliance
// with applicable laws, damage to or loss of data, programs or equipment, and
// the unavailability or interruption of operation. This software is not intended
// to be used in any situation where a failure could cause risk of injury or
// damage to property. The software developed by NIST employees is not subject to
// copyright protection within the United States.
//

#ifndef LWC_CRYPTO_AEAD_H
#define LWC_CRYPTO_AEAD_H

#ifdef __cplusplus
extern "C" {
#endif

typedef int (*fn_aead_encrypt)(
	unsigned char *c, unsigned long long *clen,
	const unsigned char *m, unsigned long long mlen,
	const unsigned char *ad, unsigned long long adlen,
	const unsigned char *nsec,
	const unsigned char *npub,
	const unsigned char *k
);

typedef int (*fn_aead_decrypt)(
	unsigned char *m, unsigned long long *mlen,
	unsigned char *nsec,
	const unsigned char *c, unsigned long long clen,
	const unsigned char *ad, unsigned long long adlen,
	const unsigned char *npub,
	const unsigned char *k
);

typedef struct {

	const char* variant_name;
	const char* impl_name;
	int KeyBytes;
	int NonceBytes;
	int ABytes;
	fn_aead_encrypt encrypt;
	fn_aead_decrypt decrypt;

} aead_ctx;

extern aead_ctx lwc_aead_cipher;

int crypto_aead_encrypt(
	unsigned char* c, unsigned long long* clen,
	const unsigned char* m, unsigned long long mlen,
	const unsigned char* ad, unsigned long long adlen,
	const unsigned char* nsec,
	const unsigned char* npub,
	const unsigned char* k
);

int crypto_aead_decrypt(
	unsigned char* m, unsigned long long* mlen,
	unsigned char* nsec,
	const unsigned char* c, unsigned long long clen,
	const unsigned char* ad, unsigned long long adlen,
	const unsigned char* npub,
	const unsigned char* k
);


#ifdef __cplusplus
}
#endif

#endif // LWC_CRYPTO_AEAD_H
