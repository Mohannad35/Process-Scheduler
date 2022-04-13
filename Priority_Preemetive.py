# Inputs:
# 		** Type of scheduler (not required for this code)
# 		-- no of Processes
# 		-- required information about each process according to the scheduler type:
# 		-- priority numbers

# Output:
# 		-- Time line showing the order and time taken by each process (Gantt Chart)
# 		-- Average waiting time.

from operator import attrgetter
class process:
    def __init__(self, name, burstTime, arrivalTime, priority):
        self.name = name
        self.burstTime = burstTime
        self.arrivalTime = arrivalTime
        self.priority = priority

def get_nameList(objList):
    outputList = []
    for obj in objList:
        outputList.append(obj.name)
    return outputList

def get_priorityList(objList):
    outputList = []
    for obj in objList:
        outputList.append(obj.priority)
    return outputList

def get_arrivalTime(objList):
    outputList = []
    for obj in objList:
        outputList.append(obj.arrivalTime)
    return outputList

def get_burstTime(objList):
    outputList = []
    for obj in objList:
        outputList.append(obj.burstTime)
    return outputList

def get_minIndices(inputlist):
    # get the minimum value in the list
    min_value = min(inputlist)
    # return the index of minimum value
    min_index = []
    for i in range(0, len(inputlist)):
        if min_value == inputlist[i]:
            min_index.append(i)
    return min_index

def get_average(inputlist):
    return sum(inputlist)/len(inputlist)

def gantt_priorityPreemptive(objList):
    gantt = []
    waitingTime = []
    # print("Processes:")
    # for obj in objList:
    #     print(obj.name, obj.burstTime, obj.arrivalTime, obj.priority)
    
    # the first list for drawing gantt and the seceond for calc waiting time
    sortedByArrive = sorted(processList, key = lambda x : x.arrivalTime)
    sortedByArrive2 = sorted(processList, key = lambda x : x.arrivalTime)
    priorityList = get_priorityList(sortedByArrive)
    arrivalList = get_arrivalTime(sortedByArrive)
    burstList = get_burstTime(sortedByArrive)
    nameList = get_nameList(sortedByArrive)
    Time = sum(burstList)
    print("Total Time =",Time)
    # print("Processes(SA):")
    # for obj in sortedByArrive:
    #     print(obj.name, obj.burstTime, obj.arrivalTime, obj.priority)
    for o in sortedByArrive2:
        waitingTime.append(0)
    for tick in range(Time):
        arrSoFar = []
        for o in sortedByArrive:
            if o.arrivalTime <= tick:
                arrSoFar.append(o)
                waitingTime[sortedByArrive2.index(o)] = waitingTime[sortedByArrive2.index(o)] + 1
        tempO = min(arrSoFar, key=attrgetter('priority'))
        gantt.append(tempO.name)
        tempO.burstTime = tempO.burstTime - 1
        if waitingTime[sortedByArrive2.index(tempO)] != 0:
            waitingTime[sortedByArrive2.index(tempO)] = waitingTime[sortedByArrive2.index(tempO)] - 1
        if tempO.burstTime == 0:
            del sortedByArrive[sortedByArrive.index(tempO)]
    
    print("Gantt chart:",*gantt)
    print("Process name:",*nameList)
    print("Waiting time:",*waitingTime)
    print("Average Waiting Time =", round((get_average(waitingTime)), 3))

# inputs (from GUI to list of objects):
processList = []
processList.append(process('P2', 4, 1, 3))
processList.append(process('P1', 6, 0, 2))
processList.append(process('P4', 2, 3, 1))
processList.append(process('P6', 3, 3, 2))
processList.append(process('P3', 5, 1, 1))
processList.append(process('P5', 1, 3, 4))

gantt_priorityPreemptive(processList)
# output (from gantt list to GUI figure?):
