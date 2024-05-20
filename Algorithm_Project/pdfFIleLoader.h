#pragma once
#include <directory.h>
#include <filesystem>
namespace fs = std::filesystem;
using namespace std;

class pdfFileLoader {
private:


public:
	void print_all_pdfs_from_directory(directory d) {
		string directory_path = d.getFulDirectory();
		for (const auto& entry : fs::directory_iterator(directory_path)) {
			if (fs::is_regular_file(entry.status())) {
				std::cout << entry.path().filename() << std::endl; // 파일 이름 출력
			}
		}
	}
	
};