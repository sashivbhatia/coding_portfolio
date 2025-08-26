import math
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as pyplot
import csv

# determines number of pipes to bring given input design
z = gp.Model("Z")

# defining inputs
# ___________________________________
# for first program
s1 = 20  # number of sections of design of length 1
s2 = 8   # number of sections of design of length 2
s3 = 8   # number of sections of design of length 3
s35 = 8  # number of sections of design of length 3.5
s4 = 0   # number of sections of design of length 4
s5 = 16  # number of sections of design of length 5
s6 = 10  # number of sections of design of length 6

Lens = [1, 2, 3, 3.5, 4, 5, 6]  # list of available pipe lengths in ascending order
avail = [35, 13, 18, 8, 10, 16, 4]  # list of lengths of pipes in same order as "Lens"

# for second program
N = 6   # maximum number of pipes that could fit in a bag
I = 21  # maximum number of rows of pipes in a bag
J = 4   # maximum number of bags allowed
Lmax = 6  # length of skibags in feet
Wmax = 45  # max weight of bag defined by airliner in lbs
Wempty = 2  # empty bag weight in lbs
rho = 0.35  # density of pipes in lb/ft

# ___________________________________
# determine vars from inputs
sideNums = [s1, s2, s3, s35, s4, s5, s6]
sides = [1]*s1 + [2]*s2 + [3]*s3 + [3.5]*s35 + [4]*s4 + [5]*s5 + [6]*s6
S = len(sides)
L = len(Lens)
Ns = sides[S-1] / Lens[0]
Ns = math.ceil(Ns)

# _____________________________________________________
# Adding Variables
# add variables for design blueprint
p = z.addVars(L, Ns, S, vtype=GRB.BINARY)

# add variables for packing
b = z.addVars(L, N, I, J, vtype=GRB.BINARY)
bInUse = z.addVars(J, vtype=GRB.BINARY)
bRowInUse = z.addVars(I, J, vtype=GRB.BINARY)

# _____________________________________________________
# constraints
# _____________________________________________________
# Design Blueprint Constraints
# implicit constraint

# Design Blueprint Constraint 1
for l in range(L):
    for s in range(S):
        sum = 0
        for n in range(N):
            sum = sum + p[l, n, s]
        z.addConstr(sum <= 1)

# side lengths are all met
# Design Blueprint Constraint 2
for s in range(S):
    sum = 0
    for l in range(L):
        for n in range(Ns):
            sum += p[l, n, s] * Lens[l] * n
    z.addConstr(sum == sides[s])

# available pipes are not exceeded
# Design Blueprint Constraint 3
for l in range(L):
    sum = 0
    for s in range(S):
        for n in range(Ns):
            sum += p[l, n, s] * n
    z.addConstr(sum <= avail[l])

# _____________________________________________________
# Packing Constraints
# implicit constraint
# Packing Constraint 1
for l in range(L):
    for i in range(I):
        for j in range(J):
            sum = 0
            for n in range(N):
                sum = sum + b[l, n, i, j]
            z.addConstr(sum <= 1)

# ifBagNotInUse (if bInUse[j]=0), then b[l,n,i,j]=0
# Packing Constraint 2
for j in range(J):
    for i in range(I):
        for n in range(N):
            for l in range(L):
                sum += b[l, n, i, j]
                z.addConstr((bInUse[j] == 0) >> (b[l, n, i, j] == 0))
                z.addConstr((b[l, n, i, j] == 1) >> (bInUse[j] == 1))

# ifRowNotInUse (if bRowInUse[j]=0), then b[l,n,i,j]=0
# Packing Constraint 2
for j in range(J):
    for i in range(I):
        for n in range(N):
            for l in range(L):
                z.addConstr((bRowInUse[i, j] == 0) >> (b[l, n, i, j] == 0))
                z.addConstr((b[l, n, i, j] == 1) >> (bRowInUse[i, j] == 1))

