# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 11:41:17 2023

@author: joban
"""

import numpy as np
from scipy.optimize import minimize


'''
#Define a metric dictionary to use as input to model
[0]=Budget
[1]=Team Size
[2]=Project Progression
[3]=Team Skill
[4]=Scope Creep
[5]=communication
[6]=Git Bugs
[7]=Deadlines (Cumulative Lateness)
[8]=Parties involved
[9]=Days Passed
[10]=Total days initially given to complete project
[11]=moneySpent
[12]=Salary
'''


#Defining contraints
#Equality constraint requires constraint function to return 0 to pass
#Inequality contraint requires contraint function to return a non-negative value to pass

#k*teamskill*teamsize*communnications >= Cumulative lateness+ scope creep + bugs
def constraint1(metricArr):
    lateness=metricArr[7]
    scopeCreep=metricArr[4]
    bugs=metricArr[6]
    teamSkill=metricArr[3]
    teamsize=metricArr[1]
    communnications=metricArr[5]
    k=1
    
    LHS=k*teamSkill*teamsize*communnications
    RHS=lateness*scopeCreep*bugs
    return LHS-RHS

#Project progression >= weeks so far / total weeks
def constraint2(metricArr):
    totalWeeks=metricArr[10]
    weeksLeft=metricArr[9]
    progress=metricArr[2]

    weeksSpent=totalWeeks=weeksLeft
    LHS=progress
    RHS=weeksSpent/totalWeeks
    return LHS-RHS

#Project progression >= money spent so far / budget
def constraint3(metricArr):
    budget=metricArr[0]
    moneySpent=metricArr[11]
    progress=metricArr[2]

    LHS=progress
    RHS=moneySpent/budget
    return LHS-RHS

#Salary / team size >= teamskill * k
def constraint4(metricArr):
    salary=metricArr[12]
    teamSize=metricArr[1]
    teamSkill=metricArr[3]
    k=1

    LHS=salary/teamSize
    RHS=teamSkill*k
    return LHS-RHS

#k*teamsize*teamskill >= UnresolvedBugs * timeleft/(total time)
def constraint5(metricArr):
    bugs=metricArr[6]
    totalWeeks=metricArr[10]
    weeksLeft=metricArr[9]
    teamSize=metricArr[1]
    teamSkill=metricArr[3]
    k=1

    LHS=k*teamSize*teamSkill
    RHS=bugs*(weeksLeft/totalWeeks)
    return LHS-RHS

#Team skill*communication >= parties Involved*k
def constraint6(metricArr):
    communication=metricArr[5]
    partiesInvolved=metricArr[8]
    teamSkill=metricArr[3]
    k=1

    LHS=teamSkill*communication
    RHS=k*partiesInvolved
    return LHS-RHS

#communication*Team skill / team size>= k
def constraint7(metricArr):
    communication=metricArr[5]
    teamSize=metricArr[1]
    teamSkill=metricArr[3]
    k=1

    LHS=(teamSize*teamSkill)/communication
    RHS=k
    return LHS-RHS

#Budget/ amount of weeks for deadline >= money spent / weeks passed so far
def constraint8(metricArr):
    totalWeeks=metricArr[10]
    weeksLeft=metricArr[9]
    budget=metricArr[0]
    moneySpent=metricArr[11]
    
    weeksSpent=totalWeeks=weeksLeft
    LHS=budget / totalWeeks
    RHS=moneySpent/weeksSpent
    return LHS-RHS

#(Budget - expenditure) * timeleft/(total time) >= scope creep * k 
def constraint9(metricArr):
    totalWeeks=metricArr[10]
    weeksLeft=metricArr[9]
    budget=metricArr[0]
    moneySpent=metricArr[11]
    scopeCreep=metricArr[4]
    k=1
    
    LHS= (budget - moneySpent) * (weeksLeft/totalWeeks)
    RHS=scopeCreep*k
    return LHS-RHS

#((Budget - expenditure)/(totals weeks left + (lateness/7)) >= expenditure/ total weeks passed
def constraint10(metricArr):
    totalWeeks=metricArr[10]
    weeksLeft=metricArr[9]
    budget=metricArr[0]
    moneySpent=metricArr[11]
    lateness=metricArr[7]  
    
    LHS= (budget - moneySpent) * (weeksLeft + (lateness/7))
    RHS=moneySpent/totalWeeks
    return LHS-RHS

#Project progression  * team skill >= k * lateness * time left/ (total time)
def constraint11(metricArr):
    totalWeeks=metricArr[10]
    weeksLeft=metricArr[9]
    teamSkill=metricArr[0]
    progress=metricArr[3]
    lateness=metricArr[2]
    k=1
    
    LHS= progress*teamSkill
    RHS=k * lateness * weeksLeft / totalWeeks
    return LHS-RHS

def calculateRisk(userMetrics):

    #This is calculating the distance between closestPoint and userInput
    def objective_function(closestPoint):
        diffArr = closestPoint - userMetrics
        distance = np.linalg.norm(diffArr)
        return distance
    
    
    allCons = [{'type':'ineq', 'fun':constraint1},{'type':'ineq', 'fun':constraint2},{'type':'ineq', 'fun':constraint3},{'type':'ineq', 'fun':constraint4},
               {'type':'ineq', 'fun':constraint5},{'type':'ineq', 'fun':constraint6},{'type':'ineq', 'fun':constraint7},{'type':'ineq', 'fun':constraint8},
               {'type':'ineq', 'fun':constraint9},{'type':'ineq', 'fun':constraint10},{'type':'ineq', 'fun':constraint11}]
    
    # Find the closest point in the feasible region to the arbitrary point
    #Set initialGuess to some project that we know is in feasaible region
    initialGuess = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1])
    result = minimize(objective_function, initialGuess, method='SLSQP', constraints=allCons)
    print("Distance from feasible region is "+str(result['fun']))

#This is the metrics input by the user e.g. deadline, budget
userMetrics = np.array([1,1,1,1,10,1,1,1,1,10,1,10,1])
calculateRisk(userMetrics)
