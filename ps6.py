#Hem N Chaudhary
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat   

def read_data(filename):
    '''

    Parameters
    ----------
    filename : string
        file storing comma separated data

    Returns
    -------
    numpy array of data stored in filename. file rows are converted to rows in the np array. The first element of each row is cast
    to an int. All other elements are cast to floats

    '''
    data = []
    with open(filename, 'r') as f:
        for x in f:
            entry = [float(i) for i in x.split(',')]
            entry[0] = int(entry[0]) #first element of each line is the class label
            data.append(entry)
    return np.array(data)

class KMeansClustering(KMeans):
    
    def __init__(self, data, k):
        super().__init__(n_clusters=k, random_state=0)
        self.fit(data)
    
    def get_centroids(self):
        'return np array of shape (n_clusters, n_features) representing the cluster centers'
        return self.cluster_centers_
    
    def get_labels(self, data):
        'Predict the closest cluster each sample in data belongs to. returns an np array of shape (samples,)'
        return self.predict(data)
    
    def total_inertia(self):
        'returns the total inertia of all clusters, rounded to 4 decimal points'
        return round(self.inertia_, 4)
    
def plot_try_k_clusters(avg_purities, inertias):
    '''
    plots the results of try_k_clusters
    assumes avg_purities and inertias are lists of equal length
    and follow the docstring of try_k_clustesrs
    '''
    assert type(avg_purities) is list and type(inertias) is list
    assert len(avg_purities) == len(inertias)
    x=np.arange(len(avg_purities)) + 1
    avg_purities = [x*100 for x in avg_purities]
    
    
    plt.plot(x, avg_purities, 'bo')
    plt.title("Average Purity of clusters")
    plt.xlabel("Num Clusters")
    plt.ylabel("% Purity")
    plt.show()
    
    
    plt.plot(x, inertias, 'rx''')
    plt.title("Total Inertia of Clusters")
    plt.xlabel("Num Clusters")
    plt.ylabel("Total Inertia")
    plt.show()

##### END HELPER CODE #####

def prep_dataset(raw_data):
    '''
    Prepares the raw dataset for clustering. Separate the raw data into sample features and labels

    Parameters
    ----------
    raw_data : np array
        A np array of shape (num_samples, num_features + 1) The first element of 
        each row is the class label for that sample. The remaining elements are the sample features

    Returns
    -------
    Tuple of (data, labels)
    
    data : np array of shape (num samples, num_features)
    labels : np array of shape (num_samples, ). labels for the data set samples

    '''
    data=raw_data[:,1:] #every thing except first column
    labels=raw_data[:,0] #Only the first column
    
    return (np.array(data),np.array(labels))
    

def kmeans(data, k):
    '''
    Run the kmeans clustering algorithm with k clusters on data. Use the KMeansClustering class provided
    to run the clustering algorithm.  

    Parameters
    ----------
    data : a numpy array with shape (N,X), where N is the number of wines and X is the number of features per wine
    k : int, number of clusters for kMeans

    Returns
    -------
    a tuple of (labels, inertia)
    labels: a size N 1-d numpy array, representing the cluster labels for each data point
    inertia: float, the total intertia for the clusters
    
    '''
    ans=KMeansClustering(data,k)
    return (ans.get_labels(data),ans.total_inertia()) #using the class methods

def scale_data(data):
    '''
    Scale data features using a MinMax scaling. Each feature should be transformed such that:
        
        f_scaled = (f - f_min) / (f_max - f_min)
    
    where f is the unscaled feature, f_min is the minimum value of that feature across
    all samples, and f_max is the maximum value of that feature across all samples.
    
    Note that, for f = f_max, f_scaled = 1. For f = f_min, f_scaled = 0.
    
    Parameters
    ----------
    data : np array of shape (num samples, num features)

    Returns
    -------
    scaled : np array of shape (num samples, num features). Each feature should be individually scaled to the range [0,1].

    '''
    f=data
           
    fscaled=(f-f.min(axis=0))/(f.max(axis=0)-f.min(axis=0)) #according to the formula
            
    
    return fscaled

def cluster_purity(clusters, labels):
    '''
    Find the purity of the clusters. Purity is defined as the proportion of a
    cluster that is taken up by the most represented class label within that cluster. If multiple class labels are represented equally,
    return the percent composition of either label. Round purity values to the 4 decimal points
    

    Parameters
    ----------
    clusters : np array of shape (num_samples,) with each element being an int
        representing the sample's cluster. Values of clusters will be in the range [0,num_clusters]
    labels : np array of shape (num_samples,). The class labels for each sample

    Returns
    -------
    purities : list of length num_clusters, purity values for each cluster
        

    '''
    dic={}
    for i in range(len(clusters)): #organizing the cluster in dictionary
        if clusters[i] not in dic.keys():
            dic[clusters[i]]=[labels[i]]
        else:
            dic[clusters[i]].append(labels[i])
 
    ans=[]
    for listt in dic.values(): #every list in the dic
        tempcount=0
        modlist=stat.mode(listt)
        for element in listt: #frequency of the most represented element
            if element==modlist:
                tempcount+=1
        ans.append(round(tempcount/len(listt),4))
    return ans

def try_k_clusters(data, labels, ks):
    '''
    Try kmeans clustering with num_clusters = 1,2,...ks. Return the average cluster purity

    Parameters
    ----------
    data : np array of shape (num samples, num features)
    labels : np array of shape (num_samples,). The class labels for each sample
    ks : int indicating the k values to try. all integer k values will be tried in the range [1,ks]

    Returns
    -------
    A tuple of (avg_purities, inertias)
    
        avg_purities: a list of floats, length ks. The average purity value of all
        clusters from kmeans clustering for all k-values in range [1,ks]. Round the average
        purity values to 4 decimal points.
        avg_purities[i] = average purity score of the i+1 clusters from kmeans clustering with k=i+1.
        
        inertias: a list of floats, length ks. The total inertia values from
        kmeans clustering for all k-values in range [1,ks]. Round the total inertia
        values to 4 decimal points.
        inertias[i] = total inertia of the i+1 clusters from kmeans clustering with k=i+1.

        
    '''
    ans=[]
    inertias=[]
    for k in range(1,ks+1):
        clusters=kmeans(data, k) #first element cluster; second element inertai
        purityarray=cluster_purity(clusters[0], labels)
        ans.append(round(np.mean(purityarray),4)) #averaging the cluster purity
        inertias.append(round(clusters[1],4))
    
    return (ans,inertias)

if __name__ == "__main__":
    pass    
    #OPTIONAL: Plot average purity and inertia
    # k = 10
    # avg_purity, inertia = try_k_clusters(scaled_features, labels, k)
    # plot_try_k_clusters(avg_purity, inertia)
    
    
    
    