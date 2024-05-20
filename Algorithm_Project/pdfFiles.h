#include <iostream>
#include <string>
#include <directory.h>
#include <filesystem>
namespace fs = std::filesystem;
using namespace std;

class pdfFIle {
private:
	string fileName;
public:
	directory directory;
	void printFileName() { cout << fileName << endl; }
	void setFileName(string input) { fileName = input; }
	string getFiileName() { return fileName; }
};
