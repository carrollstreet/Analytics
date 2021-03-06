#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import scipy.stats as st
from tqdm import tqdm
import matplotlib.pyplot as plt

class Bootstrap:
    
    def __init__(self, alpha=0.05, boot_samples=1000, statistic=np.mean, random_state=42):
        self.bootstrap_samples = boot_samples
        self.statistic = statistic
        self.random_state = random_state
        self.bootstrap_conf_level = 1 - alpha
        self.left_quant = (1 - self.bootstrap_conf_level) / 2
        self.right_quant = 1 - (1 - self.bootstrap_conf_level) / 2
        
    def __str__(self):
        return f'{type(self)}\n\
bootstrap_samples: {self.bootstrap_samples}\n\
statistic: {self.statistic}\n\
confidence_level: {self.bootstrap_conf_level}\n\
left_quant: {self.left_quant}\n\
right_quant: {self.right_quant}\n\
random_state: {self.random_state}'
        
    def fit(self, sample_a, sample_b):
        np.random.seed(self.random_state)
        boot_len = max([len(sample_a), len(sample_b)])
        self.boot_data = []
    
        for i in tqdm(range(self.bootstrap_samples)): # извлечение подвыборок 
            sub_a = np.random.choice(sample_a, size=boot_len, replace = True)
            sub_b = np.random.choice(sample_b, size=boot_len, replace = True)
            self.boot_data.append(self.statistic(sub_a-sub_b)) 

        self.quants = np.quantile(self.boot_data,[self.left_quant, self.right_quant])
    
    def compute(self):
        p_1 = st.norm.cdf(x = 0, loc = np.mean(self.boot_data), scale = np.std(self.boot_data))
        p_2 = st.norm.cdf(x = 0, loc = -np.mean(self.boot_data), scale = np.std(self.boot_data))
        p_value = min(p_1, p_2) * 2
        return p_value
    
    def get_graph(self, title=None):
        _, _, bars = plt.hist(self.boot_data, bins = 50)
        for bar in bars:
            bar.set_edgecolor('white')
            if bar.get_x() <= self.quants[0] or bar.get_x() >= self.quants[1]:
                bar.set_facecolor('#EF553B')
            else: 
                bar.set_facecolor('#636EFA')

        plt.vlines(self.quants,ymin=0,ymax=len(bars),linestyle='--')
        plt.xlabel('differences')
        plt.ylabel('frequency')
        plt.title(title)


def confidence_interval(data, conf_level=0.95,boot_samples=1000,random_state=42,statistic=np.mean,**kwargs):
    np.random.seed(random_state)
    left_quant, right_quant = (1 - conf_level) / 2, 1 - (1-conf_level) / 2
    
    values = []
    for i in (range(boot_samples)):
        subsample = np.random.choice(data, size=len(data), replace=True)
        values.append(statistic(subsample, **kwargs))

    return np.quantile(values, [left_quant, right_quant])
    

def correlation_ratio(categories, values):
    cat = np.unique(categories, return_inverse=True)[1]
    values = np.array(values)
    
    ssw = 0
    ssb = 0
    for i in np.unique(cat):
        subgroup = values[np.argwhere(cat == i).flatten()]
        ssw += np.sum((subgroup-np.mean(subgroup))**2)
        ssb += len(subgroup)*(np.mean(subgroup)-np.mean(values))**2

    return (ssb / (ssb + ssw))**.5


