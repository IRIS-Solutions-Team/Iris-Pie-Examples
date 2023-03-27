
# Short example of a linear gap model


## Import irispie

import sys
sys.path.append("..")

from irispie import *


## Create model object

m = Model.from_file("./linear_3eq.model", linear=True, flat=False)


## Assign parameters

m.assign(
    ss_rrs = 0.5,
    ss_diff_cpi = 2,
    c0_y_gap = 0.75,
    c1_y_gap = 0.10,
    c0_diff_cpi = 0.55,
    c1_diff_cpi = 0.15,
    c0_rs = 0.75,
    c1_rs = 4,
)


# Write the model file and parameters to text files

#with open("./linear_3eq.model", "w+") as fid:
#    fid.write(source)
#
#with open("./linear_3eq_params.json", "w+") as fid:
#    fid.write(m.get_parameters(output="json4"))


## Calculate steady state

m.steady()

chk = m.check_steady(details=True, )


## Calculate first-order solution matrices

m.solve()



## Run shock simulation

sim_range = ii(1) >> ii(40) 

ss_db = Databank._for_model(m, sim_range)

in_db = ss_db._copy()

#in_db.shk_y_gap[ sim_range[0] >> sim_range[3] ] = [1, 1.5, 0.5, 0.2]
in_db.shk_y_gap[sim_range[3]] = 5

out_db = m.simulate(in_db, sim_range)
out_db1 = m.simulate(in_db, sim_range, anticipate=False)

sys.exit()

## Plot results

fig = make_subplots(2, 2, subplot_titles=["Output gap", "Inflation Q/Q PA", "Interest rate", "Output gap shocks"])

out_db.y_gap       .plot(subplot=(1, 1), figure=fig)
out_db.diff_cpi    .plot(subplot=(1, 2), figure=fig)
out_db.rs          .plot(subplot=(2, 1), figure=fig)
out_db.shk_y_gap   .plot(subplot=(2, 2), figure=fig, xline=ii(0))

fig.show()


#################################################################################


## Load data from a CSV file

fred_db = Databank._from_sheet("fred-data.csv", descript_row=True)


## Preprocess data

fred_db.cpi = 100*log(fred_db.CPI)
fred_db.diff_cpi = 4*diff(fred_db.cpi)
fred_db.diff4_cpi = diff(fred_db.cpi, -4)

fred_db.y = 100*log(fred_db.GDPC)
fred_db.y_tnd, fred_db.y_gap = fred_db.y.hpf()

fred_db.rs = fred_db.TB3M


## Plot historical data

plot_range = qq(2010,1)>>qq(2022,4)

fig = make_subplots(2, 2, subplot_titles=["Output and potential", "Output gap", "Inflation Q/Q PA | Y/Y", "Interest rate"])


# Concatenate two time series into one 2-column series

(fred_db.y | fred_db.y_tnd)             .plot(subplot=(1,1), figure=fig, range=plot_range)
fred_db.y_gap                           .plot(subplot=(1,2), figure=fig, range=plot_range)
(fred_db.diff_cpi | fred_db.diff4_cpi)  .plot(subplot=(2,1), figure=fig, range=plot_range)
fred_db.rs                              .plot(subplot=(2,2), figure=fig, range=plot_range)

fig.show()


#################################################################################


## Run a forecast

fcast_range = qq(2022,3) >> qq(2026,4)

fred_db.shk_diff_cpi = Series()
fred_db.shk_diff_cpi[ qq(2022,3) ] = -2

fcast_db = m.simulate(fred_db, fcast_range)

fig = make_subplots(
    2, 2, 
    subplot_titles=["Output gap", "Inflation Q/Q PA", "Interest rate", "Output gap shocks"]
)

fcast_db.y_gap      .plot(subplot=(1, 1), figure=fig)
fcast_db.diff_cpi   .plot(subplot=(1, 2), figure=fig)
fcast_db.rs         .plot(subplot=(2, 1), figure=fig)
fcast_db.shk_y_gap  .plot(subplot=(2, 2), figure=fig, xline=fcast_range[0]-1)

fig.show(renderer="pdf")


## Save results to a CSV file

fcast_db._to_sheet(
    "forecast.csv", 
    range=qq(2000,1)>>fcast_range[-1],
    frequency=Frequency.QUARTERLY,
)


