import random
import math
import numpy as np
import decimal
import time
from joblib import Parallel,delayed                                


Voc = decimal.Decimal(57.1)
Vmp = decimal.Decimal(43.9)
Isc = decimal.Decimal(3.41)
Imp = decimal.Decimal(2.96)
Vt =  decimal.Decimal(2.7416036483)

k1 = decimal.Decimal(1)
k2 = decimal.Decimal(1)
k3 = decimal.Decimal(0.001)

#ranges for the initial population

Iph_min,Iph_max = 0.96 * float(Isc) , 1.14 * float(Isc) 
Io1_min,Io1_max = pow(10,-40) , pow(10,-20)
Rs_min,Rs_max   = 1.0 , 1.5
n1_min,n1_max   = 0.9 , 1.0
Rp_min,Rp_max   = 100,2000

x = 1
y = 1

def error_oc(Iph,Io1,n1,Rs,Rp): #erro do componente de circuito aberto

   return k1 * modelo(0,Voc,Iph,Io1,n1,Rs,Rp)**2


def error_sc(Iph,Io1,n1,Rs,Rp): #erro no componente de curto circuito

   return k2 * (modelo(Isc,decimal.Decimal(0),Iph,Io1,n1,Rs,Rp) - Isc)**2


def error_mp(Iph,Io1,n1,Rs,Rp): #erro no componente de máxima potência

   return k3 * (modelo(Imp,Vmp,Iph,Io1,n1,Rs,Rp) - Imp*Vmp)**2


def modelo(I,V,Iph,Io1,n1,Rs,Rp) :
    current = decimal.Decimal(Iph - Io1*(decimal.Decimal(math.e)**((V+Rs*I)/(n1*Vt))-1) - ((V + Rs*I)/Rp) )
    return current

def fitness(Iph,Io1,n1,Rs,Rp):
    f = k1 * modelo(0,Voc,Iph,Io1,n1,Rs,Rp)**2 + k2 * (modelo(Isc,decimal.Decimal(0),Iph,Io1,n1,Rs,Rp) - Isc)**2 + k3 * (modelo(Imp,Vmp,Iph,Io1,n1,Rs,Rp) - Imp*Vmp)**2
    return f

    



solutions = []
t1_begin = time.perf_counter()
for s in range(1000): #número de indivíduos na população
   solutions.append ((  decimal.Decimal( random.uniform(x*Iph_min,y*Iph_max ) ),
                        decimal.Decimal( random.uniform(x*Io1_min,y*Io1_max ) ),
                        decimal.Decimal( random.uniform(x*n1_min,y*n1_max   ) ),
                        decimal.Decimal( random.uniform(x*Rs_min,y*Rs_max   ) ),
                        decimal.Decimal( random.uniform(x*Rp_min,y*Rp_max   ) ) ) )
   
t1_end = time.perf_counter()

