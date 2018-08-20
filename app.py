from flask import Flask, render_template, request, redirect
import requests as rq
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import file_html
import requests as rq
import simplejson as sj
import pickle
import os

import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
    
tickerCompanies = ['EQUIFAX, INC.', 'Experian Information Solutions Inc.', 'TRANSUNION INTERMEDIATE HOLDINGS, INC.',  
                   'WELLS FARGO & COMPANY', 'BANK OF AMERICA, NATIONAL ASSOCIATION', 'JPMORGAN CHASE & CO.', 
                   'CITIBANK, N.A.', 'Navient Solutions, LLC.', 'CAPITAL ONE FINANCIAL CORPORATION', 'SYNCHRONY FINANCIAL', 
                   'NATIONSTAR MORTGAGE', 'U.S. BANCORP', 'Ditech Financial LLC', 'AMERICAN EXPRESS COMPANY', 
                   'PORTFOLIO RECOVERY ASSOCIATES INC', 'ENCORE CAPITAL GROUP INC.', 'PNC Bank N.A.', 'DISCOVER BANK',
                   'SELECT PORTFOLIO SERVICING, INC.', 'TD BANK US HOLDING COMPANY', 'SUNTRUST BANKS, INC.', 'ERC', 
                   'PAYPAL HOLDINGS INC.', 'TRANSWORLD SYSTEMS INC', 'HSBC NORTH AMERICA HOLDINGS INC.', 
                   'ALLY FINANCIAL INC.', 'UNITED SERVICES AUTOMOBILE ASSOCIATION', 'SANTANDER CONSUMER USA HOLDINGS INC.', 
                   'Seterus, Inc.', 'CITIZENS FINANCIAL GROUP, INC.', 'BB&T CORPORATION', 'NAVY FEDERAL CREDIT UNION', 
                   'FIFTH THIRD FINANCIAL CORPORATION', 'Caliber Home Loans, Inc.', 'Convergent Resources, Inc.', 
                   'Diversified Consultants, Inc.', 'CARRINGTON MORTGAGE SERVICES, LLC', 'M&T BANK CORPORATION', 
                   'REGIONS FINANCIAL CORPORATION', 'NELNET, INC.', 'I.C. System, Inc.', 'AFNI INC.', 'KEYCORP', 
                   'Resurgent Capital Services L.P.', 'Shellpoint Partners, LLC', 'BBVA COMPASS FINANCIAL CORPORATION',
                   'ONEMAIN FINANCIAL HOLDINGS, LLC.', 'FREEDOM MORTGAGE COMPANY', 'WESTERN UNION COMPANY, THE', 
                   'SANTANDER BANK, NATIONAL ASSOCIATION', 'National Credit Systems,Inc.', 'TENET HEALTHCARE CORPORATION',
                   'Commonwealth Financial Systems, Inc.', 'Southwest Credit Systems, L.P.','Comerica','CCS Financial Services, Inc.',
                   'PHH Mortgage Services Corporation', 'SLM CORPORATION', 'QUICKEN LOANS, INC.', 
                   'Fidelity National Information Services, Inc. (FNIS)', 'RUSHMORE LOAN MANAGEMENT SERVICES LLC',
                   'PENNYMAC LOAN SERVICES, LLC.', 'TOYOTA MOTOR CREDIT CORPORATION', 'Selene Finance LP', 'Hunter Warfield, Inc.',
                   'Big Picture Loans, LLC', 'Stellar Recovery, Inc.', 'RoundPoint Mortgage Servicing Corporation', 'CL HOLDINGS LLC', 
                   'CAVALRY INVESTMENTS, LLC', 'TCF NATIONAL BANK', 'HCFS Health Care Financial Services, Inc.', 'NETSPEND CORPORATION', 
                   'Ad Astra Recovery Services Inc', 'Midwest Recovery Systems', 'Servis One, Inc.', 'EOS Holdings, Inc.', 
                   'GENERAL MOTORS FINANCIAL COMPANY, INC.', 'ACE CASH EXPRESS, INC.', 'ACS Education Services',
                   'Pinnacle Credit Services, LLC', 'Credit Karma, Inc.', 'CIT BANK, NATIONAL ASSOCIATION', "Conn's, Inc.",
                   'I.Q. DATA INTERNATIONAL, INC.', 'BMO HARRIS BANK NATIONAL ASSOCIATION', 'AMERICAN HONDA FINANCE CORP',
                   'FAIR COLLECTIONS & OUTSOURCING, INC.', 'FLAGSTAR BANK, FSB', 'The CBE Group, Inc.', 'CMRE Financial Services, Inc.',
                   'ProCollect, Inc', 'CURO Intermediate Holdings', 'CREDIT ACCEPTANCE CORPORATION', 'Westlake Services, LLC',
                   'CNG FINANCIAL CORPORATION', 'NISSAN MOTOR ACCEPTANCE CORPORATION', 'First Data Corporation', 'CORELOGIC INC', 
                   'Coinbase, Inc.', 'GC Services Limited Partnership', 'Credence Resource Management, LLC', 'STERLING JEWELERS, INC.', 
                   'FIRST NATIONAL BANK OF OMAHA', 'ECMC Group, Inc.', 'The CMI Group, Inc.', 'Penn Credit Corporation', 
                   'PENTAGON FEDERAL CREDIT UNION', 'BANK OF THE WEST', 'Enova International, Inc.', 'HYUNDAI CAPITAL AMERICA', 
                   'Amsher Collection Services, Inc.', 'NCC Business Services, Inc.', 'Financial Credit Service, Inc.',
                   'Receivables Management Partners, LLC', 'Radius Global Solutions LLC', 'National Credit Adjusters, LLC', 
                   'COMMUNITY CHOICE FINANCIAL, INC.', 'WAKEFIELD & ASSOCIATES, INC.', 'Medical Data Systems, Inc.', 'URS Holding, LLC', 
                   'Dynamic Recovery Solutions, LLC', 'HEARTLAND PAYMENT SYSTEMS INC', 'FORD MOTOR CREDIT CO.', 
                   'Dovenmuehle Mortgage, Inc.', 'SQUARETWO FINANCIAL CORPORATION', 'Franklin Collection Service, Inc.', 
                   'EXETER FINANCE CORP.', 'Continental Finance Company, LLC', 'Colony Brands, Inc.', 'Debt Recovery Solutions, LLC', 
                   'MOHELA', 'Residential Credit Solutions, Inc.', 'CASHCALL, INC.', 'Phoenix Financial Services LLC', 
                   'BMW Financial Services NA, LLC', 'Retrieval-Masters Creditors Bureau, Inc.', 'First National Collection Bureau, Inc.', 
                   'Real Time Resolutions, Inc.', 'AmeriCollect', 'Aargon Agency, Inc.', 'Focus Holding Company', 'SECURITY FINANCE CORP', 
                   'Trident Asset Management, L.L.C.', 'Alorica Inc.', 'OPTIMUM OUTCOMES, INC.', 
                   'Advance America, Cash Advance Centers, Inc.', 'REVERSE MORTGAGE SOLUTIONS, INC.', 'Monterey Financial Services LLC', 
                   'Ability Recovery Services, LLC', 'Capital Accounts, LLC', 'BlueChip Financial', 'NCB MANAGEMENT SERVICES INC', 
                   'FIRST NATIONAL BANK OF PENNSYLVANIA', 'CAINE & WEINER COMPANY, INC.', 'Synovus Bank', 
                   'CONSUMER PORTFOLIO SERVICES, INC.', 'Harris & Harris, Ltd.', 'Avant Credit Corporation', 'SCOTTRADE BANK', 
                   'SUNRISE CREDIT SERVICES, INC', 'Statebridge Company', 'Performant Financial Corporation', 'ARVEST BANK GROUP, INC.', 
                   'Blackhawk Network Holdings Inc.', 'WORLD ACCEPTANCE CORPORATION', 'Rent Recovery Solutions', 'VW Credit']

