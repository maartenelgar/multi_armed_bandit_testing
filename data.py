import pyasx
import pandas as pd



class ASX(object):

    def return_company_list(self):
        try:
            df = self.get_listed_companies()
            companies = list(df['ticker'])
            print(companies)
            return companies
        except ValueError:
            print('error')

    def industry_list(self):
        try:
            df = self.get_listed_companies()
            industry_list = df['gics_industry'].unique().tolist()
            return industry_list
        except ValueError:
            print('error')

    def all_industry_dataframes(self, industry_list):
        i = 0
        num_entries = len(industry_list)
        while i<num_entries:
            x = industry_list[i]
            df = self.get_listed_companies()
            grouped_df = df.groupby('gics_industry')
            industry_df = grouped_df.get_group('%s' % (x))
            i += 1

    #function returns the dataframe of all the names of companies in a industry
    def get_industry_dataframe(self, industry):
        df = self.get_listed_companies()
        grouped_df = df.groupby('gics_industry')
        industry_df = grouped_df.get_group('%s' % (industry))
        return industry_df

    def price(self, ticker):
        df = self.get_company_data(ticker)
        return print(df)

    def get_company_data(self, ticker):
        try:
            json_response = pyasx.data.companies.get_company_info(ticker)
            df = pd.read_json(json_response)
            return df
        except ValueError:
            print('ticker not exist')

    def get_listed_security(self):
        try:
            json_response = pyasx.data.securities.get_listed_securities()
            json_response = json.dumps(json_response)
            df_security_information = pd.read_json(json_response, orient='columns')
            return df_security_information
        except OverflowError:
            print("unable to gain list of all securities on IndustryINFO")
            pass

    def get_listed_companies(self):
        results = pyasx.data.companies.get_listed_companies()
        results = json.dumps(results)
        df_listed_companies = pd.read_json(results, orient = 'columns')
        return df_listed_companies


    def all_security_information(self, ticker):
        json_response = pyasx.data.securities.get_security_info(ticker)
        df = pd.DataFrame.from_dict(json_response, orient = 'index')
        df.index.information = ['DataPoints']
        df.reset_index(inplace=True)
        df = df.astype(str)
        print(df)
        return df

