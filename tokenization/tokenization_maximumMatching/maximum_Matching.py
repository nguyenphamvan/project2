import re
import unicodedata
import sys

fileDictionary = open('Dict-UTF8.txt', 'r',  encoding="utf8")
fileResult =  open('result.txt', 'a',  encoding="utf8")
dictionary = []


for line in fileDictionary:
    if line == "### Number of part-of-speech tag: 17 ###\n":
        break;
    elif line == "### Number of words: 31137 ###\n":
        continue
    else:
        regex = "{.*?}"
        line = re.sub(re.compile(regex), "", line)
        line = line.split(" \n")[0]
        dictionary.append(line)

fileDictionary.close()

def syllablze(text):
        text = unicodedata.normalize('NFC', text)
        specials = ["==>", "->", "\.\.\.", ">>"]
        sign = ["==>", "->", "\.\.\.", ">>"]
        digits = "\d+([\.,_]\d+)+"
        email = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        web = "^(http[s]?://)?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
        datetime = [
            "\d{1,2}\/\d{1,2}(\/\d+)?",
            "\d{1,2}-\d{1,2}(-\d+)?",
        ]
        word = "\w+"
        non_word = "[^\w\s]"
        abbreviations = [
            "[A-ZĐ]+\.",
            "Tp\.",
            "Mr\.", "Mrs\.", "Ms\.",
            "Dr\.", "ThS\."
        ]
        patterns = []
        patterns.extend(abbreviations)
        patterns.extend(sign)
        patterns.extend(specials)
        patterns.extend([web, email])
        patterns.extend(datetime)
        patterns.extend([digits, non_word, word])
        patterns = "(" + "|".join(patterns) + ")"
        if sys.version_info < (3, 0):
            patterns = patterns.decode('utf-8')
        tokens = re.findall(patterns, text, re.UNICODE)
        return [token[0] for token in tokens]


def maximumMatching(listWord , start, lengthList):
    words = []
    s = start
    n = lengthList - 1
    e = n

    while(s < n):
        tempWord = ""
        for i in range(s , e + 1, 1):
            if (i == e):
                tempWord = tempWord + listWord[i]
            else:
                tempWord = tempWord + listWord[i] + "_"
        if tempWord.lower()  not in dictionary:
            e = e - 1
        elif tempWord.lower() in dictionary:
            words.append(tempWord)
            s = e + 1
            e = n

        if ( e == s):
            words.append(listWord[s])
            s = e + 1
            e = n
            if (s == n):
                words.append(listWord[n])
    return  words

#tach doan van thanh cac cau ko co dau tach cau va ap dung thuat toan tach tu cho tung cau
def tokenize(data):
    list = syllablze(data)
    symbolEndSentence = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[",
                         "]", "|", "\\", ":", ";", "'", '"', "<", ",", ".", "<", ">", "?", "/"]
    listDiemNgatCau = []

    for i in range(len(list)):
        if list[i] in symbolEndSentence:
            listDiemNgatCau.append(i)

    result = []
    if (len(listDiemNgatCau) == 0):
        result.extend(maximumMatching(list, 0, len(list)))
    else:
        result.extend(maximumMatching(list,0,listDiemNgatCau[0]))

        for i in range(0, len(listDiemNgatCau), 1):
            result.extend(list[listDiemNgatCau[i]])
            if (i == len(listDiemNgatCau)-1):
                result.extend(maximumMatching(list, listDiemNgatCau[len(listDiemNgatCau) - 1] + 1, len(list)))
            else:
                result.extend(maximumMatching(list, listDiemNgatCau[i] + 1, listDiemNgatCau[i + 1]))
    return result


def maximumMatching_test(listWord , start, lengthList):
    s = start
    n = lengthList - 1
    e = n
    resultTest = []

    while(s < n):
        tempWord = ""
        for i in range(s , e + 1, 1):
            if (i == e):
                tempWord = tempWord + listWord[i]
            else:
                tempWord = tempWord + listWord[i] + "_"
        if tempWord.lower()  not in dictionary:
            e = e - 1
        elif tempWord.lower() in dictionary:
            for i in range(s,e+1,1):
                if(i == s):
                    resultTest.append('B')
                else:
                    resultTest.append('I')
            s = e + 1
            e = n

        if ( e == s):
            resultTest.append('B')
            s = e + 1
            e = n
            if (s == n):
                resultTest.append('B')
    return  resultTest

#tach doan van thanh cac cau ko co dau tach cau va ap dung thuat toan tach tu cho tung cau
def tokenize_test(data):
    list = syllablze(data)
    symbolEndSentence = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[",
                         "]", "|", "\\", ":", ";", "'", '"', "<", ",", ".", "<", ">", "?", "/"]
    listDiemNgatCau = []

    for i in range(len(list)):
        if list[i] in symbolEndSentence:
            listDiemNgatCau.append(i)

    result = []
    if (len(listDiemNgatCau) == 0):
        result.extend(maximumMatching_test(list, 0, len(list)))
    else:
        result.extend(maximumMatching_test(list,0,listDiemNgatCau[0]))
        for i in range(0, len(listDiemNgatCau), 1):
            result.extend('B')
            if (i == len(listDiemNgatCau)-1):
                result.extend(maximumMatching_test(list, listDiemNgatCau[len(listDiemNgatCau) - 1] + 1, len(list)))
            else:
                result.extend(maximumMatching_test(list, listDiemNgatCau[i] + 1, listDiemNgatCau[i + 1]))
    return result

# hàm test với file BI tương ứng
def test(path):
    countLine = 0
    resultTestTotal = 0
    resultTrue = 0
    resultForEachLine = []
    data = ""
    data_token = []
    file = open(path, 'r', encoding="utf8")

    for line in file:
        countLine += 1;
        if (countLine == 25000):
            break
        if line != "\n":
            content = line.split('\n')
            resultForEachLine.append(content[0].split("\t")[1])
            data += (content[0].split("\t")[0] + " ")
        else:
            data_token.extend(tokenize(data))
            result = tokenize_test(data)
            resultTestTotal += len(result)
            k = min(len(result), len(resultForEachLine))
            for i in range(0, k):
                if resultForEachLine[i] == result[i]:
                    resultTrue += 1
            print(str(resultTrue) + " / " + str(resultTestTotal))
            data = ""
            resultForEachLine.clear()

    print(data_token)

if __name__ == '__main__':
    test('test-BI.txt')
# 9976 / 11032
