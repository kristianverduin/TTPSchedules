import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime
import os
import sys

PATH = os.path.dirname(os.path.realpath(__file__))
U = 3

def checkScheduleConstraints(schedule, nrTeams):
    """Calculates the number of violations present in the schedule

    Arguments:
        schedule ([int, int]) : Schedule 

        nrTeams (int) : The number of teams present in the schedule

    Returns:
        violations ([int]) : The number of violations present in the schedule, in the format [Home/Away streak, No-repeat, Double round-robin, mismatched games, games against itself]
    """

    nrRounds = (2*nrTeams)-2
    violations = [0, 0, 0, 0, 0]
    for team in range(nrTeams):
        homeStreak = 0
        awayStreak = 0
        gamesPlayed = np.zeros(nrTeams)
        homePlayed = np.zeros(nrTeams)
        awayPlayed = np.zeros(nrTeams)

        for round in range(nrRounds):
            #Check maxStreak
            if schedule[round, team] > 0:
                awayStreak = 0
                homeStreak += 1
                homePlayed[abs(schedule[round, team])-1] += 1
            else:
                awayStreak += 1
                homeStreak = 0
                awayPlayed[abs(schedule[round, team])-1] += 1
            if homeStreak > U or awayStreak > U:
                violations[0] += 1

            gamesPlayed[abs(schedule[round, team])-1] += 1

            #Check noRepeat
            if round > 0:
                if abs(schedule[round, team]) == abs(schedule[round-1, team]):
                    violations[1] += 1

            #Check if the opponent also has the current team as opponent (matches are paired)
            if team != abs(schedule[round, abs(schedule[round, team])-1])-1:
                violations[3] += 1

            #Check if the current team is playing against itself
            if abs(schedule[round, team])-1 == team:
                violations[4] += 1

        #Check for double round-robin violations
        for i in range(len(gamesPlayed)):
            if i != team:
                if gamesPlayed[i] == 0:
                    violations[2] += 2
                elif gamesPlayed[i] == 1:
                    violations[2] += 1
                elif gamesPlayed[i] == 2:
                    if homePlayed[i] != 1 and awayPlayed[i] != 1:
                        violations[2] += 1
                else:
                    violations[2] += gamesPlayed[i]-2
                    if homePlayed[i] == 0 or awayPlayed[i] == 0:
                        violations[2] += 1

    return  violations

def createRandomSchedulePairs(nrTeams):
    """Generates a randomly paired schedule

    Arguments:
        nrTeams (int) : The number of teams present in the schedule

    Returns:
        Schedule ([int, int]) : The randomly generated schedule generated
    """
        
    nrRounds = (2*nrTeams)-2
    schedule = np.full((nrRounds, nrTeams), None)
    choices = list(range(-nrTeams, nrTeams+1))
    choices.remove(0)

    for round in range(nrRounds):
        teamsToPick = choices.copy()
        for team in range(nrTeams):
            if schedule[round, team] == None:
                team += 1
                teamsToPick.remove(team)
                teamsToPick.remove(-team)
                choice = random.choice(teamsToPick)
                teamsToPick.remove(choice)
                teamsToPick.remove(-choice)
                if choice > 0:
                    schedule[round, team-1] = choice
                    schedule[round, choice-1] = -team
                else:
                    schedule[round, team-1] = choice
                    schedule[round, abs(choice)-1] = team

    return schedule

def createSchedules(nrTeams, n, iteration):
    """Generates n schedules and saves the violations of the schedules

    Arguments:
        n (int) : The number of schedules to generate

        nrTeams (int) : The number of teams present in the schedule

    Returns:
        TotalViolations ([int, int]) : The violations present in all n schedules
    """

    start=datetime.now()

    homeAway1 = []
    repeat1 = []
    robin1 = []
    total1 = []

    for i in range(n):
        schedule = createRandomSchedulePairs(nrTeams)
        violations = checkScheduleConstraints(schedule, nrTeams)

        homeAway = violations[0]
        repeat = violations[1]
        robin = violations[2]

        value = np.sum(violations)

        homeAway1.append(homeAway)
        repeat1.append(repeat)
        robin1.append(robin)
        total1.append(value)

    time = datetime.now()-start
    time = time.total_seconds()

    #Used to save all violations in seperate file

    #totalViolations = [homeAway1, repeat1, robin1, total1]
    #outF = open("/home/verduin/MasterProject/NewResults/MinViolationExperiment/" + str(iteration) + "/Violations" + str(nrTeams) +".txt", "w")
    #np.savetxt(outF, totalViolations, fmt='%i', delimiter=',')
    #outF.close()

    #outF = open("/home/verduin/MasterProject/NewResults/MinViolationExperiment/" + str(iteration) + "/time" + str(nrTeams) +".txt", "w")
    #np.savetxt(outF, [time], delimiter=',')
    #outF.close()

if int(sys.argv[1]) % 2 == 0:
    for i in range(0, 5):
        createSchedules(int(sys.argv[1]), 1000000, i)
else:
    print("n must be even")
