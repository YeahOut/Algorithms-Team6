#include <iostream>
#include <filesystem>
#include <string>
namespace fs = std::filesystem;

class directory {
private:
	std::string folderName;		//해당 디렉토리의 폴더 이름
	std::string fullDirectory;	//해당디렉토리까지의 경로 전체
public:
	void printFolderName() { std::cout << folderName << std::endl; }
	void printFulDirectory() { std::cout << printFulDirectory << std::endl; }
	std::string getFolderName() { return folderName; }
	std::string getFulDirectory() { return fullDirectory; }
	void setFolderName(std::string input) { folderName = input; }
	void setFulDirectory(std::string input) { fullDirectory = input; }

};

bool is_there_same_thing(std::string folder_path) { //입력:위치+만들고자 하는 파일의 명
	if (fs::exists(folder_path)) //이미 존재한다면 true -> 파일 생성 불가
		return true;
	else return false;			//존재하지 않다면 false -> 파일 생성 가능
}

void make_folder_in_directory(std::string directory_path, std::string folder_name) {
	std::string folder_path = directory_path + "/" + folder_name;
	if (is_there_same_thing(folder_path)) {
		std::cout << "There exist already same file !! " << std::endl;
	}
	else {
		if (fs::create_directory(folder_path)) {
			std::cout << "폴더 생성 성공!" << std::endl;
		}
		else {
			std::cerr << "폴더 생성 실패!" << std::endl;
		}
	}
}
