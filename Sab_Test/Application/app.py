from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for
from CPU_Processes import Process
from FirstComeFirstServe import FirstComeFirstServe
from ShortestJobFirst import ShortestJobFirst
from PriorityNonPreemptive import PriorityNonPreemptive
from PriorityPreemptive import PriorityPreemptive
from RoundRobin import RoundRobin
from ShortestRemainingJobFirst import ShortestRemainingJobFirst
from MultiLevelQueue import MultiLevelQueue
from MultiLevelFeedbackQueue import MultiLevelFeedbackQueue

# from views import views

# app = Flask(__name__)
# app.register_blueprint(views, url_prefix="/views")


# if __name__ == "__main__":
#     app.run(debug=True)  # port is optional

app = Flask(__name__)

# if __name__ == "__main__":
#     app.run(debug=True)  # port is optional


@app.route("/")
def userInput():
    return render_template("userInput.html")


# @app.route("/userInput")
# def userInput():
#     return render_template("userInput.html")


@app.route("/sendInput", methods=["POST"])
def handle_user_input():
    # try:
    data = request.get_json()

    # Process the data as needed
    main_algorithm = data.get("main_algorithm")
    arrival_time = data.get("arrival_time")
    burst_time = data.get("burst_time")
    priority = data.get("priority") or None
    quantum_time = data.get("quantum_time") or None
    mlfq_qt = data.get("mlfq_qt") or []
    mlfq_algorithm = data.get("mlfq_algorithm") or None
    mlq_algorithms = data.get("mlq_algorithms") or []
    level = data.get("level") or None

    print(priority)

    AT = [int(x) for x in arrival_time.split()]
    BT = [int(x) for x in burst_time.split()]
    P = [int(x) for x in priority.split()] if priority else None
    L = [int(x) for x in level.split()] if level else None

    # Construct the processes_list
    processes_list = [
        [
            f"P{i + 1}",
            AT[i] if i < len(AT) else 0,
            BT[i] if i < len(BT) else 0
        ]
        for i in range(len(BT))
    ]

    if P:
        for i in range(len(processes_list)):
            processes_list[i].append(P[i]);
    if L:
        for i in range(len(processes_list)):
            processes_list[i].append(L[i]);


    print(processes_list)

    if main_algorithm == "FirstComeFirstServe":
        pInfo = Process("FirstComeFirstServe")
        pInfo.processes_list = processes_list
        pInfo.multi_check = pInfo.prio_check = False
        pInfo.trimProcessList()
        print("FirstComeFirstServe:")
        FirstComeFirstServe(pInfo)
        return jsonify(
            data=[pInfo.timestamps, pInfo.orderOfProcesses, pInfo.processes_list]
        )
    elif main_algorithm == "ShortestJobFirst":
        pInfo2 = Process("ShortestJobFirst")
        pInfo2.processes_list = processes_list
        pInfo2.multi_check = pInfo2.prio_check = False
        pInfo2.trimProcessList()
        print("\n\nShortestJobFirst:")
        ShortestJobFirst(pInfo2)
        return jsonify(
            data=[pInfo2.timestamps, pInfo2.orderOfProcesses, pInfo2.processes_list]
        )
    elif main_algorithm == "PriorityNonPreemptive":
        pInfo3 = Process("PriorityNonPreemptive")
        pInfo3.processes_list = processes_list
        pInfo3.multi_check = False
        pInfo3.trimProcessList()
        print("\n\nPriority (Non-Preemptive):")
        PriorityNonPreemptive(pInfo3)
        return jsonify(
            data=[pInfo3.timestamps, pInfo3.orderOfProcesses, pInfo3.processes_list]
        )
    elif main_algorithm == "PriorityPreemptive":
        pInfo4 = Process("PriorityPreemptive")
        pInfo4.processes_list = processes_list
        pInfo4.multi_check = False
        pInfo4.trimProcessList()
        print("\n\nPriority (Preemptive):")
        PriorityPreemptive(pInfo4)
        return jsonify(
            data=[pInfo4.timestamps, pInfo4.orderOfProcesses, pInfo4.processes_list]
        )
    elif main_algorithm == "RoundRobin":
        pInfo5 = Process("Round-Robin")
        pInfo5.processes_list = processes_list
        pInfo5.QT = int(quantum_time)
        pInfo5.multi_check = pInfo5.prio_check = False
        pInfo5.trimProcessList()
        print(f"\n\nRound Robin (Quantum Time: {pInfo5.QT}):")
        RoundRobin(pInfo5)
        return jsonify(
            data=[pInfo5.timestamps, pInfo5.orderOfProcesses, pInfo5.processes_list]
        )
    elif main_algorithm == "ShortestRemainingJobFirst":
        pInfo6 = Process("ShortestRemainingJobFirst")
        pInfo6.processes_list = processes_list
        pInfo6.multi_check = pInfo6.prio_check = False
        pInfo6.trimProcessList()
        print("\n\nShortestRemainingJobFirst:")
        ShortestRemainingJobFirst(pInfo6)
        return jsonify(
            data=[pInfo6.timestamps, pInfo6.orderOfProcesses, pInfo6.processes_list]
        )
    elif main_algorithm == "MultiLevelQueue":
        pInfo7 = Process("MultiLevelQueue", *(mlq_algorithms))
        # pInfo7 = Process("PriorityNonPreemptive", "ShortestRemainingJobFirst")
        pInfo7.processes_list = processes_list
        pInfo7.trimProcessList()
        print(f"\n\nMLQ (Algorithms: {pInfo7.algorithms}):")
        MultiLevelQueue(pInfo7)
        return jsonify(
            data=[pInfo7.timestamps, pInfo7.orderOfProcesses, pInfo7.processes_list]
        )
    elif main_algorithm == "MultiLevelFeedbackQueue":
        if mlfq_algorithm == "MultiLevelQueue":
            pInfo8 = Process("MultiLevelFeedbackQueue", *mlq_algorithms)
        else:
            pInfo8 = Process("MultiLevelFeedbackQueue", mlfq_algorithm)
        pInfo8.processes_list = processes_list
        pInfo8.QT = int(quantum_time) if quantum_time else None
        pInfo8.mlfq_qt = mlfq_qt
        pInfo8.mlfq_levels = len(mlfq_qt) + 1
        # print(pInfo8.processes_list)
        pInfo8.trimProcessList()
        print("\n\nMLFQ:")
        MultiLevelFeedbackQueue(pInfo8)
        return jsonify(
            data=[
                pInfo8.timestamps,
                pInfo8.orderOfProcesses,
                pInfo8.processes_list,
                pInfo8.mlfq_timestamps,
                pInfo8.mlfq_orderOfProcesses,
            ]
        )


if __name__ == "__main__":
    app.run()
