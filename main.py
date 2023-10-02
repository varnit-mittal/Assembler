import pandas as pd
import addressStore
import machine

address=addressStore.address
code=machine.code

machine.machineCode()

addressStore.storeAddress()

df=pd.DataFrame(columns=['Address','Machine Code'])

# print(code)
# print(address)

df['Address']=address
df['Machine Code']=code

df.to_excel('MachineCodeGenerated.xlsx',index=False)
df.to_csv('MachineText.txt',index=False)