import idaapi
import idc
import idautils
import struct
import ctypes
import pefile

list_lib = [
{"hash": 0x00523422, "name": "advapi32.dll" },
{"hash": 0x00246132, "name": "kernel32.dll" },
{"hash": 0x00176684, "name": "ntdll.dll"    },
{"hash": 0x07468951, "name": "oleaut32.dll" },
{"hash": 0x04258672, "name": "ole32.dll"    },
{"hash": 0x00052325, "name": "ws2_32.dll"   },
{"hash": 0x00234324, "name": "user32.dll"   },
{"hash": 0x43493856, "name": "gdi32.dll"    }
]

def getfncname(hashName, libName):
    pe = pefile.PE("C:\\windows\\system32\\%s" % libName)
    fncName = b""
    for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if exp.name == None:
            continue
        fncHash = hash_fnc(exp.name)
        if (fncHash == ctypes.c_int(hashName).value):
            fncName = exp.name
            break
    return fncName.decode("utf-8")
def hash_fnc(fncName):
    init_hash = ctypes.c_int(64)
    for c in fncName:
        init_hash = ctypes.c_int(ctypes.c_int(c).value - ctypes.c_int(0x45523F21).value * init_hash.value)
    return init_hash.value
    

def get_dword_param(addr):
    i = 0
    mov_data = b"\xc7\x45"+ struct.pack("B",(idaapi.get_byte(addr+2)))
    while i < 50:
        addr = idc.prev_head(addr)
        if idc.print_insn_mnem(addr) == "mov" and idc.get_bytes(addr, 3) == mov_data:
            return idaapi.get_dword(addr+3)
        i+=1
    return -1
def get_mov_reg(addr, reg):
    i = 0
    while i < 50:
        addr = idc.prev_head(addr)
        if idc.print_insn_mnem(addr) == "mov" and reg in idc.print_operand(addr, 0):
            if idc.get_operand_type(addr,1) == 0x5:
                return idc.get_operand_value(addr, 1)
            elif idc.get_operand_type(addr,1) == 0x4:
                return(get_dword_param(addr)) 
        i+=1
    return -1
i = 0

if (ida_enum.get_enum("fnc_hash_database") == 0xffffffff):
    enum_id = idc.add_enum(-1, "fnc_hash_database", idaapi.hex_flag())
else:
    enum_id = ida_enum.get_enum("fnc_hash_database")
for addr in XrefsTo(0x4054B0, flags=0):
    ecx = get_mov_reg(addr.frm, "ecx")
    edx = get_mov_reg(addr.frm, "edx")
    if (ecx == -1 or edx == -1):
        print("0x%08x: error not found" % addr.frm)
        continue
    
    for lib in list_lib:
        if ecx == lib['hash']:
            fncname = getfncname(edx, lib['name'])
            if fncname != "":
                print("%03d__ 0x%08x: ecx: 0x%08x; edx: 0x%08x ==> %s.%s" %(i, addr.frm, ecx, edx, lib['name'], fncname))    
                idc.set_cmt(addr.frm, "%s.%s" % (lib['name'], fncname), 0)
                idc.set_cmt(addr.frm, "%s.%s" % (lib['name'], fncname), 1)
                idc.add_enum_member(enum_id , "FNC_" + fncname.upper(), edx, -1)
            else:
                print("0x%08x: error not found %s.0x%08x" % (addr.frm, lib['name'], edx))
    i+=1
    
    # blob key 90 50 96 AE EB F1 D2 8E 0E 31 BC 27 27 40 97 05
    # blob key e3 fc 31 f4 d8 e9 b0 78 77 06 6b 5a a2 4f 5b 95 
    #L0ve
    #s3cret
    #5Ex
    #g0d
