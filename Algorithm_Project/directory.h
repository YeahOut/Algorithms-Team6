#include <iostream>
#include <filesystem>
#include <string>
namespace fs = std::filesystem;

class directory {
private:
	std::string folderName;		//�ش� ���丮�� ���� �̸�
	std::string fullDirectory;	//�ش���丮������ ��� ��ü
public:
	void printFolderName() { std::cout << folderName << std::endl; }
	void printFulDirectory() { std::cout << printFulDirectory << std::endl; }
	std::string getFolderName() { return folderName; }
	std::string getFulDirectory() { return fullDirectory; }
	void setFolderName(std::string input) { folderName = input; }
	void setFulDirectory(std::string input) { fullDirectory = input; }

};

bool is_there_same_thing(std::string folder_path) { //�Է�:��ġ+������� �ϴ� ������ ��
	if (fs::exists(folder_path)) //�̹� �����Ѵٸ� true -> ���� ���� �Ұ�
		return true;
	else return false;			//�������� �ʴٸ� false -> ���� ���� ����
}

void make_folder_in_directory(std::string directory_path, std::string folder_name) {
	std::string folder_path = directory_path + "/" + folder_name;
	if (is_there_same_thing(folder_path)) {
		std::cout << "There exist already same file !! " << std::endl;
	}
	else {
		if (fs::create_directory(folder_path)) {
			std::cout << "���� ���� ����!" << std::endl;
		}
		else {
			std::cerr << "���� ���� ����!" << std::endl;
		}
	}
}
