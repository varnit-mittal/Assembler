import pandas as pd


def hexa(i):
    s=format(i,'08x')
    return '0x'+s

fp= open('./kaalKoot.asm','r')

address=[]
instruct={}
size={}
rinst={}
Iinst={}
Jinst={}
branch={}
procedure={}

# df = pd.DataFrame()

machine={}

inst=open('./instructions.txt','r')
pinst=open('./psuedo_instructions.txt','r')

#This is two-pass MIPS assembler
def storeAddress():
    """
    This function reads the assembly code from a file and stores the addresses of instructions and data in a dictionary.
    """
    instAddress='0x00400000' #Starting address of the instructions
    control=0
    proc=0  #procedure control variable
    total=0
    procName=""  #procedure name storing variable for temporary purposes
    for line in fp:
        x=line.strip()
        k=0
        found=0
        for i in range(len(x)):  #this iteration is done in order to remove comments in the code
            if(x[i]=='#'):
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
        if(x==".text"):  #this marks the starting of the instructions by changing the control to 1
            control=1
            continue

        if(x != ".data" and x !=".text" and x!='\n' and x!=''):
            if(control==0):  #Here the sizes of the dynamically allocated memory are stored with respective keys
                temp=x.split(': .')
                p=0
                for i in range(len(temp[1])):
                    if(temp[1][i]==' '):
                        p=i
                        break

                op=temp[1][0:p]
                s=""
                a=0
                if(op!="space"):
                    p=p+2
                    s=temp[1][p:-1]
                    a=len(s)
                    for i in s:
                        if(i=='\\'):
                            a-=1
                    a+=1
                else:
                    s=temp[1][p+1:]
                    a=int(s)
                size[temp[0]]=total
                total+=a

            if (control ==1): 
                t=x.split() # Makeing a list in order to extract the instruction from the line 

                if(t[0][-1]==":"): #this segment stores and controls the procedure names in order to store their addresses
                    proc=1
                    procName=t[0][:-1]
                    continue

                instTrue=False  #this variable stores if the instruction is psuedo or not
                for row in inst: 
                    temp=row.split()  #parsing through the instructions 
                    if(temp[0]==t[0]):
                        instTrue=True #marking the instruction as basic instruction
                        add=int(instAddress,16)
                        instruct[t[0]]=hexa(add)  #to generte 8-bit hexadecimal address of the instruction
                        add+=4
                        instAddress=hexa(add)
                        address.append(instruct[t[0]])
                        # print(t[0],instruct[t[0]])
                        if(temp[0]=='jr' or temp[0]=='lb' or temp[0]=='sb' or temp[0]=='lw' or temp[0]=='syscall' or temp[0]=='beqz' or temp[0]=='sw' or temp[0]=='move'):
                            machine[t[0]]=temp[1]
                            if(proc==1):
                                procedure[procName]=instruct[t[0]] #storing the address of procedure
                                procName=''
                                proc=0
                            break

                        if(proc==1): #confirming the storage
                            procedure[procName]=instruct[t[0]]
                            procName=''
                            proc=0

                        if(temp[1]=='000000'):  #checking for R- Type instruction
                            l=[]
                            l.append(temp[1])
                            l.append(temp[2])
                            rinst[t[0]]=l

                        elif(temp[-1]=='jump'): #checking for jump instruction
                            Jinst[t[0]]=temp[1]
                        
                        elif(temp[-1]=='branch'): #checking if the instruction branches
                            branch[t[0]]=temp[1]

                        else: #checking for I-type instructions
                            Iinst[t[0]]=temp[1]
                        
                        break
                
                inst.seek(0)
                if(instTrue==False):  #if the instruction is psuedo then it breaks the instruction into basic and stores their addresses

                    for row in pinst: #parsing through psuedo instructions file
                        temp=row.split()
                        if(temp[0]==t[0]):
                            for i in range(1,len(temp)):
                                for a in inst:
                                    m=a.split()
                                    if(m[0]==temp[i]):
                                        add=int(instAddress,16)
                                        instruct[t[0]]=hexa(add)
                                        add+=4
                                        instAddress=hexa(add)
                                        address.append(instruct[t[0]])
                                        if(proc==1):
                                            procedure[procName]=instruct[t[0]]
                                            procName=''
                                            proc=0
                                        if(m[1]=='000000'):
                                            l=[]
                                            l.append(m[1])
                                            l.append(m[2])
                                            rinst[t[0]]=l
                                        elif(m[-1]=='jump'):
                                            Jinst[t[0]]=m[1]
                                        elif(m[-1]=='branch'):
                                            branch[t[0]]=m[1]
                                        else:
                                            Iinst[t[0]]=m[1]
                                        break                                  
                            break
                pinst.seek(0) #returning the file pointers back to the starting point
                inst.seek(0)

pinst.seek(0)
inst.seek(0)
fp.seek(0)