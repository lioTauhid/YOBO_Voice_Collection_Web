# Program

# 1. a <- not b, 0.9
# 2. b <- not c, 0.7
# 3. c <- t, not a, 0.7

# 4. t <- not p, 0.8

# 5. p <- not q, 0.6
# 6. q <- not r, 0.8
# 7. r <- not s, 0.9
# 8. s <- t, 0.7
# 9. s <- x, 0.6

# 10. x <- not x, 0.8
# 11. x <- t, 0.6
# new  line

# code
from numpy import random

inputList = []
for i in range(0, 8):
    x = round(random.uniform(0.5, 1), 2)
    inputList.append(x)
# print(dl)


t_0 = 0
p_0 = 0
q_0 = 0
r_0 = 0
s_0 = 0
x_0 = 0
z_0 = 0
print("i:  N(t)  N(p)  N(q)  N(r)  N(s)  N(x)")
print("----------------------------------------")

t = t_0
p = p_0
q = q_0
r = r_0
s = s_0
x = x_0

listData = []
isFound = False
clusterStart = 0
clusterEnd = 0
clusterDiffer = 0
clusterCount = 0
uniques = []
repeats = []
i = 0

# for i in range(0, 100):
while True:
    listData.append(f"{t:.2f} | {p:.2f} | {q:.2f} | {r:.2f} | {s:.2f} | {x:.2f}")
    t = float(min(1 - p_0, inputList[0]))
    p = float(min(1 - q_0, inputList[1]))
    q = float(min(1 - r_0, inputList[2]))
    r = float(min(1 - s_0, inputList[3]))
    s = float(max(min(1 - t_0, inputList[4]), min(x_0, inputList[5])))

    x = float(max(min(1 - t_0, inputList[6]), min(1 - x_0, inputList[7])))

    each = listData[i]
    if each not in uniques:
        uniques.insert(i, each)
        print(i, each)
        clusterEnd = i
        isFound = False
    else:
        if isFound:
            repeats.insert(i, each)
            clusterCount = clusterCount + 1
            print(i, each)
            if clusterCount == clusterDiffer:
                isFound = False
                clusterCount = 0
                print("--------------------Cluster End-----------------------")
                break
        else:
            print("-------------------Cluster Started--------------------")
            print(i, each)
            repeats.insert(i, each)
            clusterStart = uniques.index(each)
            clusterDiffer = clusterEnd - clusterStart + 1
            # print("Cluster element length : ", clusterDiffer)
            if clusterDiffer == 1:
                print("--------------------Cluster End-----------------------")
                break
            isFound = True
            clusterCount = clusterCount + 1
    t_0 = t
    p_0 = p
    q_0 = q
    r_0 = r
    s_0 = s
    x_0 = x
    i = i + 1

print(inputList)
print("----------------------------------------")
print("Average of Cluster")
# print("N(t): ", sum(list(map(float, repeats[0].split("|")))) / len(repeats))
nT, nP, nQ, nR, nS, nX = 0, 0, 0, 0, 0, 0
clusterLength = len(repeats)
for i in range(0, clusterLength):
    nT = nT + float(repeats[i].split("|")[0])
    nP = nP + float(repeats[i].split("|")[1])
    nQ = nQ + float(repeats[i].split("|")[2])
    nR = nR + float(repeats[i].split("|")[3])
    nS = nS + float(repeats[i].split("|")[4])
    nX = nX + float(repeats[i].split("|")[5])

print("N(t): ", nT / clusterLength)
print("N(p): ", nP / clusterLength)
print("N(q): ", nQ / clusterLength)
print("N(r): ", nR / clusterLength)
print("N(s): ", nS / clusterLength)
print("N(x): ", nX / clusterLength)
print("----------------------------------------")
print(f"Iterations count : {i}")
# print(f"Unique count : {len(uniques)}")
print(f"Cluster length : {clusterLength}")
