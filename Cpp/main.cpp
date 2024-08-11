#include <iostream>
#include <fstream>

#include <filesystem>
#include <string>
#include "command.h"
using namespace std;
Operation operate;

int main(int argc,char* argv[]){
    //declare variables
    const string cwd = filesystem::current_path();
    const string username = getenv("USER");
    const string folder = "/Users/"+ username +"/Documents/CodeSnippets";
    const string file = folder+"/cnd.code";
    const string cmd = argv[1];
    const string keep[] = {"add","delete","conf","update",","};
    const string cmdlist = operate.cmdlist(file.data());
    operate.check(folder.data(),file.data());

    return 0;
}