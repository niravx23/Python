from concurrent.futures import process
from itertools import count
from lib2to3.pgen2.token import EQUAL
import queue
import random as rand ;
import operator
from xmlrpc.client import boolean ;

p_arrival   = [] 
p_execution = []
gantt_chart = []


#------------------------------------WRITING IN FILE---------------------------------------------------------
def process_table(n) :

    f0  = open("time.txt","w");
    f0.write(" PROCESS   ARRIVAL_TIME   EXECUTION TIME   " +"\n")
    f0.write(" -------  --------------  --------------   " +"\n")
    for i in range(n) : 
        t1   = rand.randint(1,10) ;
        t2 =  rand.randint(0,10) ; 
        t3 = rand.randint(1,10) ; 

        p_arrival.append(t2) ;
        p_execution.append(t1);
        

        f0.write(" {0:^7d} {1:^15d} {2:^15d}  ".format(i+1,t2,t1) + "\n"); 


#--------------------PROCESS TABLE DATA------------------------------------------------------------------------
#main 
table= [] 

no_processes = 10
process_table(no_processes) ;

for i in range(no_processes) : 
    table.append([i ,p_arrival[i],p_execution[i]])

table1 = sorted(table, key=operator.itemgetter(1))


TAT = [ ]  #TURNAROUND TIME 
WAT = [ ]  #WAITING TIME 
RPT = [ ]  #resultPONSE TIME 
TOT = [ ]  #TROUGH PUT 
#------------------------------------FIRST COME FIRST SERVE-----------------------------------------------------
def FCFS()  :
    t1= 0 ;
    sum1=0 ; 
    sum2=0 ;
    sum3=0 ;
    sum4=0 ;

    f0  = open("time.txt","a");
    f0.write("FCFS"+"\n");
    for i in range(no_processes) : 
        RPT.append(t1);  
        t1 += table[i][2] ;

        for k in range(0,table[i][2]) :
            f0.write(str(table[i][0]))

        TOT.append(t1-1);
        TAT.append(t1-table[i][1])
        WAT.append(t1-table[i][1]-table[i][2]) 

    for i in range(no_processes) : 
        sum1+= TAT[i] ;
        sum2+= WAT[i] ;
        sum3+= RPT[i] ; 
        sum4+= TOT[i] ;

    
    f0.write("\n"); 
    f0.write("AVERAGE TURNAROUND TIME : " + str(float(sum1/no_processes))+"\n") ;
    f0.write("AVERAGE WAITING    TIME : " + str(float(sum2/no_processes))+"\n") ;
    f0.write("AVERAGE RESPONSE   TIME : " + str(float(sum3/no_processes))+"\n") ;
    f0.write("THROUGH PUT             : " + str(float(sum4/no_processes))+"\n") ;


    TAT.clear();
    WAT.clear();
    RPT.clear();
    TOT.clear(); 

# print(table1)

#------------------------------------------SHORTEST JOB FIRST-----------------------------------------------------

def SJF(table1)  :
    n  = no_processes 

    wt = [0]*n
    tat = [0]*n
    rt = [0]*n
    ct = [0]*n

     #sorting arrival time
    table1 = sorted(table1, key=operator.itemgetter(1))

    # table.append(process);table.append(arrivaltime);table.append(bursttime);table.append(ct);table.append(wt);table.append(tat)
   

  
    # calculate completion time
    value = 0
    compleition_time = []#3
    tat= [ ] #5
    wait= [ ] #4
    compleition_time.append([0, table[0][1] + table[0][2]])
    tat.append([0, compleition_time[0]-table[0][1]])
    wait.append([0, tat[0]- table[0][2]])

    for i in range(1, n):
        temp = compleition_time[i-1][1]
        minimum = table1[i][2]

        for j in range(i, n): # to find min burst time
            if temp >= table1[j][1] and minimum >= table1[j][2]:
                minimum = table1[j][2]
                value = j

        compleition_time[value][1] = temp + table1[2][value]

        tat[value] [5]= compleition_time[value][1] - table1[value][1]# turnaround time
         
        wait[value][1] = tat[value][1] - table1[value][2] # waiting time

        
        

        for i in range(0, n):
            
            rt[i] = wait[i][1] # wt = rt as non preemptive
           
    print("\nProcess\t\tArrival Time\t\tBurst Time\t\tTurn Around Time\t\tWaiting Time\t\tResponse Time")
    for i in range(n):
        print("{}\t\t{:5d}\t\t{:12d}\t\t{:15d}".format(tat[i],wt[i],rt[i]))

    print("\nGantt Chart: ",end = "")
    for i in range(n):
        if i==0:
            for j in range(compleition_time[i]):
                print(table[i][0],end="")
        else:
            for j in range(compleition_time[i]-compleition_time[i-1]):
                print(table[i][0],end="")
                
    # average turnaround time
    total = 0
    for i in range(n):
        total = total + tat[i][1]
    avg = total/n
    print("\nAVERAGE TURNAROUND TIME:",avg)
    # average waiting time
    total = 0
    for i in range(n):
        total = total + wt[i][1]
    avg = total/n
    print("AVERAGE WAITING TIME:",avg)
    # average response time
    total = 0
    for i in range(n):
        total = total + rt[i][1]
    avg = total/n
    print("AVERAGE RESPONSE TIME:",avg)
    # overall throughput
    print("OVERALL THROUGHPUT:",max(ct)/n)



