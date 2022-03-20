# %%
from getch import getch
f = open("trace.t")
context = f.readlines()
f.close()

# %%
import os
import time

# %%
read = False
trace_text = []
for line in context:
    if line == "\n":
        continue
    if line == "End of the error trace.\n":
        read = False
    if read:
        trace_text.append(line[:-1])
    if line == "The following is the error trace for the error:\n":
        read = True

# %%
trace_stage = [[]]
i = 0
error_msg = trace_text[0]
for line in trace_text[1:-1]:
    if line == '----------':
        i += 1
        trace_stage.append([])
        continue
    trace_stage[i].append(line)

trace_stage_processed = []
for stage in trace_stage:
    trace_stage_processed.append([])
    HomeNode_info = {}
    HomeNode_info["sharers"] = []
    Proc_info = [{},{},{}]
    Net_info_P1 = []
    Net_msg_P1 = [""] * 5
    Net_info_P2 = []
    Net_msg_P2 = [""] * 5
    Net_info_P3 = []
    Net_msg_P3 = [""] * 5
    Net_info_H = []
    Net_msg_H = [""] * 5
    count = 0
    action = []
    last_val = "-1"
    msg_processed = ""
    pending_msg = []
    for line in stage:
        if line[0:8] == "HomeNode":
            if line[0:14] == "HomeNode.state":
                HomeNode_info["state"] = line[15:]
            elif line[0:14] == "HomeNode.owner":
                HomeNode_info["owner"] = line[15:]
            elif line[0:16] == "HomeNode.sharers":
                HomeNode_info["sharers"].append(line[20:])
            else:
                HomeNode_info["value"] = line[13:]
        elif line[0:11] == "Procs[Proc_":
            for i in range(3):
                if line[0:19] == "Procs[Proc_" + str(i+1) + "].state":
                    Proc_info[i]["state"] = line[20:]
                elif line[0:17] == "Procs[Proc_" + str(i+1) + "].val":
                    Proc_info[i]["value"] = line[18:]
                elif line[0:23] == "Procs[Proc_" + str(i+1) + "].ack_count":
                    Proc_info[i]["count"] = line[24:]
        elif line[0:8] == "Net[Home":
            if count == 5:
                count = 0
            if count == 0:
                Net_info_H.append([])
            count += 1
            Net_info_H[-1].append(line[line.index(":")+1:])
        elif line[0:10] == "Net[Proc_1":
            if count == 5:
                count = 0
            if count == 0:
                Net_info_P1.append([])
            count += 1
            Net_info_P1[-1].append(line[line.index(":")+1:])
        elif line[0:10] == "Net[Proc_2":
            if count == 5:
                count = 0
            if count == 0:
                Net_info_P2.append([])
            count += 1
            Net_info_P2[-1].append(line[line.index(":")+1:])
        elif line[0:10] == "Net[Proc_3":
            if count == 5:
                count = 0
            if count == 0:
                Net_info_P3.append([])
            count += 1
            Net_info_P3[-1].append(line[line.index(":")+1:])
        elif line[0:16] == "LastWrite:Value_":
            last_val = line[16:]
        elif line[0:14] == "msg_processed:":
            msg_processed = line[14:]
        elif line[0:5] == "InBox":
            if line[-9:] != "Undefined":
                pending_msg.append(line)
        else:
            action.append(line)

    Net_msg_H[0] = "mtype :"
    Net_msg_H[1] = "source:"
    Net_msg_H[2] = "vc    :"
    Net_msg_H[3] = "value :"
    Net_msg_H[4] = "count :"
    for i in range(len(Net_info_H)):
        for j in range(5):
            Net_msg_H[j] += "{:<21}".format(Net_info_H[i][j])
    Net_msg_P1[0] = "mtype :"
    Net_msg_P1[1] = "source:"
    Net_msg_P1[2] = "vc    :"
    Net_msg_P1[3] = "value :"
    Net_msg_P1[4] = "count :"
    for i in range(len(Net_info_P1)):
        for j in range(5):
            Net_msg_P1[j] += "{:<21}".format(Net_info_P1[i][j])
    Net_msg_P2[0] = "mtype :"
    Net_msg_P2[1] = "source:"
    Net_msg_P2[2] = "vc    :"
    Net_msg_P2[3] = "value :"
    Net_msg_P2[4] = "count :"
    for i in range(len(Net_info_P2)):
        for j in range(5):
            Net_msg_P2[j] += "{:<21}".format(Net_info_P2[i][j])
    Net_msg_P3[0] = "mtype :"
    Net_msg_P3[1] = "source:"
    Net_msg_P3[2] = "vc    :"
    Net_msg_P3[3] = "value :"
    Net_msg_P3[4] = "count :"
    for i in range(len(Net_info_P3)):
        for j in range(5):
            Net_msg_P3[j] += "{:<21}".format(Net_info_P3[i][j])
        
    
    
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("Last Value: " + last_val)
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("HomeNode:")
    trace_stage_processed[-1].append("State: {:<8} Owner: {:<14} Value: {:<8}".format(HomeNode_info["state"], HomeNode_info["owner"], HomeNode_info["value"]))
    trace_stage_processed[-1].append("Sharers: " + str(HomeNode_info["sharers"]))
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("{:<20} {:<20} {:<20}".format("Proc_1","Proc_2","Proc_3"))
    trace_stage_processed[-1].append("State: {:<14}State: {:<14}State: {:<14}".format(Proc_info[0]["state"], Proc_info[1]["state"], Proc_info[2]["state"]))
    trace_stage_processed[-1].append("Value: {:<14}Value: {:<14}Value: {:<14}".format(Proc_info[0]["value"], Proc_info[1]["value"], Proc_info[2]["value"]))
    trace_stage_processed[-1].append("Count: {:<14}Count: {:<14}Count: {:<14}".format(Proc_info[0]["count"], Proc_info[1]["count"], Proc_info[2]["count"]))
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("Home Net:")
    for i in range(5):
        trace_stage_processed[-1].append(Net_msg_H[i])
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("Proc1 Net:")
    for i in range(5):
        trace_stage_processed[-1].append(Net_msg_P1[i])
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("Proc2 Net:")
    for i in range(5):
        trace_stage_processed[-1].append(Net_msg_P2[i])
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("Proc3 Net:")
    for i in range(5):
        trace_stage_processed[-1].append(Net_msg_P3[i])
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("Message Processed: " + msg_processed)
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("action")
    for line in action:
        trace_stage_processed[-1].append(line)
    trace_stage_processed[-1].append("")
    trace_stage_processed[-1].append("Inbox")
    count = 0
    for line in pending_msg:
        # if count == 4:
        #     trace_stage_processed[-1].append("")
        #     count = 0
        # count += 1
        trace_stage_processed[-1].append(line)
        
        
    

    
    



# %%
command = ""
os.system("clear")
i = 0
while command != "e":
    print("Error" + error_msg)
    print()
    print("Stage: " + str(i+1))
    for line in trace_stage_processed[i]:
        print(line)
        
    command = getch()
    if command == "n":
        i += 1
    if command == "b":
        i -= 1
    if i == len(trace_stage_processed):
        i -= 1
    if i < 0:
        i = 0
    
    os.system("clear")

# %%



