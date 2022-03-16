'''
Used to deal with datetime string
'''
import datetime
from dateutil.relativedelta import relativedelta


def duration2List(dateDurationList: tuple, inputDateFmt="%Y-%m-%d", outputDateStrFmt="%Y-%m-%d") -> list:
    """
    Input a tuple of date pairs, getting A list of date string between that.
    Example:
        >>> dateTuple = ("20220216", "20220218")
        >>> duration2List(dateTuple, "%Y%m%d", "%Y-%m-%d")
        ["2022-02-16", "2022-02-17", "2022-02-18"]

    :param dateDurationList: A tuple of date string pairs
    :param inputDateFmt: A string of date format for input date string, for example, "%Y-%m-%d"
    :param inputDateFmt: A string of date format for output date string, for example, "%Y-%m-%d"
    :return: A list of date string, which are between `dateDurationList` and `inputDateFmt`
    """
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
    """
    Transform a date string from one format to another.
    Example:
    >>> dateStrFormatTransformation("20220216", "%Y%m%d", "%Y-%m-%d")
    2022-02-16

    :param dateStr:
    :param inputDateFmt:
    :param outputDateStrFmt:
    :return:
    """
    inputDatetime = datetime.datetime.strptime(dateStr, inputDateFmt)
    outputDatetimeStr = datetime.datetime.strftime(inputDatetime, outputDateStrFmt)
    return outputDatetimeStr


def dateStrDelta(dateStr: str, dateDelta: int, inputDateFmt="%Y-%m-%d") -> str:
    """
    Get a date string for some day.
    Example:
    >>> dateStrDelta("20220216", -2, "%Y%m%d")
    20220214

    :param dateStr:
    :param dateDelta:
    :param inputDateFmt:
    :return:
    """
    inputDatetime = datetime.datetime.strptime(dateStr, inputDateFmt)
    outputDatetime = inputDatetime + datetime.timedelta(days=dateDelta)
    outputDatetimeStr = datetime.datetime.strftime(outputDatetime, inputDateFmt)
    return outputDatetimeStr


def dateStrDeltaWithFormatTransformation(dateStr: str, dateDelta: int, inputDateFmt="%Y-%m-%d", outputDateStrFmt="%Y%m%d") -> str:
    """
    Get a date string for some day.
    Example:
    >>> dateStrDelta("20220216", -2, "%Y%m%d", "%Y-%m-%d")
    2022-02-14

    :param dateStr:
    :param dateDelta:
    :param inputDateFmt:
    :param outputDateStrFmt:
    :return:
    """
    operatedDateString = dateStrDelta(dateStr, dateDelta, inputDateFmt)
    outputDatetimeStr = dateStrFormatTransformation(operatedDateString, inputDateFmt, outputDateStrFmt)
    return outputDatetimeStr

def dateStrMonthDelta(dateStr: str, dateDelta: int, inputDateFmt="%Y-%m-%d") -> str:
    """
    Get a date string for some day.
    Example:
    >>> dateStrMonthDelta("20220216", -2, "%Y%m%d")
    20211216

    :param dateStr:
    :param dateDelta:
    :param inputDateFmt:
    :return:
    """
    inputDatetime = datetime.datetime.strptime(dateStr, inputDateFmt)
    outputDatetime = inputDatetime + relativedelta(months=dateDelta)
    outputDatetimeStr = datetime.datetime.strftime(outputDatetime, inputDateFmt)
    return outputDatetimeStr


def dateStrMonthDeltaWithFormatTransformation(dateStr: str, dateDelta: int, inputDateFmt="%Y-%m-%d", outputDateStrFmt="%Y%m%d") -> str:
    """
    Get a date string for some day.
    Example:
    >>> dateStrMonthDeltaWithFormatTransformation("20220216", -2, "%Y%m%d", "%Y-%m-%d")
    2021-12-16

    :param dateStr:
    :param dateDelta:
    :param inputDateFmt:
    :param outputDateStrFmt:
    :return:
    """
    operatedDateString = dateStrMonthDelta(dateStr, dateDelta, inputDateFmt)
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

    print(
        dateStrMonthDelta(
            "20220216",
            -2,
            "%Y%m%d")
    )

    print(
        dateStrMonthDeltaWithFormatTransformation(
            "20220216",
            -2,
            "%Y%m%d",
            "%Y-%m-%d")
    )

    help(duration2List)

