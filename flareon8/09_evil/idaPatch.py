import idaapi
import idc
import idautils
import struct

# find all access violent and div zero exception code
def find_changed_bytes():

    changed_bytes = list()
    for seg_start in Segments():
        for ea in range(seg_start, SegEnd(seg_start) ):
            if isLoaded(ea):
                byte = Byte(ea)
                original_byte = GetOriginalByte(ea)
                if byte != original_byte:
                    changed_bytes.append( (ea, byte, original_byte) )
            
    return changed_bytes


def path_mov_edx_ins(addr, dwValue):
    patch_byte(addr, 0xba)
    patch_dword(addr+1, dwValue)
    patch_word(addr+1+4, 0x9090)
  
def path_mov_ecx_ins(addr, dwValue):
    patch_byte(addr, 0xb9)
    patch_dword(addr+1, dwValue)
    patch_word(addr+1+4, 0x9090)  
    
def patch_call_ins(ins_addr):
    # patched_byte = b"\xE8" + "\xa8\xcf\xff\xff" + "\xFF\xD0\x90\x90\x90\x90\x90\x90"
    addr = ins_addr+6
    patched_byte = b"\xE8" + bytes(struct.pack("<i", 0x4054b0-addr-5)) + b"\xFF\xD0"
    for i,b in enumerate(patched_byte):
        patch_byte(addr+i, b) 


def get_dword_param(addr):
    mov_data = "c7 45 %x" % (idaapi.get_byte(addr+2))
    mov_addr = ida_search.find_binary(addr-0x4b, ida_idaapi.BADADDR, mov_data, 16, ida_search.SEARCH_DOWN)
    if mov_addr == ida_idaapi.BADADDR:
        return ida_idaapi.BADADDR, -1
    else:
        return mov_addr, idaapi.get_dword(mov_addr+3)
    
addr = idaapi.get_imagebase()
bin_str_arr = ["8B 55 ?? 8B 4D ?? 33 ?? 8B ??", "8B 55 ?? 8B 4D ?? 33 ?? F7 ??", "8B 95 78 FF FF FF 8B 4D ?? 33 ?? F7 ??"]

mov_edx_ins = ["ba 44 33 22 11 90 90"]    # mov    edx,0x11223344
mov_ecx_ins = ["b9 44 33 22 11 90 90"]    # mov ecx, 0x11223344

for bin_str in bin_str_arr:
    i = 0
    addr = idaapi.get_imagebase()
    while True:    
        addr = ida_search.find_binary(addr, ida_idaapi.BADADDR, bin_str, 16, ida_search.SEARCH_NEXT|ida_search.SEARCH_DOWN)
        if addr == ida_idaapi.BADADDR:
            break
        print("Patching 0x%08x to call api deobfuscate" % (addr))
        patch_byte(addr+1, 0x4d)
        patch_byte(addr+4, 0x55)
        #mov_ecx_addr, ecx_value = get_dword_param(addr)
        #mov_edx_addr, edx_value = get_dword_param(addr+3)
        #if (mov_edx_addr == ida_idaapi.BADADDR):
        #    print("error find mov_edx_addr")
        #    continue
        #if (mov_ecx_addr == ida_idaapi.BADADDR):
        #    print("error find mov_ecx_addr")
        #    continue
        #print("Found mov edx at 0x%08x - 0x%08x.. Patching to mov ecx!" %(mov_ecx_addr, ecx_value))
        #print("Found mov ecx at 0x%08x - 0x%08x.. Patching to mov edx!" %(mov_edx_addr, edx_value))
        patch_call_ins(addr)
        #path_mov_ecx_ins(mov_ecx_addr, ecx_value)
        #path_mov_edx_ins(mov_edx_addr, edx_value)
        i+=1
        
    