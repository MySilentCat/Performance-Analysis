import time
import random
from .simulator import new_simulator


def cal_work_time(w_list):
    work_time = 0.0
    new_list = []
    sleep_time = 0.0
    w_list.sort(key=lambda x: x[0])
    i = 0
    while i < len(w_list):
        end_time = w_list[i][1]
        j = i + 1
        while j < len(w_list):
            if w_list[j][0] < end_time:
                if w_list[j][1] > end_time:
                    end_time = w_list[j][1]
                j += 1
            else:
                break
        new_list.append([w_list[i][0], end_time])
        i = j
    for w in new_list:
        work_time += w[1] - w[0]
    if len(new_list) > 1:
        for i in range(1, len(new_list)):
            sleep_time += new_list[i][0] - new_list[i-1][1]
    return round(sleep_time, 9), round(work_time, 9)


def deal_action(action_trup, simulate_dict, step_idx, user_id):
    if isinstance(action_trup, tuple):
        # tw
        wakeup_time = 0
        # tij
        calculate_time = 0
        # tc
        network_time = 0
        wait_time = 0
        return_time = 0
        action_start = float("inf")
        action_end = float("inf")
        reciver_name = action_trup[1].split(".")[0]
        wakeup_time = simulate_dict["wake_up_time"][reciver_name]
        calculate_time = action_trup[-3]
        if action_trup[0] == "Actor":
            network_time = 0
            return_time = 0
        else:
            sender_name = action_trup[0].split(".")[0]
            network_time = action_trup[-2] / simulate_dict["network_speed"][(sender_name, reciver_name)]
            return_time = action_trup[-1] / simulate_dict["network_speed"][(reciver_name, sender_name)]
        return [user_id, action_trup[0], action_trup[1], action_trup[2], action_trup[3], action_start, action_end, wakeup_time, calculate_time, network_time, return_time, wait_time, step_idx]
    elif isinstance(action_trup, list):
        rst = []
        for step in action_trup:
            rst.append(deal_action(step, simulate_dict, step_idx, user_id))
        return rst
    else:
        return None


def perfomance_every_action(path, simulate_dict, user_id):
    total_time_list = []
    for step_idx, step in enumerate(path):
        total_time_list.append(deal_action(step, simulate_dict, step_idx, user_id))
    return total_time_list


def random_prob(num):
    random.seed(123)
    actor_prob = [random.random() for i in range(num)]
    random.seed(1234)
    business_prob = [random.random() for i in range(num)]
    random.seed(12345)
    path_prob = [random.random() for i in range(num)]
    return actor_prob, business_prob, path_prob


