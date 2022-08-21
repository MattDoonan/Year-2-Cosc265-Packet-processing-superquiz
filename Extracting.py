#Extracting the destination address
def destination_address(packet):
    addr = (packet[16] << 24) | (packet[17] << 16) | (packet[18] << 8) | packet[19]
    d = f"{packet[-4]}.{packet[-3]}.{packet[-2]}.{packet[-1]}"
    return (addr, d)
 
#Extracting the payload
def payload(packet):
  l = []
  for i in range(20,len(packet)):
      if packet[i] != 0:
           l.append(packet[i])
  return bytearray(l)
