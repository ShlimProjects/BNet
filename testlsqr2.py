# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 14:33:25 2016

@author: Joseph
"""


import numpy as np
import scipy as sp
from numpy.linalg import inv
from numpy import pi, dot, transpose, radians, exp, log
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import time
# from sympy import *

NN = 5
rr = np.arange(0.1,1,0.1)
m = 1
N = 700
dphi = 2
beta = 0.0
space = np.array([0,1,2,3])
NumCorr = 13
#alpha2 = np.arange(0.1,10.0,0.05)
CR = list()
alpha2 = np.array([.587, .6, .5])

R = np.zeros((N+1,N/2))
P = np.zeros((N+1,N/2))

lattice = np.zeros((N,N+1))
run = 0
xc = np.arange(0,NumCorr+1,1)

def Pn2(w,v,index):
    return np.multiply(L[index],v[:,-1])/(w[-1]*v[index,-1])

def Randvar(Pn,limits=space):
    Pnorm = (Pn/np.sum(Pn))
    return np.random.choice(limits,p=Pnorm)

"""
def Lattice_new(inp,w,v,limits=space):
    Prb = abs(np.multiply(L[inp],v[:,-1])/(w[-1]*v[inp,-1]))
    Pnorm = (Prb)/np.sum(Prb)
    return np.random.choice(limits,p=Pnorm)
