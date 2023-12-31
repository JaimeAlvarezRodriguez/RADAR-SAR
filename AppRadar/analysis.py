"""
Description:    Algoritm to analysis doppler, ranging and SAR imaging coffee can RADAR

Based on course 'Build A Small Radar System Capable Of Sensing Range, Doppler, And Synthetic Aperture Radar Imaging' from MIT
This algorithm was written by Gregory L. Charvat
"""

import numpy as np
import numpy.fft as fft
import gc
from .file_management import load_RADARSAR, DEFAULT_NAME
from .import debug

__Scale__ = 0.405273437500000/13280
__c__ = 3E8


def dbv(input):
    return 20 * np.log10(abs(input))

def doppler(file = DEFAULT_NAME, progressbar = print):
    data, samplerate = load_RADARSAR(file)
    data = data * __Scale__

    Tp = 0.250
    n = Tp * samplerate
    n = int(n)
    Fc = 2257E6

    progressbar(20)

    s = data[0] * 1

    colums = round(len(s)/n)-1
    sif = np.ndarray([colums, n])

    for ii in range(colums):
        sif[ii, :] = s[(ii)*n : (ii+1)*n]

    progressbar(40)

    sif = sif - np.mean(sif)

    zpad = round(8*n/2)

    #Doppler vs time plot
    v = dbv(fft.ifft(sif, zpad))
    v = v[:, 1:round(len(v[0])/2)]
    mmax = v.max()

    progressbar(60)

    #Calculate velocity
    delta_f = np.linspace(0, samplerate/2, len(v[0]))
    lamb = __c__ / Fc
    velocity = delta_f * lamb / 2

    progressbar(80)

    #calculate time
    time = np.linspace(0, Tp*len(v), len(v))


    """for i in range(len(v)):
    for ii in range(len(v[i])):
        if (v[i][ii]-mmax) < -35:
            v[i][ii] = -35 + mmax
    """

    progressbar(95)
    velocity = velocity * 3.6
    return (time, velocity, (v-mmax).T)

