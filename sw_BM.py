import os
import shutil
import time
import fitz



def boyer_moore_search(pat, txt):
    # 불일치 문자 히스틱을 초기화
    right = {}
    for j in range(len(pat)):
        right[pat[j]] = j

    M = len(pat)  # 패턴의 길이
    N = len(txt)  # 텍스트의 길이
    count = 0     # 패턴이 나타난 횟수를 저장할 변수
    skip = 0      # 건너뛸 문자 수

    # 텍스트를 순차적으로 검사
    i = 0
    while i <= N - M:
        skip = 0
        # 패턴의 끝에서 시작하여 앞쪽으로 비교
        for j in range(M - 1, -1, -1):
            if pat[j] != txt[i + j]:
                # 불일치 발생 시, 건너뛸 문자 수 계산
                skip = max(1, j - right.get(txt[i + j], -1))
                break
        if skip == 0:
            # 패턴이 나타난 횟수 증가
            count += 1
            skip = 1
        i += skip
    return count

# PDF 파일 내용 읽기


def read_pdf_text(pdf_path):
    text = ''
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
    return text

# 해당 폴더에 있는 서브 폴더의 이름 불러오기


def list_subfolders(directory):
    subfolders = [f.name for f in os.scandir(directory) if f.is_dir()]
    return subfolders

# 해당 폴더에 있는 PDF 파일 이름 불러오기


def list_pdf(path):
    pdf_files = [f.name for f in os.scandir(
        path) if f.is_file() and f.name.lower().endswith('.pdf')]
    return pdf_files


def main():
    pdf_path = r'C:\Users\최예인\Desktop\downloads'
    directory_path = r'C:\Users\최예인\Desktop\project'
    pdf_files = list_pdf(pdf_path)

    # 폴더 갯수와 이름 입력받기
    folder_count = int(input("필요한 폴더 갯수를 입력하시오 : "))
    folder_names = input("폴더 이름을 입력하시오 : ").split(", ")
    labels = []

    for i in range(folder_count):
        label = input(f'{i+1}번째 폴더의 label을 입력하시오 : ')
        labels.append(label)

    # 폴더 생성
    for folder in folder_names:
        os.makedirs(os.path.join(directory_path, folder), exist_ok=True)

    for file in pdf_files:
        file_path = os.path.join(pdf_path, file)
        pdf_text = read_pdf_text(file_path)
        T_len = len(pdf_text)
        result = []
        dict = {}
        start_time = time.time()

        for label in labels:
            count = boyer_moore_search(label, pdf_text)
            result.append(count)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('{} 파일 Z-array 알고리즘 매칭 시간 {:5f} 초'.format(file, elapsed_time))

        for i in range(len(labels)):
            dict[folder_names[i]] = result[i]

        max_match = max(result)
        matched_folders = [folder for folder,
                           count in dict.items() if count == max_match]

        if matched_folders:
            target_folder = matched_folders[0]
            target_directory = os.path.join(directory_path, target_folder)
            shutil.copy2(file_path, target_directory)
            os.remove(file_path)


if __name__ == '__main__':
    main()
