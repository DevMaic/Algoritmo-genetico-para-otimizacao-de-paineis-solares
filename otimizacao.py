import random
import math
import decimal                                

Voc = decimal.Decimal(57.1)
Vmp = decimal.Decimal(43.9)
Isc = decimal.Decimal(3.41)
Imp = decimal.Decimal(2.96)
Vt =  decimal.Decimal(2.7416036483)

def modelo(I,V,Iph,Io1,n1,Rs,Rp) :
    current = decimal.Decimal(Iph - Io1*(decimal.Decimal(math.e)**((V+Rs*I)/(n1*Vt))-1) - ((V + Rs*I)/Rp) )
    return current

def fitness(Iph,Io1,n1,Rs,Rp):
    f = modelo(0,Voc,Iph,Io1,n1,Rs,Rp)**2 + (modelo(Isc,decimal.Decimal(0),Iph,Io1,n1,Rs,Rp) - Isc)**2 + (modelo(Imp,Vmp,Iph,Io1,n1,Rs,Rp) - Imp*Vmp)**2
    return f

solutions = []
for s in range(500): #número de indivíduos na população
  solutions.append (( decimal.Decimal( random.uniform(0,1000) ),
                      decimal.Decimal( random.uniform(0,1000) ),
                      decimal.Decimal( random.uniform(0,1000) ),
                      decimal.Decimal( random.uniform(0,1000) ),
                      decimal.Decimal( random.uniform(0,1000) ) ) )

for i in range(10000):
   ranked_solutions = []
   for s in solutions:
      ranked_solutions.append( (fitness(s[0],s[1],s[2],s[3],s[4]),s) )
    
   ranked_solutions.sort()
   #ranked_solutions.reverse()
   print(f"=== Gen {i} best solutions ===")
   print(ranked_solutions[0])

   if ranked_solutions [0][0] < 0.001:
      break

   best_solutions = ranked_solutions[:100]

   elements = []
   for s in best_solutions:
      elements.append(s[1][0])
      elements.append(s[1][1])
      elements.append(s[1][2])
      elements.append(s[1][3])
      elements.append(s[1][4])

   newGen = []
   for _ in range(1000):
      e1 = random.choice(elements) * decimal.Decimal(random.uniform(0.95,1.05) )
      e2 = random.choice(elements) * decimal.Decimal(random.uniform(0.95,1.05) )
      e3 = random.choice(elements) * decimal.Decimal(random.uniform(0.95,1.05) )
      e4 = random.choice(elements) * decimal.Decimal(random.uniform(0.95,1.05) )
      e5 = random.choice(elements) * decimal.Decimal(random.uniform(0.95,1.05) )

      newGen.append((e1,e2,e3,e4,e5))
     
   solutions = newGen

#print(modelo(ranked_solutions[0][1][0],ranked_solutions[0][1][1],ranked_solutions[0][1][2]))
