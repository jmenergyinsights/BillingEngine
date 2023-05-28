import pandas as pd

class BillingEngine:
    def __init__(self, usage_data_file, network_tariff_file, retail_tariff_file, feed_in_tariff_file):
        self.usage_data = pd.read_csv(usage_data_file)
        self.usage_data['Usage_kW'] = pd.to_numeric(self.usage_data['Usage_kW'], errors='coerce')
        self.usage_data['Time'] = pd.to_datetime(self.usage_data['Time'])
        self.network_tariff_data = pd.read_csv(network_tariff_file)
        self.retail_tariff_data = pd.read_csv(retail_tariff_file)
        self.feed_in_tariff_data = pd.read_csv(feed_in_tariff_file)

    def calculate_cost(self):
        self.usage_data['Usage_kWh'] = self.usage_data['Usage_kW'] / 4  # Convert kW to kWh
        self.usage_data['Time'] = pd.to_datetime(self.usage_data['Time'])
        self.usage_data['Day'] = self.usage_data['Time'].dt.day_name()
        self.usage_data['Network_Cost_kWh'] = 0.0
        self.usage_data['Network_Cost_kW'] = 0.0
        self.usage_data['Retail_Cost_kWh'] = 0.0
        self.usage_data['Feed_in'] = 0.0

        for i, row in self.usage_data.iterrows():
            for _, tariff_row in self.network_tariff_data.iterrows():
                if row['Time'].hour >= int(tariff_row['start_time'][:2]) and row['Time'].hour < int(tariff_row['end_time'][:2]) and ((row['Day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and tariff_row['weekdays']) or (row['Day'] in ['Saturday', 'Sunday'] and tariff_row['weekend'])):
                    if row['Usage_kW'] > 0:
                        self.usage_data.loc[i, 'Network_Cost_kWh'] += (tariff_row['peak'] * row['Usage_kWh'] + tariff_row['off_peak'] * row['Usage_kWh'] + tariff_row['shoulder'] * row['Usage_kWh'])
                        if tariff_row['charge_period'] == 'daily':
                            self.usage_data.loc[i, 'Network_Cost_kW'] += tariff_row['demand_charge'] * row['Usage_kW']
                    else:
                        feed_in_tariff = self.feed_in_tariff_data.loc[0, 'feed_in_tariff']
                        self.usage_data.loc[i, 'Feed_in'] += feed_in_tariff * abs(row['Usage_kWh'])
            for _, tariff_row in self.retail_tariff_data.iterrows():
                if row['Time'].hour >= int(tariff_row['start_time'][:2]) and row['Time'].hour < int(tariff_row['end_time'][:2]) and ((row['Day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and tariff_row['weekdays']) or (row['Day'] in ['Saturday', 'Sunday'] and tariff_row['weekend'])):
                    if row['Usage_kW'] > 0:
                        self.usage_data.loc[i, 'Retail_Cost_kWh'] += (tariff_row['peak'] * row['Usage_kWh'] + tariff_row['off_peak'] * row['Usage_kWh'] + tariff_row['shoulder'] * row['Usage_kWh'])

    def write_output(self, output_file):
        self.usage_data.to_csv(output_file, index=False)

# Usage
engine = BillingEngine('usage_data.csv', 'network_tariff.csv', 'retail_tariff.csv', 'tariff_data.csv')
engine.calculate_cost()
engine.write_output('Usage_Cost.csv')
