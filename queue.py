class Queue:

    def __init__(self, list_of_len = 10):
        self.list_of_len = list_of_len

    def remove_end(self, operatingList):
        if len(operatingList) != 0:
            return operatingList[1:]
        else:
            raise LookupError('The Queueing is empty!')

    def insert_head(self, operatingList, val):
        if len(operatingList) < self.list_of_len:
            operatingList.append(val)
            return operatingList
        else:
            raise LookupError('The Queueing is full!')

    def queueingList(self, operatingList, val):
        operatingList = self.insert_head(self.remove_end(operatingList), val)
        return operatingList


if __name__ == '__main__':

    import time

    # Maximum length of list is 10
    que = Queue(10)
    sampleList = [1, 2, 3]

    print('Original list : ' + str(sampleList))
    print('Insert 100 : ' + str(que.insert_head(sampleList, 100)))
    print('Remove the first value : ' + str(que.remove_end(sampleList)))

    print('-----------')

    sampleList = [0 for i in range(10)]
    print(sampleList)
    for i in range(35):
        #sampleList = que.insert_head(que.remove_end(sampleList), i)
        sampleList = que.queueingList(sampleList, i)
        time.sleep(0.5)
        print(sampleList)


