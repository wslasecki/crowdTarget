import csv
import json
import sys
import collections
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

#to extract csvs from the databs
#SELECT * FROM targethits INTO OUTFILE '/tmp/targethits.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

class TargetHit:
    def __init__(self, row):
        self.ID = row[0]
        self.workerId = row[1]
        self.trialId = row[2]
        self.assignmentId = row[3]
        self.frameDuration = int(row[4])
        self.targetSpeed = int(row[5])
        self.targetCount = int(row[6])
        self.startTime = int(row[7])
        self.timeTakenToClick = int(row[8])
        self.startTargetPos = json.loads(row[9])
        self.endTargetPos = json.loads(row[10])
        self.mousePath = json.loads(row[11])
        self.mouseDistance = float(row[12])
        self.proximity = float(row[13])
        self.misclicks = int(row[14])

class Trial:
    def __init__(self, row):
        self.ID = row[0]
        self.workerId = row[1]
        self.trialId = row[2]
        self.assignmentId = row[3]
        self.frameDuration = int(row[4])
        self.targetSpeed = int(row[5])
        self.startTime = int(row[6])
        self.trialDuration = int(row[7])
        self.avgProximity = float(row[8])
        self.misclicks = int(row[9])
        self.targetTotalCount = int(row[10])
        self.targetHitCount = int(row[11])
        self.targetMissedCount = int(row[12])

def constructDataArray(trialsByFrameDuration, calcFunc):
    dataArrs = {}
    numSamplesArrs = {}
    xTicks = set()
    yTicks = set()
    for frameDuration in trialsByFrameDuration.keys():
        dataDict = collections.defaultdict(lambda :collections.defaultdict(list))
        for trial in trialsByFrameDuration[frameDuration]:
            doIAdd, value = calcFunc(trial)
            if doIAdd:
                if type(value) is list:
                    dataDict[trial.targetTotalCount][trial.targetSpeed].extend(value)
                else:
                    dataDict[trial.targetTotalCount][trial.targetSpeed].append(value)
                xTicks.add(trial.targetSpeed)
                yTicks.add(trial.targetTotalCount)

        dataArr = np.zeros((6,6), dtype=np.float64)
        numSamplesArr = np.zeros((6,6), dtype=np.float64)
        for y, k1 in enumerate(sorted(dataDict)):
            for x, k2 in enumerate(sorted(dataDict[k1])):
                dataArr[y,x] = np.average(dataDict[k1][k2])
                numSamplesArr[y,x] = len(dataDict[k1][k2])

        dataArrs[frameDuration] = dataArr
        numSamplesArrs[frameDuration] = numSamplesArr

    return dataArrs, sorted(xTicks), sorted(yTicks), numSamplesArrs

def plotHeatmap(titles, dataArrs, xLabels, yLabels, title):
    #create the figure we're going to plot
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.suptitle(title, fontsize=14, fontweight='bold')

    vmin = sys.float_info.max
    vmax = sys.float_info.min
    for frameDuration in dataArrs.keys():
        dataArr = dataArrs[frameDuration]
        vmin = min(dataArr.min(), vmin)
        vmax = max(dataArr.max(), vmax)


    for i, frameDuration in enumerate(sorted(dataArrs.keys())):
        dataArr = dataArrs[frameDuration]

        # Now print the data
        subfig = axes.flat[i]
        subfig.set_title(titles[frameDuration])

        heatmap = subfig.pcolor(dataArr, vmin=vmin, vmax=vmax)

        for y in range(dataArr.shape[0]):
            for x in range(dataArr.shape[1]):
                subfig.text(x + 0.5, y + 0.5, '%.2f' % dataArr[y, x],
                         horizontalalignment='center',
                         verticalalignment='center',
                         )

        midTickLoc = [0.5,1.5,2.5,3.5,4.5,5.5]
        subfig.set_xticks(midTickLoc)
        subfig.set_yticks(midTickLoc)
        subfig.set_xticklabels(xLabels)
        subfig.set_yticklabels(yLabels)

    fig.text(0.5, 0.04, 'Speed of Targets in Pixels per Second', ha='center')
    fig.text(0.04, 0.5, 'Number of Simultaneous Targets', va='center', rotation='vertical')


datadir = sys.argv[1]
#keep a log of why assingments were rejected
whyWasAssIdRejected = {}
assIdToFrameDuration = {}

