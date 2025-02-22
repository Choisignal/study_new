import pandas as pd
import random
import googletrans
from tqdm import tqdm
import numpy as np
import os
from os.path import exists, isfile, basename
import re
import 엑셀_구분저장

def 엑셀파일구분하기(data_direct, filename,보존 = False,구분_나누기=True,날짜_나누기=True):
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    날짜_목록 = []
    구분_목록 = []
    if 날짜_나누기 == True:
        try:
            날짜목록 = list(set(data["날짜"]))
            for 날짜 in 날짜목록:
                save_filename1 = f"{data_direct}{filename}_{날짜}.xlsx"
                data1 = data[data["날짜"] == 날짜]
                if 보존 == True:
                    if isfile(save_filename1):
                        pass
                    else:
                        data1.to_excel(save_filename1, index=False)
                        print(save_filename1)
                else:
                    data1.to_excel(save_filename1, index=False)
                    print(save_filename1)
            날짜_목록 += [f"{filename}_{날짜}"]
        except:
            print("날짜 없음!")

    if 구분_나누기 == True:
        try:
            구분목록 = list(set(data["구분"]))
            for 구분 in 구분목록:
                save_filename2 = f"{data_direct}{filename}_{구분}.xlsx"
                data2 = data[data["구분"] == 구분]
                if 보존 == True:
                    if isfile(save_filename2):
                        pass
                    else:
                        data2.to_excel(save_filename2, index=False)
                        print(save_filename2)
                else:
                    data2.to_excel(save_filename2, index=False)
                    print(save_filename2)
                구분_목록 += [f"{filename}_{구분}"]
                print(save_filename2)
        except:
            print("구분 없음!")
    return 날짜_목록, 구분_목록


def 객관식_만들기_한자어(파일명, data_direct, 단답형=True, 설명=True, 글자수=2, 번역=False):
    translator = googletrans.Translator()
    data = pd.read_excel(data_direct+파일명+".xlsx")
    한자 = []
    한글 = []
    for i in tqdm(range(data["대답"].size)):
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        if len(질문.split('/')[0]) == 글자수:
            if 번역 == True:
                한자번역 = translator.translate(질문, dest='en')
                한자번역 = 한자번역.text
                if len(한자번역.split(" ")) <= 2 and 한자번역 != "no" and "(" not in 대답:
                    대답 = f"{대답}({한자번역})"
            한자 += [질문]
            한글 += [대답]
    data = pd.DataFrame({"질문": 한자, "대답": 한글})

    출력_질문목록 = []
    출력_대답목록 = []
    for i in range(data["대답"].size):
        대답목록 = list(set(data["대답"]))
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        질문 = 질문.replace(대답, "[   ]")

        대답목록.remove(대답)
        선지번호 = [1, 2, 3]
        random.shuffle(선지번호)
        random.shuffle(대답목록)
        선지목록 = [1, 2, 3]
        if 설명 == True:
            선지목록[선지번호[0] - 1] = f"{선지번호[0]}. {대답}"
            for j in [1, 2]:
                선지목록[선지번호[j] - 1] = f"{선지번호[j]}. {대답목록[j]}"
            출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
        else:
            선지목록[선지번호[0] - 1] = f"{선지번호[0]}. {str(대답).split(',')[0]}"
            for j in [1, 2]:
                선지목록[선지번호[j] - 1] = f"{선지번호[j]}. {str(대답목록[j]).split(',')[0]}"
            출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"

        출력_질문목록 += [출력_질문]
        출력_대답목록 += [f"{선지번호[0]}, {대답}"]

    save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
    if 번역 == True:
        번역 = "_번역"
    else:
        번역 = ""
    save_filename = data_direct + "객관식_" + 파일명 + f"{글자수}글자{번역}.xlsx"
    print(save_filename)
    save_data.to_excel(save_filename, index=False)

