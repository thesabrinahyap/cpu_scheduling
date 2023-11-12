from CPU_Processes import Process
from FirstComeFirstServe import FirstComeFirstServe
from ShortestJobFirst import ShortestJobFirst
from PriorityNonPreemptive import PriorityNonPreemptive
from PriorityPreemptive import PriorityPreemptive
from ShortestRemainingJobFirst import ShortestRemainingJobFirst

def MultiLevelQueue(pInfo):
    while pInfo.plist or pInfo.queue:
        if pInfo.multi_feedback_check and (pInfo.plist and not pInfo.queue):
            return
        if pInfo.plist and not pInfo.multi_feedback_check:
            if not pInfo.queue and pInfo.plist[0][1] > pInfo.time:
                pInfo.time = pInfo.plist[0][1]
                pInfo.timestamps.append(pInfo.time)
                pInfo.orderOfProcesses.append('idle')
            while True:
                if pInfo.plist and pInfo.plist[0][1] <= pInfo.time:
                    pInfo.queue.append(pInfo.plist[0])
                    pInfo.plist.pop(0)
                else:
                    break
        if pInfo.prio_check:
            pInfo.min_process = min(pInfo.queue, key=lambda x: (x[4], x[3], x[2], x[1], x[0]))
            colML = 4
        else:
            pInfo.min_process = min(pInfo.queue, key=lambda x: (x[3], x[2], x[1], x[0]))
            colML = 3
        algo = pInfo.algorithms[pInfo.min_process[colML]]
        if algo == "FirstComeFirstServe":
            FirstComeFirstServe(pInfo)
        elif algo == "ShortestJobFirst":
            ShortestJobFirst(pInfo)
        elif algo == "PriorityNonPreemptive":
            PriorityNonPreemptive(pInfo)
        elif algo == "PriorityPreemptive":
            PriorityPreemptive(pInfo)
        elif algo == "ShortestRemainingJobFirst":
            ShortestRemainingJobFirst(pInfo)
        else:
            print("Invalid algorithm.")
    if not pInfo.multi_feedback_check:
        pInfo.displayGanttChart()
        pInfo.calculateTable()
        pInfo.displayTable()
        pInfo.displayEfficiency()

if __name__ == "__main__":
    # SET THE ALGORITHMS HERE. FIRST ALGORITHM CORRESPONDS TO LEVEL 1, SECOND ALGORITHM TO LEVEL 2, AND SO ON
    pInfo = Process("MultiLevelQueue", *("PriorityNonPreemptive", "ShortestRemainingJobFirst", "FirstComeFirstServe"))
    # pInfo = Process("MultiLevelQueue", *("PriorityNonPreemptive", "ShortestRemainingJobFirst"))
    # Customization
    # pInfo.processes_list = [
    #     ["P1", 10, 5, 3],
    #     ["P2", 1, 4, 1],
    #     ["P3", 12, 12, 6],
    #     ["P4", 3, 3, 7],
    #     ["P5", 2, 4, 2]
    # ]
    pInfo.trimProcessList()

    MultiLevelQueue(pInfo)



