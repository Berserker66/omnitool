from Crypto.Cipher import AES


def get_all(filename):
    with open(filename, "rb") as f:
        return f.read()


if __name__ == "__main__":
    bsecret = u"h3y_gUyZ"
    print
    "keystring:", bsecret
    secret = ""
    for e in bsecret:
        secret += "%x" % ord(e)
    print
    "encoded key:", secret
    print
    "raw:", get_all("player1.plr")
    print("")
    for x in range(1, 6):
        cipher = AES.new(secret, x, secret)
        decoded = cipher.decrypt(get_all("player1.plr"))
        print
        "Decrypted string " + str(x) + ":", decoded
        print("")
        with open(str(x) + "decode.txt", "wb") as f:
            f.write(decoded)
