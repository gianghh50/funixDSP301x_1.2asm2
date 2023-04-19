import os
import re
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")


answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"

def checkValidLine(_line,df):
    list_lines = _line.split(',')
    if not len(list_lines) == 26:
        return False, "does not contain exactly 26 values"
    else:       
        if not re.match('^N\d{8}$', list_lines[0]):
            return False, "N# is invalid"
        df[list_lines[0]] = list_lines[1:]
        return True,None

def checkMark(_line):
    mark = 0
    list_lines = _line.split(',')
    list_ans = answer_key.split(',')
    for i in range(1,len(list_lines)):
        if list_lines[i] == list_ans[i-1]:
            mark = mark + 4
        if list_lines[i] != '' and list_lines[i] != list_ans[i-1]:
            mark = mark - 1
    return list_lines[0],mark


def process(file):
    df = pd.DataFrame({'Answer': answer_key.split(',')})
    print('**** ANALYZING ****\n')
    students = file.readlines()
    valid_lines = 0
    invalid_lines = 0
    for student in students:
        isValid, message = checkValidLine(student,df)
        if not isValid:
            print('Invalid line of data: ' + message + " :")
            print(student)
            invalid_lines = invalid_lines + 1
        else:
            valid_lines = valid_lines + 1
    if invalid_lines == 0:
        print('No errors found!\n')
    print('**** REPORT ****\n')
    print('Total valid lines of data:' + str(valid_lines) + '\n')
    print('Total invalid lines of data:' + str(invalid_lines) + '\n')

    writter = open(file.name.replace('.txt','_grades.txt'),'w')


    list_mark = np.empty((0,), dtype=int)
    high_scores = 0
    highest_score = 0
    lowest_score = 1000
    for student in students:
        isValid, message = checkValidLine(student.strip(),df)
        if isValid:
            curr_student, mark = checkMark(student.strip())
            list_mark =  np.append(list_mark, mark)
            if mark > 80:
                high_scores = high_scores + 1
            if mark > highest_score:
                highest_score = mark
            if mark < lowest_score:
                lowest_score = mark
        writter.write(curr_student + ',' + str(mark) + '\n')
    writter.close()
    print('Total student of high scores: ' + str(high_scores) + '\n')
    print('Mean (average) score: ' + str(np.mean(list_mark)) + '\n')
    print('Highest score: ' + str(highest_score) + '\n')
    print('Lowest score: ' + str(lowest_score) + '\n')
    print('Range of scores: ' + str(highest_score - lowest_score) + '\n')
    print('Median score: ' + str(np.median(list_mark)) + '\n')
    

    counts_skips = df.apply(lambda row: row == '').sum(axis=1)
    max_counts_skips = counts_skips.max()
    rows_with_max_counts_skips = df[counts_skips == max_counts_skips]
    _skip = ''
    for row in rows_with_max_counts_skips.index.tolist():
        if _skip != '':
            _skip = _skip + ' , '
        _skip = _skip + str(row + 1) + ' - ' +  str(max_counts_skips) + ' - ' + str(round(max_counts_skips/valid_lines,2))
    print('Question that most people skip: ' + _skip + '\n')


    df_temp = df.apply(lambda row: (row != row.iloc[0]), axis=1).sum(axis=1)
    count_wrongs = df_temp - counts_skips
    max_counts_wrongs = count_wrongs.max()
    rows_with_max_counts_wrongs = df[count_wrongs == max_counts_wrongs]
    _wrong = ''
    for row in rows_with_max_counts_wrongs.index.tolist():
        if _wrong != '':
            _wrong = _wrong + ' , '
        _wrong = _wrong + str(row + 1) + ' - ' + str (max_counts_wrongs) + ' - ' + str(round(max_counts_wrongs/valid_lines,2))
    print('Question that most people answer incorrectly: ' + _wrong + '\n')


def main():
    while(True):
        filename = input("Enter a class to grade (i.e. class1 for class1.txt): ")
        if filename == 'q':
            break
        if not filename.endswith('.txt'):
            filename = filename + '.txt'
        if os.path.exists(filename):
            try:
                file = open(filename,'r')
                print('Successfully opened ' + filename + '\n')
                process(file)
                print('>>> ================================ RESTART ================================')
                print('>>> ')
            except Exception as e:
                print(str(e))
                print("Error while open file")
        else:
            print ("Sorry, I can't find this filename")

main()

