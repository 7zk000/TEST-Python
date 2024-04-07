import csv

def read_gdp_data(filename, country_name):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)
        country_index = headers.index('CountryName')
        year_indices = range(headers.index('1960'), headers.index('2023') + 1)
        years = headers[headers.index('1960'):headers.index('2023') + 1]
        gdp_data = []

        for row in csvreader:
            if row[country_index].strip() == country_name:
                gdp_data = [(years[i-headers.index('1960')], row[i] if row[i] else "---None---") for i in year_indices]
                break

        return gdp_data

country_name = input("Enter the Country Name: ")
filename = 'C:\\Users\\denfo\\python-test\\Python\\GDP\\GDP-test.csv'
gdp_data = read_gdp_data(filename, country_name)

if gdp_data:
    print(f"GDP data for {country_name} from 1960 to 2023:")
    for year, gdp in gdp_data:
        print(f"{year}: {gdp}")
else:
    print(f" !!!WARNING!!! No data found for {country_name}.")
