# Inputs:
# 		-- Type of scheduler (priority)
# 		-- no of Processes (NumberofProcesses)
# 		-- required information about each process according to the scheduler type:
# 		    ++ priority numbers

# Output:
# 		-- Time line showing the order and time taken by each process (Gantt Chart)
# 		-- Average waiting time.

global NumberofProcesses
NumberofProcesses = 0
global preemptive_orNot
preemptive_orNot = 0
global processList
processList = []
global outputPriority
outputPriority = []
global time
time = 0.0
global avgWaitingTimePriority
avgWaitingTimePriority = 0.0

class process:
    def __init__(self, pid, burstTime = 0, arrivalTime = 0, priority = 0):
        self.pid = pid
        self.burstTime = float(burstTime)
        self.arrivalTime = float(arrivalTime)
        self.priority = float(priority)
        self.leaveTime = 0.0
    
    def waitingTime(self):
        return self.leaveTime - self.arrivalTime - self.burstTime

def Handler_ganttPriorityCalc():
    global NumberofProcesses
    number_of_processes = NumberofProcesses
    global time
    time = 0.0
    total_waitingTime = 0.0
    global avgWaitingTimePriority
    global outputPriority
    outputPriority.clear()
    # to_nextCheck is a slice of time to recheck the running process for premeetive swap
    min_burst = min(obj.burstTime for obj in processList)
    to_nextCheck = float(min_burst)* 0.1

    # sort by arrival and priority if arrival == arrival
    for i in range(0, int(number_of_processes)):
        for j in range(i+1, int(number_of_processes)):
            if(processList[i].arrivalTime > processList[j].arrivalTime):
                temp = processList[i]
                processList[i] = processList[j]
                processList[j] = temp
            elif (processList[i].arrivalTime == processList[j].arrivalTime and processList[i].priority > processList[j].priority):
                temp = processList[i]
                processList[i] = processList[j]
                processList[j] = temp

    # non preemetive
    if int(preemptive_orNot) == 0:
        for i in range(int(number_of_processes)):
            outputPriority.append({'process' : processList[i].pid, 'arrival': processList[i].arrivalTime, 'length': processList[i].burstTime})
            time = outputPriority[-1]['length'] + (time if processList[i].arrivalTime <= time else processList[i].arrivalTime)
            process_leaveTime = time
            total_waitingTime += process_leaveTime - processList[i].arrivalTime - processList[i].burstTime

    # preemetive
    else:
        current_process = processList[0]
        burst_time = current_process.burstTime
        length = 0
        current_time=0

        while(1):
            # print (burst_time)
            # print(current_time)
            current_time += to_nextCheck
            burst_time -= to_nextCheck
            length += to_nextCheck

            #deleting the process when it is done and new current process
            if(burst_time <= 0):
                length = length + burst_time
                outputPriority.append({'process': current_process.pid, 'arrival' : current_process.arrivalTime, 'length': round(length,3)})
                time = outputPriority[-1]['length'] + (time if current_process.arrivalTime <= time else current_process.arrivalTime)
                process_leaveTime = time
                total_waitingTime += process_leaveTime - current_process.arrivalTime - current_process.burstTime

                processList.pop(0)
                number_of_processes = number_of_processes-1
                if (number_of_processes == 0):break

                #rearrange the priority according to current time and priority and arrival time
                for i in range(0, int(number_of_processes)):
                    for j in range(i + 1, int(number_of_processes)):
                        if (current_time >= processList[j].arrivalTime and processList[i].priority >processList[j].priority):
                            temp = processList[i]
                            processList[i] = processList[j]
                            processList[j] = temp
                current_process = processList[0]
                burst_time = current_process.burstTime
                length = 0
            else:
                # print("hello")
                # switch context and swapping current process if arrival time = current time and of higher priority
                for i in range(1,int(number_of_processes)):
                    if(current_time >= processList[i].arrivalTime and current_process.priority > processList[i].priority):
                        pp = current_time - processList[i].arrivalTime
                        current_time = processList[i].arrivalTime
                        processList[0].burstTime = burst_time + pp #pp is the impurities
                        outputPriority.append({'process': current_process.pid, 'arrival' : current_process.arrivalTime, 'length': round(length - pp,3)})
                        time = outputPriority[-1]['length'] + (time if current_process.arrivalTime <= time else current_process.arrivalTime)
                        process_leaveTime = time
                        total_waitingTime += process_leaveTime - current_process.arrivalTime - current_process.burstTime

                        temp=current_process
                        current_process = processList[i]
                        processList[0]=current_process
                        processList[i]=temp
                        burst_time = current_process.burstTime
                        length = 0

            if (number_of_processes == 0): break

    avgWaitingTimePriority = round(total_waitingTime / NumberofProcesses, 3)
    print('output is',outputPriority)
    print('avg.', avgWaitingTimePriority)

def get_average(inputlist):
    return sum(inputlist)/len(inputlist)

# inputs (from GUI to list of objects):
# process (pid, burstTime, arrivalTime, priority)
# processList.append(process(2, 4, 1.2, 3))
# processList.append(process(1, 6, 0, 2))
# processList.append(process(4, 2, 3.5, 1))
# processList.append(process(6, 3, 3.5, 2))
# processList.append(process(3, 5, 1.2, 1))
# processList.append(process(5, 1, 3.5, 4))

# Handler_ganttPriorityCalc()

# output (from gantt list to GUI figure?):
