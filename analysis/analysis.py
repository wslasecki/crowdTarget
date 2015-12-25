import csv
import json
import sys
import collections
import os

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

datadir = sys.argv[1]

#load the approved assignments from mturk
approvedAssignments = []
mturkfiles = ["frameduration0.csv", "frameduration1000.csv"]
for file in mturkfiles:
    with open(os.path.join(os.path.join(datadir,"mturk_dowloaded_results"),file), 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        for lineNum, row in enumerate(csvreader):
            if lineNum > 0:
                assId = row[3]
                approvedAssignments.append(assId)

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

        if trial.assignmentId in approvedAssignments:
            trialsByFrameDuration[trial.frameDuration].append(trial)

print "loaded"
#
# trialsByFrameAndAssIdAndTrialId = collections.defaultdict(dict)
# for trial in trialsByFrameDuration:
#     trialsByFrameAndAssIdAndTrialId[frameDuration][trial.assignmentId][trial.trialId] = trial
#
# hitsByAssId = collections.defaultdict(list)
# for hit in targethits:
#     hitsByAssId[hit.assignmentId].append(hit)

## WSL's terrible take on analytics
proxByTargetCount = collections.defaultdict(list)
for frameDuration in targetHitsByFrameDuration:
    for targetHit in targetHitsByFrameDuration[frameDuration]:
        idx = targetHit.targetCount
        # try:
        #     idx = trialsByAssIdAndTrialId[e.assignmentId][e.trialId].targetTotalCount
        # except:
        #     print("broken")
        #     continue
    proxByTargetCount[idx].append(targetHit.proximity)


## Handle trial data ##



for frameDuration in trialsByFrameDuration:
    print frameDuration
    proxByTrial = collections.defaultdict(lambda :collections.defaultdict(list))
    for trial in trialsByFrameDuration[frameDuration]:
        #if trial.targetHitCount == trial.targetTotalCount:
        proxByTrial[trial.targetTotalCount][trial.targetSpeed].append(trial.avgProximity)

    # Measure % completed trials
    #if e.targetHitCount == e.targetTotalCount:
    #    addToByTrial(100.0)
    #else:
    #    addToByTrial(0.0)

##############

    print "Tabulating..."

    for key in proxByTargetCount:
        #print "%s -> %s" % (key, proxByTargetCount[key])
        ttlProx = 0
        for val in proxByTargetCount[key]:
            ttlProx += val
        print "AVERAGE PROX for %s targets = %f" % (key, ttlProx/len(proxByTargetCount[key]))

    # First, print the header
    #print "Num Targets, Speed, Trial Duration"
    print '',
    for key1 in sorted(proxByTrial):
        for key2 in sorted(proxByTrial[key1]):
            print key2,
        break  # WSL: a little hacky, but should work for most of the cases we need
    print ''

    # Now print the data
    for key1 in sorted(proxByTrial):
        firstInRow = True
        for key2 in sorted(proxByTrial[key1]):
            ttlAvgProx = 0
            for val in proxByTrial[key1][key2]:
                ttlAvgProx += val
                #print "avrgProx from trial with %s targets, speed %s, and duration %s (with %d datapoints) = %f" % (key1, key2, key3, len(proxByTrial[key1][key2][key3]), ttlAvgProx/len(proxByTrial[key1][key2][key3]))
            if firstInRow:
                print key1,
                firstInRow = False
            #print "%s,%s,%s,%f" % (key1, key2, key3, ttlAvgProx/len(proxByTrial[key1][key2][key3]))
            #print "%s,%s,%f" % (key1, key2, ttlAvgProx/len(proxByTrial[key1][key2]))
            print ttlAvgProx/len(proxByTrial[key1][key2]),
        print ''


    print "\nDone."

