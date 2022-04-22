# priority module
# Inputs:
# 		-- (NumberofProcesses):
#                               no of Processes
# 		-- (processList):
#                               will be filled with the required values (Pid, burstTime, arrivalTime, priority)a
#                               the lower the priority number the higher the priority (0 is the highest priority)
#       -- (preemptive_orNot)

# Output:
# 		-- (global outputPriority):
#                               Time line showing the order and time taken by each process (Gantt Chart) 
# 		-- (global avgWaitingTimePriority):
#                               Average waiting time

global NumberofProcesses
NumberofProcesses = 0
global preemptive_orNot
preemptive_orNot = 0
global processList
processList = []
global outputPriority
outputPriority = []
global avgWaitingTimePriority
avgWaitingTimePriority = 0.0
global time
time = 0.0

class process:
    def __init__(self, Pid, burstTime = 0, arrivalTime = 0, priority = 0):
        self.Pid = Pid
        self.burstTime = float(burstTime)
        self.arrivalTime = float(arrivalTime)
        self.priority = float(priority)
        self.leaveTime = 0.0
        self.leftoverTime = 0.0

    def waitingTime(self):
        return self.leaveTime - self.arrivalTime - self.burstTime - self.leftoverTime

def Handler_ganttPriorityCalc():
    global NumberofProcesses
    number_of_processes = NumberofProcesses
    global avgWaitingTimePriority
    global outputPriority
    outputPriority.clear()
    global time
    time = 0.0
    total_waitingTime = 0.0
    # to_nextCheck is a slice of time to recheck the running process for premeetive swap
    min_burst = min(obj.burstTime for obj in processList)
    to_nextCheck = float(min_burst)* 0.1
    # T is time line in non preemptive (current time)
    T = 0.0
    # sort by arrival and priority if arrival == arrival
    for i in range(0, int(number_of_processes)):
        for j in range(i+1, int(number_of_processes)):
            # sort by arrival at first
            if(processList[i].arrivalTime > processList[j].arrivalTime):
                temp = processList[i]
                processList[i] = processList[j]
                processList[j] = temp
            # sort by priority if arrival == arrival
            elif (processList[i].arrivalTime == processList[j].arrivalTime and processList[i].priority > processList[j].priority):
                temp = processList[i]
                processList[i] = processList[j]
                processList[j] = temp
            # sort by priority for all arrived processes
            elif ((processList[j].arrivalTime < T) and (processList[i].priority > processList[j].priority)):
                temp = processList[i]
                processList[i] = processList[j]
                processList[j] = temp
        T += processList[i].burstTime

    # non preemetive
    if int(preemptive_orNot) == 0:
        total_waitingTime = 0.0
        for i in range(int(number_of_processes)):
            outputPriority.append({'process' : processList[i].Pid, 'arrival': processList[i].arrivalTime, 'length': processList[i].burstTime})
            time = outputPriority[-1]['length'] + (time if processList[i].arrivalTime <= time else processList[i].arrivalTime)
            processList[i].leaveTime = time
            total_waitingTime += processList[i].waitingTime()
            print(processList[i].Pid, processList[i].waitingTime())

    # preemetive
    else:
        currentProcess = processList[0]
        burstTime = currentProcess.burstTime
        length = 0
        currentTime=0
        total_waitingTime = 0.0
        while(1):
            currentTime += to_nextCheck
            burstTime -= to_nextCheck
            length += to_nextCheck
            #deleting the process when it is done and new current process
            if(burstTime <= 0):
                length = length + burstTime
                #append the finished process to outputPriority to draw it with gantt
                outputPriority.append({'process': currentProcess.Pid, 'arrival' : currentProcess.arrivalTime, 'length': round(length,3)})
                # check if there's a gap in time line (ex: first process arrived at time 1 not 0) we start from 1 not 0
                time = outputPriority[-1]['length'] + (time if currentProcess.arrivalTime <= time else currentProcess.arrivalTime)
                # calculating finished process waiting time and adding it to total waiting time
                currentProcess.leaveTime = time
                total_waitingTime += currentProcess.waitingTime()
                # delete the finished process
                processList.pop(0)
                number_of_processes = number_of_processes-1
                if (number_of_processes == 0):break
                # rearrange the priority according to current time with priority and arrival time
                for i in range(0, int(number_of_processes)):
                    for j in range(i + 1, int(number_of_processes)):
                        if (currentTime >= processList[j].arrivalTime and processList[i].priority >processList[j].priority):
                            temp = processList[i]
                            processList[i] = processList[j]
                            processList[j] = temp
                currentProcess = processList[0]
                burstTime = currentProcess.burstTime
                length = 0
            # check if there's any process arrived with higher priority so it will be the current process to run on the processor
            # ex: current process 'P1', current time (1.2) and 'P3' arrive at (1.2) with higher priority: then it will be the current process
            else:
                # switch context and swapping current process if arrival time = current time and of higher priority
                for i in range(1,int(number_of_processes)):
                    if(currentTime >= processList[i].arrivalTime and currentProcess.priority > processList[i].priority):
                        # timeImpurities is a very small time slice that may exist between a process and anthor while swapping them
                        # timeImpurities decrease with the factor (0.1) multiplied here:(to_nextCheck = float(min_burst)* 0.1)
                        # ex: current process 'P1', current time (1.2) and 'P3' arrive at (1.15) with higher priority: timeImpurities = 0.05
                        timeImpurities = currentTime - processList[i].arrivalTime
                        # we remove timeImpurities from current time
                        currentTime = processList[i].arrivalTime
                        # saving the burst time done till now so we can calculate the avg waiting time later
                        processList[0].leftoverTime += processList[0].burstTime - burstTime
                        # we update the remaining burst time of the process that is getting swap out of the processor
                        processList[0].burstTime = burstTime + timeImpurities
                        # append the partially finished process (getting swap out of processor) to output list
                        outputPriority.append({'process': currentProcess.Pid, 'arrival' : currentProcess.arrivalTime, 'length': round(length - timeImpurities,3)})
                        # swapping  the current process with the process with highest priority till now
                        temp=currentProcess
                        currentProcess = processList[i]
                        processList[0]=currentProcess
                        processList[i]=temp
                        # update the burst tiem and length
                        burstTime = currentProcess.burstTime
                        length = 0
            if (number_of_processes == 0): break
    avgWaitingTimePriority = round(total_waitingTime / NumberofProcesses, 3)
    print('output is',outputPriority)
    print('avg.', avgWaitingTimePriority)

# inputs (from GUI to list of objects):
# process (Pid, burstTime, arrivalTime, priority)
# processList.append(process(1, 6, 0, 3))
# processList.append(process(2, 4, 1.2, 2))
# processList.append(process(3, 5, 2.2, 1))
# processList.append(process(4, 2, 3.5, 1))
# processList.append(process(5, 1, 3.5, 4))
# processList.append(process(6, 3, 3.5, 3))

# Handler_ganttPriorityCalc()

# output (from gantt list to GUI figure?):
