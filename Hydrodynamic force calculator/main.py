# -*- coding: utf-8 -*-
from math import radians, sin, cos, pi, tanh, cosh, degrees, atan
from funcs import float_range
import cmath as cm
from openpyxl import Workbook

H=h=T=D=b=d=n=kx=kz=S=0 #zmienne z pliku z danymi 

potential_pressure = lambda x,z,t: cosh(k*(d-z))/cosh(k*d)*cm.exp(complex(0,1)*(k*x-w*t))
diffusion_pressure = lambda x,z,t: cm.cosh(mi*(kx/kz)**0.5*(d-z))/cm.cosh(mi*(kx/kz)**0.5*d)*cm.exp(complex(0,1)*(k*x-w*t)) 

with open('dane.txt', 'r') as file:
    for line in file.readlines()[1::2]:
        exec(line)

ro = 1025 #gęstosć wody morskiej [kg/m3]
g = 9.81 #przyspieszenie ziemskie [m/s2]
gmm = ro * g #ciężar wody morskiej [N/m3]
dvn = 16 #liczba punktów obliczeniowych
df = 360/dvn #kąt srodkowy wycinka ograniczonego dwoma punktami
del dvn
DGRS_ = [radians(dgr) for dgr in float_range(df/2,360,df)]
X_ = [(D/2) * sin(x) for x in DGRS_]
Z_ = [b - (D/2) * cos(x) for x in DGRS_]
T_ = [t/100*T for t in range(0,100)]

L0 = g*T**2/(2*pi) #Długosć fali głębokowodnej
L1 = 0
L = L0
#Równanie nieliniowe na długosc fali
while (abs(L1-L) > 0.01):
    L1 = L
    L = L0 * tanh(2*pi*h/L1)
k = 2*pi/L
w = 2*pi/T
#Wypór hydrostatyczny
Fw = gmm * pi*D**2/4
#Wypór hydrodynamiczny
P0 = gmm * H/2 * 1/cosh(k*h)
bw = 4 * 10**(-10)
ph = 101325 + gmm*h
B = bw + (1-S)/ph
K = 1/B

m_mi = (k**4+(w*n*gmm/(kx*K))**2)**0.25
Arg_mi = 0.5*atan(-n*gmm*L**2/(2*pi*kx*K*T))
mi = m_mi * cm.exp(complex(0,1)*Arg_mi)

Fd_pot_max = 0
Fd_dif_max = 0
for t in T_:
    Fd_temp_pot = 0
    Fd_temp_dif = 0
    P_POT_Z = [potential_pressure(x,z,t) for (x,z) in zip(X_, Z_)]
    P_POT_R = [p.real for p in P_POT_Z]
    P_DIF_Z = [diffusion_pressure(x,z,t) for (x,z) in zip(X_, Z_)]
    P_DIF_R = [p.real for p in P_DIF_Z]
    for pp, pd, f in zip(P_POT_R, P_DIF_R, DGRS_):
        Fd_temp_pot += pp*(D/2)*radians(df)*cos(f)
        Fd_temp_dif += pd*(D/2)*radians(df)*cos(f)
    if (abs(Fd_temp_pot) >= abs(Fd_pot_max)):
        Fd_pot_max = Fd_temp_pot
        t_pot_max = t
        P_POT_R_MAX = P_POT_R
        P_POT_Z_MAX = P_POT_Z
    elif (abs(Fd_temp_dif) > abs(Fd_dif_max)):
        Fd_dif_max = Fd_temp_dif
        t_dif_max = t
        P_DIF_R_MAX = P_DIF_R
        P_DIF_Z_MAX = P_DIF_Z
print(f'Model potencjalny:\nFd = {Fd_pot_max*P0} dla t = {t_pot_max}')
print(f'Model dyfuzyjny:\nFd = {Fd_dif_max*P0} dla t = {t_dif_max}')

#Zapis wartosci cisnień do excel
wb = Workbook()
sheet1 = wb.active
sheet1.title = 'Potential'  

sheet1.append(('Nr punktu', 'Kąt', 'x', 'z', 'pz', 'pr', 'amp'))
sheet1.append(('','[ ]', '[m]', '[m]', '[-]', '[-]', '[-]'))
sheet1.merge_cells(start_row=1, start_column=1, end_row=2, end_column=1)
sheet2 = wb.copy_worksheet(sheet1)
sheet2.title = 'Diffusion'

for count, (f, x, z, pz, pr) in enumerate(zip(DGRS_, X_, Z_, P_POT_Z_MAX, P_POT_R_MAX)):
    sheet1.append((count+1, round(degrees(f),2), round(x,3), round(z,3),
                   f'=COMPLEX({round(pz.real,4)}, {round(pz.imag,4)})', 
                   round(pr,4), round(potential_pressure(0, z, 0).real,4)))

for count, (f, x, z, pz, pr) in enumerate(zip(DGRS_, X_, Z_, P_DIF_Z_MAX, P_DIF_R_MAX)):
    sheet2.append((count+1, round(degrees(f),2), round(x,3), round(z,3),
                   f'=COMPLEX({round(pz.real,4)}, {round(pz.imag,4)})', 
                   round(pr,4), round(diffusion_pressure(0, z, 0).real,4)))

wb.save('results.xlsx')