#Ryan Sikora
#This program will take the data from seedsData.txt and use K-Means clustering 
#to correctly sort the kernels into three groups, it will also compute each cluster's
#cohesion, separation, and integerity

import random,pylab

#figure 22.6 (repeated)
def minkowskiDist(v1, v2, p):
    """Assumes v1 and v2 are equal-length arrays of numbers
       Returns Minkowski distance of order p between v1 and v2"""
    dist = 0.0
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i])**p
    newdist = dist**(1/float(p))
    return newdist 

#Figure 23.2
class Example(object):
    
    def __init__(self, name, features, label = None):
        #Assumes features is an array of floats
        self.name = name
        self.features = features
        self.label = label
        
    def dimensionality(self):
        return len(self.features)
    
    def getFeatures(self):
        return self.features[:]
    
    def getLabel(self):
        return self.label
    
    def getName(self):
        return self.name
    
    def distance(self, other):
        return minkowskiDist(self.features, other.getFeatures(), 2)
    
    def __str__(self):
        return self.name +':'+ str(self.features) + ':'\
               + str(self.label)

#Figure 23.3
class Cluster(object):
    
    def __init__(self, examples):
        """Assumes examples a non-empty list of Examples"""
        self.examples = examples
        self.centroid = self.computeCentroid()
        
    def update(self, examples):
        """Assume examples is a non-empty list of Examples
           Replace examples; return amount centroid has changed"""
        oldCentroid = self.centroid
        self.examples = examples
        self.centroid = self.computeCentroid()
        return oldCentroid.distance(self.centroid)
    
    def computeCentroid(self):
        vals = pylab.array([0.0]*self.examples[0].dimensionality())
        for e in self.examples: #compute mean
            vals += e.getFeatures()
        centroid = Example('centroid', vals/len(self.examples))
        return centroid

    def getCentroid(self):
        return self.centroid

    def variability(self):
        totDist = 0.0
        for e in self.examples:
            totDist += (e.distance(self.centroid))**2
        return totDist
        
    def members(self):
        for e in self.examples:
            yield e

    def __str__(self):
        names = []
        kama = []
        rosa = []
        canadian = []
        for e in self.examples:
            names.append(e.getName())
        names.sort()
        for e in self.examples:
            f = e.getFeatures()
            if f[7] == 1:
                kama.append(f)
            if f[7] == 2:
                rosa.append(f)
            if f[7] == 3:
                canadian.append(f)
        result = 'Cluster with centroid '\
               + str(self.centroid.getFeatures()) + ' contains:\n  ' + str(len(kama)) + ' Kama ' + str(len(rosa)) + ' Rosa ' + str(len(canadian)) + ' Canadian.'
        
        return result[:] 

#Figure 23.4
def dissimilarity(clusters):
    totDist = 0.0
    for c in clusters:
        totDist += c.variability()
    return totDist
    
def trykmeans(examples, numClusters, numTrials, verbose = False):
    """Calls kmeans numTrials times and returns the result with the
          lowest dissimilarity"""
    best = kmeans(examples, numClusters, verbose)
    minDissimilarity = dissimilarity(best)
    trial = 1
    while trial < numTrials:
        try:
            clusters = kmeans(examples, numClusters, verbose)
        except ValueError:
            continue #If failed, try again
        currDissimilarity = dissimilarity(clusters)
        if currDissimilarity < minDissimilarity:
            best = clusters
            minDissimilarity = currDissimilarity
        trial += 1
    return best

#figure 23.5
def kmeans(examples, k, verbose = False):
    #Get k randomly chosen initial centroids, create cluster for each
    initialCentroids = random.sample(examples, k)
    clusters = []
    for e in initialCentroids:
        clusters.append(Cluster([e]))
        
    #Iterate until centroids do not change
    converged = False
    numIterations = 0
    while not converged:
        numIterations += 1
        #Create a list containing k distinct empty lists
        newClusters = []
        for i in range(k):
            newClusters.append([])
            
        #Associate each example with closest centroid
        for e in examples:
            #Find the centroid closest to e
            smallestDistance = e.distance(clusters[0].getCentroid())
            index = 0
            for i in range(1, k):
                distance = e.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            #Add e to the list of examples for appropriate cluster
            newClusters[index].append(e)
            
        for c in newClusters: #Avoid having empty clusters
            if len(c) == 0:
                raise ValueError('Empty Cluster')
        
        #Update each cluster; check if a centroid has changed
        converged = True
        for i in range(k):
            if clusters[i].update(newClusters[i]) > 0.0:
                converged = False
                
        if verbose:
            print('Iteration #' + str(numIterations))
            for c in clusters:
                print(c)
            print('') #add blank line
    return clusters


def feature(featureDatafile):
    infile=open(featureDatafile,'r')
    feature={}
    badlist = []
    ID=1
    for line in infile: #adding all the data to the feature dictionary
        feature[ID]=line.replace('\n',' ').split('\t')
        ID+=1
    infile.close()
    for i in feature: #getting rid of all dictionary entries that are empty
        if feature[i] == [' ']:
            badlist.append(i)
    for b in badlist:
        del feature[b]
    return feature 

