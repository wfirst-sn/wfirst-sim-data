from numpy import *
from FileRead import readcol
import glob

for fl in glob.glob("*dat"):
    [phase, wave, flux] = readcol(fl, 'fff')
    if len(phase) > 0:
        
        assert median(wave) > 5000 and median(wave) < 15000, fl
        dwave = wave[1:] - wave[:-1]
        print fl, sum(dwave != median(dwave))/float(len(dwave))
        inds = where(dwave < 0)[0]
        
        for ind in inds:
            assert wave[ind - 1] < 18000.
            
        for i in range(len(wave))[::-1]:
            if wave[i] >= 18000.:
                dwave = wave[i] - wave[i - 1]
                print dwave
                new_waves = arange(wave[i] + dwave, 21999.9 + dwave, dwave)
                new_phases = ones(len(new_waves), dtype=float64)*phase[i]
                new_fluxes = ones(len(new_waves), dtype=float64)*flux[i]
                
                wave = concatenate((wave[:i+1], new_waves, wave[i+1:]))
                phase = concatenate((phase[:i+1], new_phases, phase[i+1:]))
                flux = concatenate((flux[:i+1], new_fluxes, flux[i+1:]))


        f = open(fl, 'w')
        for i in range(len(wave)):
            f.write(str(phase[i]) + "  " + str(wave[i]) + "  " + str(flux[i]) + '\n')
            
        f.close()

    else:
        print fl, "By hand!"