tickerSymbols = ['EFX', 'EXPN', 'TRU', 'WFC', 'BAC', 'JPM', 'C', 'NVMM', 'COF', 'SYF', 'TRMT', 'USB', 'EFC', 'AXP', 'OESX', 'ECPG', 'BMA', 
                 'DISCA', 'CPSS', 'CIZN', 'STI', 'UHAL', 'PYPL', 'CASA', 'SMHI', 'ALLY', 'UAMY', 'SC', 'VEC', 'CFG', 'BBT', 'CFBK', 'ETFC', 
                 'LGIH', 'CLR', 'SAUC', 'CSV', 'MTB', 'RF', 'NNI', 'IDSY', 'EGOV', 'KEY', 'SOR', 'SDLP', 'CCB', 'ESQ', 'F', 'WU', 'SXI', 
                 'BASI', 'THC', 'BASI', 'DSS', 'BMRA','CBFV', 'PRIM', 'SLM', 'CKX', 'FIS', 'CRUSC', 'PFSI', 'MDP', 'KRNY', 'CLFD', 'FPH', 
                 'ERII', 'ASC', 'HSBC', 'CIC', 'ONB', 'HALL', 'NEOG', 'AMN', 'MRCY', 'VERI', 'IESC', 'GM', 'EXPR', 'KAR', 'PNK', 'MEIP', 
                 'CAC', 'NNBR', 'ATNI', 'PRK', 'ANAT', 'FCN', 'FBC', 'MEET', 'CBFV', 'ALE', 'EARS', 'CACC', 'KELYA', 'CNA', 'WRLD', 'FDC', 
                 'CLGX', 'OPTN', 'EHIC', 'CDEV', 'LINK', 'FMNB', 'EME', 'HCI', 'MDP', 'CFBK', 'BMLP', 'ENVA', 'DX', 'KAR', 'BBSI', 'CBFV', 
                 'ENBL', 'ASH', 'NPK', 'NICK', 'JKHY', 'CASM', 'LXFR', 'MICR', 'HTLD', 'F', 'ORM', 'AROW', 'FELE', 'ENFC', 'CPTA', 'LB', 
                 'RETO', 'MTL', 'ARR', 'CHMA', 'PFS', 'CBFV', 'ELVT', 'FIS', 'STRM', 'UHAL', 'AKAO', 'CHCO', 'CPTA', 'BAM', 'ALCO', 'PVG', 
                 'AMD', 'NXEO', 'AMP', 'BAS', 'MMAC', 'KRNY', 'CRUSC', 'UVSP', 'COHN', 'OPB', 'CPSS', 'CTHR', 'HCAP', 'SSBI', 'LQDT', 
                 'PRGO', 'PFMT', 'B', 'BMCH', 'WRLD', 'RETO', 'PW']

