from CPU_Processes import Process
from FirstComeFirstServe import FirstComeFirstServe
from ShortestJobFirst import ShortestJobFirst
from PriorityNonPreemptive import PriorityNonPreemptive
from PriorityPreemptive import PriorityPreemptive
from RoundRobin import RoundRobin
from ShortestRemainingJobFirst import ShortestRemainingJobFirst
from MultiLevelQueue import MultiLevelQueue
from MultiLevelFeedbackQueue import MultiLevelFeedbackQueue

if __name__ == "__main__":
    pInfo = Process("FirstComeFirstServe")
    pInfo.multi_check = pInfo.prio_check = False
    pInfo.trimProcessList()
    print("FirstComeFirstServe:")
    FirstComeFirstServe(pInfo)

    pInfo2 = Process("ShortestJobFirst")
    pInfo2.multi_check = pInfo2.prio_check = False
    pInfo2.trimProcessList()
    print("\n\nShortestJobFirst:")
    ShortestJobFirst(pInfo2)

    pInfo3 = Process("Priority-NP")
    pInfo3.multi_check = False
    pInfo3.trimProcessList()
    print("\n\nPriority (Non-Preemptive):")
    PriorityNonPreemptive(pInfo3)

    pInfo4 = Process("Priority-P")
    pInfo4.multi_check = False
    pInfo4.trimProcessList()
    print("\n\nPriority (Preemptive):")
    PriorityPreemptive(pInfo4)

    pInfo5 = Process("Round-Robin")
    pInfo5.QT = 3
    pInfo5.multi_check = pInfo5.prio_check = False
    pInfo5.trimProcessList()
    print(f"\n\nRound Robin (Quantum Time: {pInfo5.QT}):")
    RoundRobin(pInfo5)

    pInfo6 = Process("ShortestRemainingJobFirst")
    pInfo6.multi_check = pInfo6.prio_check = False
    pInfo6.trimProcessList()
    print("\n\nShortestRemainingJobFirst:")
    ShortestRemainingJobFirst(pInfo6)

    pInfo7 = Process("MultiLevelQueue", *("PriorityPreemptive", "ShortestRemainingJobFirst", "FirstComeFirstServe"))
    # pInfo7 = Process("MultiLevelQueue", *("PriorityNonPreemptive", "ShortestRemainingJobFirst"))
    pInfo7.trimProcessList()
    print(f"\n\nMLQ (Algorithms: {pInfo7.algorithms}):")
    MultiLevelQueue(pInfo7)

    pInfo8 = Process("MultiLevelFeedbackQueue", *("PriorityPreemptive", "ShortestRemainingJobFirst", "FirstComeFirstServe"))
    # pInfo8 = Process("MultiLevelFeedbackQueue", "ShortestJobFirst")
    pInfo8.QT = 2
    pInfo8.mlfq_levels = 5
    pInfo8.mlfq_qt = [2, 1, 2, 1]
    pInfo8.trimProcessList()
    print("\n\nMLFQ:")
    MultiLevelFeedbackQueue(pInfo8)
