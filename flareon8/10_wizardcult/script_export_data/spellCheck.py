import idaapi
spellResult1 = """PRIVMSG #dungeon :I cast Moonbeam on the Goblin for 205d205 damage!
PRIVMSG #dungeon :I cast Reverse Gravity on the Goblin for 253d213 damage!
PRIVMSG #dungeon :I cast Water Walk on the Goblin for 216d195 damage!
PRIVMSG #dungeon :I cast Mass Suggestion on the Goblin for 198d253 damage!
PRIVMSG #dungeon :I cast Planar Ally on the Goblin for 199d207 damage!
PRIVMSG #dungeon :I cast Water Breathing on the Goblin for 140d210 damage!
PRIVMSG #dungeon :I cast Conjure Barrage on the Goblin for 197d168 damage!
PRIVMSG #dungeon :I cast Water Walk on the Goblin for 204d198 damage!
PRIVMSG #dungeon :I cast Call Lightning on the Goblin for 193d214 damage!
PRIVMSG #dungeon :I cast Branding Smite on the Goblin for 256d256""".replace("\n", "").replace("PRIVMSG #dungeon :I cast ", "").replace(" on the Goblin for ", ";").replace(" damage!", ",").split(",")

blockInt = []
for i in range(0, 0xff+1):
    blockInt.append(i)
print(blockInt)

SpellTableAddr = 0x94E5A0
SpellTableSize = 341

SpellTable = []
for i in range(0, SpellTableSize):
    Spell = idaapi.get_qword(SpellTableAddr + i*16)
    SpellSize = idaapi.get_qword(SpellTableAddr + i*16 + 8)
    SpellTable.append(idaapi.get_bytes(Spell, SpellSize).decode("utf-8"))
print("SpellTable = %s" % str(SpellTable))

SpellByte1 = bytearray("", "utf-8")
for i in range(0, len(spellResult1)):
    SpellName = spellResult1[i].split(";")[0]
    SpellDame = spellResult1[i].split(";")[1].split("d")
    index = SpellTable.index(SpellName)
    SpellByte1.append(index ^ 0xa2)
    print(SpellDame)
    if (int(SpellDame[0]) < 256 and int(SpellDame[1]) < 256):
        SpellByte1.append(int(SpellDame[0], 10) ^ 0xa2)
        SpellByte1.append(int(SpellDame[1], 10) ^ 0xa2)
    
print("SpellByte1: %s" % str(SpellByte1))
