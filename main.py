import pandas as pd
import country_converter as coco


def iso2_to_iso3(iso2):  # country code converter
    return coco.convert(names=[iso2], to='ISO3')


def main():
    # read csvs
    gdp = pd.read_csv("./gdp_2017.csv")
    starbucks = pd.read_csv("./starbucks_2017.csv")

    # load data
    ## load gdp
    gdp_filtered = (gdp[['LOCATION', 'Value']])

    ## load starbucks, preprocessing starbucks data
    starbucks_filtered = starbucks.groupby('Country')[['Store Number'
                                                       ]].nunique()
    stores = starbucks_filtered['Store Number']
    starbucks_country_code_fixed = [{
        "LOCATION": iso2_to_iso3(key),
        "stores_cnt": stores[key],
    } for key in stores.keys()]
    starbucks_df = pd.DataFrame(starbucks_country_code_fixed)

    result = pd.merge(
        gdp_filtered,
        starbucks_df,
        left_on='LOCATION',
        right_on='LOCATION',
        how='inner',
    )

    # nation
    result = result.sort_values(by=['Value'], ascending=False)
    print(result)

    # city
    starbucks_city = starbucks.groupby('City')[['Store Number']].nunique()
    starbucks_city = starbucks_city.sort_values(by=['Store Number'],
                                                ascending=False)
    print(starbucks_city)


main()