def run(simulate_dict, business_path, people_list, actor_prob, business_prob, path_prob, actor_business, file_name):
    business_sync = business_path
    thread_map = {}
    for key in simulate_dict["thread_dict"].keys():
        thread_map[key] = {}
        thread_map[key]["thread"] = simulate_dict["thread_dict"][key]
        thread_map[key]["work"] = []
        thread_map[key]["wait"] = []
        thread_map[key]['work_time'] = 0.0
        thread_map[key]['flag'] = False
    time_file_name = file_name
    business_list = []
    time_info = []
    business_info = []
    for i in range(len(people_list)):
        ac = None
        if actor_prob[i] < 0.7:
            ac = "Student"
        else:
            ac = "Librarian"
        business = None
        for key in actor_business[ac].keys():
            if actor_business[ac][key][0] <= business_prob[i] < actor_business[ac][key][1]:
                business = key
                break
        path = None
        for key in business_sync["business"][business]["prob"].keys():
            if business_sync["business"][business]["prob"][key][0] <= path_prob[i] < business_sync["business"][business]["prob"][key][1]:
                path = key
                break
        if business == "Print Book":
            tmp = [j for j in business_sync["business"]["Read Book"]["path0"]]
            tmp.extend(business_sync["business"][business][key])
            business_list.append(tmp)
            time_info.append([i, ac, business, people_list[i][1]])
        else:
            business_list.append(business_sync["business"][business][path])
            time_info.append([i, ac, business, people_list[i][1]])
        business_info.append([i, ac, business, path])
    with open(f"{time_file_name}_business_info.txt", "w") as f:
        for b in business_info:
            f.write(f"{b[0]}\t{b[1]}\t{b[2]}\t{b[3]}\n")
    for idx, bn in enumerate(business_list):
        timed_list = perfomance_every_action(bn, simulate_dict, idx)
        timed_list[0][5] = time_info[idx][-1] + timed_list[0][-4]
        time_info[idx].append(timed_list)
    new_plist = []
    new_tmp_list = []
    return_dict = {}
    r_dict = {}
    for i in range(len(people_list)):
        arr_time = people_list[i][1]
        ac_list = time_info[i][-1]
        return_dict[i] = []
        tmp_list = []
        device_list = []
        end_time = arr_time
        r_time_list = []
        for idx, ac in enumerate(ac_list):
            if isinstance(ac[0], int):
                if ac[1] == "Actor":
                    device_name = ac[2].split(".")[0]
                    end_end_list = []
                    pre_out_idx = []
                    end_start_list = []
                    start_start_list = []
                    start_end_list = []
                    caller = ac[1]
                    if idx == 0:
                        start_time = end_time
                        if idx != len(ac_list) - 1:
                            if isinstance(ac_list[idx+1][0], int):
                                if ac_list[idx+1][1] == "Actor":
                                    if len(device_list)+1 not in end_start_list:
                                        end_start_list.append(len(device_list)+1)
                                    if [len(device_list), True] not in start_end_list:
                                        start_end_list.append([len(device_list), True])
                                else:
                                    if [len(device_list)+1, ac_list[idx+1][-4]] not in start_start_list:
                                        start_start_list.append([len(device_list)+1, ac_list[idx+1][-4]])
                                    if ac[4] == "Synchronous":
                                        if len(device_list)+1 not in pre_out_idx:
                                            pre_out_idx.append(len(device_list)+1)
                                    else:
                                        if [len(device_list), True] not in start_end_list:
                                            start_end_list.append([len(device_list), True])
                            else:
                                wait_flag = False
                                for tidx, tmp_ac in enumerate(ac_list[idx+1]):
                                    if [len(device_list) + tidx, tmp_ac[-4]] not in start_start_list:
                                        start_start_list.append([len(device_list) + tidx, tmp_ac[-4]])
                                    if tmp_ac[4] == "Synchronous":
                                        if len(device_list) + tidx not in pre_out_idx:
                                            pre_out_idx.append(len(device_list) + tidx)
                                        wait_flag = True
                                if not wait_flag:
                                    if [len(device_list)+1, True] not in start_end_list:
                                        start_end_list.append([len(device_list)+1, True])
                        else:
                            if [len(device_list), True] not in start_end_list:
                                start_end_list.append([len(device_list), True])
                    else:
                        start_time = float("inf")
                        if idx != len(ac_list) - 1:
                            if isinstance(ac_list[idx+1][0], int):
                                if ac_list[idx+1][1] == "Actor":
                                    if len(device_list)+1 not in end_start_list:
                                        end_start_list.append(len(device_list)+1)
                                    if [len(device_list), True] not in start_end_list:
                                        start_end_list.append([len(device_list), True])
                                else:
                                    if [len(device_list)+1, ac_list[idx+1][-4]] not in start_start_list:
                                        start_start_list.append([len(device_list)+1, ac_list[idx+1][-4]])
                                    if ac[4] == "Synchronous":
                                        if len(device_list)+1 not in pre_out_idx:
                                            pre_out_idx.append(len(device_list)+1)
                                    else:
                                        if [len(device_list), True] not in start_end_list:
                                            start_end_list.append([len(device_list), True])
                            else:
                                wait_flag = False
                                for tidx, tmp_ac in enumerate(ac_list[idx+1]):
                                    if [len(device_list) + tidx, tmp_ac[-4]] not in start_start_list:
                                        start_start_list.append([len(device_list) + tidx, tmp_ac[-4]])
                                    if tmp_ac[4] == "Synchronous":
                                        if len(device_list) + tidx not in pre_out_idx:
                                            pre_out_idx.append(len(device_list) + tidx)
                                        wait_flag = True
                                if not wait_flag:
                                    if [len(device_list)+1, True] not in start_end_list:
                                        start_end_list.append([len(device_list)+1, True])
                        else:
                            if [len(device_list), True] not in start_end_list:
                                start_end_list.append([len(device_list), True])
                    end_time = float("inf")
                    tmp_list.append([device_name, start_time, end_time, ac[7], ac[8], pre_out_idx, start_start_list, end_start_list, end_end_list, start_end_list, "Actor"])
                    device_list.append(device_name)
                    r_time_list.append([ac[-1], ac[10]])
                    return_dict[i].append(ac[-1])
                else:
                    send_device = ac[1].split(".")[0]
                    recive_device = ac[2].split(".")[0]
                    if send_device != device_list[-1]:
                        end_end_list = []
                        pre_out_idx = []
                        end_start_list = []
                        start_start_list = []
                        start_end_list = []
                        index = 0
                        for id in range(len(device_list)-1, -1, -1):
                            if device_list[id] == send_device:
                                index = id
                                break
                        if len(device_list) not in tmp_list[index][7]:
                            tmp_list[index][7].append(len(device_list))
                        start_end_list.append([len(device_list), False])
                        start_start_list.append([len(device_list)+1, ac[-4]])
                        start_time = float("inf")
                        end_time = float("inf")
                        if ac[4] == "Synchronous":
                            pre_out_idx.append(len(device_list)+1)
                        tmp_list.append([send_device, start_time, end_time, simulate_dict['wake_up_time'][send_device], 0.0, pre_out_idx, start_start_list, end_start_list, end_end_list, start_end_list, send_device])
                        device_list.append(send_device)
                        r_time_list.append([ac[-1], 0.0])
                        return_dict[i].append(ac[-1])
                        if recive_device != send_device:
                            start_time = float("inf")
                            end_time = float("inf")
                            end_end_list = []
                            pre_out_idx = []
                            end_start_list = []
                            start_start_list = []
                            start_end_list = []
                            if idx != len(ac_list) - 1:
                                if isinstance(ac_list[idx+1][0], int):
                                    next_device = ac_list[idx+1][1].split(".")[0]
                                    if next_device != recive_device:
                                        tmp_idx = 0
                                        for id in range(len(tmp_list)-1, -1, -1):
                                            if tmp_list[id][-1] == next_device:
                                                tmp_idx = id
                                                break
                                        if tmp_idx not in tmp_list[tmp_idx][7]:
                                            tmp_list[tmp_idx][7].append(len(device_list)+1)
                                        if [len(device_list), True] not in start_end_list:
                                            start_end_list.append([len(device_list), True])
                                    else:
                                        if [len(device_list)+1, ac_list[idx+1][-4]] not in start_start_list:
                                            start_start_list.append([len(device_list)+1, ac_list[idx+1][-4]])
                                        if ac[4] == "Synchronous":
                                            if len(device_list)+1 not in pre_out_idx:
                                                pre_out_idx.append(len(device_list)+1)
                                        else:
                                            if [len(device_list), True] not in start_end_list:
                                                start_end_list.append([len(device_list), True])
                                else:
                                    wait_flag = False
                                    for tidx, tmp_ac in enumerate(ac_list[idx+1]):
                                        if [len(device_list) + tidx + 1, tmp_ac[-4]] not in start_start_list:
                                            start_start_list.append([len(device_list) + tidx + 1, tmp_ac[-4]])
                                        if tmp_ac[4] == "Synchronous":
                                            if len(device_list) + tidx + 1 not in pre_out_idx:
                                                pre_out_idx.append(len(device_list) + tidx + 1)
                                            wait_flag = True
                                    if not wait_flag:
                                        if [len(device_list), True] not in start_end_list:
                                            start_end_list.append([len(device_list), True])
                            else:
                                if [len(device_list), True] not in start_end_list:
                                    start_end_list.append([len(device_list), True])
                            tmp_list.append([recive_device, start_time, end_time, ac[7], ac[8], pre_out_idx, start_start_list, end_start_list, end_end_list, start_end_list, "##"])
                            device_list.append(recive_device)
                            r_time_list.append([ac[-1], ac[10]])
                        else:
                            tmp_list[-1][3] = ac[7]
                            tmp_list[-1][4] = ac[8]
                            if idx != len(ac_list) - 1:
                                if isinstance(ac_list[idx+1][0], int):
                                    next_device = ac_list[idx+1][1].split(".")[0]
                                    if next_device != recive_device:
                                        tmp_idx = 0
                                        for id in range(len(tmp_list)-1, -1, -1):
                                            if tmp_list[id][-1] == next_device:
                                                tmp_idx = id
                                                break
                                        if tmp_idx not in tmp_list[tmp_idx][7]:
                                            tmp_list[tmp_idx][7].append(len(device_list))
                                        tmp_list[-1][6].remove([len(device_list)+1, ac[-4]])
                                        for tmp_par in tmp_list[-1][9]:
                                            if tmp_par[0] == len(device_list):
                                                tmp_par[1] = True
                                        tmp_list[-1][5].remove(len(device_list)+1)
                                    else:
                                        for tmp_par in tmp_list[-1][9]:
                                            if tmp_par[0] == len(device_list):
                                                tmp_par[1] = True
                                else:
                                    wait_flag = False
                                    for tidx, tmp_ac in enumerate(ac_list[idx+1]):
                                        if [len(device_list) + tidx + 1, tmp_ac[-4]] not in start_start_list:
                                            start_start_list.append([len(device_list) + tidx + 1, tmp_ac[-4]])
                                        if tmp_ac[4] == "Synchronous":
                                            if len(device_list) + tidx + 1 not in pre_out_idx:
                                                pre_out_idx.append(len(device_list) + tidx + 1)
                                            wait_flag = True
                                    if not wait_flag:
                                        if [len(device_list), True] not in start_end_list:
                                            start_end_list.append([len(device_list), True])
                            else:
                                if [len(device_list), True] not in start_end_list:
                                    start_end_list.append([len(device_list), True])
                    else:
                        start_time = float("inf")
                        end_time = float("inf")
                        end_end_list = []
                        pre_out_idx = []
                        end_start_list = []
                        start_start_list = []
                        start_end_list = []
                        if idx != len(ac_list) - 1:
                            if isinstance(ac_list[idx+1][0], int):
                                next_device = ac_list[idx+1][1].split(".")[0]
                                if next_device != recive_device:
                                    tmp_idx = 0
                                    for id in range(len(tmp_list)-1, -1, -1):
                                        if tmp_list[id][-1] == next_device:
                                            tmp_idx = id
                                            break
                                    if tmp_idx not in tmp_list[tmp_idx][7]:
                                        tmp_list[tmp_idx][7].append(len(device_list)+1)
                                    if [len(device_list), True] not in start_end_list:
                                        start_end_list.append([len(device_list), True])
                                else:
                                    if [len(device_list)+1, ac_list[idx+1][-4]] not in start_start_list:
                                        start_start_list.append([len(device_list)+1, ac_list[idx+1][-4]])
                                    if ac[4] == "Synchronous":
                                        if len(device_list)+1 not in pre_out_idx:
                                            pre_out_idx.append(len(device_list)+1)
                                    else:
                                        if [len(device_list), True] not in start_end_list:
                                            start_end_list.append([len(device_list), True])
                            else:
                                next_pall_start = ac_list[idx+1][0][1].split(".")[0]
                                if next_pall_start != recive_device:
                                    tmp_idx = 0
                                    for id in range(len(tmp_list)-1, -1, -1):
                                        if tmp_list[id][-1] == next_pall_start:
                                            tmp_idx = id
                                            break
                                    if tmp_idx not in tmp_list[tmp_idx][7]:
                                        tmp_list[tmp_idx][7].append(len(device_list)+1)
                                    if [len(device_list), True] not in start_end_list:
                                        start_end_list.append([len(device_list), True])
                                else:
                                    if [len(device_list)+1, ac_list[idx+1][-4]] not in start_start_list:
                                        start_start_list.append([len(device_list)+1, ac_list[idx+1][-4]])
                                    wait_flag = False
                                    for tidx, tmp_ac in enumerate(ac_list[idx+1]):
                                        if tmp_ac[4] == "Synchronous":
                                            wait_flag = True
                                            break
                                    if not wait_flag:
                                        if [len(device_list)+1, True] not in start_end_list:
                                            start_end_list.append([len(device_list)+1, True])
                                    else:
                                        if len(device_list) + 1 not in pre_out_idx:
                                            pre_out_idx.append(len(device_list) + 1)
                        else:
                            if [len(device_list), True] not in start_end_list:
                                start_end_list.append([len(device_list), True])
                        tmp_list.append([recive_device, start_time, end_time, ac[7], ac[8], pre_out_idx, start_start_list, end_start_list, end_end_list, start_end_list, "##"])
                        device_list.append(recive_device)
                        r_time_list.append([ac[-1], ac[10]])
            else:
                send_device = ac[1][1].split(".")[0]
                if send_device != device_list[-1]:
                    index = 0
                    for id in range(len(tmp_list)-1, -1, -1):
                        if tmp_list[id][-1] == send_device:
                            index = id
                            break
                    if len(device_list) not in tmp_list[index][7]:
                        tmp_list[index][7].append(len(device_list))
                    end_end_list = []
                    pre_out_idx = []
                    end_start_list = []
                    start_start_list = []
                    start_end_list = []
                    start_time = float("inf")
                    end_time = float("inf")
                    for tidx, tmp_ac in enumerate(ac):
                        if [len(device_list) + tidx + 1, tmp_ac[-4]] not in start_start_list:
                            start_start_list.append([len(device_list) + tidx + 1, tmp_ac[-4]])
                        if tmp_ac[4] == "Synchronous":
                            if len(device_list) + tidx + 1 not in pre_out_idx:
                                pre_out_idx.append(len(device_list) + tidx + 1)
                    if idx != len(ac_list) - 1:
                        if isinstance(ac_list[idx+1][0], int):
                            next_device = ac_list[idx+1][1].split(".")[0]
                            if next_device != send_device:
                                tmp_idx = 0
                                for id in range(len(tmp_list)-1, -1, -1):
                                    if tmp_list[id][-1] == next_device:
                                        tmp_idx = id
                                        break
                                if tmp_idx not in tmp_list[tmp_idx][7]:
                                    tmp_list[tmp_idx][7].append(len(device_list)+tidx+1+1)
                            else:
                                if len(device_list)+tidx+1+1 not in end_start_list:
                                    end_start_list.append(len(device_list)+tidx+1+1)
                                if [len(device_list), False] not in start_end_list:
                                    start_end_list.append([len(device_list), False])
                        else:
                            next_pall_start = ac_list[idx+1][0][1].split(".")[0]
                            if next_pall_start != send_device:
                                tmp_idx = 0
                                for id in range(len(tmp_list)-1, -1, -1):
                                    if tmp_list[id][-1] == next_pall_start:
                                        tmp_idx = id
                                        break
                                if tmp_idx not in tmp_list[tmp_idx][7]:
                                    tmp_list[tmp_idx][7].append(len(device_list)+tidx+1+1)
                                if [len(device_list), False] not in start_end_list:
                                    start_end_list.append([len(device_list), False])
                            else:
                                if len(device_list)+tidx+1+1 not in end_start_list:
                                    end_start_list.append(len(device_list) + tidx + 1+1)
                                if [len(device_list), False] not in start_end_list:
                                    start_end_list.append([len(device_list), False])
                    else:
                        if [len(device_list), False] not in start_end_list:
                            start_end_list.append([len(device_list), False])
                    tmp_list.append([send_device, start_time, end_time, simulate_dict['wake_up_time'][send_device], 0.0, pre_out_idx, start_start_list, end_start_list, end_end_list, start_end_list, send_device])
                    now_idx = len(device_list)
                    device_list.append(send_device)
                    r_time_list.append([ac[-1], 0.0])
                    return_dict[i].append(idx-1)
                    for tidx, tmp_ac in enumerate(ac):
                        recive_device = tmp_ac[2].split(".")[0]
                        if recive_device != send_device:
                            start_time = float("inf")
                            end_time = float("inf")
                            end_end_list = []
                            pre_out_idx = []
                            end_start_list = []
                            start_start_list = []
                            start_end_list = []
                            if tmp_ac[4] == "Synchronous":
                                if now_idx+tidx+1 not in tmp_list[now_idx][5]:
                                    tmp_list[now_idx][5].append(now_idx+tidx+1)
                                if [now_idx, tmp_ac[10]] not in end_end_list:
                                    end_end_list.append([now_idx, tmp_ac[10]])
                            start_end_list.append([now_idx+tidx+1, True])
                            tmp_list.append([recive_device, start_time, end_time, tmp_ac[7], tmp_ac[8], pre_out_idx, start_start_list, end_start_list, end_end_list, start_end_list, "##"])
                            device_list.append(recive_device)
                            r_time_list.append([tmp_ac[-1], tmp_ac[10]])
                        else:
                            start_time = float("inf")
                            end_time = float("inf")
                            end_end_list = []
                            pre_out_idx = []
                            end_start_list = []
                            start_start_list = []
                            start_end_list = []
                            if tmp_ac[4] == "Synchronous":
                                if now_idx+tidx+1 not in tmp_list[now_idx][5]:
                                    tmp_list[now_idx-1][5].append(now_idx+tidx+1)
                                if [now_idx, 0.0] not in end_end_list:
                                    end_end_list.append([now_idx, 0.0])
                            start_end_list.append([now_idx+tidx+1, True])
                            for tmp_par in tmp_list[now_idx][6]:
                                if tmp_par[0] == now_idx + tidx+1:
                                    tmp_par[1] = 0.0
                            tmp_list.append([recive_device, start_time, end_time, tmp_ac[7], tmp_ac[8], pre_out_idx, start_start_list, end_start_list, end_end_list, start_end_list, "##"])
                            device_list.append(recive_device)
                            r_time_list.append([tmp_ac[-1], 0.0])
                else:
                    now_idx = len(device_list)
                    for tidx, tmp_ac in enumerate(ac):
                        recive_device = tmp_ac[2].split(".")[0]
                        if recive_device != send_device:
                            start_time = float("inf")
                            end_time = float("inf")
                            end_end_list = []
                            pre_out_idx = []
                            end_start_list = []
                            start_start_list = []
                            start_end_list = []
                            if tmp_ac[4] == "Synchronous":
                                if now_idx + idx not in tmp_list[now_idx-1][5]:
                                    tmp_list[now_idx-1][5].append(now_idx+idx)
                                if [now_idx-1, tmp_ac[10]] not in end_end_list:
                                    end_end_list.append([now_idx-1, tmp_ac[10]])
                            start_end_list.append([now_idx+tidx+1, True])
                            tmp_list.append([recive_device, start_time, end_time, tmp_ac[7], tmp_ac[8], pre_out_idx, start_start_list, end_start_list, end_end_list, start_end_list, "##"])
                            device_list.append(recive_device)
                            r_time_list.append([tmp_ac[-1], tmp_ac[10]])
                        else:
                            start_time = float("inf")
                            end_time = float("inf")
                            end_end_list = []
                            pre_out_idx = []
                            end_start_list = []
                            start_start_list = []
                            start_end_list = []
                            if tmp_ac[4] == "Synchronous":
                                if now_idx + idx not in tmp_list[now_idx-1][5]:
                                    tmp_list[now_idx-1][5].append(now_idx+idx)
                                if [now_idx-1, 0.0] not in end_end_list:
                                    end_end_list.append([now_idx-1, 0.0])
                            start_end_list.append([now_idx+tidx, True])
                            for tmp_par in tmp_list[now_idx][6]:
                                if tmp_par[0] == now_idx + tidx:
                                    tmp_par[1] = 0.0
                            tmp_list.append([recive_device, start_time, end_time, tmp_ac[7], tmp_ac[8], pre_out_idx, start_start_list, end_start_list, end_end_list, start_end_list, "##"])
                            device_list.append(recive_device)
                            r_time_list.append([tmp_ac[-1], 0.0])
        for tidx, tmp in enumerate(tmp_list):
            for jdx in tmp[5]:
                if [tidx, r_time_list[jdx][1]] not in tmp_list[jdx][-3]:
                    tmp_list[jdx][-3].append([tidx, r_time_list[jdx][1]])
            tmp.append([])
        for tidx, tmp in enumerate(tmp_list):
            if tidx == 0:
                tmp[-1].append(-1)
            for jdx, _ in tmp[6]:
                if tidx not in tmp_list[jdx][-1]:
                    tmp_list[jdx][-1].append(tidx)
            for jdx in tmp[7]:
                if jdx not in tmp_list[jdx][-1]:
                    tmp_list[jdx][-1].append(tidx)
        new_plist.append([i, arr_time, tmp_list, 0.0, 0.0])

    time0 = time.time()
    new_simulator(new_plist, thread_map)
    with open(f"{time_file_name}_plist.txt", "w") as f:
        for person in new_plist:
            f.write(f"{person[0]} arrive time: {person[1]}\n")
            for i in person[2]:
                f.write(f"{i[0]}\t{round(i[1], 9)}\t{round(i[2], 9)}\t{round(i[2] - i[1], 9)}\n")
            f.write("----------------------------\n")
    node_dict = {}
    for key in thread_map.keys():
        node_dict[key] = []
    time_cost = []
    first_time = people_list[0][1]
    last_time = 0.0
    for people in new_plist:
        ser_list = people[2]
        min_time = float("inf")
        max_time = 0.0
        arr_time = people[1]
        for i in range(len(ser_list)):
            act_node = ser_list[i][0]
            time_s = ser_list[i][1]
            time_e = ser_list[i][2]
            if time_s < min_time:
                min_time = time_s
            if time_e > max_time:
                max_time = time_e
            node_dict[act_node].append([people[0], people[1], time_info[people[0]][1], time_info[people[0]][2], round(time_s, 9), round(time_e, 9), round(time_e - time_s, 9)])
        time_cost.append([people[0], people[1], time_info[people[0]][1], time_info[people[0]][2], round(min_time, 9), round(max_time, 9), round(max_time - min_time, 9), round(min_time - arr_time, 9)])
        if max_time > last_time:
            last_time = max_time

    AEU_list = []
    AEU_dict = {}
    for key in node_dict.keys():
        w_list = [[i[4], i[5]] for i in node_dict[key]]
        sleep_time, w_time = cal_work_time(w_list)
        AEU_dict[key] = round(w_time / last_time, 5)
        AEU_list.append([key, w_time, sleep_time])
    # print(AEU_dict)
    AEU = round((sum([i[1]/last_time for i in AEU_list])/len(AEU_list)) * 100, 9)
    BR_dict = {}
    for t in time_cost:
        if t[3] not in BR_dict.keys():
            BR_dict[t[3]] = [t[6]+t[7]]
        else:
            BR_dict[t[3]].append(t[6]+t[7])
    ASR = round((sum([t[6]+t[7] for t in time_cost])/len(time_cost)), 9)
    TPS = round((len(time_cost) / last_time), 5)
    ACU = round(ASR * TPS, 5)
    for key in node_dict.keys():
        node_dict[key] = sorted(node_dict[key], key=lambda x: x[4])

    with open(f"{time_file_name}_node_dict.txt", "w") as f:
        for key in node_dict.keys():
            f.write(f"{key}:\n")
            for i in node_dict[key]:
                f.write(f"{i[0]}\t{i[1]}\t{i[4]}\t{i[5]}\t{i[6]}\n")
            f.write("----------------------------\n")
    # print("time:", time.time()-time0)
    with open(f"{time_file_name}_time_cost.txt", "w") as f:
        for i in time_cost:
            f.write(f"{i[0]}\t{i[1]}\t{i[4]}\t{i[5]}\t{i[6]}\t{i[7]}\n")
    with open(f"{time_file_name}_AEU_list.txt", "w") as f:
        for i in AEU_list:
            f.write(f"{i[0]}\t{i[1]}\t{i[2]}\n")
    with open(f"{time_file_name}_AEU_ASR_TPS_ACU.txt", "w") as f:
        f.write(f"AEU: {AEU}%, ASR: {ASR}, TPS: {TPS}, ACU: {ACU}\n")
    # print(f"AEU: {AEU}%, ASR: {ASR}, TPS: {TPS}, ACU: {ACU}, last_time: {round(last_time,9)}")
    return AEU, ASR, TPS, ACU, last_time, AEU_dict
