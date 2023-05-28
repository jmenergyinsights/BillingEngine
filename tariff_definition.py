import csv

# Network tariff
with open('network_tariff.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["start_time", "end_time", "weekdays", "weekend", "peak", "off_peak", "shoulder", "demand_charge", "charge_period"])
    writer.writerow(["00:00", "07:00", True, False, 0.0, 0.0428, 0.0, 10.2, "daily"])
    writer.writerow(["07:00", "21:00", True, False, 0.0685, 0.0, 0.0, 10.2, "daily"])
    writer.writerow(["21:00", "07:00", True, False, 0.0, 0.0428, 0.0, 10.2, "daily"])
    writer.writerow(["00:00", "00:00", False, True, 0.0, 0.0428, 0.0, 10.2, "daily"])


# Retail tariff
with open('retail_tariff.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["start_time", "end_time", "weekdays", "weekend", "peak", "off_peak", "shoulder"])
    writer.writerow(["00:00", "07:00", True, False, 0.0, 0.046045, 0.0])
    writer.writerow(["07:00", "21:00", True, False, 0.103906, 0.0, 0.0])
    writer.writerow(["21:00", "07:00", True, False, 0.0, 0.046045, 0.0])
    writer.writerow(["00:00", "00:00", False, True, 0.0, 0.046045, 0.0])


with open('tariff_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["start_time", "end_time", "weekdays", "weekend", "peak", "off_peak", "shoulder", "demand_charge", "charge_period", "feed_in_tariff"])
    writer.writerow(["00:00", "00:00", True, True, 0.00, 0.00, 0.00, 0, "daily", 0.04])
