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

# 메인 함수: 테스트용
if __name__ == "__main__":
    txt = "남주상지하영중필정키자남상훈정지하상원졍킨누닉남상원정키구나룬걓넵니루남상원"  # 검색할 텍스트
    pat = "남상원"  # 검색할 패턴
    count = boyer_moore_search(pat, txt)
    print(f"Pattern found {count} times.")  # 결과 출력
