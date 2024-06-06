import os
import shutil
import time
import fitz


# pdf 파일 내용 읽기
def read_pdf_text(pdf_path):
    text = ''
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
    return text


# 해당 플더에 있는 사이브 플더의 이름 불어오기
def list_subfolders(directory):
    subfolders = [f.name for f in os.scandir(directory) if f.is_dir()]
    return subfolders


# 해당 플더에 있는 pdf 파일 이름 불어오기
def list_pdf(path):
    pdf_files = [f.name for f in os.scandir(path) if f.is_file() and f.name.lower().endswith('.pdf')]
    return pdf_files


# def KMP(Pattern, Text, P_len, T_len):
#     # LPS 배열 초기화
#     lps = [0] * P_len
#
#     # 초기화
#     j = 0
#     count = 0
#     # LPS 배열 계산
#     computeLPSArray(Pattern, P_len, lps)
#
#     # 텍스트 문자열을 검색
#     i = 0
#     while (T_len - i) >= (P_len - j):
#         # 패턴과 텍스트의 문자가 일치하는 경우
#         if Pattern[j] == Text[i]:
#             i += 1
#             j += 1
#
#         if j == P_len:
#             # 패턴을 찾은 경우, 경과 시간 계산
#
#             # LPS 배열 초기화 후 반환
#             j = lps[j - 1]
#             count += 1
#             # return Pattern, elapsed_time
#         # 패턴과 텍스트의 문자가 일치하지 않는 경우
#         elif i < T_len and Pattern[j] != Text[i]:
#             # j가 0보다 큰 경우, LPS 배열을 이용하여 j 갱신
#             if j != 0:
#                 j = lps[j - 1]
#             # j가 0인 경우, i만 증가
#             else:
#                 i += 1
#     return count
#
#
# def computeLPSArray(Pattern, P_len, lps):
#     # 초기화
#     lenth = 0
#     lps[0] = 0
#     i = 1
#
#     # LPS 배열 계산
#     while i < P_len:
#         # 패턴의 현재 위치와 이전 위치가 일치하는 경우
#         if Pattern[i] == Pattern[lenth]:
#             # LPS 배열 갱신 후 다음 위치로 이동
#             lenth += 1
#             lps[i] = lenth
#             i += 1
#         # 패턴의 현재 위치와 이전 위치가 일치하지 않는 경우
#         else:
#             # lenth가 0보다 큰 경우, lenth 갱신
#             if lenth != 0:
#                 lenth = lps[lenth - 1]
#             # lenth가 0인 경우, lps[i]에 0을 할당하고 다음 위치로 이동
#             else:
#                 lps[i] = 0
#                 i += 1
def Sunday(P, T, P_len, T_len):
    i = 0
    T += '\0'
    count = 0
    shift_dict = {}
    for index, value in enumerate(P):
        shift_dict[value] = P_len - index
    print(shift_dict)
    while i <= T_len - P_len:
        j = 0
        while P[j] == T[i + j]:

            j += 1
            if j >= P_len:
                count += 1
                break
        offset = shift_dict[T[i + P_len]] if T[i + P_len] in shift_dict else P_len + 1

        i += offset
    return count


def main():
    pdf_path = r'C:/Users/22818/Downloads/'
    directory_path = r'C:/Users/22818/PycharmProjects/algorithm2homework/'
    pdf_files = list_pdf(pdf_path)

    for file in pdf_files:
        file_path = os.path.join(pdf_path, file)

        pdf_text = read_pdf_text(file_path)
        PatternString = list_subfolders(directory_path)
        T_len = len(pdf_text)
        result = []
        matched = []
        dict = {}
        start_time = time.time()
        for i in PatternString:
            P_len = len(i)

            count = Sunday(i, pdf_text, P_len, T_len)
            result.append(count)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('{}파일  Sunday 알고리즘 매칭 시간{:5f}'.format(file, elapsed_time))
        for i in range(len(PatternString)):
            dict[PatternString[i]] = result[i]
    
        max_match = max(result)
        for key, value in dict.items():
            if value == max_match:
                matched.append(key)
        
        directory_file = os.path.join(directory_path, os.path.basename(matched[0])) + '/'

        shutil.copy2(file_path, directory_file)
        os.remove(file_path)


if __name__ == '__main__':
    main()
