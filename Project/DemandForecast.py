import matplotlib.pyplot as plt
import numpy as np

demand_data_pro = [
    [28906, 31250, 32031, 35156, 35156, 35156, 38281, 36563, 34125],
    [35156, 35938, 38281, 39844, 39844, 39844, 42969, 40156, 39000],
    [36719, 36719, 39063, 40625, 41406, 40625, 43750, 39688, 39875],
    [37500, 37500, 39844, 41406, 41406, 41406, 43750, 40625, 40438],
    [42969, 42969, 44531, 46875, 47656, 47656, 49219, 47500, 46188],
    [48438, 50000, 50781, 53906, 53906, 53125, 54688, 52969, 52656],
    [56250, 57813, 60156, 60938, 60938, 60938, 63281, 59688, 59975],
    [58594, 59375, 60156, 62500, 62500, 63281, 66406, 62813, 61938],
    [47656, 46875, 50781, 51563, 51563, 52344, 55469, 53438, 51213],
    [46094, 45313, 47656, 50781, 50000, 50000, 53125, 49219, 49025],
    [41406, 40625, 44531, 46094, 46094, 45313, 46875, 46875, 44738],
    [28125, 28125, 32031, 33594, 32813, 33594, 35156, 33906, 32138],
    [27344, 27344, 28906, 31250, 32031, 32031, 34375, 33125, 30825]
]

demand_data_air = [
    [58594, 58594, 60938, 63281, 63281, 62500, 66406, 64063, 62350],
    [60156, 60938, 63281, 66406, 65625, 66406, 67188, 65469, 62688],
    [64844, 65625, 67188, 68750, 69531, 68750, 71094, 69219, 70000],
    [68750, 70313, 71875, 74219, 74219, 73438, 75000, 72813, 73650],
    [76563, 76563, 80469, 81250, 81250, 81250, 85156, 82188, 79188],
    [85156, 87500, 89844, 90625, 91406, 91406, 93750, 92188, 93381],
    [98438, 98438, 101563, 103125, 103125, 103906, 107031, 105469, 104063],
    [103906, 104688, 107031, 107813, 108594, 107813, 109375, 106406, 104375],
    [89844, 89844, 92188, 93750, 93750, 93750, 95313, 92188, 94375],
    [88281, 89063, 91406, 92969, 92969, 92969, 93750, 92031, 89063],
    [77344, 79688, 80469, 83594, 83594, 82813, 85938, 81563, 81125],
    [70313, 71094, 72656, 75000, 75000, 75000, 76563, 74531, 75375],
    [67969, 68750, 70313, 71875, 71875, 71875, 75000, 71406, 71406]
]

def compute_forecast(demand_data):
    # compute average demand
    total_demand = sum(sum(week_demand) for week_demand in demand_data)
    average_demand = total_demand / (len(demand_data) * len(demand_data[0]))

    # compute seasonal factors
    seasonal_factors = []
    for week_demand in demand_data:
        week_total_demand = sum(week_demand)
        seasonal_factor = week_total_demand / (len(week_demand) * average_demand)
        seasonal_factors.append(seasonal_factor)

    # forecast demand for next year
    forecast_data = [0]
    for week_idx, week_demand in enumerate(demand_data):
        # compute forecast for the next year
        seasonal_factor = seasonal_factors[week_idx % len(seasonal_factors)]
        forecast_demand = seasonal_factor * average_demand
        rounded_forecast_demand = round(forecast_demand)
        forecast_data.append(rounded_forecast_demand)

    return forecast_data

forecast_data_pro = compute_forecast(demand_data_pro)
forecast_data_air = compute_forecast(demand_data_air)

print(forecast_data_air)
print(forecast_data_pro)

forecast_data_pro_w0 = forecast_data_pro[1:]
for i in range(len(list(zip(*demand_data_pro)))):
    b=2014+i
    plt.plot(list(zip(*demand_data_pro))[i],label=str(b))
plt.plot(forecast_data_pro_w0,linewidth=5,label="2023")
plt.xlabel("weeks")
plt.legend()
plt.ylim(0,70000)
plt.xlim(1,12)
plt.title("Macbook Pro Demand")
plt.show()
plt.savefig('MacbookPro.png')

forecast_data_air_w0 = forecast_data_air[1:]
for i in range(len(list(zip(*demand_data_air)))):
    b=2014+i
    plt.plot(list(zip(*demand_data_air))[i],label=str(b))
plt.plot(forecast_data_air_w0,linewidth=5,label="2023")
plt.xlabel("weeks")
plt.legend()
plt.ylim(50000,120000)
plt.xlim(1,12)
plt.title("Macbook Air Demand")
plt.show()
plt.savefig('MacbookAir.png')