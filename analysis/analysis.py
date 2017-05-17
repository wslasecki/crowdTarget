import csv
import json
import sys
import collections
import os
import matplotlib as mpl
# mpl.rcParams['pdf.fonttype'] = 42
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
        self.timeTakenToClickCumulative = -1
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
    stdDevArrs = {}
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
        stdDevArr = np.zeros((6,6), dtype=np.float64)
        numSamplesArr = np.zeros((6,6), dtype=np.float64)
        for y, k1 in enumerate(sorted(dataDict)):
            for x, k2 in enumerate(sorted(dataDict[k1])):
                if len(dataDict[k1][k2]) > 0:
                    dataArr[y,x] = np.average(dataDict[k1][k2])
                    stdDevArr[y,x] = np.std(dataDict[k1][k2])
                else:
                    dataArr[y,x] = 0
                    stdDevArr[y, x] = -1
                numSamplesArr[y,x] = len(dataDict[k1][k2])

        dataArrs[frameDuration] = dataArr
        stdDevArrs[frameDuration] = stdDevArr
        numSamplesArrs[frameDuration] = numSamplesArr

    return dataArrs, sorted(xTicks), sorted(yTicks), numSamplesArrs, stdDevArrs

def plotHeatmap(titles, dataArrs, xLabels, yLabels, title, textformat="%.2f"):
    #create the figure we're going to plot
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.suptitle(title, fontsize=24, fontweight='bold')

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
        subfig.set_title(titles[frameDuration], fontsize=20)

        heatmap = subfig.pcolor(dataArr, vmin=vmin, vmax=vmax)

        for y in range(dataArr.shape[0]):
            for x in range(dataArr.shape[1]):
                colorThresh = vmin + ((vmax - vmin) * 0.4)
                color = 'black'
                if dataArr[y, x] < colorThresh:
                    color = 'white'
                subfig.text(x + 0.5, y + 0.5, textformat % dataArr[y, x],
                         horizontalalignment='center',
                         verticalalignment='center',
                         color = color
                         )

        midTickLoc = [0.5,1.5,2.5,3.5,4.5,5.5]
        subfig.set_xticks(midTickLoc)
        subfig.set_yticks(midTickLoc)
        subfig.set_xticklabels(xLabels, fontsize=14)
        subfig.set_yticklabels(yLabels, fontsize=14)

    fig.text(0.5, 0.04, 'Speed of Targets in Pixels per Second', ha='center', fontsize=16)
    fig.text(0.04, 0.5, 'Number of Simultaneous Targets', va='center', rotation='vertical', fontsize=16)

    fig.set_size_inches(10, 10)
    plt.savefig("{}.pdf".format(title).replace(" ", "_"))

def timeToIdentifyMultiple(trialsByFrameDuration, hitByAssId, targetTotalCount=6):
    dataArrs = {}
    numSamplesArrs = {}
    xTicks = set()
    yTicks = set()
    for frameDuration in trialsByFrameDuration.keys():
        dataDict = collections.defaultdict(lambda: collections.defaultdict(list))
        for trial in trialsByFrameDuration[frameDuration]:
            if True:#trial.targetTotalCount == targetTotalCount:
                hits = hitByAssId[trial.assignmentId][trial.trialId]
                for hit in hits:
                    totalRoundDuration = (500.0 / trial.targetSpeed) * 1000
                    dataDict[hit.targetCount][trial.targetSpeed].append(hit.timeTakenToClickCumulative / totalRoundDuration)
                    xTicks.add(trial.targetSpeed)
                    yTicks.add(hit.targetCount)

        dataArr = np.zeros((6, 6), dtype=np.float64)
        numSamplesArr = np.zeros((6, 6), dtype=np.float64)
        for y, k1 in enumerate(sorted(dataDict)):
            for x, k2 in enumerate(sorted(dataDict[k1])):
                if len(dataDict[k1][k2]) > 0:
                    dataArr[y, x] = np.mean(dataDict[k1][k2])
                else:
                    dataArr[y, x] = 0
                numSamplesArr[y, x] = len(dataDict[k1][k2])


        dataArrs[frameDuration] = dataArr
        numSamplesArrs[frameDuration] = numSamplesArr

    return dataArrs, sorted(xTicks), sorted(yTicks), numSamplesArrs