for i in range(10000):
   ranked_solutions = []
   t2_begin = time.perf_counter()
   for s in solutions:
      ranked_solutions.append( (fitness(s[0],s[1],s[2],s[3],s[4]),s) )
   t2_end = time.perf_counter()

   ranked_solutions.sort()
   #ranked_solutions.reverse()
   print(f"=== Gen {i} best solutions ===")

   print("Fitness : ",ranked_solutions[0][0])
   print("Iph : ", ranked_solutions[0][1][0])
   print("Io1 : ", ranked_solutions[0][1][1])
   print("n1  : ", ranked_solutions[0][1][2])
   print("Rs  : ", ranked_solutions[0][1][3])
   print("Rp  : ", ranked_solutions[0][1][4])
   
   print("\n")
   print("Open circuit component error : ",error_oc(ranked_solutions[0][1][0],ranked_solutions[0][1][1],ranked_solutions[0][1][2],ranked_solutions[0][1][3],ranked_solutions[0][1][4]))
   print("Short circuit component error : ",error_sc(ranked_solutions[0][1][0],ranked_solutions[0][1][1],ranked_solutions[0][1][2],ranked_solutions[0][1][3],ranked_solutions[0][1][4]))
   print("Maximum power component error : ",error_mp(ranked_solutions[0][1][0],ranked_solutions[0][1][1],ranked_solutions[0][1][2],ranked_solutions[0][1][3],ranked_solutions[0][1][4]))

   
   


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
   t3_begin = time.perf_counter()
   for j in range(1000):

      parent_1 = random.choice(best_solutions)
      parent_2 = random.choice(best_solutions)
      
      #print(parent_1)

      #CROSS-OVER
      alpha_e1 = decimal.Decimal(0.5)
      alpha_e2 = decimal.Decimal(0.5)
      alpha_e3 = decimal.Decimal(0.5)
      alpha_e4 = decimal.Decimal(0.5)
      alpha_e5 = decimal.Decimal(0.5)

      #first parameter
      e1_ParentMin = min(parent_1[1][0],parent_2[1][0])
      e1_ParentMax = max(parent_1[1][0],parent_2[1][0])

      e1_RangeMin =  float(e1_ParentMin - alpha_e1 * (e1_ParentMax - e1_ParentMin))
      e1_RangeMax =  float(e1_ParentMax + alpha_e1 * (e1_ParentMax - e1_ParentMin))

      e1 = decimal.Decimal(abs(random.uniform(e1_RangeMin,e1_RangeMax)) )


      #second parameter
      e2_ParentMin = min(parent_1[1][1],parent_2[1][1])
      e2_ParentMax = max(parent_1[1][1],parent_2[1][1])

      e2_RangeMin =  float(e2_ParentMin - alpha_e2 * (e2_ParentMax - e2_ParentMin))
      e2_RangeMax =  float(e2_ParentMax + alpha_e2 * (e2_ParentMax - e2_ParentMin))

      e2 = decimal.Decimal(abs(random.uniform(e2_RangeMin,e2_RangeMax)) )

      

      #third parameter
      e3_ParentMin = min(parent_1[1][2],parent_2[1][2])
      e3_ParentMax = max(parent_1[1][2],parent_2[1][2])

      e3_RangeMin =  float(e3_ParentMin - alpha_e3 * (e3_ParentMax - e3_ParentMin))
      e3_RangeMax =  float(e3_ParentMax + alpha_e3 * (e3_ParentMax - e3_ParentMin))

      e3 = decimal.Decimal(abs(random.uniform(e3_RangeMin,e3_RangeMax)))

      #fourth parameter
      e4_ParentMin = min(parent_1[1][3],parent_2[1][3])
      e4_ParentMax = max(parent_1[1][3],parent_2[1][3])

      e4_RangeMin =  float(e4_ParentMin - alpha_e4 * (e4_ParentMax - e4_ParentMin))
      e4_RangeMax =  float(e4_ParentMax + alpha_e4 * (e4_ParentMax - e4_ParentMin))

      e4 = decimal.Decimal(abs(random.uniform(e4_RangeMin,e4_RangeMax)))

      #fifth parameter
      e5_ParentMin = min(parent_1[1][4],parent_2[1][4])
      e5_ParentMax = max(parent_1[1][4],parent_2[1][4])

      e5_RangeMin =  float(e5_ParentMin - alpha_e5 * (e5_ParentMax - e5_ParentMin))
      e5_RangeMax =  float(e5_ParentMax + alpha_e5 * (e5_ParentMax - e5_ParentMin))

      e5 = decimal.Decimal(abs(random.uniform(e5_RangeMin,e5_RangeMax)))


      #MUTAÇÃO
       
      #standard deviations for each of the five parameters
      sigma_Iph = (0.005 * Iph_max)/3
      sigma_Io1 = (0.005 * Io1_max)/3
      sigma_n1  = (0.005 * n1_max)/3
      sigma_Rs  = (0.005 * Rs_max)/3
      sigma_Rp  = (0.005 * Rp_max)/3
      
      mutation_rate = 0.5

      mutation_value1 = decimal.Decimal(np.random.normal(0,sigma_Iph)) if random.uniform(0,1) <= mutation_rate else 0
      mutation_value2 = decimal.Decimal(np.random.normal(0,sigma_Io1)) if random.uniform(0,1) <= mutation_rate else 0
      mutation_value3 = decimal.Decimal(np.random.normal(0,sigma_n1))  if random.uniform(0,1) <= mutation_rate else 0
      mutation_value4 = decimal.Decimal(np.random.normal(0,sigma_Rs))  if random.uniform(0,1) <= mutation_rate else 0
      mutation_value5 = decimal.Decimal(np.random.normal(0,sigma_Rp))  if random.uniform(0,1) <= mutation_rate else 0

      e1 = abs(e1 + mutation_value1)
      e2 = abs(e2 + mutation_value2)
      e3_2 = abs(e3 + mutation_value3)
      e4 = abs(e4 + mutation_value4)
      e5 = abs(e5 + mutation_value5)
      
      

      newGen.append((e1,e2,e3_2,e4,e5))
   t3_end = time.perf_counter()
   
   solutions = newGen

   # print(t1_end - t1_begin)
   print(t2_end - t2_begin)
   # print(t3_end - t3_begin)



test_current = decimal.Decimal(random.uniform(5,50) )
test_voltage = decimal.Decimal(random.uniform(5,50) )

print("\n")
print("test current input : ",test_current)
print("model output : ",modelo(test_current,test_voltage,ranked_solutions[0][1][0],ranked_solutions[0][1][1],ranked_solutions[0][1][2],ranked_solutions[0][1][3],ranked_solutions[0][1][4]))
#Parallel(n_jobs=3)(delayed(funcao)() for _ in range(1))
  
