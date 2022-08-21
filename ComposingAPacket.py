def compose_packet(hdrlen, tosdscp, identification, flags, fragmentoffset, timetolive, protocoltype, sourceaddress, destinationaddress, payload):
    if hdrlen >= 2**4 or hdrlen < 0 or hdrlen < 5:
        return 2    
    if tosdscp >= 2**6 or tosdscp < 0:
        return 3
    if identification >= 2**16 or identification < 0:
        return 5
    if flags >= 2**3 or flags < 0:
        return 6
    if fragmentoffset >= 2**13 or fragmentoffset < 0:
        return 7
    if timetolive >= 2**8 or timetolive < 0:
        return 8
    if protocoltype >= 2**8 or protocoltype < 0:
        return 9
    if sourceaddress >= 2**32 or sourceaddress < 0:
        return 11
    if destinationaddress >= 2**32 or destinationaddress < 0:
        return 12  
    add = bytearray([])
    totallength = 20 + len(payload)    
    if hdrlen > 5:
        add = bytearray([0,0,0,0]) 
        totallength = 20 + 4 + len(payload)        
    version = 4
    headerchecksum = 0 
    if totallength >= 2**16 or totallength < 0:
        return 4    
    test = compose_header(version, hdrlen, tosdscp, totallength, identification, flags, fragmentoffset, timetolive, protocoltype, headerchecksum, sourceaddress, destinationaddress)
    x = 0
    for i in range(0,20,2):
        x += (test[i] << 8) | test[i+1]    
    while x > 0xFFFF:
        x0 = x & 0xFFFF
        x1 = x >> 16
        x = x0 + x1
    headerchecksum = 0xFFFF - x
    final = compose_header(version, hdrlen, tosdscp, totallength, identification, flags, fragmentoffset, timetolive, protocoltype, headerchecksum, sourceaddress, destinationaddress)
    return final+add+payload
    
    
def compose_header(version, hdrlen, tosdscp, totallength, identification, flags, fragmentoffset, timetolive, protocoltype, headerchecksum, sourceaddress, destinationaddress):
    if version != 4:
        return 1
    if hdrlen >= 2**4 or hdrlen < 0:
        return 2
    if tosdscp >= 2**6 or tosdscp < 0:
        return 3
    if totallength >= 2**16 or totallength < 0:
        return 4
    if identification >= 2**16 or identification < 0:
        return 5
    if flags >= 2**3 or flags < 0:
        return 6
    if fragmentoffset >= 2**13 or fragmentoffset < 0:
        return 7
    if timetolive >= 2**8 or timetolive < 0:
        return 8
    if protocoltype >= 2**8 or protocoltype < 0:
        return 9
    if headerchecksum >= 2**16 or headerchecksum < 0:
        return 10
    if sourceaddress >= 2**32 or sourceaddress < 0:
        return 11
    if destinationaddress >= 2**32 or destinationaddress < 0:
        return 12
    array1 = bytearray ([((version << 4) | (hdrlen)),((tosdscp << 2) | 00), (totallength >> 8), (totallength & 0x00ff)])    
    array2 = bytearray ([(identification >>8),(identification & 0x00ff),((flags<<3) | (fragmentoffset>>8)), (fragmentoffset & 0x00000ff)])
    array3 = bytearray ([timetolive,protocoltype,(headerchecksum >> 8), (headerchecksum & 0x00ff)])
    array4 = bytearray ([(sourceaddress >> 24), ((sourceaddress >> 16) & 0x00ff),((sourceaddress >> 8)&0x00ff),(sourceaddress & 0x000ff) ])
    array5 = bytearray ([(destinationaddress >> 24), ((destinationaddress >> 16) & 0x00ff),((destinationaddress >> 8)&0x00ff),(destinationaddress & 0x000ff) ])
    return array1+array2+array3+array4+array5