# spatial constraint
# Packing Constraint 3
for i in range(I):
    for j in range(J):
        length = 0
        for n in range(N):
            for l in range(L):
                length += b[l, n, i, j] * n * Lens[l]
        z.addConstr(length <= Lmax)

# weight constraint
# Packing Constraint 4
for j in range(J):
    weight = 0
    for i in range(I):
        for n in range(N):
            for l in range(L):
                weight = weight + b[l, n, i, j] * n * Lens[l] * rho
    z.addConstr(weight <= Wmax - Wempty)

# _____________________________________________________
# Combining Design Blueprint and Packing Constraint
# Counting number of pipes of each length used in Design Blueprint
nums = [0] * L
for l in range(L):
    sum = 0
    for s in range(S):
        for n in range(Ns):
            sum += n * p[l, n, s]
    nums[l] = sum

# Number of pipes in design blueprint is same as number in packing
# Combine Constraint 1
for l in range(L):
    sum = 0
    for i in range(I):
        for n in range(N):
            for j in range(J):
                sum += b[l, n, i, j] * n
    z.addConstr(sum == nums[l])

# defining objective function
# _____________________________________________________
# counting number of bags used
nB = 0.0
for j in range(J):
    nB += bInUse[j]

# counting number of rows used
nRow = 0.0
for j in range(J):
    for i in range(I):
        nRow += bRowInUse[i, j]

# counting number of pipes used
nPipes = 0
for s in range(S):
    for l in range(L):
        for n in range(Ns):
            nPipes += p[l, n, s] * n

z.setObjective(1000*nB + 10*nRow + nPipes, GRB.MINIMIZE)
z.optimize()

# _____________________________________________________
# Outputting Solution
print()
print(f"SOLUTION:")
print()

# Outputting Design Blueprint
print()
print(f"Set Design Blueprint:")
print()

sideIndex = 0
for sideLength in range(L):
    if sideNums[sideLength] > 0:
        print(f"{sideNums[sideLength]} sides of length {Lens[sideLength]}’ are needed in the"
              f"These sides are made up of the following combinations of pipes:")
        for index in range(sideNums[sideLength]):
            print(f" _____________________________")
            for l in range(L):
                for n in range(Ns):
                    if p[l, n, index+sideIndex].X == 1:
                        print(f" {n} pipe(s) of length {Lens[l]}’")
            print(f" -----------------------------")
        sideIndex += sideNums[sideLength]

# Outputting packing configuration
print()
print(f"Bag Packing List and Configuration:")
print()
print(f"_____________________________")
for l in range(L):
    sum = 0
    for s in range(S):
        for n in range(Ns):
            sum += n * p[l, n, s].X
    print(f"{sum} pipes of length {Lens[l]}’")
print(f"_____________________________")

# Finding total pipe length in and Weight of Bags
totalLengthInBag = [0] * J
totalWeightOfBag = [Wempty] * J
for j in range(J):
    for i in range(I):
        for l in range(L):
            for n in range(N):
                totalLengthInBag[j] += b[l, n, i, j].X * n * Lens[l]
                totalWeightOfBag[j] += b[l, n, i, j].X * n * Lens[l] * rho

# Printing the packing output
bagNum = 1
counts = [0] * len(Lens)
for j in range(J):
    if bInUse[j].X == 1:
        print(f"_____________________________")
        print(f"Bag {bagNum}:")
        print()
        print(f"Total Weight: {round(totalWeightOfBag[j],1)} pounds")
        print(f"Percent of Volume Used: {round(100*totalLengthInBag[j]/(I*Lmax))}%")
        print()
        bagNum += 1
        rowNum = 1
        for i in range(I):
            if bRowInUse[i, j].X == 1:
                print(f" Row {rowNum}")
                rowNum += 1
                for l in range(L):
                    for n in range(N):
                        if b[l, n, i, j].X == 1:
                            print(f" {n} pipe(s) of length {Lens[l]}’")
                            counts[l] += n
        print(f"_____________________________")

# testing to make sure solution has right number of pipes included
# print(counts)
