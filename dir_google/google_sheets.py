import gspread

#gs = gspread.service_account(filename='google_api.json')
# sh = gs.open_by_key('14HcaJJ0mMt7pBvbJgX-QXbFPHkCVXrH6_OuPqVDGRpw')
gs = gspread.service_account(filename='google_api_test.json') #Test
sh = gs.open_by_key('1iGTjX-dLFe60cE5i6Asoplk3gahohvfeZrpEGovfjvM') #Test
worksheet1 = sh.sheet1
worksheet2 = sh.get_worksheet(1)
worksheet3 = sh.get_worksheet(2)
worksheet4 = sh.get_worksheet(3)


async def get_lessons_inf(title):
    information = []
    if title == 'date':
        information = worksheet1.col_values(1)
    elif title == 'time':
        information = worksheet1.col_values(2)
    elif title == 'name':
        information = worksheet1.col_values(3)
    information.pop(0)
    return information