def 단답형_만들기_한자어(파일명, data_direct, 단답형=True, 설명=True, 글자수=2, 번역=False):
    translator = googletrans.Translator()
    data = pd.read_excel(data_direct+파일명+".xlsx")
    한자 = []
    한글 = []
    for i in tqdm(range(data["대답"].size)):
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        if 글자수 == 4 and ',' in 대답[0:10]:
            대답_위치 = 대답.find(',')
            대답 = list(대답)
            대답[대답_위치]="|"
            대답 = ''.join(대답)
        대답 = re.sub('\([^)]+\)', '', 대답)
        대답 = 대답.replace("\n","")
        대답 = 대답.replace("1.","\n1)")
        대답 = 대답.replace("2.","\n2)")
        대답 = 대답.replace("3.","\n3)")
        대답 = 대답.replace(".","")
        대답 = 대답.replace("  "," ")
        if "1)" not in 대답:
            대답 = 대답.replace("「","\n「")
            대답 = 대답.replace("」\n「","」「")
            if len(대답) > len("「사마귀가 넓적한 앞다리를 쳐드는 모습이 마치 도끼를 휘두르는 것 같다」"):
                대답 = 대답.replace("이라는 뜻으로,","\n")
                대답 = 대답.replace("라는 뜻으로,","\n")
                대답 = 대답.replace("는 뜻으로,","\n")
                대답 = 대답.replace("는 뜻","\n")
                대답 = 대답.replace("」라","」\n")
            else:
                대답 = 대답.replace("이라는 뜻으로,",",")
                대답 = 대답.replace("라는 뜻으로,",",")
                대답 = 대답.replace("는 뜻으로,",",")
                대답 = 대답.replace("는 뜻",",")
        else:
            대답 = 대답.replace("또는","")
            if len(대답) > len("「사마귀가 넓적한 앞다리를 쳐드는 모습이 마치 도끼를 휘두르는 것 같다」"):
                대답 = 대답.replace("이라는 뜻으로,","\n")
                대답 = 대답.replace("라는 뜻으로,","\n")
                대답 = 대답.replace("는 뜻으로,","\n")
                대답 = 대답.replace("는 뜻","\n")
            else:
                대답 = 대답.replace("이라는 뜻으로,",",")
                대답 = 대답.replace("라는 뜻으로,",",")
                대답 = 대답.replace("는 뜻으로,",",")
                대답 = 대답.replace("는 뜻",",")
        if len(질문.split('/')[0]) == 글자수:
            if 번역 == True:
                try:
                    한자번역 = translator.translate(질문, dest='en')
                    한자번역 = 한자번역.text
                    if len(한자번역.split(" ")) <= 2 and 한자번역 != "no":
                        if "|" in 대답:
                            대답 = f"{대답.split('|')[0]}({한자번역})|{대답.split('|')[-1]}"
                        else:
                            대답 = f"{대답}({한자번역})"
                except:
                    print(f"번역 에러! : {질문}")
            한자 += [질문]
            한글 += [대답]
    data = pd.DataFrame({"질문": 한자, "대답": 한글})
    if 번역 == True:
        save_filename = data_direct +  파일명 + f"{글자수}글자_번역.xlsx"
    else:
        save_filename = data_direct +  파일명 + f"{글자수}글자.xlsx"
    print(save_filename)

    try:
        data_original = pd.read_excel(save_filename)
        data = pd.concat([data_original, data], ignore_index=True)
        data = data.drop_duplicates(['질문', '대답'])
    except:
        print(f"기존 파일 없음 : {save_filename}")
    data.to_excel(save_filename, index=False)

def 객관식_만들기(파일명, data_direct, 단답형=True, 설명=True):
    data = pd.read_excel(data_direct+파일명+".xlsx")

    출력_질문목록 = []
    출력_대답목록 = []
    for i in range(data["대답"].size):
        대답목록 = list(set(data["대답"]))
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        try:
            질문 = 질문.replace(대답, "[   ]")
        except:
            pass
        대답목록.remove(대답)
        선지번호 = [1, 2, 3]
        random.shuffle(선지번호)
        random.shuffle(대답목록)
        선지목록 = [1, 2, 3]
        if 설명 == True:
            선지목록[선지번호[0]-1] = f"{선지번호[0]}. {대답}"
            선지목록[선지번호[1]-1] = f"{선지번호[1]}. {대답목록[0]}"
            선지목록[선지번호[2]-1] = f"{선지번호[2]}. {대답목록[1]}"
            출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
        else:
            선지목록[선지번호[0]-1] = f"{선지번호[0]}. {str(대답).split(',')[0]}"
            선지목록[선지번호[1]-1] = f"{선지번호[1]}. {str(대답목록[0]).split(',')[0]}"
            선지목록[선지번호[2]-1] = f"{선지번호[2]}. {str(대답목록[1]).split(',')[0]}"
            출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"

        출력_질문목록 += [출력_질문]
        출력_대답목록 += [f"{선지번호[0]}, {대답}"]

    save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
    save_filename = data_direct+"객관식_"+파일명+".xlsx"
    print(save_filename)
    save_data.to_excel(save_filename, index=False)

    # 여기 아래는 단답형
    if 단답형 == True:
        출력_질문목록 = list(data["질문"]) + 출력_질문목록
        출력_대답목록 = list(data["대답"]) + 출력_대답목록

        save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
        save_filename = data_direct+"객관식+단답형_"+파일명+".xlsx"
        print(save_filename)
        save_data.to_excel(save_filename, index=False)


