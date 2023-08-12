input = ["0106000000FF",    "010600000000",
         "0206000000FF",    "020600000000",
         "0306000000FF",    "030600000000",
         "0406000000FF",    "040600000000",
         "0506000000FF",    "050600000000",
         "0606000000FF",    "060600000000",
         "0706000000FF",    "070600000000",
         "0806000000FF",    "080600000000",
         "0F06000000FF",    "0F0600000000",
         "0C0300050001",    "0C0600080009"]
def modbusCrc(msg:str) -> int:
    crc = 0xFFFF
    for n in range(len(msg)):
        crc ^= msg[n]
        for i in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

for turn in input:
    c2 = [int(turn[i:i + 2], 16) for i in range(0, len(turn), 2)]
    msg = bytes.fromhex(turn)
    crc = modbusCrc(msg)
    #print("0x%16X"%(crc))
    ba = crc.to_bytes(2, byteorder='little')
    c2.append(ba[0])
    c2.append(ba[1])

    #Result
    #print(turn)
    print(c2)
    print()
    #print("[%02X,%02X]"%(ba[0], ba[1]))