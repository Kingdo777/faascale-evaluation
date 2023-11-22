import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import burr
import random

TIME = 0
MEMORY = 1
num_samples = 1000

page_fault_overhead_per_MB = 0.821
page_fault_overhead_per_MB_pre_pop = 0.0039


def gen_memory_data():
    # 设置Burr分布的参数
    c = 11.652
    d = 0.221
    lam = 107.083

    # 生成符合Burr分布的随机数据
    data = burr.rvs(c, d, loc=lam, scale=280, size=num_samples)

    return data.tolist()


def gen_time_data():
    log_mean = -0.38
    log_std_dev = 2.36
    data = np.random.lognormal(mean=log_mean, sigma=log_std_dev, size=num_samples)
    return data.tolist()


def plt_cdf(data, xticks):
    # 计算模拟数据的CDF
    x = np.sort(data)
    y = np.arange(1, len(x) + 1) / len(x)

    # 绘制模拟数据的CDF，使用对数坐标轴和小数纵坐标
    plt.semilogx(x, y, label='Empirical CDF')

    # 设置x轴刻度为指定的值
    plt.xticks(xticks)
    plt.yticks([0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
    # 启用网格线
    # 启用纵向和横向网格线
    plt.grid(which='both', linestyle='--', linewidth=0.5)

    plt.title("Empirical CDF of Burr Distribution (log scale x-axis)")
    plt.xlabel("Value (log scale)")
    plt.ylabel("Cumulative Probability")
    plt.legend()
    plt.show()


def generate_random_number(max_value):
    # 生成 [1, max_value] 范围内的随机整数
    random_number = random.randint(1, max_value)
    return random_number


def generate_sorted_random_array(n, sort=True):
    # 生成包含 n 个 [1, 99] 之间的随机数的数组
    random_array = [random.randint(1, 99) for _ in range(n)]

    # 对数组进行排序
    if sort:
        sorted_array = sorted(random_array)
    else:
        sorted_array = random_array
    return sorted_array


def generate_sorted_poisson_random_array(n, lambda_param=20, min_=1, max_=99, sort=False):
    # 生成符合泊松分布的随机数数组
    poisson_random_array = np.random.poisson(lam=lambda_param, size=n)

    # 将数组中的值限制在 [1, 99] 范围内
    poisson_random_array = np.clip(poisson_random_array, min_, max_)

    # 对数组进行排序
    if sort:
        sorted_array = np.sort(poisson_random_array)
    else:
        sorted_array = poisson_random_array

    return sorted_array.tolist()


def plot_points(points1, points2, points3, points4):
    x1, y1 = zip(*points1)
    x2, y2 = zip(*points2)
    x3, y3 = zip(*points3)
    x4, y4 = zip(*points4)

    plt.scatter(x1, y1, color='blue', label='Lazy-Population', s=10)
    plt.scatter(x2, y2, color='red', label='Pre-Population', s=10)
    plt.scatter(x3, y3, color='green', label='Lazy-Population-Recycle', s=10)
    plt.scatter(x4, y4, color='yellow', label='Pre-Population-Recycle', s=10)

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('2D Point Plot')
    plt.legend()
    plt.xscale('log')  # 将横轴设置为对数刻度
    # plt.xlim(0.1, 1000)
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    time_data = list(sorted(map(lambda x: max(1, int(x * 1000)), gen_time_data())))
    memory_data = list(sorted(map(lambda x: int(x), gen_memory_data())))

    # plt_cdf(time_data, [1, 10, 100, 1000, 10000, 100000, 1000000])
    # plt_cdf(memory_data, [100, 1000])

    time_memory_tuple = list(zip(time_data, memory_data))

    pop_overhead_percent_utilization_list = []
    pop_recycle_overhead_percent_utilization_list = []
    pre_pop_overhead_percent_utilization_list = []
    pre_pop_recycle_overhead_percent_utilization_list = []

    recycle_count = []

    for function in time_memory_tuple:
        reach_max_memory_time = generate_random_number(function[TIME])
        mem_usage_percent_before = generate_sorted_random_array(reach_max_memory_time - 1) + [100]
        mem_usage_percent_after = generate_sorted_random_array(function[TIME] - reach_max_memory_time)
        mem_usage_percent_after_recycle = list(map(lambda x: max(x, 85), mem_usage_percent_after))
        mem_usage_percents = mem_usage_percent_before + mem_usage_percent_after
        mem_usage_percents_recycle = mem_usage_percent_before + mem_usage_percent_after_recycle

        pop_overhead = page_fault_overhead_per_MB * function[MEMORY]
        pre_pop_overhead = page_fault_overhead_per_MB_pre_pop * function[MEMORY]
        pop_overhead_percent = pop_overhead / function[TIME] * 100
        pre_pop_overhead_percent = pre_pop_overhead / function[TIME] * 100

        pre_pop_utilization = sum(mem_usage_percents) / len(mem_usage_percents)
        max_m = mem_usage_percents[0]
        pop_utilization = mem_usage_percents[0] / max_m * 100
        for m in mem_usage_percents[1:]:
            if m > max_m:
                max_m = m
            pop_utilization += ((m / max_m) * 100)
        pop_utilization /= len(mem_usage_percents)
        pop_overhead_percent_utilization_list.append((pop_overhead_percent, pop_utilization))
        pre_pop_overhead_percent_utilization_list.append((pre_pop_overhead_percent, pre_pop_utilization))

        pre_pop_utilization_recycle = sum(mem_usage_percents_recycle) / len(mem_usage_percents_recycle)
        max_m = mem_usage_percents_recycle[0]
        pop_utilization_recycle = mem_usage_percents_recycle[0] / max_m * 100
        for m in mem_usage_percents_recycle[1:]:
            if m > max_m:
                max_m = m
            pop_utilization_recycle += ((m / max_m) * 100)
        pop_utilization_recycle /= len(mem_usage_percents_recycle)
        pop_recycle_overhead_percent_utilization_list.append((pop_overhead_percent, pop_utilization_recycle))
        pre_pop_recycle_overhead_percent_utilization_list.append(
            (pre_pop_overhead_percent, pre_pop_utilization_recycle))

        if len(mem_usage_percent_after) > 0:
            pre_v = mem_usage_percent_after[0]
            count = 0
            for item in mem_usage_percent_after:
                if item - pre_v > 10:
                    count += item - pre_v
            recycle_count.append(int(count * function[MEMORY] / 100))
        else:
            recycle_count.append(0)

    plot_points(pop_overhead_percent_utilization_list, pre_pop_overhead_percent_utilization_list,
                pop_recycle_overhead_percent_utilization_list, pre_pop_recycle_overhead_percent_utilization_list)

    print("pop_overhead_percent_utilization_list:")
    print(pop_overhead_percent_utilization_list)

    print("pre_pop_overhead_percent_utilization_list:")
    print(pre_pop_overhead_percent_utilization_list)

    print("pop_recycle_overhead_percent_utilization_list:")
    print(pop_recycle_overhead_percent_utilization_list)

    print("pre_pop_recycle_overhead_percent_utilization_list:")
    print(pre_pop_recycle_overhead_percent_utilization_list)

    print("recycle_count:")
    print(recycle_count)
