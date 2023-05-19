
import sys
sys.path.append('../..')
from irispie import *
from irispie.parsers import preparser as pp
import scipy as sp_

m = Model.from_file("spbc.model", flat=True, )

m.assign(
    alpha = 1,
    beta = 0.985**(1/4),
    beta0 = 0,
    beta1 = 0.8,
    gamma = 0.60,
    delta = 0.03,
    pi = 1,
    eta = 6,
    k = 10,
    psi = 0.25,

    chi = 0.85,
    xiw = 60,
    xip = 300,
    rhoa = 0.90,
    rhoterm20 = 0.80,

    rhor = 0.85,
    kappap = 4,
    kappan = 0,

    Short_ = 0,
    Long_ = 0,
    Infl_ = 0,
    Growth_ = 0,
    Wage_ = 0,

    A = 1,
    P = 1,
    Pk = 10,
)


q = m._get_quantities(kind=TRANSITION_VARIABLE | MEASUREMENT_VARIABLE)
q = filter_quantities_by_name(q, exclude_names=["A", "P"])

s = m.create_steady_evaluator(quantities=q)

r = sp_.optimize.root(
    s.eval_with_jacobian,
    s.initial_guess,
    method="lm",
    jac=True,
)


