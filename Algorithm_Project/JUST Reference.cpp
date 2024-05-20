#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    std::string directory_path = "C:\\Users\\dldnd\\Desktop\\Univ\\3-1\\Algorithms\\Project\\download"; // ���丮 ��� ����

    for (const auto& entry : fs::directory_iterator(directory_path)) {
        if (fs::is_regular_file(entry.status())) {
            std::cout << entry.path().filename() << std::endl; // ���� �̸� ���
        }
    }

    std::string folder_name;
    std::cout << "���� �̸��� �Է��ϼ���: ";
    std::cin >> folder_name;

    // ���� �۾� ���丮�� ���ο� ���� ����
    std::string folder_path = directory_path + "/" + folder_name;

    if (!fs::exists(folder_path)) { // ������ �������� �ʴ� ��쿡�� ����
        if (fs::create_directory(folder_path)) {
            std::cout << "���� ���� ����!" << std::endl;
        }
        else {
            std::cerr << "���� ���� ����!" << std::endl;
        }
    }
    else {
        std::cerr << "�̹� ������ �����մϴ�." << std::endl;
    }

    return 0;
}
