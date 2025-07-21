import argparse
import hmac
import hashlib
import time
from cryptography.fernet import Fernet

yes_this_is_cybersecurity : bytes = b'byTBAloO7KD_tHP5BNvywi54S6Lag53DWo2tG3JpU2U='

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", action="store_true", help="he program receives as argument a hexadecimal key of at least 64 characters. The program stores this key safely in a file called ft_otp.key, which is encrypted.")
    parser.add_argument("-k", action="store_true", help="The program generates a new temporary password based on the key given as argument and prints it on the standard output.")
    parser.add_argument("key", type=str, help="the given key to either encrypt or use to generate the OTP password")
    args = parser.parse_args()

    # XOR the argument so that only one is allowed
    if (not (args.g ^ args.k)):
        parser.error("Argument Error: Program needs only one of the options!")
    return args

def read_file(key: str):
    if (key.endswith(".hex", 1) == False):
        raise Exception("hex file needs to have extention .hex!")
    with open(key, "r") as file:
        content = file.read()
        if (len(content) != 64):
            raise KeyError("key must be 64 hexadecimal characters.")
        # check to see that its hexadecimal
        int(content, 16)
        return content

def encrypt_key(content: str):
    chipher_suite = Fernet(yes_this_is_cybersecurity)
    key = chipher_suite.encrypt(content.encode("utf-8"))

    with open("ft_otp.key", "wb") as file:
     file.write(key)
     print("Key was successfully saved in ft_otp.key.")

def decrypt_key(key_path: str):
    if (key_path.endswith("ft_otp.key") == False):
        raise Exception("incorrect file given! should be [ft_otp.key]")
    cipher_suite = Fernet(yes_this_is_cybersecurity)
    with open(key_path, "r") as file:
        key_content = file.read()
        return cipher_suite.decrypt(key_content.encode("utf-8"))



def hotp(key: bytes, counter: bytes):    
    hmacResult = hmac.new(key, counter, hashlib.sha1).digest()
    
    # this will pick an offster based on the last byte
    # &0xf means we want to extract the lowest 4 bits of byte
    # security: We do this so that we dont have a fixed place where we extract the 31 bit interger
    # This makes it much harder to actually reverse engineer the code since its based on the hmac hash which 4 bits we are extracting
    offset = hmacResult[-1] & 0xf

    # the first bytes ensures that the most signifant bit is 0 meaning the interger is postive since we only want to use postive intergers
    binCode = (hmacResult[offset] & 0x7f) << 24 \
        | (hmacResult[offset+1] & 0xff) << 16 \
        | (hmacResult[offset+2] & 0xff) << 8 \
        | (hmacResult[offset+3] & 0xff)
    # after combining all the 4 bytes with the bitwise OR will result in a interger that we can work with 
    digits = 6
    # This integer is still to large so we want to use only the last 6 digits so we modulo to extract the 6 digets form the code
    # for example [234239402] -> [239402]
    code = str(binCode % (10 ** digits))
    # even if the result is smaller than 6 digits zfill will make sure to make it 6 digits by filling it up with zeros
    # for example [123] -> [000123]
    code = code.zfill(digits)
    return code


if __name__ == "__main__":
    args = parse_arguments()
    try:
        if (args.g):
            content = read_file(args.key)
            encrypt_key(content)
        elif (args.k):
            content = decrypt_key(args.key)
            counter = int(time.time() // 30).to_bytes(8, 'big')
            code = hotp(content, counter)
            print(code)
    except Exception as error:
        print("error:", error)
        exit(-1)
