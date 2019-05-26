import tokenization_maximumMatching.maximum_Matching as mm
import tokenization_maximumMatching.plotHistogram as plotHis
import operator

def word_segmentation():
    file = open('test.txt', 'r', encoding="utf8") #file chứa đoạn văn cần tách từ
    fileResult = open('result.txt', 'a', encoding="utf8") # file chứa kết quả trả về số lượng từ đã được thống kê sau khi tách
    fileResult1 = open('result_token.txt', 'a', encoding="utf8") # file chứa đoạn văn đã tách các từ, các từ ghép sẽ nối nhau bằng dấu gạch dưới
    dict = {}
    list_word = ""
    count = 0
    symbolEndSentence = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[",
                         "]", "|", "\\", ":", ";", "'", '"', "<", ",", ".", "<", ">", "?", "/"]
    for line in file:
        count += 1
        print(count)
        data = mm.tokenize(line) #gọi hàm tách từ
        for i in range(0, len(data), 1):
            list_word += data[i] + " " # ghi từng từ được tách vào list_word
        list_word += '\n' #kết thúc dòng them \n
        for word in data:
            #bắt đầu thống kê các từ có trong từng câu
            if word in symbolEndSentence:
                continue
            if word not in dict:
                dict[word] = 1
            else:
                dict[word] += 1

    fileResult1.write(list_word) #thực hiện ghi từ vào file

    #in ra màn hình các từ đã được tách
    for x, y in sorted(dict.items(), key=operator.itemgetter(1), reverse=True):
        print("%s : %d" % (x, y))
        fileResult.write(x + " : " + str(y) + "\n")

    file.close()
    fileResult.close()
    fileResult1.close()
    plotHis.PlotHistogram('result.txt') #su dung bieu do

if __name__ == '__main__':
    word_segmentation()