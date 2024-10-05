import gspread

#gs = gspread.service_account(filename='google_api.json')
# sh = gs.open_by_key('14HcaJJ0mMt7pBvbJgX-QXbFPHkCVXrH6_OuPqVDGRpw')
gs = gspread.service_account(filename='google_api_test.json') #Test
sh = gs.open_by_key('1iGTjX-dLFe60cE5i6Asoplk3gahohvfeZrpEGovfjvM') #Test
worksheet1 = sh.sheet1
worksheet2 = sh.get_worksheet(1)
worksheet3 = sh.get_worksheet(2)
worksheet4 = sh.get_worksheet(3)
worksheet5 = sh.get_worksheet(4)


async def get_data_sheet(title):
    information = []
    if title == 'date':
        information = worksheet1.col_values(1)
    elif title == 'time':
        information = worksheet1.col_values(2)
    elif title == 'name':
        information = worksheet1.col_values(3)
    information.pop(0)
    return information


async def get_modules(is_name):
    all_module_names = await get_data_sheet('date')
    modules_inf = []
    for index, module_name in enumerate(all_module_names, 0):
        if 'Модуль' in module_name:
            if is_name:
                modules_inf.append(module_name)
            else:
                modules_inf.append(index)
    return modules_inf


async def get_module_inf(index_module):
    name_lessons = await get_data_sheet('name')
    time_lessons = await get_data_sheet('time')
    date_and_module = await get_data_sheet('date')
    index_lessons_module = [i for i, module in enumerate(date_and_module, 0) if 'Модуль' in module]
    index_lessons_module.append(len(date_and_module))

    module_name = date_and_module[index_lessons_module[index_module]]
    lessons_name = []
    lessons_date = []
    lessons_time = []
    for i_lesson in range(index_lessons_module[index_module] + 1, index_lessons_module[index_module+1]):
        lessons_name.append(name_lessons[i_lesson][name_lessons[i_lesson].find(".")+1:])
        lessons_date.append(date_and_module[i_lesson])
        lessons_time.append(time_lessons[i_lesson])
    return [module_name, lessons_name, lessons_date, lessons_time]

