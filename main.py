'''
mainpred.py
Main function for the OpenAPS Prediction Algorithms

Trevor Tsue
2017
'''


from bgdataframe import get_bg_data
from bgarray import get_bg_array
from collections import namedtuple
from datamatrix import make_data_matrix
from sklearn import linear_model
from sklearn import svm
from sklearn import neural_network
from mlalgorithm import *



#DATA CONSTANTS

#Array of the ID to use
ID_ARRAY = np.array(["00897741"])
#Array of the data minutes that will be tested
DATA_MINUTES_ARRAY = np.array([1])
#Array of the minutes in the future that the predictions will be made for.
PRED_MINUTES_ARRAY = np.array([30])
#Array of the algorithms that will be tested.
ALGORITHM_ARRAY = np.array(["Linear Regression"])


#PLOTTING CONSTANTS

#List of lomb-scargle plots to print
#Leave empty to print none. Otherwise, 0:bg, 1:iob, 2:cob. e.g. [0,2]
PLOT_LOMB_ARRAY = np.array([])

#Boolean to show the prediction plot versus the actual bg
SHOW_PRED_PLOT = False
#Boolean to show the Clarke Error Grid plot
SHOW_CLARKE_PLOT = False



#ALGORITHM CONTANTS
#Dictionary with the name of the algorithm as the key and the function as the value
ALGORITHM_DICT = {"Linear Regression":linear_model.LinearRegression(normalize=True),
                    "SVM Linear Regression":svm.SVR(kernel='linear', C=0.01),
                    "Ridge Regression":linear_model.Ridge(normalize=True, alpha=0.1),
                    "Logistic Regression":linear_model.LogisticRegression(C=0.0001),
                    "Neural Network":neural_network.MLPRegressor()}

#Dictionary with the name of the algorithm as the key and boolean to apply the StandardScaler transformation as the value
ALGORITHM_TRANSFORM = {"Linear Regression":False,
                        "SVM Linear Regression":True,
                        "Ridge Regression":False,
                        "Logistic Regression": True,
                        "Neural Network":True}


#ID CONSTANTS
#               0           1           2           3           4           5           6           7           8           9           10          11         12
ID_LIST = ["00897741", "01352464", "01884126", "14092221", "15634563", "17161370", "24587372", "40997757", "41663654", "45025419", "46966807", "68267781", "84984656"]

START_TRAIN_DATE_DICT = {"00897741": "2017-02-03", "01352464": "2017-01-09", "01884126": "2017-02-03",
                            "14092221": "2017-01-06", "15634563": "2017-01-06", "17161370": "2017-02-09",
                            "24587372": "2017-01-10", "40997757": "2017-01-07", "41663654": "2017-01-25",
                            "45025419": "2017-02-10", "46966807": "2017-01-06", "68267781": "2016-12-11",
                            "84984656": "2017-01-08"}

END_TRAIN_DATE_DICT = {"00897741": "2017-02-09", "01352464": "2017-01-22", "01884126": "2017-02-07",
                            "14092221": "2017-01-19", "15634563": "2017-01-19", "17161370": "2017-02-13",
                            "24587372": "2017-01-21", "40997757": "2017-01-20", "41663654": "2017-01-25",
                            "45025419": "2017-02-15", "46966807": "2017-01-19", "68267781": "2016-12-24",
                            "84984656": "2017-01-24"}

START_TEST_DATE_DICT = {"00897741": "2017-02-10", "01352464": "2017-01-23", "01884126": "2017-02-08",
                            "14092221": "2017-01-20", "15634563": "2017-01-20", "17161370": "2017-02-14",
                            "24587372": "2017-01-22", "40997757": "2017-01-21", "41663654": "2017-01-26",
                            "45025419": "2017-02-16", "46966807": "2017-01-20", "68267781": "2016-12-25",
                            "84984656": "2017-01-25"}

END_TEST_DATE_DICT = {"00897741": "2017-02-12", "01352464": "2017-01-29", "01884126": "2017-02-09",
                            "14092221": "2017-01-26", "15634563": "2017-01-26", "17161370": "2017-02-15",
                            "24587372": "2017-01-26", "40997757": "2017-01-27", "41663654": "2017-01-26",
                            "45025419": "2017-02-17", "46966807": "2017-01-26", "68267781": "2016-12-31",
                            "84984656": "2017-01-26"}


#Function to return the training and testing dates given the string of the ID number
def _get_id_dates(id_string):
    return START_TRAIN_DATE_DICT[id_string], END_TRAIN_DATE_DICT[id_string], START_TEST_DATE_DICT[id_string], END_TEST_DATE_DICT[id_string]


#Main function
def main():
    for id_string in ID_ARRAY:
        print "\nID Number: " + id_string
        start_train_string, end_train_string, start_test_string, end_test_string = _get_id_dates(str(id_string))
        bg_df, start_train_index, end_train_index, start_test_index, end_test_index = get_bg_data(str(id_string), start_train_string, end_train_string, start_test_string, end_test_string)
        train_lomb_data, test_lomb_data = get_bg_array(bg_df, start_train_index, end_train_index, start_test_index, end_test_index, PLOT_LOMB_ARRAY)

        for data_minutes in DATA_MINUTES_ARRAY:
            print "    Data Minutes: " + str(data_minutes)
            for pred_minutes in PRED_MINUTES_ARRAY:
                print "        Prediction Minutes: " + str(pred_minutes)
                for algorithm_string in ALGORITHM_ARRAY:
                    print "            Algorithm: " + algorithm_string
                    train_data_matrix, actual_bg_train_array = make_data_matrix(bg_df, train_lomb_data, start_train_index, end_train_index,
                                                                        data_minutes, pred_minutes)
                    test_data_matrix, actual_bg_test_array = make_data_matrix(bg_df, test_lomb_data, start_test_index, end_test_index,
                                                                        data_minutes, pred_minutes)

                    bg_prediction = apply_algorithm(ALGORITHM_DICT[algorithm_string], ALGORITHM_TRANSFORM[algorithm_string], train_data_matrix, test_data_matrix, actual_bg_train_array)
                    analyze_data(SHOW_PRED_PLOT, SHOW_CLARKE_PLOT, actual_bg_test_array, bg_prediction)


#Run the main function
if __name__ ==  "__main__":
    main()
