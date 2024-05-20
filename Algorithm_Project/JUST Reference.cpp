#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    std::string directory_path = "C:\\Users\\dldnd\\Desktop\\Univ\\3-1\\Algorithms\\Project\\download"; // 디렉토리 경로 설정

    for (const auto& entry : fs::directory_iterator(directory_path)) {
        if (fs::is_regular_file(entry.status())) {
            std::cout << entry.path().filename() << std::endl; // 파일 이름 출력
        }
    }

    std::string folder_name;
    std::cout << "폴더 이름을 입력하세요: ";
    std::cin >> folder_name;

    // 현재 작업 디렉토리에 새로운 폴더 생성
    std::string folder_path = directory_path + "/" + folder_name;

    if (!fs::exists(folder_path)) { // 폴더가 존재하지 않는 경우에만 생성
        if (fs::create_directory(folder_path)) {
            std::cout << "폴더 생성 성공!" << std::endl;
        }
        else {
            std::cerr << "폴더 생성 실패!" << std::endl;
        }
    }
    else {
        std::cerr << "이미 폴더가 존재합니다." << std::endl;
    }

    return 0;
}
