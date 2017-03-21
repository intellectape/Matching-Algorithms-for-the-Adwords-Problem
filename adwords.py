"""
This file is created by:
Name: Aditya Bhardwaj
Unity ID: abhardw2
Project Title: Matching Algorithms for the Adwords Problem (Project 5)
"""

import numpy as np
import pandas as pd
import sys
import csv
import random
import operator
import collections
import math

random.seed(0)

# User input for greedy/ balance/ msvv
if len(sys.argv) != 2:
    print("python adwords.py <greedy | balance | msvv>")
    exit(1)

budget = {}
matching = {}
spending = {}
algorithm = sys.argv[1]
queries = []
opt = 0
ans = 0
alg = 0


def main(): 
    global alg, opt, budget, matching

    load_queries()
    load_adwords_graph()
    if algorithm == "greedy":
        greedy() 
    elif algorithm == "balance":
        balance() 
    elif algorithm == "mssv":
        mssv() 
    else:
        print("Enter the input in following format: python sentiment.py <greedy | balance | mssv>")


# Initializing the queries list so that it can be explored anywhere in the program

def load_queries():
    global queries
    with open("queries.txt", "r") as file:
        for line in file:
            queries.append(line.strip('\n'))


# Loading adwords graph function

def load_adwords_graph():
    global budget
    global matching
    global spending
    global opt

    with open("bidder_dataset.csv",'r') as dataframe:
        fileread = csv.reader(dataframe)
        next(fileread, None)

        for row in fileread:
            if int(row[0]) not in budget:
                budget[int(row[0])] = float(row[3])
                spending[int(row[0])] = float(0)
            if row[1] not in matching:
                matching[row[1]] = []
                matching[row[1]].append((int(row[0]), float(row[2])))
            else:
                matching[row[1]].append((int(row[0]), float(row[2])))
    opt = sum(budget.values())
    


"""
This section contains code for Greedy algorithm
"""
def greedy():

    global opt, ans, alg
    
    ans = greedy_algo(queries)
    for i in range(100):
        alg += greedy_algo(queries)
    

    alg /= 100
    print(ans)
    print(alg/opt)

def greedy_algo(query):
    global matching, budget
    match = matching.copy()
    budgetPrime = budget.copy()

    for keys in match:
            match[keys].sort(key=operator.itemgetter(1), reverse = True)

    revenue = 0
    for q in query:
        for item in match[q]:
            neighbour = budgetPrime[item[0]]
            if neighbour - item[1] >= 0:
                revenue += item[1]
                budgetPrime[item[0]] = neighbour - item[1]
                break
    return revenue

"""
This section contains code for Balance Algorithm
"""
def balance():

    global opt, ans, alg
    
    ans = balance_algo(queries)
    for i in range(100):
        alg += balance_algo(queries)
    
    alg /= 100
    print(ans)
    print(alg/opt)

def balance_algo(query):
    global budget, matching
    match = matching.copy()
    budgetPrime = budget.copy()

    revenue = 0

    for q in query:
        bids = 0
        maximum = 0
        neighbour = -1

        for item in match[q]:
            if budgetPrime[item[0]] > neighbour:
                neighbour = budgetPrime[item[0]]
                bids = item[1]
                maximum = item[0]
        if neighbour - bids >= 0:
            revenue += bids
            budgetPrime[maximum] -= bids

    return revenue

"""
This section contains code for MSVV algorithm 
"""

def mssv():
    
    global opt, ans, alg

    ans = mssv_algo(queries)
    for i in range(100):
        alg += mssv_algo(queries)
    
    alg /= 100
    print(ans)
    print(alg/opt)

def chi(x_u, spend, budgetPrime): 
    return (1 - np.exp(spend[x_u[0]]/budgetPrime[x_u[0]] - 1)) * x_u[1]

def mssv_algo(query): 
    global matching, budget

    match = matching.copy()
    budgetPrime = budget.copy()
    spend = spending.copy()

    revenue = 0
    for q in query:
        bids, maximum, neighbour = 0, 0, -1

        for item in match[q]:
            psy_calc = chi(item, spend, budgetPrime)
            if psy_calc > neighbour and (spend[item[0]] + item[1]) <= budgetPrime[item[0]]:
                neighbour = psy_calc
                bids = item[1]
                maximum = item[0]
        revenue += bids
        spend[maximum] += bids

    return revenue


if __name__ == "__main__":
    main()