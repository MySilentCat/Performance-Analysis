from simulate.run import run, random_prob
from global_profile.data_async import business_async
from global_profile.data_sync import business_sync
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

# 28最小极值task
simulate_dict['thread_dict'] = {
    "Controller Server": 27,
    "Service Server": 27,
    "DAO Server": 27,
    "SQL DataBase": 27,
    "Printer": 27
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "all-task27-4-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)
# print("------------------------------------------")

exp_path = business_async
file_name = path + "/tmp_result/exp2-10-" + "all-task27-4-a-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['a'].append(ASR)
result['TPS']['a'].append(TPS)
result['last_time']['a'].append(last_time)
# print("------------------------------------------")


simulate_dict['thread_dict'] = {
    "Controller Server": 28,
    "Service Server": 27,
    "DAO Server": 27,
    "SQL DataBase": 27,
    "Printer": 27
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "CS-task28-4-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)
# print("------------------------------------------")

exp_path = business_async
file_name = path + "/tmp_result/exp2-10-" + "CS-task28-4-a-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['a'].append(ASR)
result['TPS']['a'].append(TPS)
result['last_time']['a'].append(last_time)
# print("------------------------------------------")


simulate_dict['thread_dict'] = {
    "Controller Server": 27,
    "Service Server": 28,
    "DAO Server": 27,
    "SQL DataBase": 27,
    "Printer": 27
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "SS-task28-4-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)
# print("------------------------------------------")

exp_path = business_async
file_name = path + "/tmp_result/exp2-10-" + "SS-task28-4-a-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['a'].append(ASR)
result['TPS']['a'].append(TPS)
result['last_time']['a'].append(last_time)
# print("------------------------------------------")


simulate_dict['thread_dict'] = {
    "Controller Server": 27,
    "Service Server": 27,
    "DAO Server": 28,
    "SQL DataBase": 27,
    "Printer": 27
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "DS-task28-4-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)
# print("------------------------------------------")

exp_path = business_async
file_name = path + "/tmp_result/exp2-10-" + "DS-task28-4-a-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['a'].append(ASR)
result['TPS']['a'].append(TPS)
result['last_time']['a'].append(last_time)
# print("------------------------------------------")


simulate_dict['thread_dict'] = {
    "Controller Server": 27,
    "Service Server": 27,
    "DAO Server": 27,
    "SQL DataBase": 28,
    "Printer": 27
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "SD-task28-4-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)
# print("------------------------------------------")

exp_path = business_async
file_name = path + "/tmp_result/exp2-10-" + "SD-task28-4-a-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['a'].append(ASR)
result['TPS']['a'].append(TPS)
result['last_time']['a'].append(last_time)
# print("------------------------------------------")


simulate_dict['thread_dict'] = {
    "Controller Server": 28,
    "Service Server": 28,
    "DAO Server": 28,
    "SQL DataBase": 28,
    "Printer": 28
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "all-task28-4-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)
# print("------------------------------------------")

exp_path = business_async
file_name = path + "/tmp_result/exp2-10-" + "all-task28-4-a-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['a'].append(ASR)
result['TPS']['a'].append(TPS)
result['last_time']['a'].append(last_time)
# print("------------------------------------------")

# simulate_dict['thread_dict'] = {
#     "Controller Server": 28,
#     "Service Server": 28,
#     "DAO Server": 27,
#     "SQL DataBase": 27,
#     "Printer": 27
# }
#
# exp_path = business_sync
# file_name = path + "/result/" + "100-path1-4-s-"
# # print(file_name)
# AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
# result['ASR']['s'].append(ASR)
# result['TPS']['s'].append(TPS)
# result['last_time']['s'].append(last_time)
# # print("------------------------------------------")
#
# exp_path = business_async
# file_name = path + "/result/" + "100-path1-4-a-"
# # print(file_name)
# AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
# result['ASR']['a'].append(ASR)
# result['TPS']['a'].append(TPS)
# result['last_time']['a'].append(last_time)
# # print("------------------------------------------")

with open(path+'/result/exp2-s-a-task-28.txt', 'w') as f:
    for i in range(len(result["ASR"]["s"])):
        f.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(result['ASR']['s'][i], result['ASR']['a'][i],
                                                  result['TPS']['s'][i], result['TPS']['a'][i],  result['last_time']['s'][i], result['last_time']['a'][i]))
