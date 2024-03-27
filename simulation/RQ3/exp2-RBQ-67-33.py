from simulate.run import run, random_prob
from global_profile.data_async import business_async
from global_profile.data_async_fork import business_async_fork
from global_profile.data_sync import business_sync
from global_profile.data_sync_fork import business_sync_fork
from RQ3.profile_67_33 import simulate_dict, actor_business
from global_profile.arrive import getPoissonArriveByNums
import os

path = os.getcwd()

print("100 people: 4 people per second")
# 100人 4人/秒
# 生成泊松分布的人数
simulate_dict["people_num"] = 100
simulate_dict["people_avg"] = 4
result = {'ASR': {'s': [], 'sc': [], 'a': [], 'ac': []}, 'TPS': {'s': [], 'sc': [], 'a': [], 'ac': []}, 'last_time': {'s': [], 'sc': [], 'a': [], 'ac': []}}
people_arr = getPoissonArriveByNums(simulate_dict["people_num"], simulate_dict["people_avg"])
# 生成概率
actor_prob, business_prob, path_prob = random_prob(simulate_dict["people_num"])

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
    file_name = path + "/tmp_result/" + "67-33-RBQ-s-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
    result['ASR']['s'].append(ASR)
    result['TPS']['s'].append(TPS)
    result['last_time']['s'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_sync_fork
    file_name = path + "/tmp_result/" + "67-33-RBQ-sc-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
    result['ASR']['sc'].append(ASR)
    result['TPS']['sc'].append(TPS)
    result['last_time']['sc'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async
    file_name = path + "/tmp_result/" + "67-33-RBQ-a-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
    result['ASR']['a'].append(ASR)
    result['TPS']['a'].append(TPS)
    result['last_time']['a'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")

    exp_path = business_async_fork
    file_name = path + "/tmp_result/" + "67-33-RBQ-ac-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
    result['ASR']['ac'].append(ASR)
    result['TPS']['ac'].append(TPS)
    result['last_time']['ac'].append(last_time)
    # print(AEU)
    # print("-------------------------------------------------")


with open(path + "/result/exp2-RBQ-67-33.txt", "w") as f:
    for i in range(len(result['ASR']['s'])):
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(result['ASR']['s'][i], result['ASR']['sc'][i], result['ASR']['a'][i], result['ASR']['ac'][i], result['TPS']['s'][i],
                result['TPS']['sc'][i], result['TPS']['a'][i], result['TPS']['ac'][i], result['last_time']['s'][i], result['last_time']['sc'][i], result['last_time']['a'][i], result['last_time']['ac'][i]))
