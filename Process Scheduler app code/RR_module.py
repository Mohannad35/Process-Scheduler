# Round Robin module
# Inputs:
# 		-- (NumberofProcesses):
#                               no of Processes
# 		-- (processList):
#                               will be filled with the required values (Pid, burstTime, arrivalTime)

# Output:
# 		-- (global outputRoundRobin):
#                               Time line showing the order and time taken by each process (Gantt Chart) 
# 		-- (global avgWaitingTime_RoundRobin):
#                               Average waiting time

from queue import Empty, PriorityQueue
import queue

global NumberofProcesses
NumberofProcesses = 6
global avgWaitingTime_RoundRobin
avgWaitingTime_RoundRobin = 0.0
global time
time = 0.0
global q
q = 2.0
global totalBurstTime_RR
totalBurstTime_RR = 0.0

class process:
    def __init__(self, Pid, burstTime = 0, arrivalTime = 0):
        self.Pid = Pid
        self.burstTime = float(burstTime)
        self.arrivalTime = float(arrivalTime)
        self.remainingTime = float(burstTime)
        self.leaveTime = 0.0

    def __lt__(self, other):
        return self.arrivalTime < other.arrivalTime

    def waitingTime(self):
        return self.leaveTime - self.arrivalTime - self.burstTime

inputQueue_RR = PriorityQueue()
readyQ = []
outputQueue_RR = queue.Queue()
totalWaitingTime_RR = 0.0

def Handler_ganttRoundRobinCalc():
    global q
    global totalBurstTime_RR
    totalBurstTime_RR = 0.0
    totalWaitingTime_RR = 0.0
    global avgWaitingTime_RoundRobin
    global time
    time = 0.0
    procs = []
    global NumberofProcesses
    number_of_processes = NumberofProcesses
    #clear last outputs
    while not outputQueue_RR.empty():
        try:
            outputQueue_RR.get(False)
        except Empty:
            continue
        outputQueue_RR.task_done()
    # output
    while (1):
        while not (inputQueue_RR.empty()):
            procs.append(inputQueue_RR.get())
            if (time >= procs[-1].arrivalTime):
                readyQ.append(procs[-1])
                procs.pop(-1)
        if procs:
            for i in range(len(procs)):
                inputQueue_RR.put(procs[-(i+1)])
        procs = []
        if readyQ:
            #slice 
            slice = q if readyQ[0].remainingTime >= q else readyQ[0].remainingTime
            slicePid = readyQ[0].Pid
            sliceArrivalTime = readyQ[0].arrivalTime
            time += slice
            outputQueue_RR.put({'pid': slicePid, 'slice': slice, 'arrival': sliceArrivalTime})
            #process to the end of the ready_queue or terminate
            readyQ[0].remainingTime -= slice
            if (readyQ[0].remainingTime == 0):
                readyQ[0].leaveTime = time
                print (time)
                totalWaitingTime_RR += readyQ[0].waitingTime()
                readyQ.pop(0)
            else:
                temp = readyQ[0]
                readyQ.append(temp)
                readyQ.pop(0)
        else:
            if not (inputQueue_RR.empty()):
                fp = inputQueue_RR.get()
                time = fp.arrivalTime
                inputQueue_RR.put(fp)
            else: break
    totalBurstTime_RR = time
    #print
    for n in list(outputQueue_RR.queue):
        print(n)
    global avgWaitingTime_RoundRobin
    avgWaitingTime_RoundRobin = round(totalWaitingTime_RR / int(number_of_processes), 3)
    print(avgWaitingTime_RoundRobin)

# def simulate_4_handler():
#     #inputs
#     while not (inputQueue_RR.empty()):
#         k = inputQueue_RR.get()
#     for i in range(int(NumberofProcesses)):
#         arrival = inputQQ[i].arrivalTime
#         burst = inputQQ[i].burstTime
#         p = process(i + 1, burst, arrival)
#         inputQueue_RR.put(p)
#     #output
#     Handler_ganttRoundRobinCalc()

# inputQQ = []
# inputQQ.append(process(1, 6, 0.0))
# inputQQ.append(process(2, 4, 0.1))
# inputQQ.append(process(3, 5, 2.2))
# inputQQ.append(process(4, 2, 3.5))
# inputQQ.append(process(5, 1, 5.5))
# inputQQ.append(process(6, 3, 6.5))
# simulate_4_handler()
