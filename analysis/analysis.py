import csv
import json
import sys

#to extract csvs from the databse
#SELECT * FROM targethits INTO OUTFILE '/tmp/targethits.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

class TargetHit:
    def __init__(self, ID, workerId, trialId, assignmentId, frameDuration, targetSpeed, targetCount, startTime, timeTakenToClick, startTargetPos, endTargetPos, mousePath, mouseDistance, proximity, misclicks):
        self.ID = ID
        self.workerId = workerId
        self.trialId = trialId
        self.assignmentId = assignmentId
        self.frameDuration = frameDuration
        self.targetSpeed = targetSpeed
        self.targetCount = targetCount
        self.startTime = startTime
        self.timeTakenToClick = timeTakenToClick
        self.startTargetPos = startTargetPos
        self.endTargetPos = endTargetPos
        self.mousePath = mousePath
        self.mouseDistance = mouseDistance
        self.proximity = proximity
        self.misclicks = misclicks

class Trial:
    def __init__(self, ID, workerId, trialId, assignmentId, frameDuration, targetSpeed, startTime, trialDuration, avgProximity, misclicks, targetTotalCount, targetHitCount, targetMissedCount):
        self.ID = ID
        self.workerId = workerId
        self.trialId = trialId
        self.assignmentId = assignmentId
        self.frameDuration = frameDuration
        self.targetSpeed = targetSpeed
        self.startTime = startTime
        self.trialDuration = trialDuration
        self.avgProximity = avgProximity
        self.misclicks = misclicks
        self.targetTotalCount = targetTotalCount
        self.targetHitCount = targetHitCount
        self.targetMissedCount = targetMissedCount

datadir = sys.argv[1]
targethits = []
with open(datadir+"/targethits.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        hit = TargetHit(row[0],
                        row[1],
                        row[2],
                        row[3],
                        int(row[4]),
                        int(row[5]),
                        int(row[6]),
                        int(row[7]),
                        int(row[8]),
                        json.loads(row[9]),
                        json.loads(row[10]),
                        json.loads(row[11]),
                        float(row[12]),
                        float(row[13]),
                        int(row[14]))
        targethits.append(hit)

trials = []
with open(datadir+"/trials.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        trial = Trial(  row[0],
                        row[1],
                        row[2],
                        row[3],
                        int(row[4]),
                        int(row[5]),
                        int(row[6]),
                        int(row[7]),
                        float(row[8]),
                        int(row[9]),
                        int(row[10]),
                        int(row[11]),
                        int(row[12]))
        trials.append(trial)

print "loaded"

## WSL's terrible take on analytics
proxByTargetCount = {}
for e in targethits:
    idx = e.targetCount
    try:
        proxByTargetCount[idx]
    except KeyError:
        proxByTargetCount[idx] = []
    proxByTargetCount[idx].append(e.proximity)


## Handle trial data ##

proxByTrial = {}
def addToByTrial( addVal ):
    idx1 = e.targetTotalCount
    try:
        proxByTrial[idx1]
    except KeyError:
        proxByTrial[idx1] = {}

    idx2 = e.targetSpeed
    try:
        proxByTrial[idx1][idx2]
    except KeyError:
        proxByTrial[idx1][idx2] = []

    proxByTrial[idx1][idx2].append(addVal)

for e in trials:
    # Measure prox for completed trials
    if e.targetHitCount == e.targetTotalCount:
        addToByTrial(e.avgProximity)

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

