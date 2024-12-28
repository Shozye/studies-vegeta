#include"client_library.hpp"
#include<iostream>
int main(){

    std::string method;
    std::string filename;
    std::string text_to_write;
    std::string mode;
    int fd;
    size_t count;
    off_t offset;
    std::string new_filename;
    int whence;
    while(1){
        
        std::cout << "What do you want to do? [open,read,write,lseek,chmod,unlink,rename]" << std::endl;
        std::cin >> method;
        if (method == "open") {
            std::cout << "enter <filename mode>" << std::endl;
            std::cin >> filename >> mode;
            long mode_num = std::strtol(mode.c_str(), nullptr, 8);  // 8 specifies octal base

            int fd = nopen(filename.c_str(), mode_num);
            std::cout << "fd is: " << fd << std::endl; 
        } else if (method == "read") {
            std::cout << "enter <fd count>" << std::endl;
            std::cin >> fd >> count;
            char* read_buffer = new char[count];
            ssize_t len = nread(fd, read_buffer, count);
            std::cout << "size of read text: " << len << std::endl;
            for(int i = 0; i < len; i++){
                std::cout << read_buffer[i];
            }
            std::cout << std::endl;

        } else if (method == "write") {
            std::cout << "enter <fd count>:" << std::endl;
            std::cin >> fd >> count;
            std::cout << "enter text to write:" << std::endl;
            std::cin >> text_to_write;
            ssize_t retval =  nwrite(fd, text_to_write.c_str(), count);
            std::cout << "return value of nwrite: " << retval << std::endl;

        } else if (method == "lseek") {
            std::cout << "enter <fd offset whence>" << std::endl;
            std::cin >> fd >> offset >> whence;
            off_t retval =  nlseek(fd, offset, whence);
            std::cout << "return value of lseek: " << retval << std::endl;

        } else if (method == "chmod") {

            std::cout << "enter <pathname mode>" << std::endl;
            std::cin >> filename >> mode;    
            long mode_num = std::strtol(mode.c_str(), nullptr, 8);  // 8 specifies octal base
            int retval =  nchmod(filename.c_str(), mode_num);
            std::cout << "return value of chmod: " << retval << std::endl;

        } else if (method == "unlink") {

            std::cout << "enter <pathname>" << std::endl;
            std::cin >> filename;   
            int retval = nunlink(filename.c_str());
            std::cout << "return value of unlink: " << retval << std::endl;

        } else if (method == "rename") {

            std::cout << "enter <pathname_old pathname_new>" << std::endl;
            std::cin >> filename >> new_filename;  
            int retval = nrename(filename.c_str(), new_filename.c_str());
            std::cout << "return value of rename: " << retval << std::endl;
        } else 
            std::cout << " no method like this. :) " << std::endl;
        
    }
}