import pandas as pd
import addressStore
import machine

address=addressStore.address
code=machine.code

machine.machineCode()

addressStore.storeAddress()

df=pd.DataFrame(columns=['Address','Machine Code'])

df['Address']=address
df['Machine Code']=code

# This is the main calling module which stores the generated machines codes and addresses into seperately created files

df.to_excel('MachineCodeGenerated.xlsx',index=False)
df.to_csv('MachineText.txt',index=False)