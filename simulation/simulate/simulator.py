"""
pepole_list: list of pepole
[[id, arrival_time, [[device_name, start_time, end_time, wakeup_time, calc_time, [pre_out_idx], [start_start_list], [end_start_list], [end_end_list], [start_end_list], caller, [before_id]], [device_name, start_time, end_time, wakeup_time, calc_time, [pre_out_idx], [start_start_list], [end_start_list], [end_end_list], [start_end_list], caller, [before_id]], ...], 0.0, 0.0]
start_start_list: After the current node updates the start time, the nodes that need to update start_time
end_start_list: After the current node updates the end time, the nodes that need to update start_time and trans_time
end_end_list: After the current node updates the end time, the node of end_time and return_time need to be updated.
thread_dict: dict of thread
{device name:{'thread': thread_num, 'flag': False, 'work': [], 'wait': [], 'work_time':0.0}}
"""
import copy
import math



def new_simulator(people_list, thread_dict):
    # step_dict:
    step_dict = {}
    for pepole in people_list:
        step_dict[pepole[0]] = [3 for i in range(len(pepole[2]))]
    thread_map = {}
    pop_work_dict = {}
    for key in thread_dict.keys():
        thread_map[key] = {}
        thread_map[key]['thread'] = thread_dict[key]['thread']
        thread_map[key]['tasks'] = [[i, -1, True] for i in range(thread_dict[key]['thread'])]
        pop_work_dict[key] = [-thread_dict[key]['thread'], [], []]
    flag_matrix = [1 for i in range(len(people_list))]
    for people_id in range(len(people_list)):
        update_phase(people_list, people_id, 0, people_list[people_id][1])
        for idx, ac in enumerate(people_list[people_id][2]):
            thread_dict[ac[0]]['wait'].append([people_id, idx, ac[1], ac[2], False, -1, ac[1]])
            step_dict[people_id][idx] = 2
    tmp_poeple_list = copy.deepcopy(people_list)
    while True:
        for key in thread_dict.keys():
            # work: [people_id, step_id, in_time, out_time, out_flag, thread_id]
            update_work(people_list, thread_dict, key, step_dict, thread_map, tmp_poeple_list)
        for key in thread_dict.keys():
            update_wait(people_list, thread_dict, key, step_dict, thread_map, tmp_poeple_list)
        for key in step_dict.keys():
            if sum(step_dict[key]) == 0:
                flag_matrix[key] = 0
        if sum(flag_matrix) == 0:
            break
