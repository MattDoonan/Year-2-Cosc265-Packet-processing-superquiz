def basic_packet_check(packet):
    if len(packet) < 20:
        return 1
    if (packet.hex()[0]) != '4':
        return 2
    x = 0
    for i in range(0,20,2):
        x += (packet[i] << 8) | packet[i+1]    
    while x > 0xFFFF:
        x0 = x & 0xFFFF
        x1 = x >> 16
        x = x0 + x1
    if x != 0xFFFF:
        return 3
    test = (packet[2]<<8)|packet[3]
    if len(packet) != test:
        return 4
    
    return True