#load the assignments we have approved from mturk
workerToDateToAssId = collections.defaultdict(dict)
buggedAssIds = set()
approvedmturkfiles = [f for f in os.listdir(os.path.join(datadir,"mturk_dowloaded_results")) if os.path.isfile(os.path.join(os.path.join(datadir,"mturk_dowloaded_results"), f))]
for file in approvedmturkfiles:
    with open(os.path.join(os.path.join(datadir,"mturk_dowloaded_results"),file), 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        for lineNum, row in enumerate(csvreader):
            if lineNum > 0:
                assId = row[3]
                workerId = row[4]
                acceptTime = datetime.strptime(row[6].replace(" PST",""), '%a %b %d %H:%M:%S %Y')

                #for each worker, store each time an assignment was accepted, and wether it was rejected or not
                if "REJECTED" in file:
                    buggedAssIds.add(assId)

                workerToDateToAssId[workerId][acceptTime] = assId


#now for each worker, take the earliest assignment (i.e., their first attempt) discarding anything they did afterwards
approvedAssignments = set()
for workerId in workerToDateToAssId:
    dates = sorted(workerToDateToAssId[workerId].keys())
    firstAssignment = workerToDateToAssId[workerId][dates[0]]
    if firstAssignment not in buggedAssIds:
        approvedAssignments.add(firstAssignment)
    else:
        #log why we rejected this assignment
        whyWasAssIdRejected[firstAssignment] = "Experiment Was Bugged"

    #for the other dates, log why this assignment was rejected
    for otherDate in dates[1:]:
        otherAssId = workerToDateToAssId[workerId][otherDate]
        if otherAssId not in buggedAssIds:
            whyWasAssIdRejected[otherAssId] = "Worker Had Already Performed Experiment"
        else:
            whyWasAssIdRejected[otherAssId] = "Experiment Was Bugged, But Rejected As Worker Had Already Performed Experiment"

#load in from the database trials and hits from approved assignments
targetHitsByFrameDuration = collections.defaultdict(list)
with open(datadir+"/targethits.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        hit = TargetHit(row)

        if hit.assignmentId in approvedAssignments:
            targetHitsByFrameDuration[hit.frameDuration].append(hit)

trialsByFrameDuration = collections.defaultdict(list)
with open(datadir+"/trials.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        trial = Trial(row)

        assIdToFrameDuration[trial.assignmentId] = trial.frameDuration

        if trial.assignmentId in approvedAssignments:
            trialsByFrameDuration[trial.frameDuration].append(trial)

#remove corrupted assignments (i.e., missing data)
#first stick the trials and hits into a map
trialByAssId = collections.defaultdict(dict)
hitByAssId = collections.defaultdict(lambda: collections.defaultdict(list))
for frameDuration in trialsByFrameDuration:
    for trial in trialsByFrameDuration[frameDuration]:
        trialByAssId[trial.assignmentId][trial.trialId]=trial
    for hit in targetHitsByFrameDuration[frameDuration]:
        hitByAssId[hit.assignmentId][hit.trialId].append(hit)

assIdsToRemove = set()
#check the assignment has the correct number of trials
for assId in trialByAssId:
    if len(trialByAssId[assId]) != 36:
        assIdsToRemove.add(assId)
        whyWasAssIdRejected[assId] = "Missing Trials"

#check if each trial has the correct number of hits
for assId in trialByAssId:
    if assId in assIdsToRemove:
        continue

    for trialId in trialByAssId[assId]:
        trial = trialByAssId[assId][trialId]

        if trial.targetHitCount != len(hitByAssId[assId][trialId]):
            # we're missing hits, this cant be reconstructed
            assIdsToRemove.add(assId)
            whyWasAssIdRejected[assId] = "Missing Target Hits"

#check if the hit has a trial associated with it
for assId in hitByAssId:
    if assId in assIdsToRemove:
        continue

    for trialId in hitByAssId[assId]:
        for hit in hitByAssId[assId][trialId]:
            if trialId not in trialByAssId[assId]:
                # we're missing trial, maybe it can be reconstructed
                assIdsToRemove.add(assId)
                whyWasAssIdRejected[assId] = "Had Target Hit, But No Associated Trial"
#check that the hit data looks valid
# for assId in hitByAssId:
#     if assId in assIdsToRemove:
#         continue
#
#     for trialId in hitByAssId[assId]:
#         for hit in hitByAssId[assId][trialId]:
#             if hit.proximity > 35.35533905932738:
#                 # proximity is greater than what is possible
#                 assIdsToRemove.add(assId)
#                 whyWasAssIdRejected[assId] = "Hit Had Bad Data (Proximity Too High)"

#remove corrupted trials and hits
for frameDuration in trialsByFrameDuration:
    trialsByFrameDuration[frameDuration] = [trial for trial in trialsByFrameDuration[frameDuration] if trial.assignmentId not in assIdsToRemove]
    targetHitsByFrameDuration[frameDuration] = [hit for hit in targetHitsByFrameDuration[frameDuration] if hit.assignmentId not in assIdsToRemove]

#count the assignments per frame duration
print("Assignments per frame duration")
for frameDuration in sorted(trialsByFrameDuration.keys()):
    assIds = set()
    for trial in trialsByFrameDuration[frameDuration]:
        assIds.add(trial.assignmentId)
    print("%d = %d"%(frameDuration, len(assIds)))

#count why we rejected assignments
rejectionsByFrameDuration = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
for assId in whyWasAssIdRejected:
    frameDuration = assIdToFrameDuration[assId]
    rejectionsByFrameDuration[frameDuration][whyWasAssIdRejected[assId]] += 1

## Handle trial data ##
dataArrs = {}
for frameDuration in sorted(trialsByFrameDuration.keys()):
    print("analysing frameDuration: %s"%frameDuration)

    proxByTotalTargets = collections.defaultdict(list)
    for targetHit in targetHitsByFrameDuration[frameDuration]:
        #get the trial this target was in
        idx = trialByAssId[targetHit.assignmentId][targetHit.trialId].targetTotalCount
        proxByTotalTargets[idx].append(targetHit.proximity)

    for key in proxByTotalTargets:
        #print "%s -> %s" % (key, proxByTargetCount[key])
        ttlProx = 0
        for val in proxByTotalTargets[key]:
            ttlProx += val
        print "AVERAGE PROX for %s targets = %f" % (key, ttlProx/len(proxByTotalTargets[key]))


#We now generate graphs based on this data
#To do that we use the function constructDataArray
#the 2nd parameter of constructDataArray is a function that returns a tuple (BOOL, value/[values])
#the tuple contains a boolean wether the data for this trial should be used (i.e., only calculating proximity when the worker has actually clicked on atleast 1 hit) (not actually sure if this is needed anymore)
#the tuple contains a single value, or a list of values, that will then be averaged by the constructDataArray function

# proximity
titles = {0:"Live", 1000:"1s Still Frame", 2000:"2s Still Frame", 3000:"3s Still Frame"}
dataArrs, xTicks, yTicks, numSamplesArrs = constructDataArray(trialsByFrameDuration, lambda trial: (trial.targetHitCount > 0, [hit.proximity for hit in hitByAssId[trial.assignmentId][trial.trialId] if hit.proximity <= 25]))
plotHeatmap(titles, dataArrs, xTicks, yTicks,"Avg Proximity")

subDataArrs = {}
for frameDuration in dataArrs.keys():
    subDataArrs[frameDuration] = dataArrs[0] - dataArrs[frameDuration]
plotHeatmap(titles, subDataArrs, xTicks, yTicks, "Diff Avg Proximity with Live")

#targets hit
dataArrs, xTicks, yTicks, numSamplesArrs = constructDataArray(trialsByFrameDuration, lambda trial: (True, (float(trial.targetHitCount) / float(trial.targetTotalCount))*100))
plotHeatmap(titles, dataArrs, xTicks, yTicks, "Percentage Targets Hit")

dataArrs, xTicks, yTicks, numSamplesArrs = constructDataArray(trialsByFrameDuration, lambda trial: (True, trial.misclicks))
plotHeatmap(titles, dataArrs, xTicks, yTicks, "Number of Misclicks")

dataArrs, xTicks, yTicks, numSamplesArrs = constructDataArray(trialsByFrameDuration, lambda trial: (True, trial.trialDuration))
plotHeatmap(titles, dataArrs, xTicks, yTicks, "Trial Duration")


plt.show()
print "\nDone."

