import pygob
import pprint
from collections import namedtuple
pp = pprint.PrettyPrinter(depth=4)
VmIns = namedtuple("VmIns", "Opcode A0 A1 A2 Bm Cond")
LinkData = namedtuple("LinkData", "LhDevice LhReg RhDevice RhReg")

def vm_operator(ins, cpuIndx):
    VM_OPCODE = {1: "MOV", 5: "", 6: "", 10: "SUB", 13: "XOR acc, 0Xffffffff", 16: "AND", 18: "XOR"}

    insStr = "cpu%d.cond=%02d: " % (cpuIndx, ins.Cond)
    insStr += VM_OPCODE[ins.Opcode]
    if ins.Opcode == 1: # mov
        if ins.Bm & 1 != 0:
            insStr += " x%d, x%d" % (ins.A1, ins.A0)
        else:
            insStr += " x%d, %d" % (ins.A1, ins.A0)

    if ins.Opcode == 5: # teq
        if ins.Bm & 1 != 0:
            var1 = "x%d" % ins.A0
        else:
            var1 = "%d" % ins.A0
        if ins.Bm & 2 == 1:
            var2 = "x%d" % ins.A1
        else:
            var2 = "%d" % ins.A1
        insStr += "if " + var1 + "==" + var2 + ": cpu%d.cond=1 else cpu%d.cond=-1" % (cpuIndx, cpuIndx)

    if ins.Opcode == 6: #tgt
        if ins.Bm & 1 != 0:
            var1 = "x%d" % ins.A0
        else:
            var1 = "%d" % ins.A0
        if ins.Bm & 2 == 1:
            var2 = "x%d" % ins.A1
        else:
            var2 = "%d" % ins.A1
        insStr += "if " + var1 + ">" + var2 + ": cpu%d.cond=1 else cpu%d.cond=-1" % (cpuIndx, cpuIndx)

    if ins.Opcode == 10 or ins.Opcode == 16 or ins.Opcode == 18: # sub | and | xor
        if ins.Bm & 1 != 0:
            insStr += " acc, x%d" % ins.A0
        else:
            insStr += " acc, %d" % ins.A0
    insStr = insStr.replace("x4", "acc").replace("x5", "dat")
    insStr = insStr.replace("x", "cpu%d.x"%cpuIndx)
    insStr = insStr.replace("acc", "cpu%d.acc"%cpuIndx)
    insStr = insStr.replace("dat", "cpu%d.dat"%cpuIndx)
    return insStr

def get_link_reg(link, nCpu, nRom):
    lhLogic = ""
    rhLogic = ""
    lhIndexCpu = 0
    lhIndexRom = 0
    rhIndexCpu = 0
    rhIndexRom = 0
    
    if (link.LhDevice == 0):
        lhLogic = "input"
    elif (link.LhDevice == 1):
        lhLogic = "output"
    
    elif (link.LhDevice - 2 < nCpu):
        lhIndexCpu = link.LhDevice - 2
        lhLogic = "cpu%d.X%d" % (lhIndexCpu, link.LhReg)
    
    elif (link.LhDevice - nCpu - 2 < nRom):
        lhIndexRom = link.LhDevice - nCpu - 2
        lhLogic = "rom%d.X%d" % (lhIndexRom, link.LhReg)
        
    
    if (link.RhDevice == 0):
        rhLogic = "input"
    elif (link.RhDevice == 1):
        rhLogic = "output"
    
    elif (link.RhDevice - 2 < nCpu):
        rhIndexCpu = link.RhDevice - 2
        rhLogic = "cpu%d.X%d" % (rhIndexCpu, link.RhReg)
    
    elif (link.RhDevice - nCpu - 2 < nRom):
        rhIndexRom = link.RhDevice - nCpu - 2
        rhLogic = "rom%d.X%d" % (rhIndexRom, link.RhReg)

    return "set %s <=> %s" % (lhLogic, rhLogic)
    
def get_program(fileName):
    with open(fileName, "rb") as f:
        data = f.read()
        Program = pygob.load(data)
        
        nCpu = len(Program[3])
        if nCpu > 0:
            print("Program Cpu(%d):" % nCpu)
            for i in range(0, nCpu):  # get all cpu list
                print("CPU%d:" % i)
                cpu = Program[3][i]
                #pp.pprint(cpu)
                for ins in cpu[4]:  # get all ins of cpu
                    ins = VmIns(ins[0], ins[1], ins[2], ins[3], ins[4], ins[5])
                    print(vm_operator(ins, i))
       
        nRom = len(Program[4])
        if nRom > 0:
            print("Program Rom(%d):"%nRom)
            for i in range(0, nRom):  # get all cpu list
                print("ROM%d:" % i)
                rom = Program[4][i]
                pp.pprint(rom)    
            
        nLink = len(Program[6])
        if nLink > 0:        
            print("Program Link(%d):" % nLink)

            for i in range(0, nLink):  # get all cpu list
                print("Link%d:" % i)
                link = Program[6][i]
                pp.pprint(link)    
                lData = LinkData(link[0], link[1], link[2], link[3])
                print(get_link_reg(lData, nCpu, nRom))
                
            
get_program("vm2")
