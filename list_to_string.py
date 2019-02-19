def list_to_string(tmpList, sep = ',', reserve_len0 = False):
    newStr = ''

    for n, i in enumerate(tmpList):

        if reserve_len0 == True and i.replace(' ', '') == '':
            continue
        newStr += i
        if n < len(tmpList) - 1:
            newStr += sep
    return newStr

if __name__ == '__main__':
    testList = ['a', 'b', 'c', 'd', '', 'e', '', 'g']
    t1 = list_to_string(testList)
    t2 = list_to_string(testList, sep = ';', reserve_len0 = True)
    print(t1)
    print(t2)
