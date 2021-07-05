#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 13:43:39 2021

@author: danielm
"""
import os
import numpy as np
import h5py

drivepath = r'/Volumes/Extreme SSD/'
nm_A_path = drivepath+'NaturalMoviesA/'
savepath = r'/Users/danielm/Desktop/columnar_dynamics_analysis/'

def whiteboard():
    
    #run_analysis('1a',nm_A_path)
    
    sweep_responses = get_sweep_responses(637669270,'1a',nm_A_path)
    
    
def run_analysis(which_movie,movie_events_path):

    for f in os.listdir(movie_events_path):
        if f[:2].find('.')==-1 and f.find('_nm_events_analysis.h5')>-1:
            session_ID = get_session_ID_from_analysis_filename(f)
            print(session_ID)
            
            sweep_responses = get_sweep_responses(session_ID,which_movie,movie_events_path)

def get_sweep_responses(session_ID,which_movie,movie_events_path):
    
    filename = session_ID_to_analysis_filename(session_ID)
    
    f = h5py.File(movie_events_path+filename,'r')
    
    sweep_responses = np.array(f[response_array_name(which_movie)])
    
    (num_frames,num_neurons,num_repeats) = sweep_responses.shape
    print(sweep_responses.shape)
    
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