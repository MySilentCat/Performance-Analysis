"""
pepole_list: list of pepole
[[id, arrival_time, [[device_name, start_time, end_time, wakeup_time, calc_time, [pre_out_idx], [start_start_list], [end_start_list], [end_end_list], [start_end_list], caller, [before_id]], [device_name, start_time, end_time, wakeup_time, calc_time, [pre_out_idx], [start_start_list], [end_start_list], [end_end_list], [start_end_list], caller, [before_id]], ...], 0.0, 0.0]
start_start_list: After the current node updates the start time, the nodes that need to update start_time
end_start_list: After the current node updates the end time, the nodes that need to update start_time and trans_time
end_end_list: After the current node updates the end time, the node of end_time and return_time need to be updated.
thread_dict: dict of thread
{device name:{'thread': thread_num, 'flag': False, 'work': [], 'wait': [], 'work_time':0.0}}
"""
import math


def new_simulator(people_list, thread_dict):
    # step_dict:
    step_dict = {}
    for pepole in people_list:
        step_dict[pepole[0]] = [3 for i in range(len(pepole[2]))]
    thread_map = {}
    pop_work_dict = {}
    for key in thread_dict.keys():
        thread_map[key] = thread_dict[key]['thread']
        pop_work_dict[key] = [-thread_dict[key]['thread'], 0, []]
    flag_matrix = [1 for i in range(len(people_list))]
    while True:
        for people in people_list:
            for idx, ac in enumerate(people[2]):
                if step_dict[people[0]][idx] == 0:
                    continue
                # start_start_list
                for i, trans_time in ac[6]:
                    if math.isinf(people[2][i][1]):
                        people[2][i][1] = ac[1] + ac[3] + ac[4] + trans_time
                    else:
                        if people[2][i][1] < ac[1] + ac[3] + ac[4] + trans_time:
                            people[2][i][1] = ac[1] + ac[3] + ac[4] + trans_time
                # start_end_list
                for i, flag in ac[9]:
                    if flag:
                        if math.isinf(people[2][i][2]):
                            people[2][i][2] = ac[1] + ac[3] + ac[4]
                            ac[2] = ac[1] + ac[3] + ac[4]
                        else:
                            if people[2][i][2] < ac[1] + ac[3] + ac[4]:
                                people[2][i][2] = ac[1] + ac[3] + ac[4]
                                ac[2] = ac[1] + ac[3] + ac[4]
                    else:
                        if math.isinf(people[2][i][1]):
                            people[2][i][2] = ac[1]
                            ac[2] = ac[1] + ac[3]  # tw
                        else:
                            if people[2][i][2] < ac[1]:
                                people[2][i][2] = ac[1]
                                ac[2] = ac[1] + ac[3]  # tw
                # end_start_list
                for i in ac[7]:
                    if math.isinf(people[2][i][1]):
                        people[2][i][1] = ac[2]
                    else:
                        if people[2][i][1] < ac[2]:
                            people[2][i][1] = ac[2]
                # end_end_list
                for i, return_time in ac[8]:
                    if math.isinf(people[2][i][2]):
                        people[2][i][2] = ac[2] + return_time
                    else:
                        if people[2][i][2] < ac[2] + return_time:
                            people[2][i][2] = ac[2] + return_time
            for idx, ac in enumerate(people[2]):
                if step_dict[people[0]][idx] == 0:
                    continue
                if not math.isinf(ac[1]):
                    if step_dict[people[0]][idx] == 3:
                        thread_dict[ac[0]]['wait'].append([people[0], ac[1], ac[2], ac[3], ac[4], ac[5], ac[6], ac[7], ac[8], ac[9], idx, ac[11]])
                        step_dict[people[0]][idx] = 2
        for key in thread_dict.keys():
            if len(thread_dict[key]['work']) > 0:
                thread_dict[key]['work'].sort(key=lambda x: (x[2], x[10]))
                for work in thread_dict[key]['work']:
                    out_flag = True
                    for out_indx in work[5]:
                        if step_dict[work[0]][out_indx] != 0:
                            out_flag = False
                            break
                    if out_flag:
                        now_time = float('inf')
                        for se in work[9]:
                            if se[1]:
                                if math.isinf(work[2]):
                                    work[2] = round(work[1] + work[3] + work[4], 9)
                                    people_list[work[0]][2][work[-2]][2] = work[2]
                                    now_time = work[2]
                                else:
                                    if round(work[2], 9) < round(work[1] + work[3] + work[4], 9):
                                        work[2] = round(work[1] + work[3] + work[4], 9)
                                        people_list[work[0]][2][work[-2]][2] = work[2]
                                    now_time = work[2]
                                    people_list[work[0]][2][work[-2]][2] = work[2]
                            else:
                                if math.isinf(work[2]):
                                    work[2] = work[1] + work[3]  # tw
                                    people_list[work[0]][2][work[-2]][2] = work[2]
                                    now_time = work[2]
                                else:
                                    if round(work[2], 9) < round(work[1] + work[3], 9):
                                        work[2] = work[1] + work[3]  # tw
                                        people_list[work[0]][2][work[-2]][2] = work[2]
                                    now_time = work[2]
                                    people_list[work[0]][2][work[-2]][2] = now_time
                        if math.isinf(now_time) and not math.isinf(work[2]):
                            now_time = work[2]
                        thread_dict[key]['thread'] += 1
                        rm_idx = None
                        for idx, tmp_work in enumerate(thread_dict[key]['work']):
                            if tmp_work[0] == work[0] and tmp_work[10] == work[10]:
                                rm_idx = idx
                                break
                        pop_work_dict[key][2].append(thread_dict[key]['work'].pop(rm_idx))
                        pop_work_dict[key][1] += 1
                        # end_start
                        for idx in work[7]:
                            people_list[work[0]][2][idx][1] = now_time
                            if step_dict[work[0]][idx] == 1:
                                for tmp_work in thread_dict[people_list[work[0]][2][idx][0]]['work']:
                                    if tmp_work[0] == work[0] and tmp_work[10] == idx:
                                        tmp_work[1] = now_time
                            elif step_dict[work[0]][idx] == 2:
                                for tmp_work in thread_dict[people_list[work[0]][2][idx][0]]['wait']:
                                    if tmp_work[0] == work[0] and tmp_work[10] == idx:
                                        tmp_work[1] = now_time
                            start_start_update(people_list, work[0], thread_dict, step_dict, idx, now_time)
                        # end_end
                        end_end_update(people_list, work[0], thread_dict, step_dict, work[10], now_time)
                        step_dict[work[0]][work[10]] = 0

            if thread_dict[key]['thread'] > 0 and len(thread_dict[key]['wait']) > 0:
                thread_dict[key]['wait'].sort(key=lambda x: (x[1], x[10]))
                while thread_dict[key]['thread'] > 0:
                    pop_idx = None
                    for tidx, ptmp in enumerate(thread_dict[key]['wait']):
                        add_flag = True
                        for bf in ptmp[11]:
                            if bf == -1:
                                continue
                            else:
                                if step_dict[ptmp[0]][bf] > 1 or (step_dict[ptmp[0]][bf] == 1 and people_list[ptmp[0]][2][bf][0] == key):
                                    add_flag = False
                                    break
                        if add_flag:
                            pop_idx = tidx
                            break
                    if pop_idx is None:
                        break
                    tmp = thread_dict[key]['wait'].pop(pop_idx)
                    thread_dict[key]['thread'] -= 1
                    if pop_work_dict[key][0] >= 0:
                        if pop_work_dict[key][1] > pop_work_dict[key][0]:
                            pop_bf = pop_work_dict[key][2][pop_work_dict[key][0]]
                            pop_work_dict[key][0] += 1
                            if tmp[1] < pop_bf[2]:
                                gap_time = pop_bf[2] - tmp[1]
                                tmp[1] = pop_bf[2]
                                tmp[2] += gap_time
                                people_list[tmp[0]][2][tmp[10]][1] = pop_bf[2]
                                people_list[tmp[0]][2][tmp[10]][2] += gap_time
                                start_start_update(people_list, tmp[0], thread_dict, step_dict, tmp[10], pop_bf[2])
                            thread_dict[key]['work'].append(tmp)
                            step_dict[tmp[0]][tmp[10]] = 1
                    else:
                        thread_dict[key]['work'].append(tmp)
                        step_dict[tmp[0]][tmp[10]] = 1
                        pop_work_dict[key][0] += 1
        for key in step_dict.keys():
            if sum(step_dict[key]) == 0:
                flag_matrix[key] = 0
        if sum(flag_matrix) == 0:
            break


