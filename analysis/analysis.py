import csv
import json
import sys
import collections

#to extract csvs from the databse
#SELECT * FROM targethits INTO OUTFILE '/tmp/targethits.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
#approvedAssignments = ["3BEFOD78W7YZXVWWBBG3Y4278IZM40","3BDCF01OGYZVPKSV063VEGRP3E8YLV","3VJ40NV2QJS7EJWY3SWOYG34JHVOTD","3D4CH1LGEBY02R6MH3EZ27TQYO19GB","3ZOTGHDK5JG6ZJJJESRYOB7IHYHOSO","3K772S5NP9GVXJSE9KC3FL624LUHES","3QECW5O0KI6L69QGYD0PPA3D2MQT5D","3PIWWX1FJKBZZ59WBLQFOEZ9MLUJJK","3L4D84MIL0X38ZE6NLNUC1JU9TQJHF","37TRT2X24RWTHMBKNTDYQQGWEGLBJR","340UGXU9DZ6H4GKK498CY4JEYOZVUD","3VELCLL3GLOCZM7W26TO5GBVZXE1FW","3P4RDNWND6B34UPQT35FCDK9965JI8","3FK0YFF9P0LHHV9K9ZIHUQLXCV8VV2","33NF62TLXK7UAPFET6QRPTZM1AUJKJ","3WJEQKOXA97H3VQORQ7WRF042H11AJ","3IXEICO793OHPDQU3WAUHGHDYH1T6T","3EF8EXOTT20S4OTSLWK9KE3NS4V1JZ","3MMN5BL1W09EFZDSBXBKOZA1UI3M3F","3VA45EW49OS65ZKP19CESAK9RY51OI","3UNH76FOCTAFV2AG0I4AET6E3JYYMX","3JWH6J9I9TIP0C252R5QJXXDN0QBNV","3TUI152ZZCS9QBX5GM4IHFF96ZN1QQ","3CPLWGV3MP46CJN847RUSR2NZ0O9NK","39L1G8WVWRWHJAR3IBSM47MYW7813M","3HMVI3QICKXIZDOR7WLCU1IB5841YT","3D8YOU6S9FPWPQ5J3104MC3FHV96UY","320DUZ38G8RP83JV3F5CR17TUTDJGG","37UEWGM5HUD92CC5T1TIM5PE2LP1RR","3J4Q2Z4UTZ82RCD8DAT3A5532CVQWD","39KFRKBFIO03V5VSDYJN6XVJYJDYOC","3U5NZHP4LS7ZUAH4IYSE9X56ISWHPD","37FMASSAYDWXMBRE5BSYEP1W11WBIF","3PJ71Z61R573YCGJZKTWVKPKWZJ194","323Q6SJS8JLN3XSA4VW9X3R2GM9HFA","3XCC1ODXDMGXJGWMEGJXN6XMAXGQRA","3DI28L7YXBJKT8707V9INYQVNWZ1EE","3X73LLYYQ2JZRP5R2JFM580BIDVHNH","3SBEHTYCWO8TZJKPF36IM0ZXMAEYIH","31EUONYN2W8MRB0N8NW3ZYRPG2BOVT","39RP059MEIYJIUH5QQQQ6I8DIAGBMV","3H8DHMCCWAGH73FMJA4GMV49WQXDKZ","3R2UR8A0IBLEV05I82XLNJOAWDJOXW","3KB8R4ZV1FCJQKLJFNSVTDOGMO4BGN","3A1PQ49WVIMWDIY2XWHO81N8FCR1HU","3L4PIM1GQUL6SIN85Q0R0S0O96XYRL","3N2BF7Y2VRZT97KRQI0MSTBBDNLHMH","33F859I567IXQGGUZTADED0H1OHBHM","3YDTZAI2WYL216A7IPX5ECE4A74147","39PAAFCODN52435V44I2T8XCFASVTM"]

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
targetHitsByFrameDuration = collections.defaultdict(list)
with open(datadir+"/targethits.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        hit = TargetHit(row)

        if len(hit.assignmentId) > 4:
            targetHitsByFrameDuration[hit.frameDuration].append(hit)

trialsByFrameDuration = collections.defaultdict(list)
with open(datadir+"/trials.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        trial = Trial(row)

        if len(hit.assignmentId) > 4:
            trialsByFrameDuration[hit.frameDuration].append(trial)

print "loaded"

trialsByAssIdAndTrialId = collections.defaultdict(dict)
for trial in trials:
    trialsByAssIdAndTrialId[trial.assignmentId][trial.trialId] = trial

hitsByAssId = collections.defaultdict(list)
for hit in targethits:
    hitsByAssId[hit.assignmentId].append(hit)

## WSL's terrible take on analytics
proxByTargetCount = {}
for e in targethits:
    idx = e.targetCount
    try:
        idx = trialsByAssIdAndTrialId[e.assignmentId][e.trialId].targetTotalCount
    except:
        print("broken")
        continue
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

