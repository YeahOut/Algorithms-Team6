import os
import shutil
import time
import fitz

# Z-array 계산 함수


def fill_z_array(S, Z):
    # 문자열 S의 길이를 n으로 설정
    n = len(S)

    # L과 R은 현재 검사 중인 부분 문자열의 좌우 경계를 나타내며, 초기값은 0으로 설정
    L, R, K = 0, 0, 0

    # 문자열 S의 두 번째 문자부터 끝까지 반복
    for i in range(1, n):
        if i > R:
            # i가 R보다 크면 새로운 경계를 설정해야 함
            L, R = i, i

            # 일치하는 부분 문자열의 길이를 찾음
            while R < n and S[R] == S[R - L]:
                R += 1

            # Z[i]에 일치하는 길이를 저장
            Z[i] = R - L

            # R을 감소시켜서 마지막 일치 위치를 설정
            R -= 1
        else:
            # i가 R보다 작으면 이미 계산된 Z 값을 활용
            K = i - L

            # Z[K] 값이 현재 부분 문자열 경계 내에 있는 경우
            if Z[K] < R - i + 1:
                Z[i] = Z[K]
            else:
                # 그렇지 않은 경우 새로운 경계를 설정하고 재검사
                L = i
                while R < n and S[R] == S[R - L]:
                    R += 1

                # Z[i]에 일치하는 길이를 저장
                Z[i] = R - L

                # R을 감소시켜서 마지막 일치 위치를 설정
                R -= 1


# Z-array 기반 문자열 매칭 함수
def z_algorithm_search(pattern, text):
    # 패턴과 텍스트를 결합하고, 그 사이에 특수 문자 '$'를 추가
    concat = pattern + "$" + text

    # 결합된 문자열에 대한 Z 배열을 초기화
    Z = [0] * len(concat)

    # 결합된 문자열에 대해 Z 배열을 채움
    fill_z_array(concat, Z)

    # 패턴이 텍스트에 몇 번 나타나는지 세기 위한 카운터
    count = 0

    # Z 배열을 순회하며 패턴과 일치하는 부분 찾기
    for i in range(len(pattern) + 1, len(Z)):
        # Z 배열의 값이 패턴의 길이와 같은 경우, 패턴이 일치하는 위치
        if Z[i] == len(pattern):
            count += 1

    # 패턴이 텍스트에 나타난 횟수를 반환
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
    return [f.name for f in os.scandir(directory) if f.is_dir()]

# 해당 폴더에 있는 PDF 파일 이름 불러오기


def list_pdf(path):
    return [f.name for f in os.scandir(path) if f.is_file() and f.name.lower().endswith('.pdf')]


def main():
    pdf_path = r'C:\Users\최예인\Desktop\download'
    directory_path = r'C:\Users\최예인\Desktop\algorithm'
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
        match_dict = {}
        start_time = time.time()

        for label in labels:
            count = z_algorithm_search(label, pdf_text)
            result.append(count)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('{} 파일 Z-array 알고리즘 매칭 시간 {:5f} 초'.format(file, elapsed_time))

        for i in range(len(labels)):
            match_dict[folder_names[i]] = result[i]

        max_match = max(result)
        matched_folders = [folder for folder,
                           count in match_dict.items() if count == max_match]

        if matched_folders:
            target_folder = matched_folders[0]
            target_directory = os.path.join(directory_path, target_folder)
            shutil.copy2(file_path, target_directory)
            os.remove(file_path)


if __name__ == '__main__':
    main()
