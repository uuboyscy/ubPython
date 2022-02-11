'''
Used to deal with datetime string
'''
import datetime

def duration2List(dateDurationList: tuple, inputDateFmt="%Y-%m-%d", outputDateStrFmt="%Y-%m-%d") -> list:
    eachDateDurationArr = list()
    startDateStr = dateDurationList[0]
    endDateStr = dateDurationList[1]
    startDate = datetime.datetime.strptime(startDateStr, inputDateFmt)
    endDate = datetime.datetime.strptime(endDateStr, inputDateFmt)

    while startDate <= endDate:
        eachDateDurationArr.append(startDate.strftime(outputDateStrFmt))
        startDate = startDate + datetime.timedelta(days=1)

    return eachDateDurationArr

def dateStrFormatTransformation(dateStr: str, inputDateFmt="%Y-%m-%d", outputDateStrFmt="%Y%m%d") -> str:
    inputDatetime = datetime.datetime.strptime(dateStr, inputDateFmt)
    outputDatetimeStr = datetime.datetime.strftime(inputDatetime, outputDateStrFmt)
    return outputDatetimeStr

def dateStrDelta(dateStr: str, dateDelta: int, inputDateFmt="%Y-%m-%d") -> str:
    inputDatetime = datetime.datetime.strptime(dateStr, inputDateFmt)
    outputDatetime = inputDatetime + datetime.timedelta(days=dateDelta)
    outputDatetimeStr = datetime.datetime.strftime(outputDatetime, inputDateFmt)
    return outputDatetimeStr

def dateStrDeltaWithFormatTransformation(dateStr: str, dateDelta: int, inputDateFmt="%Y-%m-%d", outputDateStrFmt="%Y%m%d") -> str:
    operatedDateString = dateStrDelta(dateStr, dateDelta, inputDateFmt)
    outputDatetimeStr = dateStrFormatTransformation(operatedDateString, inputDateFmt, outputDateStrFmt)
    return outputDatetimeStr


if __name__ == '__main__':
    dateFormatStr = '%Y-%m-%d'
    datePeriodPair = ('2021-10-01', '2021-10-05')

    print(duration2List(datePeriodPair))

    print(
        dateStrFormatTransformation(
            dateStr="2021-12-01",
            inputDateFmt="%Y-%m-%d",
            outputDateStrFmt="%Y/%m/%d"
        )
    )

    print(
        dateStrDelta(
            dateStr="2021-12-01",
            dateDelta=-3,
            inputDateFmt="%Y-%m-%d"
        )
    )