def 객관식_만들기_구분통합(filename, data_direct, 단답형=True, 설명=True):
    최종저장파일명 = data_direct + "객관식_" + filename + "_구분통합.xlsx"
    날짜_목록, 파일명_목록 = 엑셀파일구분하기(data_direct, filename)
    for filename in 날짜_목록:
        객관식_만들기(filename, data_direct, 단답형=False, 설명=True)
    저장파일명목록 = []
    for 파일명 in 파일명_목록:
        data = pd.read_excel(data_direct+파일명+".xlsx")
        os.remove(data_direct+파일명+".xlsx")
        출력_질문목록 = []
        출력_대답목록 = []
        for i in range(data["대답"].size):
            대답목록 = list(set(data["대답"]))
            질문 = data["질문"][i]
            대답 = data["대답"][i]
            try:
                질문 = 질문.replace(대답, "[   ]")
            except:
                pass

            if len(대답목록) > 2:
                대답목록.remove(대답)
                선지번호 = [1, 2, 3]
                random.shuffle(선지번호)
                random.shuffle(대답목록)
                선지목록 = [1, 2, 3]
                대답목록 = [대답] + 대답목록
                if 설명 == True:
                    선지목록[선지번호[0]-1] = f"{선지번호[0]}. {대답목록[0]}"
                    선지목록[선지번호[1]-1] = f"{선지번호[1]}. {대답목록[1]}"
                    선지목록[선지번호[2]-1] = f"{선지번호[2]}. {대답목록[2]}"
                    출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
                else:
                    선지목록[선지번호[0] -
                         1] = f"{선지번호[0]}. {str(대답목록[0]).split(',')[0]}"
                    선지목록[선지번호[1] -
                         1] = f"{선지번호[1]}. {str(대답목록[1]).split(',')[0]}"
                    선지목록[선지번호[2] -
                         1] = f"{선지번호[2]}. {str(대답목록[2]).split(',')[0]}"
                    출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"

                출력_질문목록 += [출력_질문]
                출력_대답목록 += [f"{선지번호[0]}, {대답}"]
            elif len(대답목록) == 2:
                선지번호 = [1, 2]
                선지목록 = [1, 2]
                대답목록.remove(대답)
                if 설명 == True:
                    선지목록[선지번호[0] - 1] = f"{선지번호[0]}. {대답}"
                    선지목록[선지번호[1] - 1] = f"{선지번호[1]}. {대답목록[0]}"
                    출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n"
                else:
                    선지목록[선지번호[0] - 1] = f"{선지번호[0]}. {str(대답).split(',')[0]}"
                    선지목록[선지번호[1] -
                         1] = f"{선지번호[1]}. {str(대답목록[0]).split(',')[0]}"
                    출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n"

                출력_질문목록 += [출력_질문]
                출력_대답목록 += [f"{선지번호[0]}, {대답}"]

        save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
        save_filename = data_direct+"객관식_"+파일명+".xlsx"

        # 여기 아래는 단답형
        if 단답형 == True:
            출력_질문목록 = list(data["질문"]) + 출력_질문목록
            출력_대답목록 = list(data["대답"]) + 출력_대답목록

            save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
            save_filename = data_direct+"객관식+단답형_"+파일명+".xlsx"
            print(save_filename)
            save_data.to_excel(save_filename, index=False)
        else:
            print(save_filename)
            save_data.to_excel(save_filename, index=False)
        저장파일명목록 += [save_filename]
    save_df = pd.read_excel(저장파일명목록[0])
    os.remove(저장파일명목록[0])
    for 저장파일명 in 저장파일명목록[1:]:
        df = pd.read_excel(저장파일명)
        save_df = pd.concat([save_df, df])
        os.remove(저장파일명)
    print(최종저장파일명)
    save_df.to_excel(최종저장파일명)


