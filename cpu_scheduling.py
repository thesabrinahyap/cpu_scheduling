import string
from tabulate import tabulate
import pandas as pd
import plotly.figure_factory as ff
class Process:
    __letters = string.ascii_uppercase
    index = -1
    def __init__(self, arrivalTime, burstTime, priority):
        Process.index += 1
        self.processId  = self.__letters[Process.index] 
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.priority = priority
        self.remainingTime = burstTime
    
    def getProcessId(self):
        return self.processId
    def getArrivalTime(self):
        return self.arrivalTime
    def getBurstTime(self):
        return self.burstTime
    def getPriority(self):
        return self.priority
    def getRemainingTime(self):
        return self.remainingTime
    def setRemainingTime (self, remainingTime):
        self.remainingTime =  remainingTime

class Gantt:
    def __init__(self, processId, arrivalTime, burstTime, startTime, endTime):
        self.processId = processId
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.startTime = startTime
        self.endTime = endTime
        
    def getProcessId(self):
        return self.processId
    def getArrivalTime(self):
        return self.arrivalTime
    def getBurstTime(self):
        return self.burstTime
    def getStartTime(self):
        return self.startTime
    def getEndTime(self):
        return self.endTime
    def setEndTime (self, newEndTime):
        self.endTime = newEndTime
    
