#include "command.h"
#include <fstream>
#include <sys/stat.h>
using namespace std;

void Operation::check(const char* folder, const char* file){
    struct stat state;
    if(stat(folder,&state) != 0){
        mkdir(folder,S_IRWXU);
    }else{}

    if(stat(file, &state) != 0 && (state.st_mode & S_IFDIR)){
        ofstream write (file);
        write.close();
    }
}

string Operation::cmdlist(const char* file){
    ofstream read (file);
    
}