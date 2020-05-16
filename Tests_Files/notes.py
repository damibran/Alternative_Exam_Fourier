def asd(x,a):
    b=[]
    for i in a:
        b.append(i)
    l=0
    r=len(b)-1
    while r-l>1:
        i=l+(r-l)//2
        if b[i]>x:
            r=i
        else:
            l=i
    if x-b[l] < b[r]-x:
        return(b[l])
    return(b[r])

s1 = [32.7, 34.65, 36.71, 38.89, 41.2, 43.65, 46.25, 49, 51.91, 55, 58.27, 61.74]
s2 = ["C","Cd","D","Dd","E","F","Fd","G","Gd","A","Ad","B"]

noty = {}
for i in range(1,8):
    if i:
        for j in range(0,12):
            noty[s1[j]]= str(i)+s2[j]
            s1[j]=s1[j]*2
print(noty[asd(1330,noty)])