def update_wait(people_list, thread_dict, key, step_dict, thread_map, tmp_poeple_list):
    if len(thread_dict[key]['wait']) > 0:
        out_working_time = [i[3] for i in thread_dict[key]['work'] if not i[4]]
        wait_in_time = [i[1] for i in thread_map[key]['tasks'] if i[2]]
        if len(out_working_time) == 0:
            min_tmp_time = min(wait_in_time)
        elif len(wait_in_time) == 0:
            min_tmp_time = min(out_working_time)
        else:
            min_tmp_time = min(min(out_working_time), min(wait_in_time))
        thread_dict[key]['wait'] = sorted(thread_dict[key]['wait'], key=lambda x: (x[2], x[6], x[1]))
        for idx, wait in enumerate(thread_dict[key]['wait']):
            if wait[2] > min_tmp_time:
                update_phase(people_list, wait[0], wait[1], wait[2])
            else:
                if people_list[wait[0]][2][wait[1]][8] == []:
                    update_phase(people_list, wait[0], wait[1], min_tmp_time)
                # update_phase(people_list, wait[0], wait[1], min_tmp_time)
            for jdx, ac in enumerate(people_list[wait[0]][2]):
                if step_dict[wait[0]][jdx] == 1:
                    for tmp_work in thread_dict[ac[0]]['work']:
                        if tmp_work[0] == wait[0] and tmp_work[1] == jdx:
                            tmp_work[2] = round(people_list[tmp_work[0]][2][tmp_work[1]][1], 9)
                            tmp_work[3] = round(people_list[tmp_work[0]][2][tmp_work[1]][2], 9)
                elif step_dict[wait[0]][jdx] == 2:
                    for tmp_wait in thread_dict[ac[0]]['wait']:
                        if tmp_wait[0] == wait[0] and tmp_wait[1] == jdx:
                            tmp_wait[2] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][1], 9)
                            tmp_wait[3] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][2], 9)
        for idx, wait in enumerate(thread_dict[key]['wait']):
            wait[6] = tmp_poeple_list[wait[0]][2][wait[1]][1]
    while thread_dict[key]['thread'] > 0 and len(thread_dict[key]['wait']) > 0:
        for idx, wait in enumerate(thread_dict[key]['wait']):
            wait[6] = tmp_poeple_list[wait[0]][2][wait[1]][1]
        thread_dict[key]['wait'] = sorted(thread_dict[key]['wait'], key=lambda x: (x[2], x[6], x[1]))
        pop_idx = None
        for idx, wait in enumerate(thread_dict[key]['wait']):
            add_flag = True
            for bf in people_list[wait[0]][2][wait[1]][13]:
                if bf == -1:
                    continue
                else:
                    if step_dict[wait[0]][bf] == 1:
                        if people_list[wait[0]][2][bf][0] == key:
                            add_flag = False
                            break
                    if step_dict[wait[0]][bf] > 1:
                        add_flag = False
                        break
            if add_flag:
                pop_idx = idx
                break
        if pop_idx is None:
            break
        tmp_pop = thread_dict[key]['wait'][pop_idx]
        if pop_idx != 0:
            for t_w in thread_dict[key]['wait'][:pop_idx]:
                for pre_out in people_list[t_w[0]][2][t_w[1]][13]:
                    if pre_out == -1:
                        continue
                    elif step_dict[t_w[0]][pre_out] == 1:
                        update_work(people_list, thread_dict, people_list[t_w[0]][2][pre_out][0], step_dict, thread_map, tmp_poeple_list)
                    else:
                        update_wait(people_list, thread_dict, people_list[t_w[0]][2][pre_out][0], step_dict, thread_map, tmp_poeple_list)
            break
        out_working_time = [i[3] for i in thread_dict[key]['work'] if not i[4]]
        wait_in_time = [i[1] for i in thread_map[key]['tasks'] if i[2]]
        if len(out_working_time) > 0:
            if min(wait_in_time) > min(out_working_time):
                break
        thread_map[key]['tasks'].sort(key=lambda x: x[1])
        use_threads = [[i[0], i[1], i[2]] for i in thread_map[key]['tasks'] if i[2]]
        use_thread = use_threads[0]
        use_in_time = use_thread[1]
        working_thread_out = [i[3] for i in thread_dict[key]['work'] if not i[4]]
        if len(working_thread_out) > 0:
            if use_in_time > min(working_thread_out):
                break
        if use_thread[1] == -1:
            thread_dict[key]['thread'] -= 1
            thread_dict[key]['work'].append([tmp_pop[0], tmp_pop[1], tmp_pop[2], tmp_pop[3], False, use_thread[0], tmp_pop[2]])
            for tt in thread_map[key]['tasks']:
                if tt[0] == use_thread[0]:
                    tt[2] = False
                    break
            step_dict[tmp_pop[0]][tmp_pop[1]] = 1
            thread_dict[key]['wait'].pop(pop_idx)
        else:
            tmp_in_time = tmp_pop[2]
            if tmp_in_time < use_thread[1]:
                for idx, ac in enumerate(people_list[tmp_pop[0]][2]):
                    if step_dict[tmp_pop[0]][idx] == 1:
                        for tmp_work in thread_dict[ac[0]]['work']:
                            if tmp_work[0] == tmp_pop[0] and tmp_work[1] == idx:
                                tmp_work[6] = round(people_list[tmp_work[0]][2][tmp_work[1]][1], 9)
                    elif step_dict[tmp_pop[0]][idx] == 2:
                        for tmp_wait in thread_dict[ac[0]]['wait']:
                            if tmp_wait[0] == tmp_pop[0] and tmp_wait[1] == idx:
                                tmp_wait[6] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][1], 9)
                update_phase(people_list, tmp_pop[0], tmp_pop[1], use_thread[1])
                for idx, ac in enumerate(people_list[tmp_pop[0]][2]):
                    if step_dict[tmp_pop[0]][idx] == 1:
                        for tmp_work in thread_dict[ac[0]]['work']:
                            if tmp_work[0] == tmp_pop[0] and tmp_work[1] == idx:
                                tmp_work[2] = round(people_list[tmp_work[0]][2][tmp_work[1]][1], 9)
                                tmp_work[3] = round(people_list[tmp_work[0]][2][tmp_work[1]][2], 9)
                    elif step_dict[tmp_pop[0]][idx] == 2:
                        for tmp_wait in thread_dict[ac[0]]['wait']:
                            if tmp_wait[0] == tmp_pop[0] and tmp_wait[1] == idx:
                                tmp_wait[2] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][1], 9)
                                tmp_wait[3] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][2], 9)
                thread_dict[key]['thread'] -= 1
                thread_dict[key]['work'].append([tmp_pop[0], tmp_pop[1], use_thread[1], people_list[tmp_pop[0]][2][tmp_pop[1]][2], False, use_thread[0], use_thread[1]])
                for idx, ac in enumerate(tmp_poeple_list[tmp_pop[0]][2]):
                    ac[1] = people_list[tmp_pop[0]][2][idx][1]
                    ac[2] = people_list[tmp_pop[0]][2][idx][2]
                for tt in thread_map[key]['tasks']:
                    if tt[0] == use_thread[0]:
                        tt[2] = False
                        break
                step_dict[tmp_pop[0]][tmp_pop[1]] = 1
                thread_dict[key]['wait'].pop(pop_idx)
                min_tmp_time = use_thread[1]
                thread_dict[key]['wait'] = sorted(thread_dict[key]['wait'], key=lambda x: (x[2], x[1]))
                if len(thread_dict[key]['wait']) > 0 and min_tmp_time > thread_dict[key]['wait'][0][2]:
                    tmp_zero_time = thread_dict[key]['wait'][0][2]
                    # update_list = [1 for i in range(len(people_list))]
                    for idx, wait in enumerate(thread_dict[key]['wait']):
                        for jdx, ac in enumerate(people_list[wait[0]][2]):
                            if step_dict[wait[0]][jdx] == 1:
                                for tmp_work in thread_dict[ac[0]]['work']:
                                    if tmp_work[0] == wait[0] and tmp_work[1] == jdx:
                                        tmp_work[6] = round(people_list[tmp_work[0]][2][tmp_work[1]][1], 9)
                            elif step_dict[wait[0]][jdx] == 2:
                                for tmp_wait in thread_dict[ac[0]]['wait']:
                                    if tmp_wait[0] == wait[0] and tmp_wait[1] == jdx:
                                        tmp_wait[6] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][1], 9)
                        if wait[2] > min_tmp_time:
                            update_phase(people_list, wait[0], wait[1], wait[2])
                        else:
                            if people_list[wait[0]][2][wait[1]][8] == []:
                                update_phase(people_list, wait[0], wait[1], min_tmp_time)
                        for jdx, ac in enumerate(people_list[wait[0]][2]):
                            if step_dict[wait[0]][jdx] == 1:
                                for tmp_work in thread_dict[ac[0]]['work']:
                                    if tmp_work[0] == wait[0] and tmp_work[1] == jdx:
                                        tmp_work[2] = round(people_list[tmp_work[0]][2][tmp_work[1]][1], 9)
                                        tmp_work[3] = round(people_list[tmp_work[0]][2][tmp_work[1]][2], 9)
                            elif step_dict[wait[0]][jdx] == 2:
                                for tmp_wait in thread_dict[ac[0]]['wait']:
                                    if tmp_wait[0] == wait[0] and tmp_wait[1] == jdx:
                                        tmp_wait[2] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][1], 9)
                                        tmp_wait[3] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][2], 9)
            else:
                thread_dict[key]['thread'] -= 1
                thread_dict[key]['work'].append([tmp_pop[0], tmp_pop[1], tmp_pop[2], tmp_pop[3], False, use_thread[0], tmp_pop[2]])
                for tt in thread_map[key]['tasks']:
                    if tt[0] == use_thread[0]:
                        tt[2] = False
                        break
                step_dict[tmp_pop[0]][tmp_pop[1]] = 1
                thread_dict[key]['wait'].pop(pop_idx)
                update_phase(people_list, tmp_pop[0], tmp_pop[1], tmp_pop[2])
                for idx, ac in enumerate(people_list[tmp_pop[0]][2]):
                    tmp_poeple_list[tmp_pop[0]][2][idx][1] = people_list[tmp_pop[0]][2][idx][1]
                    tmp_poeple_list[tmp_pop[0]][2][idx][2] = people_list[tmp_pop[0]][2][idx][2]


