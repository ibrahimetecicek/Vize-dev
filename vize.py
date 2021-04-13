# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 22:13:52 2021
 
@author: İbrahim Mete Çiçek
"""

# Çinli Postacı Algoritması.
# Algoritmanın uygulanmasında aşağıdaki adımlar izlenir:
# 1. Girdiyi graf olarak tanımlama
# 2. Dijkstra’nın algoritmasını işlev olarak uygulama
# 3. Bir işleve sahip tek derece tepe noktalarını Bulma
# 4. Özyinelemeli tüm tek tepe eşleşmelerini oluşturma
# 5. Dijkstra’nın işlevinin yardımıyla optimal eşleştirmeyi seçme
# 6. Tüm kenarların toplamını elde etmek için uygulama işlevi
# 7. Tüm kod bloklarını bir araya getirmek
# 8. Çinli postacı mesafesini graf girdisi çıktısı olarak verme

#girdi olarak yönsüz, pozitif ağırlıklı bir graf alıyoruz.
#matrix olarak saklayacağız.


#import pandas as pd  
#graph=pd.read_csv(r"C:\Users\metec\Desktop\vize\input.txt") #graph matrixisini okutma
# graph = graph1.to_numpy()

graph =                [[3, 0, 2, 0, 0, 4], 
                        [0, 0, 0, 1, 3, 6], 
                        [1, 0, 0, 0, 0, 2], 
                        [0, 0, 0, 0, 1, 1], 
                        [1, 1, 0, 0, 0, 4], 
                        [5, 6, 0, 0, 5, 0], 
                         
                    ]; 


def kenar_topla(graph):   #kenar sayı toplamı
    w_sum = 0
    l = len(graph)
    for i in range(l):
        for j in range(i,l):
            w_sum += graph[i][j]
    return w_sum
            
#eşlemeler arasındaki olası en kısa yolu hesaplamak için Dijkstra’nın Algoritmasını kullanacağız.

def dijktra_en_kısa_yol(graph, source, dest):  #dijktra algoritması fonksiyonunu tanımlama
    shortest = [0 for i in range(len(graph))]
    selected = [source]
    l = len(graph)
    inf = 10000000
    min_sel = inf
    for i in range(l):
        if(i==source):
            shortest[source] = 0 
        else:
            if(graph[source][i]==0):
                shortest[i] = inf
            else:
                shortest[i] = graph[source][i]
                if(shortest[i] < min_sel):
                    min_sel = shortest[i]
                    ind = i
                
    if(source==dest):
        return 0
    #dijktra_en_kısa_yol algoritması çalışıyor
    selected.append(ind) 
    while(ind!=dest):
        #print('ind',ind)
        for i in range(l):
            if i not in selected:
                if(graph[ind][i]!=0):
                    #mesafenin güncellenmesi gerekip gerekmediğinin kontrolü
                    if((graph[ind][i] + min_sel) < shortest[i]):
                        shortest[i] = graph[ind][i] + min_sel
        temp_min = 1000000
        #print('seçilen:',en kısa yol)
        
        for j in range(l):
            if j not in selected:
                if(shortest[j] < temp_min):
                    temp_min = shortest[j]
                    ind = j
        min_sel = temp_min
        selected.append(ind)
    
    return shortest[dest]
                            
#graftaki tek dereceli köşeler
#graflardaki tek köşe noktalarının sayısı 
#her zaman HandShaking Teoremine göre eşit olacaktır.

def tekli(graph):
    degrees = [0 for i in range(len(graph))]
    for i in range(len(graph)):
        for j in range(len(graph)):
                if(graph[i][j]!=0):
                    degrees[i]+=1
                
    #print(köşeler)
    odds = [i for i in range(len(degrees)) if degrees[i]%2!=0]
    #print('odds are:',odds)
    return odds


#bize tüm unique çiftleri verebilecek bir fonksiyon tanımlıyoruz
def ikiliOlusturma(odds):
    pairs = []
    for i in range(len(odds)-1): 
        pairs.append([])
        for j in range(i+1,len(odds)):
            pairs[i].append([odds[i],odds[j]])
        
    #print('pairs are:',pairs)
    #print('\n')
    return pairs

#recursion ancak sonunda bir kombinasyon elde ettiğimizde duracaktır.
#ancak, kombinasyonun son çifti sütunların herhangi birinden olabileceğinden,
#bir kombinasyon listesinin uzunluğu "Tepe Sayısı / 2" ye eşitse, bu koşulu eşleştirerek kontrol ederiz.
#son derlenmiş fonksiyonumuz
def CinliPostaci(graph):
    odds = tekli(graph)
    if(len(odds)==0):
        return kenar_topla(graph)
    pairs = ikiliOlusturma(odds)
    l = (len(pairs)+1)//2
    
    pairings_sum = []
    
    def ikili(pairs, done = [], final = []):
        
        if(pairs[0][0][0] not in done):
            done.append(pairs[0][0][0])
            
            for i in pairs[0]:
                f = final[:]
                val = done[:]
                if(i[1] not in val):
                    f.append(i)
                else:
                    continue
                
                if(len(f)==l):
                    pairings_sum.append(f)
                    return 
                else:
                    val.append(i[1])
                    ikili(pairs[1:],val, f)
                    
        else:
            ikili(pairs[1:], done, final)
            
    ikili(pairs)
    minimum_toplam = []
    
    for i in pairings_sum:
        s = 0
        for j in range(len(i)):
            s += dijktra_en_kısa_yol(graph, i[j][0], i[j][1])
        minimum_toplam.append(s)
    
    added_dis = min(minimum_toplam)
    cinli_uzaklık = added_dis + kenar_topla(graph)
    return cinli_uzaklık   
#eklenen en kısa ekstra kenarları hesaba katarak Çinli postacı için minimum mesafeyi hesaplıyoruz.   

print('Çinli Postacı Mesafesi ',CinliPostaci(graph))