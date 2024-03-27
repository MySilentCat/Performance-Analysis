from simulate.run import run, random_prob
from global_profile.data_async import business_async
from global_profile.data_async_fork import business_async_fork
from global_profile.data_sync import business_sync
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

i = 0
for i in range(1, 30):
    simulate_dict['thread_dict'] = {
        "Controller Server": i,
        "Service Server": i,
        "DAO Server": i,
        "SQL DataBase": i,
        "Printer": i
    }

    exp_path = business_sync
    file_name = path + "/tmp_result/exp1-10-task" + str(i) + "-4-s-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
    result['ASR']['s'].append(ASR)
    result['TPS']['s'].append(TPS)
    result['last_time']['s'].append(last_time)
    # print("------------------------------------------")

    exp_path = business_sync_fork
    file_name = path + "/tmp_result/exp1-10-task" + str(i) + "-4-sc-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
    result['ASR']['sc'].append(ASR)
    result['TPS']['sc'].append(TPS)
    result['last_time']['sc'].append(last_time)
    # print("------------------------------------------")

    exp_path = business_async
    file_name = path + "/tmp_result/exp1-10-task" + str(i) + "-4-a-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
    result['ASR']['a'].append(ASR)
    result['TPS']['a'].append(TPS)
    result['last_time']['a'].append(last_time)
    # print("------------------------------------------")

    exp_path = business_async_fork
    file_name = path + "/tmp_result/exp1-10-task" + str(i) + "-4-ac-"
    # print(file_name)
    AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
    # print("------------------------------------------")
    result['ASR']['ac'].append(ASR)
    result['TPS']['ac'].append(TPS)
    result['last_time']['ac'].append(last_time)

with open(path + '/result/exp1-multi-task.txt', 'w') as f:
    for i in range(1, 30):
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(result['ASR']['s'][i-1], result['ASR']['sc'][i-1], result['ASR']['a'][i-1],
                result['ASR']['ac'][i-1], result['TPS']['s'][i-1], result['TPS']['sc'][i-1], result['TPS']['a'][i-1], result['TPS']['ac'][i-1], result['last_time']['s'][i-1], result['last_time']['sc'][i-1], result['last_time']['a'][i-1], result['last_time']['ac'][i-1]))
