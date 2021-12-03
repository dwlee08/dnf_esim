from random import *
from tqdm import tqdm

#설정
ratio_inc = 0.03 #추가 강화 확률 3%
cube_cost = 125 #무큐 가격
protect_cost = 5300000 #장보권 가격
max_enchant = 15 #최대 강화 수치 (15보다 크면 안됨)
retry = 100 #목표 성공 횟수

#확률 및 비용
ratio = [1, 1, 1, 1, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.25, 0.15, 0.14, 0.13, 0.12]
cost = [354600, 354600, 354600, 354600, 709200, 780120, 851040, 921960, 992880, 1063800, 1063800, 1773000, 2836800, 4255200, 6028200]
cube = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200]

#중간값 계산용
ctf = [None, None, None, None]
ctf[1] = [0 for i in range(1000)]
ctf[2] = [0 for i in range(1000)]
ctf[3] = [0 for i in range(1000)]

def calculate():
    enchant = 0
    target_enchant = 1
    fail11 = 0
    fail12 = 0
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

    result = f"강화 수치\t성공횟수\t실패횟수\t성공확률\t평균골드\t평균무큐\t평균장보\t평균비용\t최소비용\t최대비용\t중간비용\t최대시도\n"
    pbar = None
    while target_enchant <= max_enchant:
        v = uniform(0.0, 1.0)
        r = ratio[enchant] + ratio_inc

        #11강 12강 실패시 확률 보정(테두리)
        if enchant == 10:
            r += (fail11 * 0.01)
        elif enchant == 11:
            r += (fail12 * 0.01)

        cost_sum += cost[enchant]
        cube_sum += cube[enchant]
        
        if enchant == target_enchant - 1:
            t_sum += 1
            c_try += 1

        if v < r: #성공
            if enchant == target_enchant - 1:
                s_sum += 1
            if enchant == 10:
                fail11 = 0
            elif enchant == 11:
                fail12 = 0
            enchant += 1
        else: #실패
            if enchant == target_enchant - 1:
                f_sum += 1
            if enchant < 10:
                enchant = enchant    
            elif enchant == 10:
                fail11 += 1
                enchant -= 3
            elif enchant == 11:
                fail12 += 1
                enchant -= 3
            else:
                protect_sum += 1
                enchant = 0
        
        #목표 강화 수치 도달
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
                #프로그레스 바 초기화
                desc = f"{target_enchant - 1} -> {target_enchant}"
                pbar = tqdm(total = 100, desc = desc, ncols=80)
            elif s_sum >= retry:
                #현재 수치 강화 종료: 결과 기록
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

                result += f"{i} -> {i+1}\t\t{s_sum}\t\t{f_sum}\t\t{srate}\t\t{totalcost}\t\t{totalcube}\t\t{totalprotect}\t\t{totalgold}\t\t{mingold}\t\t{maxgold}\t\t{midgold}\t\t{try_max}회\n"                               
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
                #프로그레스바 업데이트
                pbar.update(1)

            enchant = 0

    print(result)
    #print(ctf)

if __name__ == "__main__":
    calculate()