def ranging(file=DEFAULT_NAME, progressbar = print):
    Y, FS = load_RADARSAR(file)

    Y = Y * 3.0518E-5

    #Constantes
    c = 3E8
    progressbar(10)
    #Parametros del RADAR
    Tp = 20E-3 #Duracion del pulso
    n = Tp * FS #Numero de muestras por pulso
    n = int(n)
    fstart = 2402E6 #Hz LFM Frecuencia de inicio por muestra
    fstop = 2495E6 #Hz LFM Frecuencia de stop de muestra

    BW = fstop - fstart #hz Ancho de banda de transmision
    f = np.linspace(fstart, fstop, int(np.round(n/2))) #Frecuenci de transmision instantanea
    progressbar(20)
    #Rango de resolucion
    rr = c/(2*BW)
    max_range = rr*n/2

    #La entrada parece estar invertida
    trig = 1 * Y[1]
    s = 1 * Y[0]
    progressbar(30)
    Y.resize(0)

    #Analiza los datos en el flanco acendente del pulso de sincronizacion
    count = 0
    thresh = 0
    start = (trig > thresh)

    sif = []
    time = []
    count = 0
    progressbar(40)

    for ii in range(100, int(len(start)-n)+1):
        ii = ii - 1
        if (start[ii] == 1) and (np.mean(start[ii-11:ii-1+1]) == 0):
            count = count + 1
            sif.append(s[ii:ii+n-1+1])
            time.append(ii*1/FS)
        
    sif = np.array(sif)
    time = np.array(time)
    progressbar(50)
    ave = np.mean(sif, axis=0)

    for ii in range(len(sif)):
        sif[ii, :] = sif[ii, :] - ave
    progressbar(60)
    zpad = 8*n//2

    v = dbv(fft.ifft(sif, zpad))

    S = v[:, 0:len(v[0])//2]
    m = v.max()
    progressbar(70)
    sif2 = sif[2-1:len(sif),:]-sif[1-1:len(sif)-1,:]
    v = fft.ifft(sif2,zpad,1)
    S = v
    R = np.linspace(0, max_range, zpad)
    progressbar(80)
    S = dbv(S[:, 1-1:len(v[0])//2])
    m = S.max()
    progressbar(95)
    return (np.linspace(0, (1/FS)*len(s), len(S)+1), np.linspace(0, max_range, len(S[0])+1), (S-m).T)

def SAR_1part(file=DEFAULT_NAME, progressbar=print):
    data, samplerate = load_RADARSAR(file)

    data = data * __Scale__

    Tp = 20e-3
    Trp = 0.250
    N = int(Tp*samplerate)
    fstart = 2402e6
    fstop = 2490e6

    Bw = fstop - fstart
    f = np.linspace(fstart, fstop, N//2)

    trig = 1 * data[1]
    s = data[0] 

    data = 0
    gc.collect()

    rpstart = np.abs(trig) > np.mean(np.abs(trig))
    count = 0
    Nrp = int(Trp * samplerate)

    progressbar(10)

    RP = []
    RPtrig = []

    for ii in range(Nrp+1, len(rpstart)-Nrp+1):
        if rpstart[ii-1] == 1 and np.sum(rpstart[ii-Nrp-1:ii-1-1+1]) == 0:
            count = count + 1
            RP.append(s[ii-1:ii+Nrp-1-1+1])
            RPtrig.append(trig[ii-1:ii+Nrp-1-1+1])

    progressbar(20)

    RP = np.array(RP)
    RPtrig = np.array(RPtrig)

    count = 0
    thresh = 0.08

    gc.collect()

    progressbar(30)

    sif = []

    for jj in range(1, len(RP)+1):
        SIF = np.zeros((N, ))
        start = (RPtrig[jj-1, :] > thresh)
        count = 0
        for ii in range(12, len(start) - 2*N + 1):
            vect = list(RPtrig[jj-1, ii-1:ii+2*N-1+1])
            Y = max(vect)
            I = vect.index(Y)
            if np.mean(start[ii-10-1:ii-2-1+1]) == 0 and I == 0:
                count = count + 1
                temp = RP[jj-1, ii-1:ii+N-1-1+1]
                SIF = temp + SIF
        q = fft.ifft(SIF/count)
        #SIF[jj-1, :] = fft.fft(q[len(q)//2+1-1:len(q)-1+1])
        extra = fft.fft(q[len(q)//2+1-1:len(q)-1+1])
        sif.append(extra)


    progressbar(40)

    sif = np.nan_to_num(np.array(sif), nan=1e-30)

    s = sif

    for ii in range(len(s)):
        s[ii, :] = s[ii, :] - np.mean(s.T, 1)

    sif = s

    gc.collect()
    c = 3e8

    #radar parameters
    fc = (fstop - fstart)/2 + fstart #(Hz) center radar frequency
    B = (fstop - fstart) #(hz) bandwidth
    #fc = (2590E6 - 2260E6)/2 + 2260E6#; %(Hz) center radar frequency
    #B = (2590E6 - 2260E6)#; %(hz) bandwidth
    cr = B/20E-3 #(Hz/sec) chirp rate
    Tp = 20E-3 #(sec) pulse width
    #VERY IMPORTANT, change Rs to distance to cal target
    #Rs = (12+9/12)*.3048#; %(m) y coordinate to scene center (down range), make this value equal to distance to cal target
    Rs = 0
    Xa = 0 #(m) beginning of new aperture length
    delta_x = 2*(1/12)*0.3048 #(m) 2 inch antenna spacing
    L = delta_x*(len(sif)) #(m) aperture length
    Xa = np.linspace(-L/2, L/2, int((L/delta_x))) #(m) cross range position of radar on aperture L
    Za = 0
    Ya = Rs #THIS IS VERY IMPORTANT, SEE GEOMETRY FIGURE 10.6
    t = np.linspace(0, Tp, len(sif[0])) #(s) fast time, CHECK SAMPLE RATE
    Kr = np.linspace(((4*np.pi/c)*(fc - B/2)), ((4*np.pi/c)*(fc + B/2)), (len(t)))
    progressbar(50)
    return (sif, delta_x, Rs, Kr, Xa)

def SAR_2part(sif, delta_x, Rs, Kr, Xa, progressbar = print):
    N = len(sif[0])
    H = []

    for ii in range(1, N + 1):
        H.append(0.5 + 0.5 * np.cos(2 * np.pi * (ii - N / 2) / N))

    H = np.array(H)
    sif_h = []
    for ii in range(len(sif)):
        sif_h.append(sif[ii, :].T*H)

    sif_h = np.array(sif_h)
    sif = sif_h
    zpad = 2048

    szeros = np.full(shape=(zpad, len(sif[0])), fill_value=0j)
    for ii in range(1, len(sif[0])+1):
        index = round((zpad - len(sif))/2) + 1
        szeros[index+1-1:(index + len(sif))-1+1, ii-1] = sif[:,ii-1]
    progressbar(60)
    sif = szeros.copy()
    szeros.resize(0)

    S = fft.fftshift(fft.fft(sif.T), 1).T.copy()

    sif.resize(0)
    gc.collect()

    Kx = np.linspace((-np.pi/delta_x), (np.pi/delta_x), len(S))

    phi_mf = np.ndarray(shape=np.shape(S))
    Krr = np.ndarray(shape=np.shape(S))
    Kxx = np.ndarray(shape=np.shape(S))

    for ii in range(1, len(S[0])+1):
        ii = ii - 1
        for jj in range(1, len(S)+1):
            jj = jj - 1
            phi_mf[jj, ii] = Rs * np.sqrt((Kr[ii])**2 - (Kx[jj])**2)
            Krr[jj, ii] = Kr[ii]
            Kxx[jj, ii] = Kx[jj]

    progressbar(70)

    smf = np.exp(0j*phi_mf)

    S_mf = S*smf

    smf.resize(0)
    phi_mf.resize(0)
    S.resize(0)
    gc.collect()

    kstart = 73
    kstop = 108.5
    #kstart = 95
    #kstop = 102

    Ky_even = np.linspace(kstart, kstop, 1024)

    count = 0
    Ky = np.ndarray(shape=(zpad, len(Kr)))
    S_st = np.full(shape=(zpad, len(Ky_even)), fill_value=0j)

    progressbar(80)

    for ii in range(1, zpad+1):
        count = count + 1
        Ky[count-1, :] = np.sqrt(Kr.T**2 - Kx[ii-1]**2)
        S_st[count-1, :] = np.interp(xp=Ky[count-1, :], fp=S_mf[ii-1, :], x=Ky_even)


    S_st = np.nan_to_num(np.array(S_st), nan=1e-30)

    S_mf.resize(0)
    Ky.resize(0)

    gc.collect()

    progressbar(85)

    N = len(Ky_even)
    H = np.ndarray(shape=(N, ))
    for ii in range(N):
        H[ii] = 0.5 + 0.5*np.cos(2*np.pi*((ii+1)-N/2)/N)


    S_sth = np.full(shape=np.shape(S_st), fill_value=0j)
    for ii in range(len(S_st)):
        S_sth[ii, :] = S_st[ii, :].T*H

    Krr.resize(0)
    Kxx.resize(0)
    gc.collect()

    progressbar(90)

    v = fft.ifft2(S_st, s=(len(S_st)*4, len(S_st[0])*4))

    bw = 3e8*(kstop-kstart)/(4*np.pi)
    max_range = (3E8*len(S_st[0])/(2*bw))*1/.3048
    S_image = v #edited to scale range to d^3/2
    S_image = np.fliplr(np.rot90(S_image))
    cr1 = -80 #(ft)
    cr2 = 80 #(ft)
    dr1 = 1 + Rs/.3048 #(ft)
    dr2 = 350 + Rs/.3048 #(ft)
    #data truncation
    dr_index1 = round((dr1/max_range)*len(S_image))
    dr_index2 = round((dr2/max_range)*len(S_image))
    cr_index1 = round(( (cr1+zpad*delta_x/(2*.3048)) /(zpad*delta_x/.3048))*len(S_image[0]))
    cr_index2 = round(( (cr2+zpad*delta_x/(2*.3048))/(zpad*delta_x/.3048))*len(S_image[0]))
    trunc_image = S_image[dr_index1-1:dr_index2, cr_index1-1:cr_index2]
    downrange = np.linspace(-1*dr1,-1*dr2, len(trunc_image)) + Rs/.3048
    crossrange = np.linspace(cr1, cr2, len(trunc_image[0]))

    for ii in range(1, len(trunc_image[0])+1):
        trunc_image[:,ii-1] = (trunc_image[:,ii-1].T).T*(abs(downrange*.3048)).T**(3/2)

    trunc_image = dbv(trunc_image); #added to scale to d^3/2
    crossrange = crossrange * 0.3048
    downrange = downrange * 0.3048
    progressbar(95)
    return (crossrange, downrange, trunc_image)


def SAR_imaging(file=DEFAULT_NAME, prograssbar=print):
    (sif, delta_x, Rs, Kr, Xa) = SAR_1part(file, prograssbar)
    gc.collect()
    (crossrange, downrange, trunc_image) = SAR_2part(sif, delta_x, Rs, Kr, Xa, prograssbar)
    min = trunc_image.max()-40
    max = trunc_image.max()-0
    if debug:
        print("SAR min-max: ", "[", min, max, "]")
    gc.collect()
    return (crossrange, downrange, trunc_image)