def aggregateTargetHits(targetHitsByFrameDuration, trialByAssId, trialsByFrameDuration):
    #create a data structure to store similar target hits
    targetHitsByFrameSpeedTrialCount = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list))))
    for frameDuration in targetHitsByFrameDuration:
        for hit in targetHitsByFrameDuration[frameDuration]:
            targetTotalCount = trialByAssId[hit.assignmentId][hit.trialId].targetTotalCount
            targetHitsByFrameSpeedTrialCount[hit.frameDuration][hit.targetSpeed][targetTotalCount][hit.targetCount].append(hit)

    #rotate all hits so theyre the same
    proxByFrameCountSpeed = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
    for frameDuration in targetHitsByFrameSpeedTrialCount:
        for targetSpeed in targetHitsByFrameSpeedTrialCount[frameDuration]:
            for targetTotal in targetHitsByFrameSpeedTrialCount[frameDuration][targetSpeed]:
                for targetCount in targetHitsByFrameSpeedTrialCount[frameDuration][targetSpeed][targetTotal]:
                    allHits = targetHitsByFrameSpeedTrialCount[frameDuration][targetSpeed][targetTotal][targetCount]

                    mouseDeltas = []
                    for hit in allHits:
                        centerPos = np.array(hit.endTargetPos) + [25,25]
                        mouseDelta = np.array(hit.mousePath, dtype=np.float64)[-1,0:2] - centerPos
                        prox = np.linalg.norm(mouseDelta)
                        if prox <= 25:
                            mouseDeltas.append(mouseDelta)
                        # npStartPos = np.array(hit.startTargetPos) + [25,25]
                        # npEndPos = np.array(hit.endTargetPos) + [25,25]
                        # hitDelta = npEndPos - npStartPos
                        #
                        # distanceTravelled = np.linalg.norm(hitDelta)
                        # dotProduct = np.dot(hitDelta, [1,0])
                        # theta = -(np.arccos(dotProduct / distanceTravelled))
                        #
                        # rotMatrix = np.array([[np.cos(theta), -np.sin(theta)],
                        # 					  [np.sin(theta),  np.cos(theta)]])
                        #
                        # rotatedDelta = rotMatrix.dot(hitDelta)
                        # npMousePath = np.array(hit.mousePath, dtype=np.float64)[:,0:2]
                        # for i in range(len(npMousePath)):
                        # 	npMousePath[i,:] = rotMatrix.dot(npMousePath[i,:] - npStartPos)
                        #
                        # #calculate mouse proximity
                        # centerPos = rotatedDelta
                        # mouseDelta = npMousePath[-1,:] - centerPos
                        # prox = np.linalg.norm(mouseDelta)
                        # if prox <= 25:
                        # 	mouseDeltas.append(mouseDelta)

                    if len(mouseDeltas) > 3:
                        avgMousePos = np.array(mouseDeltas).mean(axis=0)
                        avgProx = np.linalg.norm(avgMousePos)
                        proxByFrameCountSpeed[frameDuration][targetTotal][targetSpeed].extend(mouseDeltas)
                    #print("FD:%d SPD:%d %d/%d Prox: %f"%(frameDuration,targetSpeed,targetCount,targetTotal,avgProx))

    canBeUsed = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: True)))
    def getAvgProx(trial):
        useThisValue = canBeUsed[trial.frameDuration][trial.targetTotalCount][trial.targetSpeed]
        canBeUsed[trial.frameDuration][trial.targetTotalCount][trial.targetSpeed] = False
        proxValues = np.array(proxByFrameCountSpeed[trial.frameDuration][trial.targetTotalCount][trial.targetSpeed])
        proxValues = np.linalg.norm(np.mean(proxValues, axis=0))

        proxValues = (1.0-(proxValues / 25.0))*100

        return (useThisValue, proxValues)
    return constructDataArray(trialsByFrameDuration, getAvgProx)

datadir = sys.argv[1]
#keep a log of why assingments were rejected
whyWasAssIdRejected = {}
assIdToFrameDuration = {}

