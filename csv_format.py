#!/usr/bin/env python
# -*-coding: utf-8-*-

from __future__ import print_function
import sys

class Csv:

    columns = []
    output_dict = {}
    output_dict_with_index = {}
    columns_format = []
    sorted_data = []
    columns_with_format = []

    def __init__(self, csv_str, argv):
        self.csv_str = csv_str
        self.argv = argv
        '''Set columns and output_dict'''
        self.csvToJson(self.csv_str)
        '''Set format for each column'''
        self.setColumnsFormat()
        '''Sort data'''
        self.sortData(self.output_dict, self.argv)


    def csvToJson(self, csv_str):
        for row_num, each_row in enumerate(csv_str.split('\n')):
            if each_row.strip().isspace() or each_row == None or each_row.strip() == '':
                continue
            if row_num == 0:
                self.columns = [item for item in each_row.split(',')]
            else:
                tmp_dict = {}
                for item_num, item in enumerate(each_row.split(',')):
                    try:
                        tmp_dict[self.columns[item_num]] = item
                    except IndexError:
                        tmp_item = []
                        q_count = 0
                        for w in item:
                            piece = ''
                            if '"' in w or (q_count != 0 and q_count < 2):
                                if '"' in w:
                                    q_count  = 1
                                piece  = w.replace('"', '')   '||'
                                if q_count == 2:
                                    tmp_item.append(piece.strip('||'))
                                    q_count = 0
                            else:
                                tmp_item.append(w)
                dict_key = str(row_num)
                '''   '|'   each_row.split(',')[2]'''
                dict_value = tmp_dict
    
                self.output_dict[dict_key] = dict_value
                self.output_dict_with_index[tmp_dict[self.columns[2]]] = dict_value
    

    def setColumnsFormat(self):
        '''Set format for each column'''
        for col_site, each_column in enumerate(self.columns):
            '''Set column width'''
            tmp_list = [len(self.output_dict[each_row_in_dict][each_column]) for each_row_in_dict in self.output_dict]
            tmp_list.append(len(each_column))
            self.columns_format.append((max(tmp_list)   3))
            '''Set columns with format'''
            self.columns_with_format.append(str('{:%s}'%(self.columns_format[col_site])).format(each_column))


    def sortData(self, data_json, argv):
        for n, indx in enumerate(data_json):
            tmp_list = []
            for col_site, each_column in enumerate(self.columns):
                tmp_list.append(str('{:%s}'%(self.columns_format[col_site])).format(self.output_dict[indx][self.columns[col_site]]))
            #self.columns_with_format.append(tmp_list)
            self.sorted_data.append(tmp_list)


    def showDataFrame(self):
        for i in self.columns_format:
            print('-' * i   '--', end='')
    
        print('')
        
        for i in self.columns_with_format:
            for j in i:
                print(j, end='')
            print('| ', end='')
    
        print('')
    
        for i in self.columns_format:
            print('=' * i   '==', end='')
    
        print('')
    
        for i in self.sorted_data:
            for j in i:
                print(j   '| ', end='')
            print()
    
        for i in self.columns_format:
            print('-' * i   '--', end='')
    
        print('')


if __name__ == '__main__':
    path = sys.argv[1]
    f = open(path, 'r')
    csv_str = f.read()
    f.close()

    sd = Csv(csv_str, sys.argv)    
    sd.showDataFrame()