def end_end_update(people_list, people_id, thread_dict, step_dict, idx, end_time):
    if len(people_list[people_id][2][idx][8]) > 0:
        for tmp_idx, return_time in people_list[people_id][2][idx][8]:
            this_end_time = round(end_time + return_time, 9)
            if math.isinf(people_list[people_id][2][tmp_idx][2]):
                people_list[people_id][2][tmp_idx][2] = this_end_time
            else:
                if this_end_time < people_list[people_id][2][tmp_idx][2]:
                    this_end_time = people_list[people_id][2][tmp_idx][2]
                people_list[people_id][2][tmp_idx][2] = this_end_time
            if step_dict[people_list[people_id][0]][tmp_idx] == 1:
                for tmp_work in thread_dict[people_list[people_id][2][tmp_idx][0]]['work']:
                    if tmp_work[0] == people_list[people_id][0] and tmp_work[10] == tmp_idx:
                        tmp_work[2] = this_end_time
                        break
            elif step_dict[people_list[people_id][0]][tmp_idx] == 2:
                for tmp_work in thread_dict[people_list[people_id][2][tmp_idx][0]]['wait']:
                    if tmp_work[0] == people_list[people_id][0] and tmp_work[10] == tmp_idx:
                        tmp_work[2] = this_end_time
                        break
            for es in people_list[people_id][2][tmp_idx][7]:
                people_list[people_id][2][es][1] = this_end_time
            end_end_update(people_list, people_id, thread_dict, step_dict, tmp_idx, this_end_time)