#--------------------------------ROUND ROBIN----------------------------------------------------------- 




def ROUND_ROBIN(table) :
    table1  =  table

    f0  = open("time.txt","a");
    f0.write("ROUND ROBIN"+"\n") ;
    n = no_processes


    process_completed =  0  # no of processes completed
    tq = int(input('Enter Time quantum  : '))
    time = 0 #total time
    ready =  [ ] # ready queue
    completed = [] # completed processes id 
    completion_time = [] # processid +  completion time

        # x is count for ready queue
    x = 0
    response = 0 
    while process_completed != no_processes  :
        z =0  # time condition for total time 

        for i in range(len(table)) :
            if table[i][1] <= time and table[i][0] not in ready and table[i][0] not in completed : # if arrival<total and not in ready queue and not in completed list
                ready.append(i)
                response += time 

        if len(ready)==1:   # to select next process in ready queue
            x= 0 
        elif len(ready)==0 : 
            time +=1 
            continue
        else : 
            x = (x + 1 )%len(ready)

        if table[ready[x]][2]<=tq:     # subtracting the tq from execution
            for i in range(table[ready[x]][2]):
                f0.write(str(table[ready[x]][0]))
            time += table[ready[x]][2] 
            table[ready[x]][2]=0 
            completion_time.append([table[ready[x]][0], time])
            z=1 
            completed.append(table[ready[x]][0]) 
            ready.remove(ready[x]) 
            process_completed +=1 ; 
        else  : 

            for i in range(tq):      # if execution time left >  time quantum
                f0.write(str(table[ready[x]][0]))

            table[ready[x]][2] -= tq 

        if(len(completed)==no_processes) :
            break

   
        if z==1 :
            pass 
        else :
            time  += tq 

    table1 = sorted(table1, key = operator.itemgetter(0)) #sorted both table with process id
    completion_time = sorted(completion_time, key = operator.itemgetter(0))


    tat = [ ]
    wat = [ ]

    for i in range(no_processes) :
        tat.append(completion_time[i][1]-table1[i][1])
        wat.append(tat[i]-table[i][2])

    turnaround  = 0  
    throughput =  completion_time[no_processes-1][1] 
    waiting =    0 

    for i in range(no_processes) : 
        turnaround += tat[i]
        waiting  += wat[i] 
    
    f0.write("\n" + "Average TurnAround Time  :" + str((float)(turnaround/no_processes))) 
    f0.write("\n" + "Average waiting Time  :" + str((float)(waiting/no_processes))) 
    f0.write("\n" + "Average throughput Time  :" + str((float)(throughput/no_processes))) 
    f0.write("\n" + "Average response Time  :" + str((float)(response/no_processes))) 




    # if(len(completed)==4) :
    #     break


    


#------------------------shortest remaining Time first---------------------------------

def SRTF(table) : 

    f0  = open("time.txt","a");
    f0.write("SRTF"+"\n") ;
    sum1=0 # WAT
    sum2=0 # tat

    WAT=[0]*no_processes
    tat=[0]*no_processes
    
    rt  = [0]*no_processes ; 
    for i in range(no_processes) : # dup of exection times
        rt[i] = table[i][2] 

    count=0 # when count =  process ready queue empty
    short=0
    time=0
    min=100000
    checker=False

    result=0
    list=[]

    while(count!=no_processes):
         for i in range(no_processes):
             if table[i][1]<=time and rt[i]<min and rt[i]>0:
                min=rt[i] # minimum execution time left
                short=i # process id of selecteed process
                checker=True



               

         if checker==False:
            time+=1
            f0.write("*") ; # if no process is available for execution
            continue


           
 
         rt[short]-=1 

         f0.write(str(table[short][0])) # for gannt chart
         if table[short][0] not in list: # ready queue

             list.append(table[short][0])
             result+= time 
             


                
         min=rt[short]

         if(min==0): # execution time over
                min=100000 

         if rt[short]==0:
                count+=1 # process with id = short completed 
                checker=False 
                final_t=time+1 # completion time
                WAT[short]=final_t-table[short][1]-table[short][2] # completion  - arrival  -  burst

                if WAT[short]<0:  # validate
                    WAT[short]=0
         time+=1

    f0.write("\nOVERALL THROUGHPUT: " + str(time/no_processes)+"\n")
    f0.write(" AVERAGE RESPONSE   : " + str(result/no_processes)+"\n") 

    for i in range(no_processes):
            tat[i]= table[i][2]+WAT[i]

    for i in range(no_processes):
                sum1=sum1+WAT[i]
                sum2=sum2+tat[i]

    f0.write(" AVERAGE WAITING TIME  : "  +str(sum1/no_processes)+"\n") 
    f0.write(" AVERAGE TURN AROUND TIME  :" + str(sum2/no_processes)+"\n") 






#----MAin CODE-----------
while True : 
    print("Enter option  : ")
    print("1 - FCFS ") 
    print("2 - SJF ")
    print("3 -  RR") 
    print("4 - SRTF " )
    print("5 - exit ")  
    choice = int(input("Choose : "))

    if choice ==1  :
        FCFS() 
    elif choice ==2  :
        SJF(table) ;
    elif choice ==3 : 
        ROUND_ROBIN(table)  ;
    elif choice == 4 : 
          SRTF(table) ;
    else :
        break ;

