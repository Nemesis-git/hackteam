# solution du challenge emu 2.0 du CTF X_MAS CTF 2019
# by Theo Parmentier

A = 0 # registre A sur 8 bits
PC = 0x100 # registre PC sur 12 bits
mem = [] # memoire sui sera rpresentee par une liste python
add_blocked = [] # liste des memoires bloquees et donc plus accessibles

def parse_opcode(opcode, arg):
    is_jump = False
    global A
    global PC
    global add_blocked
    global mem
    x = int(arg, base=16) 

    if opcode == "00":
        A = A + x
        A = A & 0xff # attention au debordement de memoire, ne pas oublier le and
        return is_jump

    elif opcode == "01":
        A = x
        return  is_jump

    elif opcode == "02":
        A = A ^ x
        return  is_jump

    elif opcode == "03":
        A = A | x
        return  is_jump

    elif opcode == "04":
        A = A & x
        return is_jump

    elif opcode[0] == "8":
        A = int(''.join(mem[2*x:2*x+2]), base=16)
        return  is_jump

    elif opcode[0] == "d":
        if x in add_blocked:
            return is_jump
        mem[2*x:2*x+2]  = list(hex(int(''.join(mem[2*x:2*x+2]), base=16) ^ A)[2:].zfill(2))
        return  is_jump

    elif opcode[0] == "f":
        if x in add_blocked:
            return  is_jump
        mem[2*x:2*x+2] = list(hex(A)[2:].zfill(2))
        return  is_jump

    elif opcode == "13":
        if x == 0x37:
            print chr(A)
            return is_jump
        else:
            A -= 1 # operande non connue
            return  is_jump

    elif opcode[0] == "2":
        PC = x
        is_jump = True
        return  is_jump

    elif opcode[0] == "3":
        if A == 0:
            PC = x
            is_jump = True
        return  is_jump

    elif opcode[0] == "4":
        if A == 1:
            PC = x
            is_jump = True
        return  is_jump

    elif opcode[0] == "5":
        if A == 255:
            PC = x 
            is_jump = True
        return  is_jump

    elif opcode == "60":
        if A == x:
            A = 0
        elif A < x:
            A = 1
        elif A > x:
            A = 255
        return  is_jump

    elif opcode[0] == "7":
        xxx = int(''.join(mem[2*x:2*x+2]), base=16)
        if A == xxx:
            A = 0
        elif A > xxx:
            A = 255
        elif A < xxx:
            A = 1 
        return is_jump

    elif opcode == "be":
        if x == 0xef:
            is_jump = True
            A = 0x42
            PC = 0x100
            return is_jump
        else:
            A -= 1
            return is_jump

    elif opcode[0] == "9":
        add_blocked.append(x)
        return is_jump

    elif opcode[0] == "a":
        add_blocked.remove(x)
        return is_jump

    elif opcode[0] == 'c':
        if x in add_blocked:
            return is_jump
        xxx = int(''.join(mem[2*x:2*x+2]), base=16)
        xxx = xxx ^ 0x42
        mem[2*x:2*x+2] = list(hex(xxx)[2:].zfill(2))
        return is_jump

    elif opcode == "ee":
        if x == 0xee:
            return is_jump
        else:
            A -= 1
            return  is_jump

    else: # operande non connue
        A -= 1
        return is_jump

if __name__ == "__main__":

    fp = open("rom", "rb")
    brute = fp.read()
    mem = list('0' * 0x200 + brute.encode('hex').lower())
    # il faut faire attention sur le fait que la taille entre une adresse (3 quartets) et celle de sa "contenance" (2 quarteets) n'est pas la meme
    x = 0
    while PC < len(brute):
        x = PC * 2
        opcode = ''.join(mem[x:x+2])
        second = ''.join(mem[x+2:x+4])
        arg = second

        if opcode[0] == "8" or opcode[0] == "2" or opcode[0] == "3" or opcode[0] == "4" or opcode[0] == "5" or opcode[0] == "7" or opcode[0] == "9" or opcode[0] == "a" or opcode[0] == "c" or opcode[0] == "d" or opcode[0] == "f":
            arg = opcode[1] + arg
            
        is_jump = parse_opcode(opcode, arg)
        # seulement incrementer PC si pas de jump a la derniere commande comme en ASM
        if is_jump == False :
            PC += 2