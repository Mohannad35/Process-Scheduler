# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import re
from time import time


def quick_sort(s, time_now):
    if len(s) == 1 or len(s) == 0:
        return s
    else:
        pivot = s[0]
        i = 0
        for j in range(len(s) - 1):
            if pivot.burst_time <= 0:
                s[j + 1], s[i + 1] = s[i + 1], s[j + 1]
                i += 1
            elif s[j + 1].arrival_time <= time_now and pivot.arrival_time <= time_now:
                if s[j + 1].burst_time < pivot.burst_time and s[j + 1].burst_time > 0:
                    s[j + 1], s[i + 1] = s[i + 1], s[j + 1]
                    i += 1
                elif s[j + 1].burst_time == pivot.burst_time:
                    if s[j + 1].arrival_time < pivot.arrival_time:
                        s[j + 1], s[i + 1] = s[i + 1], s[j + 1]
                        i += 1
            elif s[j + 1].arrival_time <= time_now or pivot.arrival_time <= time_now:
                if s[j + 1].arrival_time <= time_now:
                    s[j + 1], s[i + 1] = s[i + 1], s[j + 1]
                    i += 1
            else:
                if s[j + 1].arrival_time < pivot.arrival_time:
                    s[j + 1], s[i + 1] = s[i + 1], s[j + 1]
                    i += 1
                elif s[j + 1].arrival_time == pivot.arrival_time:
                    if s[j + 1].burst_time < pivot.burst_time and s[j + 1].burst_time > 0:
                        s[j + 1], s[i + 1] = s[i + 1], s[j + 1]
                        i += 1

        s[0], s[i] = s[i], s[0]
        first_part = quick_sort(s[:i], time_now)
        second_part = quick_sort(s[i + 1:], time_now)
        first_part.append(s[i])
        return first_part + second_part

global time_sjf
time_sjf = 0.0

class Process(object):
    def __init__(self, name, arrival_time = 0, burst_time = 0):
        super(Process, self).__init__()
        self.name = name
        self.arrival_time = float(arrival_time)
        self.burst_time = float(burst_time)
        self.last_time_run = float(arrival_time)
        self.waiting_time = 0


class SJFPreemptive(object):

    def __init__(self, processes, preemptive=False):
        if not isinstance(processes, list):
            raise TypeError
        super(SJFPreemptive, self).__init__()
        self.processes = processes
        self.preemptive = preemptive
        self.time_now = 0
        self.graph = []
        old_processes = list(map(lambda key: key.name, self.processes))
        new_processes = list(set(old_processes))
        if len(old_processes) != len(new_processes):
            raise ValueError

    def get_graph(self):
        global time_sjf
        graph = []
        for line in self.graph:
            if len(graph) <= 0:
                graph.append(line)
            else:
                if graph[-1][0] == line[0]:
                    graph[-1][2] = line[2]
                else:
                    graph.append(line)
        print(graph)
        time_sjf = float(graph[-1][2])
        return graph

    def get_average_waiting_time(self):
        time = list(map(lambda key: key.waiting_time, self.processes))
        # print(time)
        total = sum(time) / len(self.processes) if len(self.processes) > 0 else 0
        # print(total)
        return total

    def sort(self, time_now=0):
        self.processes = quick_sort(self.processes, time_now)
        self.printall()

    def printall(self):
        processes = list(map(lambda key: key.name, self.processes))
        # print(processes)
        return processes

    def get_next_arrival_time(self, num):
        nums = list(sorted(map(lambda k: k.arrival_time, list(
            filter(lambda key: key.arrival_time > num and key.burst_time > 0, self.processes)))))
        if nums:
            return nums[0]
        else:
            return False

    def run(self):
        if self.processes:
            self.sort(self.time_now)
            current_process = self.processes[0]
            if current_process.arrival_time <= self.time_now:
                if current_process.burst_time > 0:
                    if len(self.processes) > 1:
                        if self.preemptive:
                            # current_process.waiting_time += self.time_now - current_process.last_time_run
                            # burst_time = 1
                            # current_process.burst_time -= burst_time
                            # time = self.time_now + burst_time
                            # current_process.last_time_run = time
                            # self.graph.append([current_process.name, self.time_now, time])
                            # self.time_now = time
                            # self.run()
                            next_time = self.get_next_arrival_time(self.time_now)
                            if not next_time:
                                current_process.waiting_time += self.time_now - current_process.last_time_run
                                burst_time = current_process.burst_time
                                current_process.burst_time -= burst_time
                                time = self.time_now + burst_time
                                current_process.last_time_run = time
                                self.graph.append([current_process.name, self.time_now, time])
                                self.time_now = time
                                self.run()
                            elif next_time:
                                current_process.waiting_time += self.time_now - current_process.last_time_run
                                burst_time = next_time - self.time_now if current_process.burst_time + self.time_now > next_time else current_process.burst_time
                                current_process.burst_time -= burst_time
                                time = self.time_now + burst_time
                                current_process.last_time_run = time
                                self.graph.append([current_process.name, self.time_now, time])
                                self.time_now = time
                                self.run()
                        else:
                            current_process.waiting_time += self.time_now - current_process.last_time_run
                            burst_time = current_process.burst_time
                            current_process.burst_time -= burst_time
                            time = self.time_now + burst_time
                            current_process.last_time_run = time
                            self.graph.append([current_process.name, self.time_now, time])
                            self.time_now = time
                            self.run()
                        # if current_process.arrival_time <= self.time_now and self.processes[1].arrival_time <= self.time_now:
                        #     current_process.waiting_time += self.time_now - current_process.last_time_run
                        #     burst_time = current_process.burst_time
                        #     current_process.burst_time -= burst_time
                        #     time = self.time_now + burst_time
                        #     current_process.last_time_run = time
                        #     self.graph.append([current_process.name, self.time_now, time])
                        #     self.time_now = time
                        #     self.run()

                    else:
                        current_process.waiting_time += self.time_now - current_process.last_time_run
                        burst_time = current_process.burst_time
                        current_process.burst_time -= burst_time
                        time = self.time_now + burst_time
                        current_process.last_time_run = time
                        self.graph.append([current_process.name, self.time_now, time])
                        self.time_now = time
                        self.run()
            else:
                next_time = self.get_next_arrival_time(self.time_now)
                if next_time:
                    # self.graph.append(["Null", self.time_now, next_time])
                    self.time_now = next_time
                    self.run()



# if __name__ == '__main__':
#     p1 = Process("P1", 4.3, 1.5)
#     p2 = Process("P2", 4.4, 2.25)
#     p3 = Process("P3", 4.2, 1.75)
#     p4 = Process("P4", 4.1, 4.1)
#     p5 = Process("P5", 14.1, 4.1)
#     scheduler = SJFPreemptive([p1, p2, p3, p4,p5], True)
#     scheduler.run()
#     scheduler.get_graph()
#     scheduler.get_average_waiting_time()
