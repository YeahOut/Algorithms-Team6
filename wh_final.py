import os
import fitz  # PyMuPDF
import time
import shutil

# Boyer-Moore 알고리즘
def boyer_moore(text, pattern):
    def preprocess_bad_character_rule(pattern):
        bad_char_shift = {}
        for i in range(len(pattern) - 1):
            bad_char_shift[pattern[i]] = len(pattern) - i - 1
        return bad_char_shift

    def preprocess_good_suffix_rule(pattern):
        m = len(pattern)
        good_suffix_shift = [m] * (m + 1)
        border_pos = [0] * (m + 1)
        i, j = m, m + 1
        border_pos[i] = j

        while i > 0:
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                if good_suffix_shift[j] == m:
                    good_suffix_shift[j] = j - i
                j = border_pos[j]
            i -= 1
            j -= 1
            border_pos[i] = j

        j = border_pos[0]
        for i in range(m + 1):
            if good_suffix_shift[i] == m:
                good_suffix_shift[i] = j
            if i == j:
                j = border_pos[j]

        return good_suffix_shift

    bad_char_shift = preprocess_bad_character_rule(pattern)
    good_suffix_shift = preprocess_good_suffix_rule(pattern)
    m, n = len(pattern), len(text)
    s = 0

    start_time = time.time()
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            print(f"Pattern found at index {s}")
            return True  # Found
        else:
            s += max(good_suffix_shift[j + 1], bad_char_shift.get(text[s + j], m))

        # Check for timeout to detect potential infinite loop or extremely slow processing
        if time.time() - start_time > 10:  # Timeout of 10 seconds for debugging
            print("Boyer-Moore algorithm taking too long for text of length", len(text))
            return False

    return False  # Not found

# Sunday 알고리즘
def sunday(text, pattern):
    def preprocess_shift_table(pattern):
        shift_table = {}
        for i in range(len(pattern)):
            shift_table[pattern[i]] = len(pattern) - i
        return shift_table

    shift_table = preprocess_shift_table(pattern)
    m, n = len(pattern), len(text)
    i = 0

    while i <= n - m:
        j = 0
        while j < m and pattern[j] == text[i + j]:
            j += 1
        if j == m:
            return True  # Found
        if i + m < n:
            i += shift_table.get(text[i + m], m + 1)
        else:
            break
    return False  # Not found

# Z-array 알고리즘
def z_array(text, pattern):
    def calculate_z(concat):
        z = [0] * len(concat)
        l, r, k = 0, 0, 0
        for i in range(1, len(concat)):
            if i > r:
                l, r = i, i
                while r < len(concat) and concat[r] == concat[r - l]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < len(concat) and concat[r] == concat[r - l]:
                        r += 1
                    z[i] = r - l
                    r -= 1
        return z

    concat = pattern + "$" + text
    z = calculate_z(concat)
    for i in range(len(z)):
        if z[i] == len(pattern):
            return True  # Found
    return False  # Not found

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
                    found = boyer_moore(text, label)
                elif algorithm == 'sunday':
                    print(f"Using Sunday algorithm for {filename} with label {label}")
                    found = sunday(text, label)
                elif algorithm == 'z_array':
                    print(f"Using Z-array algorithm for {filename} with label {label}")
                    found = z_array(text, label)
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