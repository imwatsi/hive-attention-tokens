""" Handles Base58 encoding and decoding operations.
    Adapted from hive-python
    https://gitlab.syncad.com/hive/hive-python/-/blob/master/hivebase/base58.py
"""

from binascii import hexlify, unhexlify
import hashlib
import sys
import string
import logging

#log = logging.getLogger(__name__)

class Base58(object):
    """Base58 base class - an abstraction layer to deal with base58 encoded
    strings and their corresponding hex and binary representation"""

    def __init__(self, data, prefix="STM"):
        self._prefix = prefix
        if data[0] == "5" or data[0] == "6":
            self._hex = base58CheckDecode(data)
        elif data[0] == "K" or data[0] == "L":
            self._hex = base58CheckDecode(data)[:-2]
        elif data[:len(self._prefix)] == self._prefix:
            self._hex = gphBase58CheckDecode(data[len(self._prefix):])
        else:
            raise ValueError("Error loading Base58 object")

    def __repr__(self):
        """ Returns hex value of object"""
        return self._hex

    def __str__(self):
        """ Return graphene-base58CheckEncoded string of data

            :return: Base58 encoded data
            :rtype: str
        """
        return gphBase58CheckEncode(self._hex)

    def __bytes__(self):
        """ Return raw bytes"""
        return unhexlify(self._hex)


# https://github.com/tochev/python3-cryptocoins/raw/master/cryptocoins/base58.py
BASE58_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58decode(base58_str):
    base58_text = base58_str.encode('ascii')
    n = 0
    leading_zeroes_count = 0
    for b in base58_text:
        n = n * 58 + BASE58_ALPHABET.find(b)
        if n == 0:
            leading_zeroes_count += 1
    res = bytearray()
    while n >= 256:
        div, mod = divmod(n, 256)
        res.insert(0, mod)
        n = div
    else:
        res.insert(0, n)
    return hexlify(bytearray(1) * leading_zeroes_count + res).decode('ascii')


def base58encode(hexstring):
    byteseq = bytes(hexstring, 'ascii')
    byteseq = unhexlify(byteseq)
    byteseq = bytes(byteseq)

    n = 0
    leading_zeroes_count = 0
    for c in byteseq:
        n = n * 256 + c
        if n == 0:
            leading_zeroes_count += 1
    res = bytearray()
    while n >= 58:
        div, mod = divmod(n, 58)
        res.insert(0, BASE58_ALPHABET[mod])
        n = div
    else:
        res.insert(0, BASE58_ALPHABET[n])

    return (BASE58_ALPHABET[0:1] * leading_zeroes_count + res).decode('ascii')


def ripemd160(s):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(unhexlify(s))
    return ripemd160.digest()


def doublesha256(s):
    return hashlib.sha256(hashlib.sha256(unhexlify(s)).digest()).digest()


def base58CheckEncode(version, payload):
    s = ('%.2x' % version) + payload
    checksum = doublesha256(s)[:4]
    result = s + hexlify(checksum).decode('ascii')
    return base58encode(result)


def base58CheckDecode(s):
    s = unhexlify(base58decode(s))
    dec = hexlify(s[:-4]).decode('ascii')
    checksum = doublesha256(dec)[:4]
    assert (s[-4:] == checksum)
    return dec[2:]


def gphBase58CheckEncode(s):
    checksum = ripemd160(s)[:4]
    result = s + hexlify(checksum).decode('ascii')
    return base58encode(result)


def gphBase58CheckDecode(s):
    s = unhexlify(base58decode(s))
    dec = hexlify(s[:-4]).decode('ascii')
    checksum = ripemd160(dec)[:4]
    assert (s[-4:] == checksum)
    return dec