def start_start_update(people_list, people_id, thread_dict, step_dict, idx, start_time):
    if len(people_list[people_id][2][idx][6]) > 0:
        for tmp_idx, trans_time in people_list[people_id][2][idx][6]:
            tmp_time = round(start_time + trans_time + people_list[people_id][2][idx][3] + people_list[people_id][2][idx][4], 9)
            if math.isinf(people_list[people_id][2][tmp_idx][1]):
                people_list[people_id][2][tmp_idx][1] = tmp_time
            else:
                if people_list[people_id][2][tmp_idx][1] < tmp_time:
                    people_list[people_id][2][tmp_idx][1] = tmp_time
            for se in people_list[people_id][2][tmp_idx][9]:
                if se[1]:
                    if math.isinf(people_list[people_id][2][se[0]][2]):
                        people_list[people_id][2][se[0]][2] = round(tmp_time + people_list[people_id][2][se[0]][3] + people_list[people_id][2][se[0]][4], 9)
                    else:
                        if round(people_list[people_id][2][se[0]][2], 9) < round(tmp_time + people_list[people_id][2][se[0]][3] + people_list[people_id][2][se[0]][4], 9):
                            people_list[people_id][2][se[0]][2] = round(tmp_time + people_list[people_id][2][se[0]][3] + people_list[people_id][2][se[0]][4], 9)
                else:
                    if math.isinf(people_list[people_id][2][se[0]][2]):
                        people_list[people_id][2][se[0]][2] = round(tmp_time + people_list[people_id][2][se[0]][3], 9)  # tw
                    else:
                        if round(people_list[people_id][2][se[0]][2], 9) < round(tmp_time + people_list[people_id][2][se[0]][3], 9):
                            people_list[people_id][2][se[0]][2] = round(tmp_time + people_list[people_id][2][se[0]][3], 9)  # tw
            if step_dict[people_list[people_id][0]][tmp_idx] == 1:
                for tmp_work in thread_dict[people_list[people_id][2][tmp_idx][0]]['work']:
                    if tmp_work[0] == people_list[people_id][0] and tmp_work[10] == tmp_idx:
                        tmp_work[1] = people_list[people_id][2][tmp_idx][1]
                        tmp_work[2] = people_list[people_id][2][tmp_idx][2]
                        break
            elif step_dict[people_list[people_id][0]][tmp_idx] == 2:
                for tmp_work in thread_dict[people_list[people_id][2][tmp_idx][0]]['wait']:
                    if tmp_work[0] == people_list[people_id][0] and tmp_work[10] == tmp_idx:
                        tmp_work[1] = people_list[people_id][2][tmp_idx][1]
                        tmp_work[2] = people_list[people_id][2][tmp_idx][2]
                        break
            start_start_update(people_list, people_id, thread_dict, step_dict, tmp_idx, people_list[people_id][2][tmp_idx][1])
