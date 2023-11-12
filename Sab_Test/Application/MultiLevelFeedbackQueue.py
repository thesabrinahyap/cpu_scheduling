from CPU_Processes import Process
from FirstComeFirstServe import FirstComeFirstServe
from ShortestJobFirst import ShortestJobFirst
from PriorityNonPreemptive import PriorityNonPreemptive
from PriorityPreemptive import PriorityPreemptive
from RoundRobin import RoundRobin
from ShortestRemainingJobFirst import ShortestRemainingJobFirst
from MultiLevelQueue import MultiLevelQueue

def MultiLevelFeedbackQueue(pInfo):
    # initializing queues, timestamps, and orderOfProcesses 
    pInfo.mlfq_queues = [[] for _ in range(pInfo.mlfq_levels)]
    pInfo.mlfq_timestamps = [[0] for _ in range(pInfo.mlfq_levels)]
    pInfo.mlfq_orderOfProcesses = [[] for _ in range(pInfo.mlfq_levels)]
    queues = False

    # print(pInfo.processes_list)

    while pInfo.plist or queues:
        if pInfo.plist:
            if not queues and pInfo.plist[0][1] > pInfo.time:
                pInfo.time = pInfo.plist[0][1]
                pInfo.timestamps.append(pInfo.time)
                pInfo.orderOfProcesses.append('idle')
                for i in range(pInfo.mlfq_levels):
                    pInfo.mlfq_timestamps[i].append(pInfo.time)
                    pInfo.mlfq_orderOfProcesses[i].append('idle')
            while True:
                if pInfo.plist and pInfo.plist[0][1] <= pInfo.time:
                    pInfo.mlfq_queues[0].append(pInfo.plist[0])
                    pInfo.plist.pop(0)
                else:
                    break


        for i in range(pInfo.mlfq_levels - 1):
            if (pInfo.plist and pInfo.plist[0][1] <= pInfo.time) or not pInfo.mlfq_queues:
                break
            while pInfo.mlfq_queues[i]:
                pInfo.orderOfProcesses.append(pInfo.mlfq_queues[i][0][0])
                for j in range(pInfo.mlfq_levels):
                    if j == i:
                        pInfo.mlfq_orderOfProcesses[j].append(pInfo.mlfq_queues[i][0][0])
                    else:
                        pInfo.mlfq_orderOfProcesses[j].append(" ")
                if pInfo.mlfq_queues[i][0][2] > pInfo.mlfq_qt[i]:
                    pInfo.mlfq_queues[i][0][2] -= pInfo.mlfq_qt[i]
                    pInfo.time += pInfo.mlfq_qt[i]
                    pInfo.mlfq_queues[i + 1].append(pInfo.mlfq_queues[i][0])
                else:
                    pInfo.time += pInfo.mlfq_queues[i][0][2]
                    integer_part = ''.join(char for char in pInfo.mlfq_queues[i][0][0] if char.isdigit())
                    pInfo.processes_list[int(integer_part) - 1].append(pInfo.time)
                pInfo.mlfq_queues[i].pop(0)
                pInfo.timestamps.append(pInfo.time)
                for j in range(pInfo.mlfq_levels):
                    pInfo.mlfq_timestamps[j].append(pInfo.time)
                # since this is the second level, you need to always check for newly arrived processes since you cannot
                # directly put all existing processes in the second gantt chart if there are newly arrived processes.
                if pInfo.plist and pInfo.plist[0][1] <= pInfo.time:
                    break
        if (pInfo.plist and pInfo.plist[0][1] <= pInfo.time) or not pInfo.mlfq_queues:
            continue

        # print()
        # for i in pInfo.processes_list:
        #     print(i)

        if pInfo.mlfq_queues[pInfo.mlfq_levels - 1]:
            pInfo.queue = pInfo.mlfq_queues[pInfo.mlfq_levels - 1]
            if len(pInfo.algorithms) > 1:
                pInfo.multi_check = True
                MultiLevelQueue(pInfo)
            elif pInfo.algorithms[1] == "FirstComeFirstServe":
                FirstComeFirstServe(pInfo)
            elif pInfo.algorithms[1] == "ShortestJobFirst":
                ShortestJobFirst(pInfo)
            elif pInfo.algorithms[1] == "PriorityNonPreemptive":
                PriorityNonPreemptive(pInfo)
            elif pInfo.algorithms[1] == "PriorityPreemptive":
                PriorityPreemptive(pInfo)
            elif pInfo.algorithms[1] == "RoundRobin":
                RoundRobin(pInfo)
            elif pInfo.algorithms[1] == "ShortestRemainingJobFirst":
                ShortestRemainingJobFirst(pInfo)
            else:
                print("Invalid algorithm.")
        queues = False if all(not queue for queue in pInfo.mlfq_queues) else True
        # print(f"This is plist: {pInfo.plist}. This is queues: {pInfo.mlfq_queues}")

    pInfo.displayGanttChart()
    pInfo.calculateTable()
    pInfo.displayTable()
    pInfo.displayEfficiency()
    pInfo.displayMLFQGanttCharts()

if __name__ == "__main__":
    pInfo = Process("MultiLevelFeedbackQueue", *("PriorityPreemptive", "ShortestRemainingJobFirst", "FirstComeFirstServe"))
    # pInfo = Process("MultiLevelFeedbackQueue", "RoundRobin")
    pInfo.QT = 2
    # SET THE TIME SPLICE OF LEVELS 1 AND 2. TO SET THE ALGORITHM/S OF LEVEL 3, GO TO CPU_Processes.py AND CHANGE
    # algo3 ON LINE 27
    pInfo.mlfq_qt = [2, 1]
    pInfo.mlfq_levels = 3
    # Customization
    # pInfo.processes_list = [
    #     ["P1", 10, 5, 3],
    #     ["P2", 1, 4, 1],
    #     ["P3", 12, 12, 6],
    #     ["P4", 3, 3, 7],
    #     ["P5", 2, 4, 2]
    # ]
    pInfo.trimProcessList()

    MultiLevelFeedbackQueue(pInfo)



