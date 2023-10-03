import addressStore

def hexa(s):
    l=format(int(s,2),'01x')
    return l

def machineHelp(n):  #Machine code generator helper
    p=''
    for i in range(0,len(n),4):
        p+=hexa(n[i:i+4])
    return '0x'+p

def signExtend(s):  #sign extending the immediate value
    temp=''
    if(s[0]=='-'):
        i=0
        while(s[i]!='1'):
            temp+='1'
            i+=1
        temp+=s[i:]
    else:
        temp=s
    return temp


fp= open('./kaalKoot.asm','r')
inst=open('./instructions.txt','r')
pinst=open('./psuedo_instructions.txt','r')
reg=open('./registers.txt','r')

address=addressStore.address
instruct=addressStore.instruct
rinst=addressStore.rinst
Iinst=addressStore.Iinst
Jinst=addressStore.Jinst
branch=addressStore.branch
procedure=addressStore.procedure
machine=addressStore.machine
size=addressStore.size
code=[]

def machineCode():
    """
    This function reads the assembly code from a file and converts it into machine code.
    It uses a dictionary 'machine' to map each instruction to its corresponding machine code.
    It also uses file 'inst' and dictionary 'Iinst' to map each instruction to its corresponding opcode.
    The function returns a list of machine code instructions.
    """
    control=0
    counter=-1
    for line in fp:
        x=line.strip()
        k=0
        found=0
        for i in range(len(x)):
            if(x[i]=='#'):  #Second parsing will remove comments and generate machine codes
                k=i
                found=1
                break
            else:
                k=len(x)
        if(k!=0 and found==1):
            x=x[0:k-1]
        elif(found==1 and k==0):
            x=x[0:k]
        if(x==".data"):
            continue
        if(x==".text"): #marks the start of instruction memory
            control=1
            continue
        if(x != ".data" and x !=".text" and x!='\n' and x!=''):
            if(control==1):
                t=x.split() #extracting the instruction
                if(t[0][-1]==":"):
                    continue
                instTrue=False
                for row in inst: 
                    temp=row.split()
                    if(temp[0]==t[0]):
                        counter+=1
                        instTrue=True
                        if(temp[0]=='jr' or temp[0]=='lb' or temp[0]=='sb' or temp[0]=='lw' or temp[0]=='syscall' or temp[0]=='beqz' or temp[0]=='sw' or temp[0]=='move'):
                            code.append(machine[t[0]]) #calling the machine code from mahcine dictionary
                            break
                        if(temp[-1]=='jump'):
                            s=procedure[t[1]]
                            l=int(s,16)
                            l=format(l,'032b') #generating 32 bit long address field for jump instruction
                            l=l[4:-2] #taking a substring to shorten the length to 26 bits
                            s=temp[1]
                            s=s+l
                            code.append(machineHelp(s))
                        
                        elif(temp[1]=='000000'): #checking for R-Type instructions
                            l=''.join(t[1:])
                            l=l.split(',')
                            s1=temp[1]
                            s2=temp[2]
                            s=''
                            for j in range(1,len(l)):
                                for regi in reg:
                                    t2=regi.split()
                                    if(l[j]==t2[0]):
                                        s+=format(int(t2[1]),'05b')
                                        break
                                reg.seek(0)
                            
                            reg.seek(0)
                            for regi in reg: #this is done for destination register
                                t2=regi.split()
                                if(l[0]==t2[0]):
                                    s+=format(int(t2[1]),'05b')
                                    break
                            reg.seek(0)
                            s=s1+s+s2
                            code.append(machineHelp(s))
                            break

                        elif(temp[-1]=='branch'): #checking if the instruction branches
                            l1=int(address[counter],16)
                            l2=int(procedure[t[-1]],16)
                            l2=int(((l2-l1)/4)) -1
                            l2=format(l2,'016b') #formatting the no. of addresses between the branch statement and the procedure into16 bit binary
                            s3=signExtend(l2)
                            s1=temp[1]
                            s=''
                            reg.seek(0) #moving the register file pointer to the start again
                            for j in range(1,len(t)-1):
                                mp=t[j].split(',')
                                for regi in reg:
                                    t2=regi.split()
                                    if(mp[0]==t2[0]):
                                        s+=format(int(t2[1]),'05b') #formatting the register used into 5 bit binary
                                        break
                                reg.seek(0)
                            s=s1+s+s3
                            code.append(machineHelp(s)) #changing the formaed 32 binary string to 8 bit hexadecimal
                            break
                        else:
                            l=''.join(t[1:])
                            l=l.split(',')
                            s1=Iinst[t[0]]
                            l2=format(int(l[-1]),'016b') #changing the immediate field to 16 bit binary and then sign extending it
                            s3=signExtend(l2)
                            s=''
                            reg.seek(0)
                            for j in range(1,-1,-1):
                                for regi in reg:
                                    t2=regi.split()
                                    if(l[j]==t2[0]):
                                        s+=format(int(t2[1]),'05b')
                                        break
                                reg.seek(0)
                            s=s1+s+s3
                            code.append(machineHelp(s))
                            break                                          
                inst.seek(0)

                if(instTrue==False):
                    l=''.join(t[1:])
                    l=l.split(',')
                    for row in pinst:
                        temp=row.split()
                        if(temp[0]==t[0]):
                            for i in range(1,len(temp)):
                                counter+=1
                                for a in inst:
                                    m=a.split()
                                    if(m[0]==temp[i]):
                                        if(m[1]=='000000'): #checking for R-type instruction
                                            s1=m[1]
                                            s2=m[-1]
                                            s=''
                                            if(t[0]=='bgt'):
                                                for j in range(1,-1,-1):
                                                    for regi in reg:
                                                        t2=regi.split()
                                                        if(l[j]==t2[0]):
                                                            s+=format(int(t2[1]),'05b')
                                                            break
                                                    reg.seek(0)
                                            else:
                                                for j in range(0,len(l)-1):
                                                    for regi in reg:
                                                        t2=regi.split()
                                                        if(l[j]==t2[0]):
                                                            s+=format(int(t2[1]),'05b')
                                                            break
                                                    reg.seek(0)
                                       
                                            s=s1+s+'00001'+s2
                                            code.append(machineHelp(s))
                                            break

                                        elif(m[-1]=='branch'): #checking for instruction if it branches
                                            if(t[0]=='bgt'):
                                                code.append('0x14200008')
                                            elif(t[0]=='blt'):
                                                code.append('0x14200006')
                                            break

                                        else: #checking for I-type instruction
                                            if(m[0]=='lui'):
                                                code.append('0x3c011001')
                                                break

                                            if(m[0]=='ori'):
                                                s3=format(int(size[l[-1]]),'016b')
                                                s='0011010000100100'+s3
                                                code.append(machineHelp(s))
                                                break

                                            if(m[0]=='addiu'): #addiu instruction s1 is opcode and s is the immediate register value always added when li instruction is used
                                                s1='001001'
                                                s='00000'
                                                for regi in reg:
                                                    t2=regi.split()
                                                    if(l[0]==t2[0]):
                                                        s+=format(int(t2[1]),'05b')
                                                        break
                                                reg.seek(0)
                                                b=format(int(l[-1]),'016b')
                                                s=s1+s+b
                                                code.append(machineHelp(s))

                            #returning the file pointer to start
                                inst.seek(0)
                    pinst.seek(0)
                                            


addressStore.storeAddress() #calling the address function in order to store the variables