companyTickerSymbols = {}
for i, key in enumerate(tickerCompanies):
    companyTickerSymbols[key] = tickerSymbols[i]

def categoryCombiner(df, categColumn, categCombine_dict):
    stringToCategs = {v: k for k, vv in categCombine_dict.items() for v in vv}
    return df.assign(product = df[categColumn].map(stringToCategs).astype('category', categories=set(stringToCategs.values())))

"""
dict above was pre-obtained with fuzzy string best-matching to companies having a count of at least 100 complaints (since 2015), when there
was a match greater than 60 (out of 100), for the decapitalized strings representing company names, as follows:

df_cCounts = df['company'].value_counts()
df_100c = df_cCounts[df_cCounts >= 100]
# companies with at least 100 complaints:
companies_100c = df_100c.index

tickerRatioLists = {}
for company in companies_100c:
    tickerRatioLists[company] = [fuzz.ratio(company.lower(), elem.lower()) for elem in stockticker_df['Name']]

companyTickerSymbols = {}
for company in tickerRatioLists.keys():
    if np.max(tickerRatioLists[company]) > 60:
        companyTickerSymbols[company] = stockticker_df['Symbol'][np.argmax(tickerRatioLists[company])]

# identified corrections (arguably should include London Stock Exchange):
companyTickerSymbols['Experian Information Solutions Inc.'] = 'EXPN'
companyTickerSymbols['CITIBANK, N.A.'] = 'C'
companyTickerSymbols['TRANSUNION INTERMEDIATE HOLDINGS, INC.'] = 'TRU'

"""  
    
# keys are first specified in heroku:config for app, in proper directory
CFPB_APP_KEY = os.environ.get('CFPB_APP_KEY')
ALPHAADVANTAGE_KEY = os.environ.get('ALPHAADVANTAGEKEY')

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def get_input():
    return render_template('input.html')