def update_work(people_list, thread_dict, key, step_dict, thread_map, tmp_poeple_list):
    for wid, work in enumerate(thread_dict[key]['work']):
        if work[4]:
            continue
        else:
            out_flag = True
            for out_idx in people_list[work[0]][2][work[1]][5]:
                if step_dict[work[0]][out_idx] != 0:
                    out_flag = False
                    break
            if out_flag:
                # if False:
                if work[3] > min([i[3] for i in thread_dict[key]['work'] if i[4] is False]):
                    continue
                else:
                    thread_dict[key]['work'][wid][4] = True
                    for tt in thread_map[key]['tasks']:
                        if tt[0] == work[5]:
                            tt[1] = people_list[work[0]][2][work[1]][2]
                            tt[2] = True
                            break
                    thread_dict[key]['thread'] += 1
                    step_dict[work[0]][work[1]] = 0
                    if len(thread_dict[key]['wait']) > 0:
                        out_working_time = [i[3] for i in thread_dict[key]['work'] if not i[4]]
                        wait_in_time = [i[1] for i in thread_map[key]['tasks'] if i[2]]
                        if len(out_working_time) == 0:
                            min_tmp_time = min(wait_in_time)
                        elif len(wait_in_time) == 0:
                            min_tmp_time = min(out_working_time)
                        else:
                            min_tmp_time = min(min(out_working_time), min(wait_in_time))
                        thread_dict[key]['wait'] = sorted(thread_dict[key]['wait'], key=lambda x: (x[2], x[1]))
                        if min_tmp_time > thread_dict[key]['wait'][0][2]:
                            for idx, wait in enumerate(thread_dict[key]['wait']):
                                if wait[2] > min_tmp_time:
                                    update_phase(people_list, wait[0], wait[1], wait[2])
                                else:
                                    # update_phase(people_list, wait[0], wait[1], min_tmp_time)
                                    if people_list[wait[0]][2][wait[1]][8] == []:
                                        update_phase(people_list, wait[0], wait[1], min_tmp_time)
                                for jdx, ac in enumerate(people_list[wait[0]][2]):
                                    if step_dict[wait[0]][jdx] == 1:
                                        for tmp_work in thread_dict[ac[0]]['work']:
                                            if tmp_work[0] == wait[0] and tmp_work[1] == jdx:
                                                tmp_work[2] = round(people_list[tmp_work[0]][2][tmp_work[1]][1],9)
                                                tmp_work[3] = round(people_list[tmp_work[0]][2][tmp_work[1]][2],9)
                                    elif step_dict[wait[0]][jdx] == 2:
                                        for tmp_wait in thread_dict[ac[0]]['wait']:
                                            if tmp_wait[0] == wait[0] and tmp_wait[1] == jdx:
                                                tmp_wait[2] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][1],9)
                                                tmp_wait[3] = round(people_list[tmp_wait[0]][2][tmp_wait[1]][2],9)
                    for pre_out in people_list[work[0]][2][work[1]][13]:
                        if pre_out == -1:
                            continue
                        update_work(people_list, thread_dict, people_list[work[0]][2][pre_out][0], step_dict, thread_map, tmp_poeple_list)

