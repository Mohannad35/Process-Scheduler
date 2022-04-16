import Priority

Priority.NumberofProcesses = 6
Priority.preemptive_orNot = 1

# inputs (from GUI to list of objects):
# process (Pid, burstTime, arrivalTime, priority)
Priority.processList.append(Priority.process(1, 6, 0, 3))
Priority.processList.append(Priority.process(2, 4, 1.2, 2))
Priority.processList.append(Priority.process(3, 5, 2.2, 1))
Priority.processList.append(Priority.process(4, 2, 3.5, 1))
Priority.processList.append(Priority.process(5, 1, 3.5, 4))
Priority.processList.append(Priority.process(6, 3, 3.5, 3))

Priority.Handler_ganttPriorityCalc()
print(Priority.avgWaitingTimePriority)
print(Priority.outputPriority)
print(Priority.time)
