import addressStore

def hexa(s):
    l=format(int(s,2),'01x')
    return l

def machineHelp(n):
    p=''
    for i in range(0,len(n),4):
        p+=hexa(n[i:i+4])
    return '0x'+p

def signExtend(s):
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
    control=0
    counter=-1
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
            if(control==1):
                t=x.split()
                # print(t)
                if(t[0][-1]==":"):
                    continue
                instTrue=False
                for row in inst: 
                    temp=row.split()
                    if(temp[0]==t[0]):
                        counter+=1
                        instTrue=True
                        if(temp[0]=='jr' or temp[0]=='lb' or temp[0]=='sb' or temp[0]=='lw' or temp[0]=='syscall' or temp[0]=='beqz' or temp[0]=='sw' or temp[0]=='move'):
                            code.append(machine[t[0]])
                            break
                        if(temp[-1]=='jump'):
                            s=procedure[t[1]]
                            l=int(s,16)
                            l=format(l,'032b')
                            l=l[4:-2]
                            s=temp[1]
                            s=s+l
                            code.append(machineHelp(s))
                        
                        elif(temp[1]=='000000'):
                            l=''.join(t[1:])
                            l=l.split(',')
                            s1=temp[1]
                            s2=temp[2]
                            s=''
                            for j in range(1,len(l)):
                                for regi in reg:
                                    t2=regi.split()
                                    if(l[j]==t2[0]):
                                        # print(l[j],t2[1])
                                        s+=format(int(t2[1]),'05b')
                                        break
                                reg.seek(0)
                            
                            reg.seek(0)
                            for regi in reg:
                                t2=regi.split()
                                if(l[0]==t2[0]):
                                    # print(l[1],t2[1])
                                    s+=format(int(t2[1]),'05b')
                                    break
                            reg.seek(0)
                            s=s1+s+s2
                            code.append(machineHelp(s))
                            break

                        elif(temp[-1]=='branch'):
                            l1=int(address[counter],16)
                            # print(address[17])
                            l2=int(procedure[t[-1]],16)
                            # print(procedure[t[-1]],t[-1])
                            l2=int(((l2-l1)/4)) -1
                            l2=format(l2,'016b')
                            s3=signExtend(l2)
                            s1=temp[1]
                            s=''
                            reg.seek(0)
                            for j in range(1,len(t)-1):
                                mp=t[j].split(',')
                                for regi in reg:
                                    t2=regi.split()
                                    if(mp[0]==t2[0]):
                                        s+=format(int(t2[1]),'05b')
                                        break
                                reg.seek(0)
                            s=s1+s+s3
                            code.append(machineHelp(s))
                            break
                        else:
                            l=''.join(t[1:])
                            l=l.split(',')
                            # print(l)
                            s1=Iinst[t[0]]
                            l2=format(int(l[-1]),'016b')
                            # print(l2)
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
                                        if(m[1]=='000000'):
                                            # print(l)
                                            s1=m[1]
                                            s2=m[-1]
                                            s=''
                                            if(t[0]=='bgt'):
                                                for j in range(1,-1,-1):
                                                    for regi in reg:
                                                        t2=regi.split()
                                                        if(l[j]==t2[0]):
                                                            # print(l[j],t2[1])
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
                                            # print(s)
                                            s=s1+s+'00001'+s2
                                            # print(s)
                                            code.append(machineHelp(s))
                                            # print(code[-1])
                                            break

                                        elif(m[-1]=='branch'):
                                            if(t[0]=='bgt'):
                                                code.append('0x14200008')
                                            elif(t[0]=='blt'):
                                                code.append('0x14200006')
                                            break

                                        else:
                                            if(m[0]=='lui'):
                                                code.append('0x3c011001')
                                                break
                                            if(m[0]=='ori'):
                                                s3=format(int(size[l[-1]]),'016b')
                                                s='0011010000100100'+s3
                                                code.append(machineHelp(s))
                                                # print(l[-1],code[-1])
                                                break
                                            if(m[0]=='addiu'):
                                                s1='001001'
                                                s='00000'
                                                for regi in reg:
                                                    t2=regi.split()
                                                    if(l[0]==t2[0]):
                                                        # print(l[1],t2[1])
                                                        s+=format(int(t2[1]),'05b')
                                                        break
                                                reg.seek(0)
                                                b=format(int(l[-1]),'016b')
                                                s=s1+s+b
                                                code.append(machineHelp(s))
                                                # print(code[-1])
                                inst.seek(0)
                    pinst.seek(0)
                                            


addressStore.storeAddress()