def start_start_time(people_list, people_id, step_id, start_time, last_return_idx):
    people_list[people_id][2][step_id][1] = start_time
    if len(people_list[people_id][2][step_id][6]) > 0:
        if step_id in [i[0] for i in people_list[people_id][2][step_id][9]]:
            last_return_idx.append(step_id)
        if people_list[people_id][2][step_id][11] == 'Synchrounous':
            calc_flag = True
        else:
            if False in [jk[1] for jk in people_list[people_id][2][step_id][9]]:
                calc_flag = False
            else:
                calc_flag = True
        for idx, tans_time in people_list[people_id][2][step_id][6]:
            if calc_flag:
                tmp_time = round(start_time + people_list[people_id][2][step_id][3] + people_list[people_id][2][step_id][4] + tans_time, 9)
            else:
                tmp_time = round(start_time + people_list[people_id][2][step_id][3]+ tans_time, 9)
            start_start_time(people_list, people_id, idx, tmp_time, last_return_idx)
    else:
        last_return_idx.append(step_id)

def end_end_time(people_list, people_id, step_id, end_time, new_phase_idx):
    if len(people_list[people_id][2][step_id][7]) > 0:
        for idx in people_list[people_id][2][step_id][7]:
            if idx not in [i[0] for i in new_phase_idx]:
                new_phase_idx.append([step_id, idx, people_list[people_id][2][step_id][12]])
    if len(people_list[people_id][2][step_id][8]) > 0:
        for idx, return_time in people_list[people_id][2][step_id][8]:
            if people_list[people_id][2][idx][11] == 'Synchronous':
                this_end_time = round(end_time + return_time, 9)
                people_list[people_id][2][idx][2] = this_end_time
                people_list[people_id][2][idx][12] = this_end_time
            else:
                if False in [jk[1] for jk in people_list[people_id][2][idx][9]]:
                    this_end_time = round(end_time + return_time, 9)
                    people_list[people_id][2][idx][12] = this_end_time
                else:
                    this_end_time = round(end_time + return_time, 9)
                    people_list[people_id][2][idx][2] = this_end_time
                    people_list[people_id][2][idx][12] = this_end_time
            if idx in [i[0] for i in new_phase_idx]:
                for p in new_phase_idx:
                    if p[0] == idx:
                        if p[2] < people_list[people_id][2][idx][12]:
                            p[2] = people_list[people_id][2][idx][12]
            end_end_time(people_list, people_id, idx, this_end_time, new_phase_idx)
    else:
        if people_list[people_id][2][step_id][11] == 'Asynchronous':
            for idx, flag in people_list[people_id][2][step_id][9]:
                if idx == step_id:
                    if flag:
                        people_list[people_id][2][idx][2] = round(people_list[people_id][2][idx][1] + people_list[people_id][2][idx][3], 9)
                    else:
                        people_list[people_id][2][idx][2] = round(people_list[people_id][2][idx][1] + people_list[people_id][2][idx][3] + people_list[people_id][2][idx][4],9)




def update_phase(people_list, people_id, step_id, start_time):
    # start_start
    last_return_idx = []
    start_start_time(people_list, people_id, step_id, start_time, last_return_idx)
    # start_end + end_end
    new_phase_idx = []
    for idx in last_return_idx:
        for jdx, flag in people_list[people_id][2][idx][9]:
            if jdx == idx:
                if flag:
                    people_list[people_id][2][jdx][2] = round(people_list[people_id][2][jdx][1] + people_list[people_id][2][jdx][3] + people_list[people_id][2][jdx][4],9)
                else:
                    people_list[people_id][2][jdx][2] = round(people_list[people_id][2][jdx][1] + people_list[people_id][2][jdx][3],9)
                people_list[people_id][2][jdx][12] = round(people_list[people_id][2][jdx][1] + people_list[people_id][2][jdx][3] + people_list[people_id][2][jdx][4],9)
        end_end_time(people_list, people_id, idx, people_list[people_id][2][idx][2], new_phase_idx)
    for old_idx, new_idx, new_start_time in new_phase_idx:
        update_phase(people_list, people_id, new_idx, new_start_time)

