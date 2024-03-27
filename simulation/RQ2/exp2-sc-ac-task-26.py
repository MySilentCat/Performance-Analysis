from simulate.run import run, random_prob
from global_profile.data_async_fork import business_async_fork
from global_profile.data_sync_fork import business_sync_fork
from RQ2.profile import simulate_dict, actor_business
from global_profile.arrive import getPoissonArriveByNums
import os

path = os.getcwd()

print("10 people: 4 people per second")
# 生成泊松分布的人数
simulate_dict["people_num"] = 10
simulate_dict["people_avg"] = 4

people_arr = getPoissonArriveByNums(simulate_dict["people_num"], simulate_dict["people_avg"])
# 生成概率
actor_prob, business_prob, path_prob = random_prob(simulate_dict["people_num"])
# 将人员概率改为学生，将业务概率改为下载书籍
actor_prob = [0.5 for i in range(simulate_dict["people_num"])]
business_prob = [0.98 for i in range(simulate_dict["people_num"])]
path_prob = [0.5 for i in range(simulate_dict["people_num"])]
# simulate_dict, business_path, people_list, actor_prob, business_prob, path_prob
result = {'ASR': {'s': [], 'sc': [], 'a': [], 'ac': []}, 'TPS': {'s': [], 'sc': [], 'a': [], 'ac': []}, 'last_time': {'s': [], 'sc': [], 'a': [], 'ac': []}}

# 4最小极值task
simulate_dict['thread_dict'] = {
    "Controller Server": 25,
    "Service Server": 25,
    "DAO Server": 25,
    "SQL DataBase": 25,
    "Printer": 25
}
exp_path = business_sync_fork
file_name = path + "/tmp_result/exp2-10-" + "all-task25-4-sc-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['sc'].append(ASR)
result['TPS']['sc'].append(TPS)
result['last_time']['sc'].append(last_time)
# print("------------------------------------------")

exp_path = business_async_fork
file_name = path + "/tmp_result/exp2-10-" + "all-task25-4-ac-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
# print("------------------------------------------")
result['ASR']['ac'].append(ASR)
result['TPS']['ac'].append(TPS)
result['last_time']['ac'].append(last_time)

simulate_dict['thread_dict'] = {
    "Controller Server": 26,
    "Service Server": 25,
    "DAO Server": 25,
    "SQL DataBase": 25,
    "Printer": 25
}
exp_path = business_sync_fork
file_name = path + "/tmp_result/exp2-10-" + "CS-task26-4-sc-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['sc'].append(ASR)
result['TPS']['sc'].append(TPS)
result['last_time']['sc'].append(last_time)
# print("------------------------------------------")


exp_path = business_async_fork
file_name = path + "/tmp_result/exp2-10-" + "CS-task26-4-ac-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
# print("------------------------------------------")
result['ASR']['ac'].append(ASR)
result['TPS']['ac'].append(TPS)
result['last_time']['ac'].append(last_time)

simulate_dict['thread_dict'] = {
    "Controller Server": 25,
    "Service Server": 26,
    "DAO Server": 25,
    "SQL DataBase": 25,
    "Printer": 25
}
exp_path = business_sync_fork
file_name = path + "/tmp_result/exp2-10-" + "SS-task26-4-sc-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['sc'].append(ASR)
result['TPS']['sc'].append(TPS)
result['last_time']['sc'].append(last_time)
# print("------------------------------------------")

exp_path = business_async_fork
file_name = path + "/tmp_result/exp2-10-" + "SS-task26-4-ac-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
# print("------------------------------------------")
result['ASR']['ac'].append(ASR)
result['TPS']['ac'].append(TPS)
result['last_time']['ac'].append(last_time)

simulate_dict['thread_dict'] = {
    "Controller Server": 25,
    "Service Server": 25,
    "DAO Server": 26,
    "SQL DataBase": 25,
    "Printer": 25
}
exp_path = business_sync_fork
file_name = path + "/tmp_result/exp2-10-" + "DS-task26-4-sc-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['sc'].append(ASR)
result['TPS']['sc'].append(TPS)
result['last_time']['sc'].append(last_time)
# print("------------------------------------------")

exp_path = business_async_fork
file_name = path + "/tmp_result/exp2-10-" + "DS-task26-4-ac-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
# print("------------------------------------------")
result['ASR']['ac'].append(ASR)
result['TPS']['ac'].append(TPS)
result['last_time']['ac'].append(last_time)

simulate_dict['thread_dict'] = {
    "Controller Server": 25,
    "Service Server": 25,
    "DAO Server": 25,
    "SQL DataBase": 26,
    "Printer": 25
}
exp_path = business_sync_fork
file_name = path + "/tmp_result/exp2-10-" + "SD-task26-4-sc-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['sc'].append(ASR)
result['TPS']['sc'].append(TPS)
result['last_time']['sc'].append(last_time)
# print("------------------------------------------")

exp_path = business_async_fork
file_name = path + "/tmp_result/exp2-10-" + "SD-task26-4-ac-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
# print("------------------------------------------")
result['ASR']['ac'].append(ASR)
result['TPS']['ac'].append(TPS)
result['last_time']['ac'].append(last_time)

simulate_dict['thread_dict'] = {
    "Controller Server": 26,
    "Service Server": 26,
    "DAO Server": 26,
    "SQL DataBase": 26,
    "Printer": 26
}
exp_path = business_sync_fork
file_name = path + "/tmp_result/exp2-10-" + "all-task26-4-sc-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['sc'].append(ASR)
result['TPS']['sc'].append(TPS)
result['last_time']['sc'].append(last_time)
# print("------------------------------------------")

exp_path = business_async_fork
file_name = path + "/tmp_result/exp2-10-" + "all-task26-4-ac-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
# print("------------------------------------------")
result['ASR']['ac'].append(ASR)
result['TPS']['ac'].append(TPS)
result['last_time']['ac'].append(last_time)

with open(path+'/result/exp2-sc-ac-task-26.txt', 'w') as f:
    for i in range(len(result["ASR"]["sc"])):
        f.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(result['ASR']['sc'][i], result['ASR']['ac'][i],
                                                  result['TPS']['sc'][i], result['TPS']['ac'][i],  result['last_time']['sc'][i], result['last_time']['ac'][i]))
