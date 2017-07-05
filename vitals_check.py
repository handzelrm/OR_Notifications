import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

def running_fxn(splits,percent):
    """prints off the precentage of patients completed"""

    print('0%|'+'#'*int(percent/(100/splits))+' '*int((100-percent)/(100/splits))+'|100%')

def load_and_pickle(path,file,sheet):
    print('load_and_pickle function is running...')
    pickle_name = 'vitals.pickle' #defines pickle name
    df = pd.read_excel(path+file,sheetname=sheet) #reads excel file
    param_list = ['Heart Rate','Heart Rate - Pleth']
    df = df[df.PARAMETER.isin(param_list)]
    df = df[df.VALUE>=30]
    df = df[df.VALUE<=225]
    print('converting columns to datetimes part 1 of 2...')
    df.ACTION_DT_TM = pd.to_datetime(df.ACTION_DT_TM) #converts column to datetime
    print('converting columns to datetimes part 2 of 2...')
    df.VALUE_DT_TM = pd.to_datetime(df.VALUE_DT_TM) #converts column to datetime
    print('pickling data...')
    df.to_pickle(path+pickle_name)

    print('writing to excel...')
    writer = pd.ExcelWriter(path+'cleaned_vitals.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.close()
    return pickle_name

path = 'S:\\or_notifications\\'
file = 'SAParameterExtract02092017.xlsx'

# load_and_pickle(path=path,file=file,sheet='Sheet1')


def compare_first_vitals(path,file):
    print('compare_first_vitals function is running...')
    df = pd.read_pickle(path+file)
    case_ids = df.CASE_NUMBER.unique()
    df['time_diff'] = df.VALUE_DT_TM-df.ACTION_DT_TM #calculates difference upfront

    time_list = []
    param_list = []

    percentage = 0
    num_of_pts = len(case_ids)
    running_fxn(20,percentage)
    for cnt, case in enumerate(case_ids):
        case_df = df[df.CASE_NUMBER==case]
        # min_df = case_df[]

        # df = df[df.CASE_NUMBER==case_ids[0]]
        # min_index = df.time_diff.idxmin()
        min_df = case_df[case_df.time_diff==case_df.time_diff.min()]

        # print(min_df.time_diff)
        # print(min_df.time_diff[0])
        time_list.append(min_df.time_diff.values[0].astype('timedelta64[m]'))
        # print(min_df.time_diff.values[0].astype('timedelta64[m]'))

        if min_df.shape[0]==1:
            param_list.append(min_df.PARAMETER.values[0])
        elif min_df.shape[0]>1:
            param_list.extend(min_df.PARAMETER.tolist())
        else:
            print('error in min_df shape')

        if round(cnt/num_of_pts*100) != percentage:
            percentage = round(cnt/num_of_pts*100)
            if percentage in range(0,101,5):
                running_fxn(20,percentage)

    df_time = pd.DataFrame({'time':time_list})
    df_param = pd.DataFrame({'param':param_list})

    # print(df_param.param.value_counts())
    # print(df_time.time.min())
    # print(df_time.time.max())

    print('pickling data...')
    df_time.to_pickle(path+'time.pickle')
    df_param.to_pickle(path+'param.pickle')

    print('writing to excel...')
    writer = pd.ExcelWriter(path+'vitals_timing.xlsx')
    df_time.to_excel(writer,'min_times')
    df_param.to_excel(writer,'min_params')
    writer.close()


    # print(min_df.shape[0])
    # print(time_list,param_list)


    # print(len(case_ids))
    # print(df.head())
    # print(type(df.ACTION_DT_TM[0]))

    # df = 
    # # print(test_df)
    # test_value = test_df.VALUE_DT_TM[0]
    # print(test_value)
    # dt = datetime.strptime(test_value,'%b/%d/%y %H:%M:%S')
    # print(dt)

    # df.ACTION_DT_TM = pd.to_datetime(df.ACTION_DT_TM)
    # df.VALUE_DT_TM = pd.to_datetime(df.VALUE_DT_TM)
    # print(df.head())
    # # print(type(df.ACTION_DT_TM[0]))

    # print(df.VALUE_DT_TM-df.ACTION_DT_TM)


# compare_first_vitals(path=path,file='vitals.pickle')

def plot_stats(path):
    df_time = pd.read_pickle(path+'time.pickle')
    df_param = pd.read_pickle(path+'param.pickle')
    times = df_time.time.values.astype('timedelta64[m]')
    print(df_time.shape[0]) #orginal size
    df_time = df_time[df_time.time.values.astype('timedelta64[h]')<np.timedelta64(1,'h')] #removes values >= 1 hour
    print(df_time.shape[0]) #size after removal of any >= 1 hour
    df_time = df_time[df_time.time>=np.timedelta64(0,'m')] #removes negative values
    print(df_time.shape[0]) #size after removal of negative values
    times = df_time.time.dt.components.minutes
    test_df = pd.DataFrame({'times':times})
    print('Number > 10mins: {}'.format(test_df[test_df.times>10].shape[0]))
    print('Total Number of pts: {}'.format(test_df.shape[0]))
    print('Percentage > 10mins: {}%'.format(round(100*test_df[test_df.times>10].shape[0]/test_df.shape[0],2)))
    # print(times)
    # print(type(times[0]))
    plt.hist(times)
    plt.title('Time from in OR to First Vitals')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Number of Patients')
    plt.show()

def test(path,file):
    df = pd.read_pickle(path+file)

    # print(df[['VALUE_DT_TM','ACTION_DT_TM']][df.VALUE>225])
    # print(df.VALUE.value_counts())


test(path=path,file='time.pickle')

plot_stats(path=path)