def makeExamples(f):
    #using a feature dictionary, creates examples for use in clustering
    examples=[]
    for key in f:
        examples.append(Example(str(key),[float(x) for x in f[key][:]]))
    return examples

def cohesion(cluster):
    '''Given a cluster, it computes the reciprocal of the sum of each example's distance from the centroid'''
    centroid = cluster.getCentroid()
    coh = 0
    for c in cluster.examples:
        cc = c.distance(centroid)
        coh = coh + cc
    return 1/coh
    
def separation(cluster1,cluster2):
    '''Given two clusters, it computes the distance between the two centroids'''
    dist = minkowskiDist(cluster1.getCentroid().getFeatures(),cluster2.getCentroid().getFeatures(),2)
    return dist

def integerity(cluster):
    '''Given a cluster, it computers the proportion of the cluster comprised by the majority type in the cluster'''
    kama = []
    rosa = []
    canadian = []
    for i in cluster.examples:
        f = i.getFeatures() 
        if f[7] == 1:
            kama.append(f)
        if f[7] == 2:
            rosa.append(f)
        if f[7] == 3:
            canadian.append(f)
    maxm = max([len(kama),len(rosa),len(canadian)])
    integ = maxm*((len(kama)+len(rosa)+len(canadian)))**-1
    return integ

#makes the examples using the generated future dictionary 
e = makeExamples(feature('seedsData.txt')) 

#computes the best kmeans cluster
best = trykmeans(e,3,500) 

#defines each cluster as Cluster 1, Cluster 2, Cluster 3
print('Cluster 1 is a ' + str(best[0]) + '\n')
print('Cluster 2 is a ' + str(best[1]) + '\n')
print('Cluster 3 is a ' + str(best[2])+ '\n')

#creates a list of each cluster's cohesion 
cohesions = []
coh1 = cohesion(best[0])
coh2 = cohesion(best[1])
coh3 = cohesion(best[2])

#prints each cluster's cohesion
print('The cohesion of Cluster 1 is ' + str(coh1))
print('The cohesion of Cluster 2 is ' + str(coh2))
print('The cohesion of Cluster 3 is ' + str(coh3) + '\n')

#finds the max cohesion 
cohesions.append(coh1)
cohesions.append(coh2)
cohesions.append(coh3)
maxcoh = max(cohesions)

#finds the cluster with the max cohesion and prints it
if maxcoh == cohesions[0]:
    print('The largest cohesion is from Cluster 1 with a cohesion of ' + str(maxcoh) + '\n')
elif maxcoh == cohesions[1]:
    print('The largest cohesion is from Cluster 2 with a cohesion of ' + str(maxcoh) + '\n')
elif maxcoh == cohesions[2]:
    print('The largest cohesion is from Cluster 3 with a cohesion of ' + str(maxcoh) + '\n')

#creates a list of each possible separation combination
seps = []
sep12 = separation(best[0],best[1])
sep23 = separation(best[1],best[2])
sep13 = separation(best[0],best[2])

#prints each separation combination
print('The separation between Cluster 1 and Cluster 2 is ' + str(sep12))
print('The separation between Cluster 2 and Cluster 3 is ' + str(sep23))
print('The separation between Cluster 1 and Cluster 3 is ' + str(sep13) + '\n')

#finds the max separation
seps.append(sep12)
seps.append(sep23)
seps.append(sep13)
maxsep = max(seps)

#finds the pair of clusters with the highest separation
if maxsep == seps[0]:
    print('The largest separation is between Cluster 1 and Cluster 2 with separation ' + str(maxsep) + '\n')
elif maxsep == seps[1]:
    print('The largest separation is between Cluster 2 and Cluster 3 with separation ' + str(maxsep) + '\n')
elif maxsep == seps[2]:
    print('The largest separation is between Cluster 1 and Cluster 3 with separation ' + str(maxsep) + '\n')

#creates a list and computes all integerities
integs = []    
integ1 = integerity(best[0])
integ2 = integerity(best[1])
integ3 = integerity(best[2])

#prints each integerity
print('The integerity of Cluster 1 is ' + str(integ1))
print('The integerity of Cluster 2 is ' + str(integ2))
print('The integerity of Cluster 3 is ' + str(integ3) + '\n')

#computes the max integerity 
integs.append(integ1)
integs.append(integ3)
integs.append(integ2)
maxinteg = max(integs)

#finds the cluster with the highest integerity and prints it
if maxinteg == integs[0]:
    print('The largest integerity is from Cluster 1 with an integerity of ' + str(maxinteg) + '\n')
elif maxinteg == integs[1]:
    print('The largest integerity is from Cluster 2 with an integerity of ' + str(maxinteg) + '\n')
elif maxinteg == integs[2]:
    print('The largest integerity is from Cluster 3 with an integerity of ' + str(maxinteg) + '\n')
    
#Computes the global integerity of the cluster grouping 
globalinteg = 0
for i in range(len(integs)):
    globalinteg = globalinteg + integs[i]
    
avg = globalinteg/len(integs)
print('The total Global Integerity is ' + str(avg))