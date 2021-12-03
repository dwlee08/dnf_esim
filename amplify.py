from random import *
from tqdm import tqdm

#설정
cube_cost = 125000 #모순가격
protect_cost = 11500000 #증보권 가격
max_enchant = 15 #최대 강화 수치 (15보다 크면 안됨)
retry = 100000 #목표 성공 횟수

#확률 및 비용
ratio = [1, 1, 1, 1, 0.8, 0.7, 0.6, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.2, 0.2]
cost = [258720, 258720, 258720, 258720, 258720, 258720, 258720, 258720, 258720, 258720, 258720, 258720, 258720, 258720, 258720]
cube = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

#중간값 계산용
ctf = [None, None, None, None]
ctf[1] = [0 for i in range(10000)]
ctf[2] = [0 for i in range(10000)]
ctf[3] = [0 for i in range(10000)]

def calculate():
    enchant = 0
    target_enchant = 1
    cost_sum = 0
    cube_sum = 0
    protect_sum = 0

    t_sum = 0
    s_sum = 0
    f_sum = 0
    t_cost_sum = 0
    t_cube_sum = 0
    t_protect_sum = 0

    t_cost_min = 1000000000000
    t_cost_max = 0
    try_max = 0
    c_try = 0

    pbar_update_rate = retry / 100

    pbar = None
    result = f"증폭 수치\t성공횟수\t실패횟수\t성공확률\t평균골드\t평균모순\t평균증보\t평균비용\t무기비용\t최소비용\t최대비용\t중간비용\t최대시도\n"
    while target_enchant <= max_enchant:
        v = uniform(0.0, 1.0)
        r = ratio[enchant]
  
        cost_sum += cost[enchant]
        cube_sum += cube[enchant]

        if enchant == target_enchant - 1:
            t_sum += 1
            c_try += 1
        if v < r:
            if enchant == (target_enchant - 1):
                s_sum += 1
            enchant += 1
        else:
            if enchant == target_enchant - 1:
                f_sum += 1

            if 4 <= enchant <= 6:
                enchant -= 1
            elif 7 <= enchant <= 9:
                enchant -= 3
            elif enchant >= 10:
                protect_sum += 1
                enchant = 0

        if enchant == target_enchant:
            t_cost_sum += cost_sum
            t_cube_sum += cube_sum
            t_protect_sum += protect_sum

            total = cost_sum + (cube_sum * cube_cost) + (protect_sum * protect_cost)

            if total < t_cost_min:
                t_cost_min = total

            if total > t_cost_max:
                t_cost_max = total
                try_max = c_try

            protect_sum = 0
            cost_sum = 0
            cube_sum = 0
            c_try = 0

            if 11 <= target_enchant <= 13:
                try:
                    totalidx = int(total / 10000000)
                    ctf[target_enchant - 10][totalidx]+=1
                except:
                    pass
            if pbar is None:
                desc = f"{target_enchant - 1} -> {target_enchant}"
                pbar = tqdm(total = 100, desc = desc, ncols=80)
            elif s_sum >= retry:
                i = target_enchant - 1
                srate = round(float(s_sum)/float(t_sum) * 100, 2)
                _totalcost = round(float(t_cost_sum) / s_sum)

                totalcost = _totalcost / 10000
                totalcost = str(round(totalcost)) + '만'

                totalcube = round(float(t_cube_sum) / s_sum)

                totalprotect = round(float(t_protect_sum) / s_sum)

                totalgold = _totalcost + (totalcube * cube_cost) + (totalprotect * protect_cost)
                totalgold /= 10000
                totalgold = str(round(totalgold)) + '만'

                mingold = t_cost_min / 10000
                mingold = str(round(mingold)) + '만'

                maxgold = t_cost_max / 10000
                maxgold = str(round(maxgold)) + '만'

                if 11 <= target_enchant <= 13:
                    cursor = 0
                    idx = 0
                    for k in ctf[target_enchant - 10]:
                        if cursor > (retry / 2):
                            break
                        cursor += k
                        idx += 1

                    midgold = idx * 1000
                    midgold = str(round(midgold)) + '만'
                else:
                    midgold = 'N/A'

                weapongold = _totalcost*2.857 + (totalcube * cube_cost) + (totalprotect * protect_cost)
                weapongold /= 10000
                weapongold = str(round(weapongold)) + '만'

                result += f"{i} -> {i+1}\t\t{s_sum}\t\t{f_sum}\t\t{srate}\t\t{totalcost}\t\t{totalcube}\t\t{totalprotect}\t\t{totalgold}\t\t{weapongold}\t\t{mingold}\t\t{maxgold}\t\t{midgold}\t\t{try_max}회\n"

                target_enchant += 1
              
                s_sum = 0
                f_sum = 0
                t_sum = 0
                t_cube_sum = 0
                t_cost_sum = 0
                t_protect_sum = 0
                t_cost_min = 1000000000000
                t_cost_max = 0
                count = 0
                try_max = 0
                pbar.update(1)
                pbar.close()
                pbar = None
            elif s_sum % pbar_update_rate == 0:
                pbar.update(1)

            enchant = 0
    print(result)

if __name__ == "__main__":
    calculate()


