#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 13:43:39 2021

@author: danielm
"""
import os
import numpy as np
import h5py
import matplotlib.pyplot as plt

drivepath = r'/Volumes/Extreme SSD/'
nm_A_path = drivepath+'NaturalMoviesA/'
nm_B_path = drivepath+'NaturalMoviesB/'
nm_C_path = drivepath+'NaturalMoviesC/'
savepath = r'/Users/danielm/Desktop/columnar_dynamics_analysis/'
figurepath = r'/Users/danielm/Desktop/columnar_dynamics_analysis/figures/'

def whiteboard():
    
    run_analysis('1a',nm_A_path)
    run_analysis('3',nm_A_path)
    run_analysis('1b',nm_B_path)
    run_analysis('1c',nm_C_path)
    run_analysis('2',nm_C_path)
    
    
    # sweep_responses = get_sweep_responses(637669270,'1a',nm_A_path)
    
    # response_percentile = get_response_percentile(637669270,'1a',nm_A_path,savepath)
    # print(response_percentile.shape)
    
    # for i in range(10):
    #     plot_neuron_movie_response(sweep_responses[:,i,:],percentile_to_NLL(response_percentile[:,i],900))
    
def run_analysis(which_movie,movie_events_path):

    for f in os.listdir(movie_events_path):
        if f[:2].find('.')==-1 and f.find('_nm_events_analysis.h5')>-1:
            session_ID = get_session_ID_from_analysis_filename(f)
            print(session_ID)
            
            response_percentile = get_response_percentile(session_ID,which_movie,movie_events_path,savepath)
    
def plot_neuron_movie_response(sweep_responses,
                               response_percentile,
                               max_range=0.1):
    (num_frames,num_repeats) = sweep_responses.shape
    max_val = np.sort(sweep_responses.flatten())[int(max_range*num_frames*num_repeats)]
    
    plt.figure()
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    ax1.imshow(sweep_responses.T,
               cmap='Reds',
               aspect='auto',
               interpolation='none')
    # ax2.imshow(response_percentile.reshape(1,num_frames),
    #            cmap='RdBu_r',
    #            aspect='auto',
    #            vmin=0.0,
    #            vmax=1.0,
    #            interpolation='none')
    ax2.imshow(response_percentile.reshape(1,num_frames),
               cmap='RdBu_r',
               aspect='auto',
               vmin=-3.0,
               vmax=3.0,
               interpolation='none')
    plt.show()
    
def percentile_to_NLL(percentile,num_shuffles):
    
    percentile = np.where(percentile==0.0,1.0/num_shuffles,percentile)
    percentile = np.where(percentile==1.0,1.0-1.0/num_shuffles,percentile)
    NLL = np.where(percentile<0.5,
                   np.log10(percentile)-np.log10(0.5),
                   -np.log10(1.0-percentile)+np.log10(0.5))
    
    return NLL
    
def get_response_percentile(session_ID,which_movie,movie_events_path,savepath):
    
    result_filepath = savepath+str(session_ID)+'_'+which_movie+'_response_percentile.npy'
    if os.path.isfile(result_filepath):
        response_percentile = np.load(result_filepath)
    else:
        sweep_responses = get_sweep_responses(session_ID,which_movie,movie_events_path)
        response_percentile = calculate_response_percentile(sweep_responses)
        np.save(result_filepath,response_percentile)
    
    return response_percentile
    
def calculate_response_percentile(sweep_responses):
    
    # generate 1 shuffle for every n-frame shift of the neuron's activity timeseries
    
    (num_frames,num_neurons,num_repeats) = sweep_responses.shape
    print(sweep_responses.shape)
    
    num_shuffles =  num_frames
    
    actual_responses = sweep_responses.mean(axis=2).reshape(num_frames,num_neurons,1)
    
    shuffle_responses = np.zeros((num_frames,num_neurons,num_shuffles))
    for ns in range(num_shuffles):
        shuffle_sweeps = shift_responses_by_frames(sweep_responses,ns)
        shuffle_responses[:,:,ns] = shuffle_sweeps.mean(axis=2)
        
    response_percentile = (shuffle_responses < actual_responses).mean(axis=2)
    
    return response_percentile
            
def shift_responses_by_frames(sweep_responses,shift_size):
    (num_frames,num_neurons,num_repeats) = sweep_responses.shape
    if shift_size==0:
        shuffle_sweeps = sweep_responses.copy()
    else:
        shuffle_sweeps = np.zeros((num_frames,num_neurons,num_repeats))
        for rep in range(num_repeats):
            shuffle_sweeps[:shift_size,:,rep] = sweep_responses[(-shift_size):,:,rep-1]
            shuffle_sweeps[shift_size:,:,rep] = sweep_responses[:(num_frames-shift_size),:,rep]
    return shuffle_sweeps

def get_sweep_responses(session_ID,which_movie,movie_events_path):
    
    filename = session_ID_to_analysis_filename(session_ID)
    f = h5py.File(movie_events_path+filename,'r')
    sweep_responses = np.array(f[response_array_name(which_movie)])
    
    return sweep_responses

def response_array_name(which_movie):
    return 'response_trials_'+which_movie

def session_ID_to_analysis_filename(session_ID):
    return str(session_ID) + '_nm_events_analysis.h5'
    
def get_session_ID_from_analysis_filename(filename,
                                          session_ID_digits=9):
    return int(filename[:9])
    

if __name__=='__main__':  
    whiteboard()