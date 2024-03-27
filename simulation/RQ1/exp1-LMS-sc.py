from simulate.run import run, random_prob
from global_profile.data_sync_fork import business_sync_fork
from RQ1.profile import simulate_dict, actor_business
from global_profile.arrive import getPoissonArriveByNums
import os

path = os.getcwd()
exp_path = business_sync_fork

print("10 people: 2, 4, 8 people per second")
# 10人 2人/秒
# 生成泊松分布的人数
people_arr = getPoissonArriveByNums(simulate_dict["people_num"], simulate_dict["people_avg"])
# 生成概率
actor_prob, business_prob, path_prob = random_prob(simulate_dict["people_num"])
# 将人员概率改为学生，将业务概率改为下载书籍
actor_prob = [0.5 for i in range(simulate_dict["people_num"])]
business_prob = [0.98 for i in range(simulate_dict["people_num"])]
path_prob = [0.5 for i in range(simulate_dict["people_num"])]
# simulate_dict, business_path, people_list, actor_prob, business_prob, path_prob
file_name = path + "/result/" + "10-path1-2-sc-"
print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
print(f"AEU: {AEU}%, ASR: {ASR}, TPS: {TPS}, ACU: {ACU}, last_time: {round(last_time,9)}")
print("-------------------------------------------------")
# 10人 4人/秒
people_arr = getPoissonArriveByNums(simulate_dict["people_num"], 2 * simulate_dict["people_avg"])
file_name = path + "/result/" + "10-path1-4-sc-"
print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
print(f"AEU: {AEU}%, ASR: {ASR}, TPS: {TPS}, ACU: {ACU}, last_time: {round(last_time,9)}")
print("-------------------------------------------------")

# 10人 8人/秒
people_arr = getPoissonArriveByNums(simulate_dict["people_num"], 4 * simulate_dict["people_avg"])
file_name = path + "/result/" + "10-path1-8-sc-"
print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
print(f"AEU: {AEU}%, ASR: {ASR}, TPS: {TPS}, ACU: {ACU}, last_time: {round(last_time,9)}")
print("-------------------------------------------------")
print("\n20 people: 2, 4, 8 people per second")
# 20人 2人/秒
# 生成泊松分布的人数
simulate_dict["people_num"] = 20
people_arr = getPoissonArriveByNums(simulate_dict["people_num"], simulate_dict["people_avg"])
# 生成概率
actor_prob, business_prob, path_prob = random_prob(simulate_dict["people_num"])
# 将人员概率改为学生，将业务概率改为下载书籍
actor_prob = [0.5 for i in range(simulate_dict["people_num"])]
business_prob = [0.98 for i in range(simulate_dict["people_num"])]
path_prob = [0.5 for i in range(simulate_dict["people_num"])]
# simulate_dict, business_path, people_list, actor_prob, business_prob, path_prob
file_name = path + "/result/" + "20-path1-2-sc-"
print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
print(f"AEU: {AEU}%, ASR: {ASR}, TPS: {TPS}, ACU: {ACU}, last_time: {round(last_time,9)}")
print("-------------------------------------------------")
# 20人 4人/秒
people_arr = getPoissonArriveByNums(simulate_dict["people_num"], 2 * simulate_dict["people_avg"])
file_name = path + "/result/" + "20-path1-4-sc-"
print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
print(f"AEU: {AEU}%, ASR: {ASR}, TPS: {TPS}, ACU: {ACU}, last_time: {round(last_time,9)}")
print("-------------------------------------------------")

# 20人 8人/秒
people_arr = getPoissonArriveByNums(simulate_dict["people_num"], 4 * simulate_dict["people_avg"])
file_name = path + "/result/" + "20-path1-8-sc-"
print(file_name)
AEU, ASR, TPS, ACU, last_time, AEU_dict = run(simulate_dict, exp_path, people_arr, actor_prob, business_prob, path_prob, actor_business, file_name)
print(f"AEU: {AEU}%, ASR: {ASR}, TPS: {TPS}, ACU: {ACU}, last_time: {round(last_time,9)}")
print("-------------------------------------------------")

