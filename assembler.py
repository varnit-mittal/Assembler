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

df = pd.DataFrame()

machine={}


inst=open('./instructions.txt','r')
pinst=open('./psuedo_instructions.txt','r')
def storeAddress():
    instAddress='0x00400000'
    control=0
    proc=0
    total=0
    procName=""
    for line in fp:
        x=line.strip()
        k=0
        found=0
        for i in range(len(x)):
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
        if(x==".text"):
            control=1
            continue

        if(x != ".data" and x !=".text" and x!='\n' and x!=''):
            if(control==0):
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
                t=x.split()
                # print(t)
                if(t[0][-1]==":"):
                    proc=1
                    procName=x[:-1]
                    continue

                instTrue=False
                for row in inst: 
                    temp=row.split()
                    # print(temp[0],t[0])
                    if(temp[0]==t[0]):
                        instTrue=True
                        add=int(instAddress,16)
                        instruct[t[0]]=hexa(add)
                        # print(t[0],instruct[t[0]])
                        add+=4
                        instAddress=hexa(add)
                        address.append(instruct[t[0]])
                        if(temp[0]=='jr' or temp[0]=='lb' or temp[0]=='sb' or temp[0]=='lw' or temp[0]=='syscall' or temp[0]=='beqz' or temp[0]=='sw' or temp[0]=='move'):
                            machine[t[0]]=temp[1]
                            if(proc==1):
                                # print(procName, t[0])
                                procedure[procName]=instruct[t[0]]
                                procName=''
                                proc=0
                            break

                        if(proc==1):
                            # print(procName, t[0])
                            procedure[procName]=instruct[t[0]]
                            procName=''
                            proc=0

                        if(temp[1]=='000000'):
                            l=[]
                            l.append(temp[1])
                            l.append(temp[2])
                            rinst[t[0]]=l

                        elif(temp[-1]=='jump'):
                            Jinst[t[0]]=temp[1]
                        
                        elif(temp[-1]=='branch'):
                            branch[t[0]]=temp[1]

                        else:
                            Iinst[t[0]]=temp[1]
                        
                        break
                
                inst.seek(0)
                if(instTrue==False):
                    for row in pinst:
                        temp=row.split()
                        # print(t[0],temp[0])
                        if(temp[0]==t[0]):
                            for i in range(1,len(temp)):
                                for a in inst:
                                    # print(a)
                                    m=a.split()
                                    # print(m)
                                    if(m[0]==temp[i]):
                                        add=int(instAddress,16)
                                        instruct[t[0]]=hexa(add)
                                        # print(m[0],instruct[t[0]])
                                        add+=4
                                        instAddress=hexa(add)
                                        address.append(instruct[t[0]])
                                        if(proc==1):
                                            # print(procName, t[0])
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
                pinst.seek(0)
                inst.seek(0)

pinst.seek(0)
inst.seek(0)
fp.seek(0)
reg=open('./registers.txt','r')
def machineCode():
    ...



storeAddress()
print(procedure)
df['Address']=address
print(df)