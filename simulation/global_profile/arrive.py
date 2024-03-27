import random
import math


def rand(l):
    """
    :param l:
    :return: delta t
    """
    random.seed(12)
    z = random.random()
    return -(1 / l) * math.log(z)


def getPoissonArriveByNums(nums, l):
    """
    :param nums: total number of people
    :param l: average number of people per second
    :return:
    """
    total = 0
    res = []
    for i in range(nums):
        total += rand(l)
        res.append((i, round(total, 9)))
    return res


def getPoissonArriveByTime(time, l):
    """
    :param time: total time
    :param l: average number of people per second
    :return:
    """
    total = 0
    res = []
    i = 0
    while True:
        total += rand(l)
        if total > time:
            break
        res.append((i, round(total, 9)))
        i += 1
    return res


if __name__ == '__main__':
    people = getPoissonArriveByNums(20, 5)
    print(people)
