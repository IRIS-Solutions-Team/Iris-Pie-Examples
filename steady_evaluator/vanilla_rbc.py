
import sys
sys.path.append("../..")
import scipy as sp_

import numpy as np_

from irispie import *

source = r'''
    !transition-variables
        "Productivity" a
        "Gross domestic product" y
        "Private consumption" c
        "Private investment" i
        "Stock of capital" k
        "Real interest rate" r
        "Private consumption to GDP ratio" c_to_y
        "Private investment to GDP ratio" i_to_y

    !transition-shocks
        "Shock to productivity" shock_a
        "Shock to consumer preferences" shock_c

    !parameters
        "Discount factor" beta
        "Capital depreciation rate" delta
        "Share of capital in production function" gamma
        "S/S Productivity" ss_a
        "A/R Productivity" rho

    !transition-equations
        c{+1}/c = beta*r*exp(shock_c);
        k = (1 - delta)*k{-1} + i;
        y = a^(1-gamma) * k{-1}^gamma;
        gamma*y = k{-1} * (r - 1 + delta);
        y = i + c;
        log(a) = rho*log(a{-1}) + (1 - rho)*log(ss_a) + shock_a;
        c_to_y = c / y;
        i_to_y = i / y;

    !log-variables !all-but
        c_to_y, i_to_y
'''

m = Model.from_string(source, flat=True)

m.assign(
    beta = 0.95,
    gamma = 0.50,
    delta = 0.10,
    rho = 1, #0.8,
    ss_a = 1,
    a = 1,
    y = 1,
)

# chk = m.check_steady(details=True, when_fails="warning")
# 
# 
# # Create object for evaluating the steady state
# #m.assign(k=3)#,y=1,c=1,i=1,r=0,c_to_y=0,i_to_y=0)
# steady = m.create_steady_evaluator()
# 
# m.steady()
# chk = m.check_steady(details=True, when_fails="warning")
# sys.exit()
# 
# # Evaluate the equations at a valid steady state
# x0 = steady.initial_guess
# y0 = steady.eval(x0)
# 
# # Change one of the values and evaluate the equations again
# x1 = np_.copy(x0)
# x1[2] = x1[2] * 1.10
# y1 = steady.eval(x1)
# 
# print("\n[x0, x1] rounded to 4 decimals")
# print(np_.hstack((x0.reshape(-1,1).round(4), x1.reshape(-1,1).round(4))))
# 
# print("\n[y0, y1] rounded to 4 decimals")
# print(np_.hstack((y0.reshape(-1,1).round(4), y1.reshape(-1,1).round(4))))
# 
# print("\nIncidence matrix (equations in rows, variables in columns)") 
# print(steady.incidence_matrix)
# 
# print("\nVariables") 
# print(steady.quantities_human)
# 
# print("\nEquations") 
# print(steady.equations_human)
# 
# 
# m.assign(k=1, y=5, )

q = m._get_quantities(kind=TRANSITION_VARIABLE)
q.pop(1)

s = m.create_steady_evaluator(quantities=q, print_iter=0, default_missing_level=1, sparse_jacobian=True)

r2 = sp_.optimize.root(
    s.eval_with_jacobian,
    s.initial_guess,
    method="lm",
    jac=True,
)
s._iter_printer.print_footer()