def 특정구분제거(data_direct, filename, 구분목록):
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    제거요소 = ""
    for 구분 in 구분목록:
        data = data[data["구분"] != 구분]
        제거요소 += f"{구분}_"
    save_filename = f"{data_direct}{filename}_{제거요소[:-1]}제거.xlsx"
    data.to_excel(save_filename, index=False)
    print(save_filename)


def OX퀴즈만들기(data_direct, filename):
    translator = googletrans.Translator()
    text1 = []
    text2 = []
    text3 = []

    df = pd.read_excel(f"{data_direct}{filename}.xlsx")
    df = df.drop_duplicates(['질문'])
    df = df.reset_index()
    kor = df["대답"]
    chi = df["질문"]
    pri = df["구분"]
    two_list = []
    for i in range(len(chi)):
        if len(chi[i]) == 2:
            two_list += [i]

    kor = kor[two_list]
    chi = chi[two_list]
    pri = pri[two_list]
    kor = np.array(kor)
    for i in range(len(kor)):
        if "|" in kor[i]:
            kor[i] = kor[i].split("|")[0]
    chi = np.array(chi)
    pri = np.array(pri)
    딕셔너리1 = {}
    for i in range(kor.size):
        단어 = str(kor[i])
        if 단어[0] not in 딕셔너리1.keys():
            딕셔너리1[단어[0]] = ""
        if chi[i] not in 딕셔너리1[단어[0]]:
            딕셔너리1[단어[0]] = 딕셔너리1[단어[0]] + chi[i] + ", "

    딕셔너리2 = {}
    for i in range(kor.size):
        단어 = str(kor[i])
        if 단어[1] not in 딕셔너리2.keys():
            딕셔너리2[단어[1]] = ""
        if chi[i] not in 딕셔너리2[단어[1]]:
            딕셔너리2[단어[1]] = 딕셔너리2[단어[1]] + chi[i] + ", "

    print_list = []
    for i in tqdm(range(kor.size)):
        pri1 = str(pri[i])
        if pri1 == "한자어":
            kor1 = str(kor[i])
            if len(딕셔너리1[kor1[0]].split(","))>2:
                chi1 = str(chi[i])
                try:
                    if "(" not in kor1:
                        trans = translator.translate(chi1, dest='en')
                        trans = trans.text
                        if len(trans.split(" ")) <= 2:
                            trans = f"({trans})".lower()
                        else:
                            trans = ""
                except:
                    trans = ""
                for j in range(kor.size):
                    kor2 = str(kor[j])
                    chi2 = str(chi[j])
                    if kor1 == kor2 and chi1 == chi2:
                        print_word = f"'{kor1}{trans}' = {chi2}?/o , ㅇ , {chi2}"
                        if print_word not in print_list:
                            #print(print_word)
                            text1 += [f"'{kor1}{trans}' = {chi2}?"]
                            text2 += [f"ㅇ"]
                            text3 += [f"{chi2}"]
                        print_list += [print_word]
                    elif kor1[0] == kor2[0] and chi1[0] != chi2[0]:
                        chi3 = chi2[0]+chi1[1]
                        print_word = f"'{kor1}{trans}' = {chi3}?/x , ㄴ, {chi1}"
                        if print_word not in print_list:
                            #print(print_word)
                            text1 += [f"'{kor1}{trans}' = {chi3}?"]
                            text2 += [f"ㄴ"]
                            text3 += [f"{chi1}"]
                        print_list += [print_word]

    print_list = []
    for i in tqdm(range(kor.size)):
        pri1 = str(pri[i])
        if pri1 == "o":
            kor1 = str(kor[i])
            if len(딕셔너리2[kor1[1]].split(","))>2:
                kor1 = str(kor[i])
                chi1 = str(chi[i])
                try:
                    if "(" not in kor1:
                        trans = translator.translate(chi1, dest='en')
                        trans = trans.text
                        if len(trans.split(" ")) <= 2:
                            trans = f"({trans})".lower()
                        else:
                            trans = ""
                except:
                    trans = ""
                for j in range(kor.size):
                    kor2 = str(kor[j])
                    chi2 = str(chi[j])
                    if kor1 == kor2 and chi1 == chi2:
                        pass
                    elif kor1[1] == kor2[1] and chi1[1] != chi2[1]:
                        chi3 = chi1[0]+chi2[1]
                        print_word = f"'{kor1}{trans}' = {chi3}?/x , ㄴ, {chi1}"
                        if print_word not in print_list:
                            #print(print_word)
                            text1 += [f"'{kor1}{trans}' = {chi3}?"]
                            text2 += [f"ㄴ"]
                            text3 += [f"{chi1}"]
                        print_list += [print_word]

    data = {"Text 1": text1, "Text 2": text2, "Text 3": text3}
    data = pd.DataFrame(data)
    try:
        data_original = pd.read_excel(f"{data_direct}{filename}.xlsx".replace("단답형", "O X 퀴즈"))
        data = pd.concat([data_original, data], ignore_index=True)
        data = data.drop_duplicates(['Text 1', 'Text 2','Text 3'])
    except:
        print(f"기존 파일 없음 : {data_direct}{filename}.xlsx".replace("단답형", "O X 퀴즈"))
    data.to_excel(
        f"{data_direct}{filename}.xlsx".replace("단답형", "O X 퀴즈"))

