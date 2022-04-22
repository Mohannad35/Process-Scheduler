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
