'''
count the item in operatedObject
type : list, string, datafram
'''
import pandas as pd

def map_reduce(operatedObject, type='list', sep=','):

    mr_dict = {}

    if type == 'list':

        for i in operatedObject:
            if i in mr_dict:
                mr_dict[i] += 1
            else:
                mr_dict[i] = 1
    elif type == 'dataframe':

            for num, each_rowdata in enumerate(operatedObject):

                try:
                    for i in each_rowdata.split(sep):
                        if i in mr_dict:
                            mr_dict[i] += 1
                        else:
                            mr_dict[i] = 1
                except AttributeError:
                    print('Error row :', num)
    else:
        # split the string to a list
        operatedObject = operatedObject.split(sep)
        for i in operatedObject:
            if i in mr_dict:
                mr_dict[i] += 1
            else:
                mr_dict[i] = 1


    # order the dict

    return mr_dict

if __name__ == '__main__':

    import pandas as pd

    df = pd.read_csv(r'./test.csv', engine='python', encoding='utf-8')
    operateddf = df['Ingredients']
    mr_dict = map_reduce(operateddf, type='dataframe', sep=';')
    print(mr_dict)

    print('==================')

    testString = '1,2,3,5,4,6,2,1,3,4,2,1,3,6,4,8,7,9,6,5,4,2,3,1,2,4,6,3,,,2,1,2,3,4,5,6,7,8,9,5,4,5,3,1,2,1,,,5,4,,,6,8,7,9,5,4,6,1'
    mr_dict = map_reduce(testString, type='string', sep=',')
    print(mr_dict)