@app.route('/', methods = ['POST'])
def make_output():
    user_inp = {}
    
    cc_url = 'http://data.consumerfinance.gov/resource/jhzv-w97w.csv?'
    cc_payload = {'$$app_token': CFPB_APP_KEY, '$limit':'200000'}
    
    cutoff = pd.to_datetime('2015-08-01 00:00:00')
    
    df = rq.get(cc_url, cc_payload)
    df = StringIO(df.text)
    df = pd.read_csv(df)
    df['date_received'] = pd.to_datetime(df['date_received'])
    df = df.set_index('date_received')
    df = df.loc[df.index >= cutoff]
    df['product'] = df['product'].astype('category')
    
    

    
    prodCombine_dict = {
         'Bank_Account': ['Bank account or service', 'Checking or savings account'],
         'Consumer_Loan' : ['Consumer Loan', 'Payday loan', 'Payday loan, title loan, or personal loan'],
         'Credit_Card' : ['Credit card', 'Credit card or prepaid card', 'Prepaid card'],
         'Credit_Reporting' : ['Credit reporting', 'Credit reporting, credit repair services, or other personal consumer reports'],
         'Debt_Collection' : ['Debt collection'],
         'Money_Transfer' : ['Money transfers', 'Money transfer, virtual currency, or money service', 'Virtual currency'],
         'Car_Loan' : ['Vehicle loan or lease'],
         'Mortgage' : ['Mortgage'],
         'Student_Loan' : ['Student loan'],
         'Other' : ['Other financial service']
    }
    
    df = categoryCombiner(df, 'product', prodCombine_dict)
    
    
    struggling_with_payment = ['Struggling to pay your bill', 'Struggling to pay your loan', 'Struggling to pay mortgage',
            'Loan modification,collection,foreclosure', 'Delinquent account', 'Arbitration', 'Bankruptcy',
            'Forbearance / Workout plans', 'Problems when you are unable to pay', "Can't stop charges to bank account", 
            "Can't stop withdrawals from your bank account", "Can't repay my loan", 'Struggling to repay your loan',
            'Repaying your loan']

    unexpected_fees_or_interest = ['Other fee', 'Fees or interest', "Charged fees or interest I didn't expect",
            "Charged fees or interest you didn't expect", 'Unexpected or other fees', 'Late fee', 'Overlimit fee',
            'Balance transfer fee', 'Cash advance fee', 'Cash advance', 'Fees', 'Problem with an overdraft',
            'Problem with overdraft', 'APR or interest rate', 'Charged bank acct wrong day or amt', 'Excessive fees',
            'Money was taken from your bank account on the wrong day or for the wrong amount', 'Settlement process and costs',
            'Problems caused by my funds being low', 'Problem caused by your funds being low','Unexpected/Other fees']

    company_not_crediting_payment = ['Problem when making payments','Loan servicing, payments, escrow account',
            'Trouble during payment process', 'Managing the loan or lease', 'Managing the line of credit',
            'Problem with the payoff process at the end of the loan', 'Payoff process', 'Problems at the end of the loan or lease',
            'Payment to acct not credited', "Loan payment wasn't credited to your account"]

    account_opening_closing_management = ['Managing, opening, or closing account',
            'Managing, opening, or closing your mobile wallet account', 'Managing an account', 'Opening an account', 
            'Getting a loan', 'Account opening, closing, or management', 'Problem getting a card or closing an account', 
            'Applying for a mortgage or refinancing an existing mortgage', 'Applying for a mortgage', 
            'Application, originator, mortgage broker', 'Taking out the loan or lease', 'Shopping for a loan or lease',
            'Closing your account', 'Closing/Cancelling account', 'Closing an account', 'Application processing delay',
            'Getting a credit card', 'Sale of account', 'Credit line increase/decrease', 'Credit limit changed',
            'Credit determination', 'Getting a line of credit', 'Shopping for a line of credit', 'Account terms and changes',
            'Closing on a mortgage', 'Credit decision / Underwriting', 'Getting a loan or lease']

    problem_using_services = ['Trouble using your card', 'Trouble using the card', 'Balance transfer', 'Rewards', 
            'Credit card protection / Debt protection', 'Credit monitoring or identity theft protection services',
            'Adding money', 'Problem adding money', 'Problem with fraud alerts or security freezes', 
            'Unable to get your credit report or credit score', 'Unable to get credit report/credit score', 'Convenience checks',
            'Overdraft, savings or rewards features', 'Overdraft, savings, or rewards features', 
            'Problem with additional add-on products or services', 'Problem with cash advance', 
            'Money was not available when promised', 'Identity theft protection or other monitoring services', 
            'Credit monitoring or identity protection', 'Deposits and withdrawals', 
            'Making/receiving payments, sending money','Using a debit or ATM card']

    approved_loan_not_delivered = ["Was approved for a loan, but didn't receive the money", 
            "Was approved for a loan, but didn't receive money", 'Applied for loan/did not receive money', 'Getting the loan']

    disputedTransaction_fraud_poorFraudProtection = ['Identity theft / Fraud / Embezzlement', 'Lost or stolen check', 
            'Problem with a purchase shown on your statement', 'Billing disputes', 'Transaction issue',
            'Unauthorized transactions or other transaction problem', 
            'Problem with a purchase or transfer', 'Unauthorized transactions/trans. issues', 'Fraud or scam', 
            'Confusing or missing disclosures', 'Disclosures', 'Confusing or misleading advertising or marketing',
            'Incorrect/missing disclosures or info', 'Unsolicited issuance of credit card', "Received a loan I didn't apply for",
            "Received a loan you didn't apply for", 'Wrong amount charged or received', 'Lost or stolen money order', 
            'Incorrect exchange rate','Problem with a lender or other company charging your account',
            'Attempts to collect debt not owed', "Cont'd attempts collect debt not owed", 'Collection debt dispute']

    incorrect_information_on_report_or_bill = ['Incorrect information on your report', 'Incorrect information on credit report',
            'Billing statement', "Problem with a credit reporting company's investigation into an existing problem",
            "Problem with a company's investigation into an existing issue", 'Problem with credit report or credit score',
            "Credit reporting company's investigation", 'Credit reporting']

    advertising_annoyance_or_privacy_violation = ['Advertising and marketing, including promotional offers',
                'Advertising and marketing', 'Advertising', 'Advertising, marketing or disclosures', 'Improper use of your report',
                'Improper use of my credit report', 'Privacy']

    item_repossessed = ['Vehicle was repossessed or sold the vehicle', 'Lender repossessed or sold the vehicle',
            'Property was sold', 'Lender sold the property']

    defective_item = ['Lender damaged or destroyed property', 'Lender damaged or destroyed vehicle', 
            'Property was damaged or destroyed property', 'Vehicle was damaged or destroyed the vehicle']

    threatening_unprofessional_illegal = ['Written notification about debt', 'Communication tactics',
            'Disclosure verification of debt', 'Took or threatened to take negative or legal action',
            'False statements or representation', 'Taking/threatening an illegal action',
            'Improper contact or sharing of info', 'Threatened to contact someone or share information improperly',
            'Collection practices']

    poorCustomerService = ['Dealing with your lender or servicer', 'Dealing with my lender or servicer', "Can't contact lender",
            "Can't contact lender or servicer", 'Problem with customer service', 'Customer service / Customer relations',
            'Customer service/Customer relations']

    other = ['Other features, terms, or problems', 'Other', 'Other transaction problem', 'Other transaction issues',
             'Other service issues', 'Other service problem']

    issueCombine_dict = {'Struggling with payment' : struggling_with_payment,
                         'Unexpected fees or interest' : unexpected_fees_or_interest,
                         'Company not crediting payment, or charging a payment fee' : company_not_crediting_payment,
                         'Account opening, closing, and managment' : account_opening_closing_management,
                         'Problem using services' : problem_using_services,
                         'Approved loan not delivered' : approved_loan_not_delivered,
                         'Disputed transaction, fraud, or poor fraud protection': disputedTransaction_fraud_poorFraudProtection,
                         'Incorrect information on report or bill' : incorrect_information_on_report_or_bill,
                         'Advertising annoyance or privacy violation' : advertising_annoyance_or_privacy_violation,
                         'Item repossessed' : item_repossessed,
                         'Defective item' : defective_item,
                         'Threatening, unprofessional, or illegal debt collection practices' : threatening_unprofessional_illegal,
                         'Poor customer service' : poorCustomerService,
                         'Other': other}
    
    df = categoryCombiner(df, 'issue', issueCombine_dict)


    
    
    
    # stock label entry is what's in the input.html file, field entered by user]
    user_inp['company_name'] = request.form['company_name']
    user_inp['product'] = request.form['product']
    user_inp['ticker_symbol'] = companyTickerSymbols[user_inp['company_name']]
    
    
    stock_payload = {'function': 'TIME_SERIES_MONTHLY', 'symbol': user_inp['ticker_symbol'], 
           'apikey': ALPHAADVANTAGE_KEY, 'datatype': 'csv'}
    
    # possibly last 6 months only 
    stock_df = rq.get('https://www.alphavantage.co/query', params = stock_payload)
    stock_df = StringIO(stock_df.text)
    stock_df = pd.read_csv(stock_df)
    

    stock_df = stock_df.set_index('timestamp', drop = False)
    
    """
    date_filter = to_datetime(user_inp['month'])
    year_month_filter = str(date_filter.year) + '-' + str(date_filter.month)
    df_f = df.loc[year_month_filter]
    df_f_close = df_f.loc[:,['timestamp', 'close']]
    
    fig = figure(x_axis_type="datetime", x_axis_label = 'date', y_axis_label = 'closing price', 
            title = 'Stock Closing Price of ' + user_inp['stock_label'] + ' Over ' + user_inp['month'],)
    
    fig.line('timestamp', 'close', source = df_f)
    """
    
    # output_html = file_html(fig, CDN, 'output plot')
    
    return  1000000 # output_html


# port grabbed from heroku deployment environ (set to default 5000 if no environ setting) 
if __name__ == '__main__':
    port = int(os.env.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
