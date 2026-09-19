import csv
from dataclasses import dataclass

@dataclass
class WeatherRecord:
    date: str
    temp: float
    summary: str
    precip_type: str
    humidity: float
    wind_speed: float

    def __str__(self):
        return f"{self.date} with a temperature of {round(self.temp, 1)}°C ({self.summary})"

def load_weather_data(filename):
    records = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            record = WeatherRecord(
                date=row['Formatted Date'][:10],
                temp=float(row['Temperature (C)']),
                humidity=float(row['Humidity']),
                summary=row['Summary'],
                wind_speed=float(row['Wind Speed (km/h)']),
                precip_type=row['Precip Type']
            )
            records.append(record)
    return records

def calculate_average_temp(records):
    temp = [r.temp for r in records]
    return sum(temp) / len(temp)

def find_hottest_day(records):
    return max(records, key=lambda r: r.temp)

def find_coldest_day(records):
    return min(records, key=lambda r: r.temp)

def count_rainy_days(records):
    return sum(1 for r in records if 'rain' in r.summary.lower())

def average_humidity(records):
    humidity = [r.humidity for r in records]
    return sum(humidity) / len(humidity)

def group_by_month(records):
    # group temperatures by month
    months = {}
    for r in records:
        month = r.date[:7]
        if month not in months:
            months[month] = []
        months[month].append(r.temp)
        
    return {month: sum(temps)/len(temps) for month, temps in months.items()}

def warmest_month(records):
    monthly = group_by_month(records)
    return max(monthly.items(), key=lambda x: x[1])

def coldest_month(records):
    monthly = group_by_month(records)
    return min(monthly.items(), key=lambda x: x[1])

def wind_speed_analysis(records):
    # wind analysis
    wind_speeds = [r.wind_speed for r in records]
    
    average_wind = sum(wind_speeds) / len(wind_speeds)
    max_wind = max(wind_speeds)
    min_wind = min(wind_speeds)
    
    return {
        'average': average_wind,
        'max': max_wind,
        'min': min_wind
    }

def windiest_day(records):
    return max(records, key=lambda r: r.wind_speed)

weather_data = load_weather_data('weatherHistory.csv')

print(f"Average Temp: {calculate_average_temp(weather_data):.2f}°C")
print(f"Hottest Day: {find_hottest_day(weather_data)}")
print(f"Coldest Day: {find_coldest_day(weather_data)}")
print(f"Rainy Days: {count_rainy_days(weather_data)}")
print(f"Average Humidity: {average_humidity(weather_data):.2f}")
# months
print(f"\nWarmest Month: {warmest_month(weather_data)}")
print(f"Coldest Month: {coldest_month(weather_data)}")
# wind speed analysis
wind_analysis = wind_speed_analysis(weather_data)
print(f"\nWind Speed Analysis:")
print(f"  Average: {wind_analysis['average']:.2f} km/h")
print(f"  Highest: {wind_analysis['max']:.2f} km/h")
print(f"  Lowest: {wind_analysis['min']:.2f} km/h")
# windiest day
print(f"\nWindiest Day: {windiest_day(weather_data)}")