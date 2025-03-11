import random

from simulate.run import run, random_prob, random_idx
from global_profile.data_async import business_async
from global_profile.data_async_fork import business_async_fork
from global_profile.data_sync import business_sync
from global_profile.data_sync_fork import business_sync_fork
from RQ3.profile_36_64 import simulate_dict, actor_business
from global_profile.arrive import getPoissonArriveByNums
import os

path = os.getcwd()
print("20 people: 8 people per second")
# 20人 8人/秒
# 生成泊松分布的人数
simulate_dict["people_num"] = 20
simulate_dict["people_avg"] = 2
result = {'ASR': {'s': [], 'sc': [], 'a': [], 'ac': []}, 'TPS': {'s': [], 'sc': [], 'a': [], 'ac': []}, 'last_time': {'s': [], 'sc': [], 'a': [], 'ac': []}}
people_arr = getPoissonArriveByNums(simulate_dict["people_num"], simulate_dict["people_avg"])
# 生成概率
actor_prob, business_prob, path_prob = random_prob(simulate_dict["people_num"])
actor_prob = [0.5 for i in range(0, simulate_dict["people_num"])]
# read book 0.5 and print book 0.8 random
random.seed(1)
business_prob_a = [0.5,0.8,0.5,0.8,0.5,0.8,0.5,0.8,0.5,0.8,0.5,0.8,0.5,0.8,0.5,0.8,0.5,0.8,0.5,0.8]
business_prob_p = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8]
business_prob_r = [i for i in business_prob_a]
random.shuffle(business_prob_r)
business_prob_r2 = []
for i in business_prob_r:
    if i == 0.5:
        business_prob_r2.append(0.8)
    else:
        business_prob_r2.append(0.5)

for i in range(0, 1):
    simulate_dict['thread_dict'] = {
        "Controller Server": i+1,
        "Service Server": i+1,
        "DAO Server": i+1,
        "SQL DataBase": i+1,
        "Printer": i+1
    }
    exp_path = business_sync
    # simulate_dict, business_path, people_list, actor_prob, business_prob, path_prob
    file_name = path + "/tmp_result/" + "RBQ-s-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_r, path_prob, actor_business, file_name)
    result['ASR']['s'].append(ASR)
    result['TPS']['s'].append(TPS)
    result['last_time']['s'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_sync_fork
    file_name = path + "/tmp_result/" + "RBQ-sc-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_r, path_prob, actor_business, file_name)
    result['ASR']['sc'].append(ASR)
    result['TPS']['sc'].append(TPS)
    result['last_time']['sc'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async
    file_name = path + "/tmp_result/" + "RBQ-a-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_r, path_prob, actor_business, file_name)
    result['ASR']['a'].append(ASR)
    result['TPS']['a'].append(TPS)
    result['last_time']['a'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async_fork
    file_name = path + "/tmp_result/" + "RBQ-ac-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_r, path_prob, actor_business, file_name)
    result['ASR']['ac'].append(ASR)
    result['TPS']['ac'].append(TPS)
    result['last_time']['ac'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")




for i in range(0, 1):
    simulate_dict['thread_dict'] = {
        "Controller Server": i+1,
        "Service Server": i+1,
        "DAO Server": i+1,
        "SQL DataBase": i+1,
        "Printer": i+1
    }
    exp_path = business_sync
    # simulate_dict, business_path, people_list, actor_prob, business_prob, path_prob
    file_name = path + "/tmp_result/" + "ABQ-s-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_a, path_prob, actor_business, file_name)
    result['ASR']['s'].append(ASR)
    result['TPS']['s'].append(TPS)
    result['last_time']['s'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_sync_fork
    file_name = path + "/tmp_result/" + "ABQ-sc-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_a, path_prob, actor_business, file_name)
    result['ASR']['sc'].append(ASR)
    result['TPS']['sc'].append(TPS)
    result['last_time']['sc'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async
    file_name = path + "/tmp_result/" + "ABQ-a-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_a, path_prob, actor_business, file_name)
    result['ASR']['a'].append(ASR)
    result['TPS']['a'].append(TPS)
    result['last_time']['a'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async_fork
    file_name = path + "/tmp_result/" + "ABQ-ac-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_a, path_prob, actor_business, file_name)
    result['ASR']['ac'].append(ASR)
    result['TPS']['ac'].append(TPS)
    result['last_time']['ac'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

for i in range(0, 1):
    simulate_dict['thread_dict'] = {
        "Controller Server": i+1,
        "Service Server": i+1,
        "DAO Server": i+1,
        "SQL DataBase": i+1,
        "Printer": i+1
    }
    exp_path = business_sync
    # simulate_dict, business_path, people_list, actor_prob, business_prob, path_prob
    file_name = path + "/tmp_result/" + "PBQ-s-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_p, path_prob, actor_business, file_name)
    result['ASR']['s'].append(ASR)
    result['TPS']['s'].append(TPS)
    result['last_time']['s'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_sync_fork
    file_name = path + "/tmp_result/" + "PBQ-sc-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_p, path_prob, actor_business, file_name)
    result['ASR']['sc'].append(ASR)
    result['TPS']['sc'].append(TPS)
    result['last_time']['sc'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async
    file_name = path + "/tmp_result/" + "PBQ-a-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_p, path_prob, actor_business, file_name)
    result['ASR']['a'].append(ASR)
    result['TPS']['a'].append(TPS)
    result['last_time']['a'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async_fork
    file_name = path + "/tmp_result/" + "PBQ-ac-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_p, path_prob, actor_business, file_name)
    result['ASR']['ac'].append(ASR)
    result['TPS']['ac'].append(TPS)
    result['last_time']['ac'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

for i in range(0, 1):
    simulate_dict['thread_dict'] = {
        "Controller Server": i+1,
        "Service Server": i+1,
        "DAO Server": i+1,
        "SQL DataBase": i+1,
        "Printer": i+1
    }
    exp_path = business_sync
    # simulate_dict, business_path, people_list, actor_prob, business_prob, path_prob
    file_name = path + "/tmp_result/" + "SRBQ-s-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_r2, path_prob, actor_business, file_name)
    result['ASR']['s'].append(ASR)
    result['TPS']['s'].append(TPS)
    result['last_time']['s'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_sync_fork
    file_name = path + "/tmp_result/" + "SRBQ-sc-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_r2, path_prob, actor_business, file_name)
    result['ASR']['sc'].append(ASR)
    result['TPS']['sc'].append(TPS)
    result['last_time']['sc'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async
    file_name = path + "/tmp_result/" + "SRBQ-a-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_r2, path_prob, actor_business, file_name)
    result['ASR']['a'].append(ASR)
    result['TPS']['a'].append(TPS)
    result['last_time']['a'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async_fork
    file_name = path + "/tmp_result/" + "SRBQ-ac-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob_r2, path_prob, actor_business, file_name)
    result['ASR']['ac'].append(ASR)
    result['TPS']['ac'].append(TPS)
    result['last_time']['ac'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

with open(path + "/result/exp3-lambda-2.txt", "w") as f:
    for i in range(len(result['ASR']['s'])):
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(result['ASR']['s'][i], result['ASR']['sc'][i], result['ASR']['a'][i], result['ASR']['ac'][i], result['TPS']['s'][i],
                result['TPS']['sc'][i], result['TPS']['a'][i], result['TPS']['ac'][i], result['last_time']['s'][i], result['last_time']['sc'][i], result['last_time']['a'][i], result['last_time']['ac'][i]))

