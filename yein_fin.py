import os
import fitz  # PyMuPDF
import time
import shutil

# Boyer-Moore 알고리즘
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

# Sunday 알고리즘
def Sunday(P, T, P_len, T_len):
    i = 0
    T += '\0'  # 텍스트 끝에 널 문자 추가 (패턴과의 비교를 위해)
    count = 0  # 패턴이 나타난 횟수를 저장할 변수
    shift_dict = {}  # 이동 거리를 저장할 딕셔너리

    # 패턴의 각 문자에 대해 이동 거리를 계산하여 딕셔너리에 저장
    for index, value in enumerate(P):
        shift_dict[value] = P_len - index

    # 텍스트를 순차적으로 검사
    while i <= T_len - P_len:
        j = 0
        # 패턴과 텍스트의 현재 위치에서 일치하는지 검사
        while P[j] == T[i + j]:
            j += 1
            if j >= P_len:
                count += 1  # 패턴이 텍스트에서 발견되면 count 증가
                break
        
        # 이동 거리를 계산
        # 패턴 뒤에 오는 문자에 대한 이동 거리를 딕셔너리에서 가져옴
        # 만약 그 문자가 딕셔너리에 없으면 패턴 길이 + 1 만큼 이동
        offset = shift_dict[T[i + P_len]] if T[i + P_len] in shift_dict else P_len + 1
        
        i += offset  # 텍스트에서 다음 검사 위치로 이동

    return count  # 패턴이 나타난 총 횟수를 반환

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

# PDF 텍스트 추출 함수
def extract_text_from_pdf(pdf_path):
    text = ""
    document = fitz.open(pdf_path)
    
    # PDF 제목을 가져와서 텍스트의 맨 앞에 추가
    title = document.metadata.get('title', 'Untitled')
    text += title + "\n\n"
    
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# PDF 파일 분류 함수
def classify_pdfs(input_dir, num_subjects, subject_dirs, labels, algorithm):
    # Ensure subject directories exist
    for subject_dir in subject_dirs:
        os.makedirs(os.path.join(input_dir, subject_dir), exist_ok=True)
    
    start_time = time.time()  # Start time measurement
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            text = extract_text_from_pdf(pdf_path)
            
            for i in range(num_subjects):
                label = labels[i]
                
                # Choose the algorithm to use
                if algorithm == 'boyer_moore':
                    print(f"Using Boyer-Moore algorithm for {filename} with label {label}")
                    found = boyer_moore_search(label, text) > 0
                elif algorithm == 'sunday':
                    print(f"Using Sunday algorithm for {filename} with label {label}")
                    found = Sunday(label, text, len(label), len(text)) > 0
                elif algorithm == 'z_array':
                    print(f"Using Z-array algorithm for {filename} with label {label}")
                    found = z_algorithm_search(label, text) > 0
                else:
                    raise ValueError("Unsupported algorithm selected")
                
                if found:
                    dest_dir = os.path.join(input_dir, subject_dirs[i])
                    shutil.move(pdf_path, os.path.join(dest_dir, filename))
                    print(f"Moved {filename} to {subject_dirs[i]}")
                    break
    
    end_time = time.time()  # End time measurement
    print(f"작업 수행 시간: {end_time - start_time:.2f} 초")

# 메인 함수
if __name__ == "__main__":
    # Example inputs
    num_subjects = int(input("Enter the number of subjects: "))
    subject_dirs = [input(f"Enter the directory name for subject {i+1}: ") for i in range(num_subjects)]
    labels = [input(f"Enter the label for subject {i+1}: ") for i in range(num_subjects)]
    
    input_dir = input("Enter the input directory containing the PDF files: ")
    algorithm = input("Enter the algorithm to use (boyer_moore, sunday, z_array): ")
    
    classify_pdfs(input_dir, num_subjects, subject_dirs, labels, algorithm)