"""

def Lattice_new(inp,w,v,limits=space):
    Prob = Prb[inp]
    Pnorm = (Prob/np.sum(Prob))
    return np.random.choice(limits,p=Pnorm)


def ConvLat_Inp(lat):
    if np.all(lat == np.array([-1,-1])):  
        return 0
    elif np.all(lat == np.array([-1,1])):
        return 1
    elif np.all(lat == np.array([1,-1])):
        return 2
    elif np.all(lat == np.array([1,1])):
        return 3

def ConvInp_Lat(inp):
    if inp == 0:
        return np.array([-1,-1])
    elif inp == 1:
        return np.array([-1,1])
    elif inp == 2:
        return np.array([1,-1])
    elif inp == 3:
        return np.array([1,1])

alpha = 0.6
beta = 0.0
L = np.zeros((4,4))
L[0,0] = exp(4*alpha+4*beta)
L[3,3] = exp(4*alpha - 4*beta)
L[0,1] = L[1,0] = L[2,0] = L[0,2] = exp(2*beta)
L[1,3] = L[3,1] = L[3,2] = L[2,3] = exp(-2*beta)
L[2,1] = L[1,2] = exp(-4*alpha)
L[3,0] = L[0,3] = L[2,2] = L[1,1] = 1.0
w,v = np.linalg.eigh(L)


al = Pn2(w,v,0)[0]
beta = Pn2(w,v,1)[0]
gamma = Pn2(w,v,0)[1]
delt = Pn2(w,v,3)[0]
nu = Pn2(w,v,1)[1]
eta = Pn2(w,v,1)[2]

vecc = np.array([al,beta,gamma,delt,nu,eta]) 

lsqr = np.zeros(NN)

xxx = np.array([0,0,1,1,2,2,3,3,4,4,5,5])
yyy = np.array([1.0,-1.0])
Prb = np.array([[al,gamma,gamma,delt],[beta,nu,eta,beta],[beta,eta,nu,beta],[delt,gamma,gamma,al]])

vecc = np.array([al,beta,gamma,delt,nu,eta]) 
vecc = abs(vecc + np.array([ 0.04,  0.03, -0.01,  0.01, -0.01, -0.01]))

vec2 = vecc
al2,beta2,gamma2,delt2,nu2,eta2 = vec2
Prb = np.array([[al2,gamma2,gamma2,delt2],[beta2,nu2,eta2,beta2],[beta2,eta2,nu2,beta2],[delt2,gamma2,gamma2,al2]])
pp = 0

plt.figure()
while pp < NN:
    t1 = time.time()
    
    if pp > 0:
        vec2 = vecc
        
        rchoice = np.random.choice([0,1,2,3,4,5])
        sn = np.random.choice([1.0,-1.0])        
        


        while(vec2[rchoice] + sn*(0.01) < 0):
            rchoice = np.random.choice([0,1,2,3,4,5])
            sn = np.random.choice([1.0,-1.0])

        print('Run {} || Random index: {} || Sign Change: {}'.format(str(pp),str(rchoice),str(sn)))
        
        vec2[rchoice] += sn*(0.01)
        
        al2,beta2,gamma2,delt2,nu2,eta2 = vec2
        Prb = np.array([[al2,gamma2,gamma2,delt2],[beta2,nu2,eta2,beta2],[beta2,eta2,nu2,beta2],[delt2,gamma2,gamma2,al2]])


    for i in xrange(0,len(lattice[0,:])):
        lattice[0,i] = np.random.choice([-1,1],p=[0.5,0.5])
    
    '''
    phi = Symbol('phi')
    phi2 = Dummy('phi2')
    En = Dummy('En')
    
    
    Psi = exp(-m/2.0 * phi**2.0)**(1.0/2.0)
    
    Lagr = -(1.0/2.0) * (((phi - phi2)/eps)**2.0 + m**2.0*((phi + phi2)/2.0)**2.0)
    Fn = (exp(eps*En)/(2.0*pi*eps)**(1.0/2.0))*exp(eps*Lagr)
    
    Pn = Fn*Psi/Psi.subs(phi,phi2)
    '''
    
    #    return (exp(-m/2.0 * x**2.0))
    #
    #def Lagr(x,space,alpha,beta):
    #    return -1.0* ( np.add((alpha*(space*x))**2.0, -beta*((space + x)/2.0)**2.0)) - En
    #
    #def F2(x,y,En):
    #    return exp(eps*Lagr(x,y,0.1,En))
    
    #This is my PC
    
    
    tt = time.time()
    w = 0 #dummy
    v = 0 #dummy
    
    
    tt2 = time.time()
    
    '''
    R[0,0] = Randvar(np.power(v[:,-1],2.0),np.array[0,1,2,3])
    '''
    
    '''
    for i in xrange(1,N):
        for j in xrange(0,N/2):
            templattice[i,2*j:2*(j+1)] = ConvInp_Lat(Lattice_new(ConvLat_Inp(lattice[i-1,2*j:2*j+1]),w,v))
            templattice[i,N] = templattice[i,0]
            lattice[i,1+(2*j):(2*j+3) ] = ConvInp_Lat(Lattice_new(ConvLat_Inp(templattice[i,1+(2*j):(3+2*j) ]),w,v))
            lattice[i,0] = lattice[i,N]
    '''
    
    lattice[0,0] = lattice[0,N]
    '''
    for i in xrange(1,N):
        for j in xrange(0,N/2):
            lattice[i,2*j:(2*j+2)] = ConvInp_Lat(Lattice_new(ConvLat_Inp(lattice[i-1,2*j:2*j+2]),w,v))
            lattice[i,(2*j+1):(2*j+3)] = ConvInp_Lat(Lattice_new(ConvLat_Inp(lattice[i,(2*j+1):(2*j+3)]),w,v))
            lattice[i,0] = lattice[i,(j*2)+2]
    '''
    tlattice = np.zeros(N+1)
    for i in xrange(1,N):
        for j in xrange(0,N/2):
            tlattice[2*j:(2*j+2)] = ConvInp_Lat(Lattice_new(ConvLat_Inp(lattice[i-1,2*j:2*j+2]),w,v))
        tlattice[-1] = tlattice[0]
        for k in xrange(0,N/2):
            lattice[i,(2*k+1):(2*k+3)] = ConvInp_Lat(Lattice_new(ConvLat_Inp(tlattice[(2*k+1):(2*k+3)]),w,v))
        lattice[i,0] = lattice[i,-1]
    
    """
    for i in xrange(1,N):
        for j in xrange(0,N/2)
            Prob = abs(Pn2(w,v,R[i,j]))
            R[i] = Randvar(Prob,space)
    """
    t2 = time.time()
    
    """
    Corr = np.zeros(NumCorr)
    
    for j in xrange(1,NumCorr+1):
        Cor = np.zeros((NumCorr,N))
        for i in xrange(0,N):
            if (i + j) <= N:
                Cor[j-1][i] = R[i]*R[i+j]
        Corr[j-1] = np.sum(Cor[j-1]/len(Cor[j-1]))
    """
    '''
    plt.figure()
    plt.hist(R, 500, normed=True)
    plt.figure()
    plt.plot(space,np.power(v[:,-1],2.0))
    '''
    
    HCorr = np.zeros((N,NumCorr+1))
    VCorr = np.zeros((N,NumCorr+1))
    VVCorr = np.zeros(NumCorr+1)
    HHCorr = np.zeros(NumCorr+1)
    
    ttt1 = time.time()
    hd = np.zeros(N)
    vd = np.zeros(N)
    
    for i in xrange(0,N):
        hd = lattice[i,:(N-1)]
        vd = lattice[:,i]
        
        for j in xrange(0,NumCorr+1):
            HC = np.diagonal(np.dot(hd[:,None],hd[None,:]),j)
            VC = np.diagonal(np.dot(vd[:,None],vd[None,:]),j)
            
            HCorr[i,j] = np.sum(HC)/HC.shape[0]
            VCorr[i,j] = np.sum(VC)/VC.shape[0]
    for i in xrange(0,NumCorr+1):
        HHCorr[i] = np.sum(HCorr[:,i])/(N)
        VVCorr[i] = np.sum(VCorr[:,i])/(N)
    
    ttt2 = time.time()
    
    lsqrr = np.sum(np.sqrt(np.power(np.add(HHCorr,-VVCorr),2.0)))

    """
    for i in xrange(0,NumCorr+1):
        HCor = np.zeros((NumCorr+1,N))
        VCor = np.zeros((NumCorr+1,N))
        for k in xrange(0,N):
            for j in xrange(0,N):
                if (i + j + 1 ) <= N:
                    HCor[i][j] = lattice[k,j]*lattice[k,j+i]
                    VCor[i][j] = lattice[j,k]*lattice[j+i,k]
            HCorr[k,i] = np.sum(HCor[i]/len(HCor[i]))
            VCorr[k,i] = np.sum(VCor[i]/len(VCor[i]))
        HHCorr[i] = np.sum(HCorr[:,i])
        VVCorr[i] = np.sum(VCorr[:,i])
    """
    
    """
    plt.figure()
    plt.title(run)
    
    plt.loglog(HHCorr)
    plt.loglog(VVCorr)
    """
    
    #plt.plot(log(xc),log(HHCorr))
    #plt.plot(log(xc),log(VVCorr))
    
    t3=time.time()
    print('Run {} || Complete Lattice in {} || Complete Correlators in {} || lsqr is {}'.format(str(pp),str(t2-t1),str(ttt2-ttt1),str(lsqrr)))
    """
    
    def Correlations(rvec,NumCorr,lattice):
        xy=lattice.shape
        slope = rvec[1] / rvec[0]
    
        for i in xrange(0,NumCorr):
            for j in xrange(0,xy[0]):
                for k in xrange(0,xy[1]):
                    if ((i*rvec[0] + j*rvec[0]) < xy[0]) and ((i*rvec[1] + k*rvec[1]) < xy[1] ):
    
                        Cor[i]
    
    
    """
    
    """
    def Correlations(rvec,NumCorr,lattice):
        xy = lattice.shape
        d = (rvec[0]**2. + rvec[1]**2.)**(1.0/2.0)
        x = xy[0]
        y = xy[1]
        xx = np.arange(0,xy[0])
        yy = np.arange(0,xy[1])
        if rvec[1] < 0:
            s = -1
        elif rvec[1] = 0:
            s = 0
        elif rvec[1] > 0:
            s = 1
    
        if s = 1:
            for i in xrange(0,NumCorr + 1):
                for j in xrange(0,xy[0]):
                    k = 1
                    while (xy[0] - i*k*rvec[0] in xx) and (xy[1] - i*k*rvec[1] in yy):
                        Corr[i][j] = lattice[x - j + i*(k-1)*rvec[0],y + (k-1)]
    

    """
    #plotting:
    
    if (pp > 0) and (lsqrr <= lsqr[pp-1]):
        lsqr[pp] = lsqrr
        vecc = vec2
        pp += 1
        CR.append([vecc,Prb,HHCorr,VVCorr])
        plt.plot(abs(HHCorr - VVCorr))
        plt.show()
    elif pp == 0:
        lsqr[pp] = lsqrr
        pp += 1
        CR.append([vecc,Prb,HHCorr,VVCorr])
        plt.plot(abs(HHCorr - VVCorr))
        plt.show()
    #plt.contourf(lattice[:,:(N-1)])