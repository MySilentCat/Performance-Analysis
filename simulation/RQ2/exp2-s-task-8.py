from simulate.run import run, random_prob
from global_profile.data_async import business_async
from global_profile.data_sync import business_sync
from RQ2.profile import simulate_dict, actor_business
from global_profile.arrive import getPoissonArriveByNums
import os

path = os.getcwd()

print("10 people: 8 people per second")
# 生成泊松分布的人数
simulate_dict["people_num"] = 10
simulate_dict["people_avg"] = 8

people_arr = getPoissonArriveByNums(simulate_dict["people_num"], simulate_dict["people_avg"])
# 生成概率
actor_prob, business_prob, path_prob = random_prob(simulate_dict["people_num"])
# 将人员概率改为学生，将业务概率改为下载书籍
actor_prob = [0.5 for i in range(simulate_dict["people_num"])]
business_prob = [0.98 for i in range(simulate_dict["people_num"])]
path_prob = [0.5 for i in range(simulate_dict["people_num"])]
# simulate_dict, business_path, people_list, actor_prob, business_prob, path_prob
result = {'ASR': {'s': [], 'sc': [], 'a': [], 'ac': []}, 'TPS': {'s': [], 'sc': [], 'a': [], 'ac': []}, 'last_time': {'s': [], 'sc': [], 'a': [], 'ac': []}}

# 8最小极值task
simulate_dict['thread_dict'] = {
    "Controller Server": 7,
    "Service Server": 7,
    "DAO Server": 7,
    "SQL DataBase": 7,
    "Printer": 7
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "all-task7-8-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)


simulate_dict['thread_dict'] = {
    "Controller Server": 8,
    "Service Server": 7,
    "DAO Server": 7,
    "SQL DataBase": 7,
    "Printer": 7
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "CS-task8-8-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)


simulate_dict['thread_dict'] = {
    "Controller Server": 7,
    "Service Server": 8,
    "DAO Server": 7,
    "SQL DataBase": 7,
    "Printer": 7
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "SS-task8-8-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)



simulate_dict['thread_dict'] = {
    "Controller Server": 7,
    "Service Server": 7,
    "DAO Server": 8,
    "SQL DataBase": 7,
    "Printer": 7
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "DS-task8-8-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)



simulate_dict['thread_dict'] = {
    "Controller Server": 7,
    "Service Server": 7,
    "DAO Server": 7,
    "SQL DataBase": 8,
    "Printer": 7
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "SD-task8-8-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)



simulate_dict['thread_dict'] = {
    "Controller Server": 8,
    "Service Server": 8,
    "DAO Server": 8,
    "SQL DataBase": 8,
    "Printer": 8
}

exp_path = business_sync
file_name = path + "/tmp_result/exp2-10-" + "all-task8-8-s-"
# print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
result['ASR']['s'].append(ASR)
result['TPS']['s'].append(TPS)
result['last_time']['s'].append(last_time)


with open(path+'/result/exp2-s-task-8.txt', 'w') as f:
    for i in range(len(result["ASR"]["s"])):
        f.write('{}\t{}\t{}\n'.format(result['ASR']['s'][i],
                                                  result['TPS']['s'][i], result['last_time']['s'][i]))
