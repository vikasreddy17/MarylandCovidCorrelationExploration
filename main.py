#import packages
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt
import os
import time

#load in data
maryland_covid_data = pd.read_csv("maryland_covid_county_data.csv")

#prints intro statements and background information
def intro_info():
  data_source = "Data is based on information taken from coronavirus.maryland.gov on august 7th, 2020 and the Maryland Poverty Profile Report from 2018 https://mda.maryland.gov/about_mda/Documents/SNAB/Maryland-Poverty-Profiles_2018_1-15-2018_T.pdf"
  print(data_source)
  print('************************************************************')
  time.sleep(3)
  print('Hello, this program will display the correlations between the severity of covid and features of a community. The correlation information is based on the the 24 different counties in Maryland and specific features from each county. Covid data from each county in Maryland was taken from coronavirus.maryland.gov on august 7th, 2020. Also, specfic features (poverty rate, child poverty rate, senior poverty rate, median income, housing wage, population, population density) were taken from the Maryland Poverty Profile Report from 2018. I hope users learn a couple new things while exploring the correlations between these variables.')
  time.sleep(3)

#cleans and formats the data from the csv file
def imp_clean_corr_data():
    if os.path.isfile('correlation_data_table.csv') == False:
      correlation_matrix = maryland_covid_data.corr()
      sea.heatmap(correlation_matrix, annot=True)
      correlation_matrix = correlation_matrix.stack()
      correlation_matrix = correlation_matrix.reset_index()
      correlation_matrix = correlation_matrix.rename(columns={'level_0': 'feature_1', 'level_1': 'feature_2', '0': 'correlation'})
      correlation_matrix.to_csv('correlation_data_table.csv')
    else:
      correlation_matrix = pd.read_csv('correlation_data_table.csv')
      correlation_matrix.sort_values(by=['correlation'], inplace=True, ascending=False)
    list_of_indexes = []
    for i in range(1, 101):
        if i < 10:
          j = i * 10
        else:
          i = str(i)
          j = int(i[::-1])
          i = int(i)
        if i < j or i == j:
          list_of_indexes.append(i)
    correlation_matrix = correlation_matrix.loc[correlation_matrix['correlation'] != 1, :]
    cleaned_correlation_matrix = None
    for index in list_of_indexes:
        temp_correlation_matrix = correlation_matrix.loc[correlation_matrix['index'] == index, :]
        cleaned_correlation_matrix = pd.concat([cleaned_correlation_matrix, temp_correlation_matrix], axis=0)
    cleaned_correlation_matrix.sort_values(by=['correlation'], inplace=True, ascending=False)
    return cleaned_correlation_matrix

#shows variable options and outputs a feature selection as integer
def menu_screen_select_fea():
  print('1. Poverty Rate: the poverty rate in a county')
  print('2. Child Poverty Rate: the child poverty rate in a county')
  print('3. Senior Poverty Rate: the senior poverty rate in a county')
  print('4. Median Income: the median income of a household in a county')
  print('5. Housing Wage: According to the Maryland Poverty Profile Report from 2018, housing wage is the income per hour needed "to afford the rent and utilities of a two-bedroom apartment without spending more than 30% of his or her income," in a specific county')
  print('6. Population: number of people in a county')
  print('7. Population Density: number of people in a county per square mile')
  print('>>>Pick one of the following features by inputing the number associated with the features to explore the relationship between in and covid cases and deaths')
  move_on = False
  while move_on == False:
    selected_feature = int(input())
    if selected_feature in range(1, 8):
      move_on = True
      return selected_feature
    else:
      print('error, please input a number from 1 to 7 that corresponds to a feature above')
      move_on = False

#takes in feature as integer and cleaned data from fil to create requested datafram of correlations 
def create_print_rows(selected_feature, cleaned_correlation_matrix):
  pov_rate_fealist = [1, 'Poverty Rate']
  child_pov_rate_fealist = [2, 'Child Poverty Rate']
  senior_pov_rate_fealist = [3, 'Senior Poverty Rate']
  med_inc_fealist = [4, 'Median Income']
  hous_wage_fealist = [5, 'Housing Wage']
  pop_fealist = [6, 'Population']
  pop_den_fealist = [7, 'Population Density']

  first_selected_rows = None
  for feature_index in ['feature_1', 'feature_2']:
    for cases_deaths in ['Cases', 'Confirmed Deaths']:
      og_selected_rows = cleaned_correlation_matrix.loc[cleaned_correlation_matrix[feature_index] == cases_deaths, :]
      first_selected_rows = pd.concat([first_selected_rows, og_selected_rows], axis=0)
  if selected_feature == pov_rate_fealist[0]:
    print_rows = first_selected_rows.loc[first_selected_rows['feature_2'] == (pov_rate_fealist[1]), :]
  elif selected_feature == child_pov_rate_fealist[0]:
    print_rows = first_selected_rows.loc[first_selected_rows['feature_2'] == (child_pov_rate_fealist[1]), :]
  elif selected_feature == senior_pov_rate_fealist[0]:
    print_rows = first_selected_rows.loc[first_selected_rows['feature_2'] == (senior_pov_rate_fealist[1]), :]
  elif selected_feature == med_inc_fealist[0]:
    print_rows = first_selected_rows.loc[first_selected_rows['feature_2'] == (med_inc_fealist[1]), :]
  elif selected_feature == hous_wage_fealist[0]:
    print_rows = first_selected_rows.loc[first_selected_rows['feature_2'] == (hous_wage_fealist[1]), :]
  elif selected_feature == pop_fealist[0]:
    print_rows = first_selected_rows.loc[first_selected_rows['feature_2'] == (pop_fealist[1]), :]
  elif selected_feature == pop_den_fealist[0]:
    print_rows = first_selected_rows.loc[first_selected_rows['feature_2'] == (pop_den_fealist[1]), :]
  print('************************************************************')
  print('***correlations requested have been printed below***')
  return print_rows

#determines whether the user would like to explore other correlations between variables
def ask_to_try_again():
  print('************************************************************')
  print('would you like to look at other features as well? Please say yes or no')
  answer_to_try_again = input()
  answer_to_try_again = answer_to_try_again.lower()
  move_on = False
  while move_on == False:
    if answer_to_try_again == 'yes' or 'no':
      move_on = True
    else:
      print('error, please say yes or no')
      answer_to_try_again = input()
      answer_to_try_again = answer_to_try_again.lower()
      move_on = False
  if answer_to_try_again == 'yes':
    return False
  elif answer_to_try_again == 'no':
    return True

#correlation heatmap creation and data files download
def user_file_down(maryland_covid_data):
  correlation_matrix = maryland_covid_data.corr()
  sea.heatmap(correlation_matrix, annot=True)
  plt.show()
  corr_table_file = imp_clean_corr_data()
  corr_table_file.to_csv('If_Program_Used_User_Dowloads_Files/USERCOPY_maryland_covid_county_correlation_data.csv')
  maryland_covid_data.to_csv('If_Program_Used_User_Dowloads_Files/USERCOPY_maryland_covid_county_data.csv')
  print('>>>All downloaded files are in the If_Program_Used_User_Dowloads_Files Folder')
  print('Correlation Heatmap and data files are in the folder')


#save files and end
user_file_down(maryland_covid_data)
time.sleep(2)
print('Thank you for using my program!!')