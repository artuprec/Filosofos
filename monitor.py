#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 14:23:55 2022

@author: mat
"""
from multiprocessing import Condition, Lock, Value

class Table(object):
    def __init__(self,NPHIL,manager):
        self.NPHIL=NPHIL
        self.phil=manager.list([True]*self.NPHIL)
        self.mutex=Lock()
        self.free_fork=Condition(self.mutex)
        self.current_phil=None
        
    def set_current_phil(self,phil):
        self.current_phil=phil
        
    def  get_current_phil(self): 
        return self.current_phil
    
    def are_free_fork(self):
        phil=self.current_phil
        return self.phil[phil] and self.phil[(phil+1) % self.NPHIL]
    
    def wants_eat(self,phil):
        self.mutex.acquire()
        self.free_fork.wait_for(self.are_free_fork)
        self.phil[phil]=False
        self.phil[(phil+1) % self.NPHIL]=False
        self.mutex.release()
            
    def wants_think(self,phil):
        self.mutex.acquire()
        self.phil[phil]=True
        self.phil[(phil+1) % self.NPHIL]=True
        self.free_fork.notify_all()
        self.mutex.release()
        
        
class CheatMonitor():
    
    def __init__(self):
        self.eating = Value('i',0)
        self.mutex = Lock()
        self.check_eating = Condition(self.mutex)
    
    def wants_think(self,n):
        self.mutex.acquire()
        self.check_eating.wait_for(self.readyToThink)
        self.eating.value -= 1
        self.mutex.release()
        
    def is_eating(self,n):
        self.mutex.acquire()
        self.eating.value += 1
        self.check_eating.notify()
        self.mutex.release()
        
    def readyToThink(self):
        return self.eating.value == 2
    
    