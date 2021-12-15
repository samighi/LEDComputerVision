import pandas as pd
import numpy as np

def getValueZfromX(r,x,y):
    z = r * np.cos(np.arcsin(x / r))
    return [x,y,z]

def cleanup(dfData,col):
    s = dfData[col]
    indexes = []

    l = []
    for i,x in dfData[col].items():
        #print(i,x)
        if (len(indexes) > 0 )and (x == x): 
            nextValue = x
            for w in indexes: 
                l.append([w,w-indexes[0]+1,len(indexes),prevValue,nextValue,prevValue+(((nextValue-prevValue)/(len(indexes)+1))*(w-indexes[0]+1))])
            indexes = []
        if x == x: 
            prevValue = x
            nextValue = x
            l.append([i,0,1,prevValue,nextValue,x])
        else: 
            indexes.append(i)
            #print("Appending ",i)

    l = {x[0] : x[-1] for x in l}
    return l 



angles = [0,90,180,270]

#path = "dualorderednew.csv" - original path
path = "dualorderednew.csv"
dfAll = pd.DataFrame()
for angle in angles: 
    for i in range(2):
       filename = path+str(i)+"-"+str(angle)
       df = pd.read_csv(filename)
       df["angle"] = angle
       dfAll = pd.concat([dfAll,df])
        
dfAll.columns = ["x","y","led","strand","angle"]
dfAll['trueLED'] = dfAll['led']+250*dfAll['strand']

dfPos = dfAll.groupby(['trueLED','angle']).sum()[['x','y']].unstack()
dfAll = dfAll.merge(dfPos,how='left',left_on='trueLED',right_on='trueLED')

#l = sorted([k for k, v in dfAll['trueLED'].value_counts().items() if v ==4 ]) ## this is all bulbs in all 4 views 
# change the 4 to 3 or 2 for which views they are in 

l = list(set(dfAll['trueLED'].values)) ## Take all LEDs
#l

dfLED = dfAll.groupby('trueLED').first().reset_index()

for N in [0,90,180,270]:
    dfnew = dfLED[(dfLED[('x', N)] == dfLED[('x', N)] ) ][['trueLED',('x', N),('y',N)]]
    dfnew.columns = ['trueLED','x'+str(N),'y'+str(N)]
    xc,yc='x'+str(N),'y'+str(N)
    print((min(dfnew[xc])+max(dfnew[xc]))/2,(min(dfnew[yc])+max(dfnew[yc]))/2)
    dfnewnew = dfnew[['trueLED',xc,yc]].apply(lambda W: pd.Series([W['trueLED'],W[xc]-(min(dfnew[xc])+max(dfnew[xc]))/2,(W[yc]-(min(dfnew[yc])+max(dfnew[yc]))/2)]),axis=1)

    dfnewnew.columns = ['trueLED',xc,yc]
    dfLED = dfLED.merge(dfnewnew,how='left',right_on='trueLED',left_on='trueLED')
    
for A in [0,90,180,270]:
#for A in [90]:

    values = dfLED[ (dfLED['x'+str(A)] == dfLED['x'+str(A)]) ][['x'+str(A),'y'+str(A),'trueLED']].apply( lambda y: [int(y[0]/5)*5,y[1],y[2]],axis=1)


    d = {}
    for y in sorted(set([y[0] for y in values])):
        xmax = -1
        for y1,x1,led in values:
            if y1 == y: 
             if xmax < abs(x1): 
                xmax=abs(x1)
        d[y] = xmax


    VV = pd.DataFrame.from_dict(d,orient='index')
    #VV[0] = VV[0].rolling(10).mean().fillna(VV[0]) ### changes Mean to Max
    VV[0] = VV[0].rolling(10).max().fillna(VV[0]) 
    d = VV[0].to_dict()
    #print(d)
    
    l = [] 
    for _,(x,y,led) in enumerate(values): 
        r = d[x]
        #r = VV[x]
        u = getValueZfromX(r,y,x)
        u = [led]+u+[A]
        l.append(u)
 
    dfL = pd.DataFrame(l)
    dfL.columns = ['led','x','y','z','angle']
    #dfL.to_csv('x-'+str(A)+'-new.csv')
    dfL.to_csv('x-'+str(A)+'-20211127.csv')
    
    
dfL = pd.DataFrame()
for A in [0,90,180,270]:
    #dfL = pd.read_csv('x-'+str(A)+'-new.csv')
    dfL1 = pd.read_csv('x-'+str(A)+'-20211127.csv')
    dfL1['size'] = .1
    dfL1['angle'] = A
    dfL = pd.concat([dfL,dfL1])


#dfL = pd.concat([df1,df2,df3,df4]) 
dfL['y'] = -dfL['y']
dfL = dfL.astype(int)
# 
# 
# 
# l=[420]
# dfL = dfL[dfL['led'].isin(l)]

l = []
for i in range(0,500):

    d = dfL[dfL['led'] ==i].set_index('angle').to_dict(orient='index')
    #display(d)
    x,y,z = -1000,-1000,-1000
    if len(d) == 0 : continue
        
    y = sum([v['y'] for k,v in d.items()])/len([v['y'] for k,v in d.items()]) # split the Y values 
    
    V12 = 2
    if y < 0: V12 = 1
    #print(y)
    LR = 'Z'
    FB = "Z"
    zForce = 1
    if 0 in d:
        angle = 0 
        if x == -1000: x = d[angle]['x']
        if x > 0 and LR == "Z": LR = "R"
        if x <= 0 and LR == "Z": LR = "L"
        if z ==-1000:z = d[angle]['z']
    if 180 in d: 
        angle = 180
        if x == -1000: x = -d[angle]['x'] 
        if x > 0 and LR == "Z": LR = "R"
        if x <= 0 and LR == "Z": LR = "L"
        if z ==-1000:z = d[angle]['z']
    if 90 in d: 
          angle = 90
          if d[angle]['x'] <0: zForce=-1
          else: zForce = 1
            
    if 270 in d: 
        angle = 270
        if d[angle]['x'] <0: zForce=1
        else: zForce = -1

    z = z * zForce
    if z > 0 and FB == "Z": FB = "B"
    if z <= 0 and FB == "Z": FB = "F"
    l.append([i,LR+FB+str(V12),x,y,z])
dfData = pd.DataFrame(l)
dfData.columns = ['led','RLFB12','x','y','z']

dfData = dfData.replace('ZF1',np.nan).replace('ZF2',np.nan).replace('ZB1',np.nan).replace('ZB2',np.nan)
dfData = dfData[dfData['RLFB12'] == dfData['RLFB12']]

dfCleanup = pd.DataFrame([[x,np.nan,np.nan,np.nan,np.nan] for x in range(0,500) if x not in dfData['led'].values])
dfCleanup.columns = dfData.columns
print(dfCleanup)
dfData = dfData.append(dfCleanup)
# dfData = dfData.append(dfCleanup).set_index('led').sort_index().ffill()

dfData['x'] = dfData['x'].fillna(cleanup(dfData,'x'))
dfData['y'] = dfData['y'].fillna(cleanup(dfData,'y'))
dfData['z'] = dfData['z'].fillna(cleanup(dfData,'z'))
dfData['RLFB12'] = dfData['RLFB12'].ffill()

# dfData[['led','x','y','z','RLFB12']].to_csv('20211127/3dfile.csv',index=False)
# !scp '20211127/3dfile.csv' pi@192.168.86.45:/home/pi/led/LEDComputerVision


dfData[['led','x','y','z','RLFB12']].to_csv('3dfile-local.csv',index=False)