#load the assignments we have approved from mturk
workerToDateToAssId = collections.defaultdict(dict)
buggedAssIds = set()
mturk_dir = os.path.join(datadir,"mturk_dowloaded_results")
approvedmturkfiles = [f for f in os.listdir(mturk_dir) if os.path.isfile(os.path.join(mturk_dir, f))]
for file in approvedmturkfiles:
    with open(os.path.join(mturk_dir,file), 'r') as csvfile:
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
with open(datadir+"/targethits.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        hit = TargetHit(row)

        if hit.assignmentId in approvedAssignments:
            targetHitsByFrameDuration[hit.frameDuration].append(hit)

trialsByFrameDuration = collections.defaultdict(list)
with open(datadir+"/trials.csv", 'r') as csvfile:
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

        else:
            targetCounts = set([int(hit.targetCount) for hit in hitByAssId[assId][trialId]])
            desiredCounts = set(range(1,trial.targetHitCount+1))
            if targetCounts != desiredCounts:
                # looks like we have unsequential hits or hits with the same number
                assIdsToRemove.add(assId)
                whyWasAssIdRejected[assId] = "Unsequential Target Hits"

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
hitByAssId = {assId:hitByAssId[assId] for assId in hitByAssId if assId not in assIdsToRemove}

#calculate cumulative timing for hits
for assId in hitByAssId:
    for trialId in hitByAssId[assId]:
        timing = np.zeros(len(hitByAssId[assId][trialId]))
        for hit in hitByAssId[assId][trialId]:
            timing[int(hit.targetCount) - 1] = hit.timeTakenToClick

        cumtiming = np.cumsum(timing)

        for hit in hitByAssId[assId][trialId]:
            hit.timeTakenToClickCumulative = cumtiming[int(hit.targetCount) - 1]


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
        print("AVERAGE PROX for %s targets = %f" % (key, ttlProx/len(proxByTotalTargets[key])))


#We now generate graphs based on this data
#To do that we use the function constructDataArray
#the 2nd parameter of constructDataArray is a function that returns a tuple (BOOL, value/[values])
#the tuple contains a boolean wether the data for this trial should be used (i.e., only calculating proximity when the worker has actually clicked on atleast 1 hit) (not actually sure if this is needed anymore)
#the tuple contains a single value, or a list of values, that will then be averaged by the constructDataArray function

# proximity
titles = {0:"Live", 1000:"1s Still Frame", 2000:"2s Still Frame", 3000:"3s Still Frame"}
dataArrs, xTicks, yTicks, numSamplesArrs, stdDevArrs = constructDataArray(trialsByFrameDuration, lambda trial: (trial.targetHitCount > 0, [(1.0-(hit.proximity/25.0))*100 for hit in hitByAssId[trial.assignmentId][trial.trialId] if hit.proximity <= 25]))
plotHeatmap(titles, dataArrs, xTicks, yTicks,"Percentage Proximity to Target Center", textformat="%d")
plotHeatmap(titles, stdDevArrs, xTicks, yTicks,"STD DEV Proximity to Target Center", textformat="%d")

subDataArrs = {}
for frameDuration in dataArrs.keys():
    subDataArrs[frameDuration] = dataArrs[frameDuration] - dataArrs[0]
plotHeatmap(titles, subDataArrs, xTicks, yTicks, "Diff Avg Proximity with Live")

#targets hit
dataArrs, xTicks, yTicks, numSamplesArrs, stdDevArrs = constructDataArray(trialsByFrameDuration, lambda trial: (True, (float(trial.targetHitCount) / float(trial.targetTotalCount))*100))
plotHeatmap(titles, dataArrs, xTicks, yTicks, "Percentage of Targets Identified", textformat="%d")
plotHeatmap(titles, stdDevArrs, xTicks, yTicks, "STD DEV of Targets Identified", textformat="%d")

dataArrs, xTicks, yTicks, numSamplesArrs, stdDevArrs = constructDataArray(trialsByFrameDuration, lambda trial: (True, (1-(trial.misclicks/(trial.targetHitCount+trial.misclicks)))*100) if trial.targetHitCount+trial.misclicks > 0 else (False, 0))
plotHeatmap(titles, dataArrs, xTicks, yTicks, "Percentage of Successful Clicks", textformat="%d")
plotHeatmap(titles, stdDevArrs, xTicks, yTicks, "STD DEV of Successful Clicks", textformat="%d")

# dataArrs, xTicks, yTicks, numSamplesArrs = constructDataArray(trialsByFrameDuration, lambda trial: (True, trial.trialDuration/((500/float(trial.targetSpeed))*1000)))
# plotHeatmap(titles, dataArrs, xTicks, yTicks, "Trial Duration")

dataArrs, xTicks, yTicks, numSamplesArrs, stdDevArrs = aggregateTargetHits(targetHitsByFrameDuration, trialByAssId, trialsByFrameDuration)
plotHeatmap(titles, dataArrs, xTicks, yTicks, "Aggregated Proximity", textformat="%d")

dataArrs, xTicks, yTicks, numSamplesArrs, stdDevArrs = constructDataArray(trialsByFrameDuration, lambda trial: (trial.targetHitCount > 0, [hit.timeTakenToClick for hit in hitByAssId[trial.assignmentId][trial.trialId] if hit.targetCount == 1]))
plotHeatmap(titles, dataArrs, xTicks, yTicks,"Avg Time To Click")

dataArrs, xTicks, yTicks, numSamplesArrs = timeToIdentifyMultiple(trialsByFrameDuration, hitByAssId)
plotHeatmap(titles, dataArrs, xTicks, yTicks, "Avg Time Taken To Identify Targets", textformat="%0.1f")

plt.show()
print("\nDone.")