def 구분_생성(data_direct, filename):
    df = pd.read_excel(f"{data_direct}{filename}.xlsx")
    if '구분' not in list(df.keys()):
        df['구분'] = ['기본' for i in range(len(df))]
    df['구분'] = df['구분'].fillna('기본')
    num_total = df.shape[0]
    for i in range(num_total):
        대답 = df['대답'][i]
        대답 = 대답.rstrip()
        '''
        if korean_to_be_englished(대답)[-1][-1] != ' ':
            df['구분'][i] = korean_to_be_englished(대답)[-1][-1]
        else:
            df['구분'][i] = korean_to_be_englished(대답)[-2][-1]
        '''
        df['구분'][i] = 대답[-1]
    df.to_excel(f"{data_direct}{filename}.xlsx",index=False)











data_direct = "./학습자료/단답형/"
filename = "국어_복습"
if filename == "국어_복습":
    #엑셀_구분저장.국어_복습()
    #단답형_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=1,번역= False)
    #단답형_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=2,번역=True)
    #단답형_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=3,번역=True)
    #단답형_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=4,번역=False)
    OX퀴즈만들기(data_direct, "국어_복습_한자어")

elif filename == "국어_암기자료":
    엑셀파일구분하기(data_direct, filename,보존=True,구분_나누기=False,날짜_나누기=True)
elif filename == "국어_57항":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "영어_단어":
    #구분_생성(data_direct, filename)
    엑셀파일구분하기(data_direct, filename,보존=True,구분_나누기=False,날짜_나누기=True)
    '''
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
    날짜_목록, 구분_목록 = 엑셀파일구분하기(data_direct, filename)
    객관식_만들기(filename, data_direct, 단답형=False,설명=True)
    for filename in 날짜_목록:
        객관식_만들기(filename, data_direct, 단답형=False, 설명=True)
    for filename in 구분_목록:
        객관식_만들기(filename, data_direct, 단답형=False, 설명=True)
    day_list = []
    for day in 날짜_목록:
        day_list += [int(day.split("Day")[-1])]
    filename = f"영어_단어_Day{str(max(day_list)).zfill(2)}"
    객관식_만들기(filename, data_direct, 단답형=False,설명=True)
    try:
        객관식_만들기(filename+"_유의어", data_direct, 단답형=False,설명=True)
    except:
        print("유의어")
    try:
        객관식_만들기(filename+"_관용어", data_direct, 단답형=False,설명=True)
    except:
        print("관용어")
    '''
elif filename == "영어_복습":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
    # =IF(C500="암기문법 : 뜻","암기문법 : 뜻",IF(C500="암기문법 : 시제","암기문법 : 시제",IF(C500="암기문법 : 접속사","암기문법 : 접속사",CONCATENATE(D500," : ",C500))))
elif filename == "삼국통합":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "삼국통합":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "불교":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "한국사_대조":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
    엑셀파일구분하기(data_direct, filename,보존=False,구분_나누기=False,날짜_나누기=True)
elif filename == "한자의지혜":
    #OX퀴즈만들기(data_direct, "한자의지혜")
    단답형_만들기_한자어(filename, data_direct, 단답형=False,설명=False,글자수=1,번역= False)
    단답형_만들기_한자어(filename, data_direct, 단답형=False,설명=False,글자수=2,번역=True)
    단답형_만들기_한자어(filename, data_direct, 단답형=False,설명=False,글자수=3,번역=False)
    단답형_만들기_한자어(filename, data_direct, 단답형=False,설명=False,글자수=4,번역=False)
else:
    #객관식_만들기(filename, data_direct, 단답형=False, 설명=True)
    #객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
    엑셀파일구분하기(data_direct, filename)
