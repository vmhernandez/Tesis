def bubleSort(data):
    exchange = True
    num = len(data)-1
    while num > 0 and exchange:
       exchange = False
       for i in range(num):
           if data[i]>data[i+1]:
               exchange = True
               temp = data[i]
               data[i] = data[i+1]
               data[i+1] = temp
       numPasada = num-1

unaLista=[20,30,40,90,50,60,70,80,100,110,1000,800,123,9242,1283]
bubleSort(unaLista)
print(unaLista)
print("Media:",unaLista[7])