class CpuScheduler:
    __ganttChart = []
    __readyQueue = []
    __sortedProcess = []
    def __init__(self, processes):
        self.sortProcessByArrivalTime(processes)
    
    def firstComeFirstServe(self):
        counter = 0
        processLock = 0  #Locks process until it is done
        while(len(self.__sortedProcess) != 0 or len(self.__readyQueue) != 0):
            if(len(self.__sortedProcess) != 0 and self.__sortedProcess[0].getArrivalTime() <= counter): #Stores processes to the ready queue
                self.__readyQueue.append(self.__sortedProcess[0])
                self.__sortedProcess.pop(0)
            if(counter >= processLock and len(self.__readyQueue) != 0):
                process = self.__readyQueue[0]
                processLock = process.getBurstTime() + counter
                self.__ganttChart.append(Gantt(process.getProcessId(),process.getArrivalTime(), process.getBurstTime(), counter, processLock))
                self.__readyQueue.pop(0)
            counter+=1
    
    def shortestJobFirst(self):
        counter = 0
        processLock = 0  #Locks process until it is done
        while(len(self.__sortedProcess) != 0 or len(self.__readyQueue) != 0):
            if(len(self.__sortedProcess) != 0 and self.__sortedProcess[0].getArrivalTime() <= counter): #Stores processes to the ready queue
                self.__readyQueue.append(self.__sortedProcess[0])
                self.__sortedProcess.pop(0)
            if(counter >= processLock and len(self.__readyQueue) != 0):
                self.__readyQueue = self.sortProcessByBurstTime(self.__readyQueue)      #Sorts readyqueue by burst time
                process = self.__readyQueue[0]
                processLock = process.getBurstTime() + counter
                self.__ganttChart.append(Gantt(process.getProcessId(),process.getArrivalTime(), process.getBurstTime(), counter, processLock))
                self.__readyQueue.pop(0)
            counter+=1
    
    def priorityNonPreemptive(self):
        counter = 0
        processLock = 0  #Locks process until it is done
        while(len(self.__sortedProcess) != 0 or len(self.__readyQueue) != 0):
            if(len(self.__sortedProcess) != 0 and self.__sortedProcess[0].getArrivalTime() <= counter): #Stores processes to the ready queue
                self.__readyQueue.append(self.__sortedProcess[0])
                self.__sortedProcess.pop(0)
            if(counter >= processLock and len(self.__readyQueue) != 0):
                self.__readyQueue = self.sortProcessByPriority(self.__readyQueue)      #Sorts readyqueue by priority
                process = self.__readyQueue[0]
                processLock = process.getBurstTime() + counter
                self.__ganttChart.append(Gantt(process.getProcessId(),process.getArrivalTime(), process.getBurstTime(), counter, processLock))
                self.__readyQueue.pop(0)
            counter+=1
    
    def priorityPreemptive(self):
        counter = 0
        process = None
        while(self.__sortedProcess != None or len(self.__readyQueue) != 0):
            if(len(self.__sortedProcess) != 0 and self.__sortedProcess[0].getArrivalTime() <= counter): #Stores processes to the ready queue
                if(len(self.__readyQueue) != 0):    #Preempts process if another process arrived and there is a process in the ready queue
                    self.__readyQueue.append(self.__readyQueue[0])
                    self.__readyQueue.pop(0)
                self.__readyQueue.append(self.__sortedProcess[0])
                self.__sortedProcess.pop(0)
                self.__readyQueue = self.sortProcessByPriority(self.__readyQueue)      #Sorts readyqueue by priority
                process = self.__readyQueue[0]
                self.__ganttChart.append(Gantt(process.getProcessId(),process.getArrivalTime(), process.getBurstTime(), counter, 0))
            if(len(self.__readyQueue) != 0 ):
                if(process.getRemainingTime() > 0):
                    process.setRemainingTime(process.getRemainingTime() - 1)
                    if (process.getRemainingTime() <= 0):
                        index = next((i for i, item in enumerate(self.__ganttChart) if item.getProcessId() == process.getProcessId()), -1)
                        self.__ganttChart[index].setEndTime(counter + 1)
                        self.__readyQueue.pop(0)
                        if(len(self.__readyQueue) != 0):
                            process = self.__readyQueue[0]
            if(len(self.__readyQueue) == 0 and len(self.__sortedProcess) == 0):
                self.__sortedProcess = None
            counter+=1
            self.__displayCurrentProcess(counter)

            
    
    def displayGanttChart(self):
        col_names = ["Process", "Arrival Time", "Burst Time", "Start Time", "End Time", "Turn Arround Time", "Waiting Time"]
        totalBurstTime = 0
        totalTurnAroundTime = 0
        totalWaitingTime = 0
        processes = []
        ganttChartParse = []
        for x in self.__ganttChart:
            processId = x.getProcessId()
            arrivalTime = x.getArrivalTime()
            burstTime = x.getBurstTime()
            startTime = x.getStartTime()
            endTime = x.getEndTime()
            turnArroundTime = endTime - arrivalTime
            waitingTime = turnArroundTime - burstTime
            totalBurstTime += burstTime
            totalTurnAroundTime += turnArroundTime
            totalWaitingTime += waitingTime
            processes.append((str(processId),str(arrivalTime), str(burstTime), str(startTime),str(endTime),str(turnArroundTime), str(waitingTime))) 
            ganttChartParse.append(dict(stack=1, Start=startTime, Finish=endTime, Task=processId))
        print(tabulate(processes, headers=col_names, tablefmt="fancy_grid"))
        print("Average Turn Around Time: %.2f" % (totalTurnAroundTime / len(self.__ganttChart)))
        print("Average Waiting Time: %.1f" % (totalWaitingTime / len(self.__ganttChart)))
        df = pd.DataFrame(ganttChartParse)
        fig = ff.create_gantt(df, index_col = 'Task',  bar_width = 0.4, show_colorbar=True)
        fig.update_layout(xaxis_type='linear', autosize=False, width=800, height=400,)
        fig.show()
    
    def sortProcessByArrivalTime(self, processes):
        self.__sortedProcess = sorted(processes, key=lambda process: process.getArrivalTime())
    
    def sortProcessByBurstTime(self, processes):
        return sorted(processes, key=lambda process: process.getBurstTime())

    def sortProcessByPriority(self, processes):
        return sorted(processes, key=lambda process: process.getPriority())
    
    def __displayCurrentProcess(self,counter):
        try:
            print(self.__readyQueue)
            print(self.__readyQueue[0].getProcessId())
            print(self.__readyQueue[0].getRemainingTime())
            print(counter)
        except:
            ...
    

class Menu:
    processes = []
    print("[1] First Come First Serve\n[2] Shortest Job First\n[3] Priority Non Preemptive\n[4] Priority Preemptive")
    algorithm = int(input())
    numberOfProcess = int(input("Number of Processes: "))
    priority = None
    for x in range(numberOfProcess):
        print("Process " + str(x + 1))
        arrivalTime = int(input("Arrival Time: "))
        burstTime = int(input("CPU Burst Time: "))
        if(algorithm == 3 or algorithm == 4):
            priority = int(input("Priority: "))
        processes.append(Process(arrivalTime, burstTime, priority))
    
    
    cpuScheduler = CpuScheduler(processes)
    match algorithm:
        case 1:
            cpuScheduler.firstComeFirstServe()
        case 2:
            cpuScheduler.shortestJobFirst()
        case 3:
            cpuScheduler.priorityNonPreemptive()
        case 4:
            cpuScheduler.priorityPreemptive()
    cpuScheduler.displayGanttChart()


def main():
     Menu()

if __name__ == "__main__":
    main()
    
