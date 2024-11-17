#include <boost/asio.hpp>
#include <boost/array.hpp>
#include <iostream>
#include"message.hpp"
#include<algorithm>
#include<random>
#include <exception>

std::random_device dev;
std::mt19937 engine(dev());
std::uniform_int_distribution<uint64_t> dist(0, UINT64_MAX);

boost::asio::io_context io_context;
boost::asio::ip::udp::socket server_socket(io_context);
boost::asio::ip::udp::endpoint server_endpoint;

std::vector<uint64_t> auths = {};

boost::array<char, 1024> recv_buffer;


void myopen(std::string pathname, mode_t mode, ServerMessage& response){
    int fd = open(pathname.c_str(), O_RDWR | O_CREAT | O_APPEND, mode);
    if(fd < 0){
        response.error = 1;
        return;
    }
    response.ret_int = fd;
}

void myread(int fd, size_t count, ServerMessage& response){
    std::vector<uint8_t> read_bytes(count, 0);
    ssize_t len = read(fd, read_bytes.data(), count);
    if(len < 0){
        response.error = 1;
        return;
    }
    response.data.assign(read_bytes.begin(), read_bytes.begin() + len); // Use only the bytes read   
}

void mywrite(int fd, const std::vector<uint8_t>& data, ServerMessage& response) {
    size_t total_written = 0;
    size_t count = data.size();
    
    while (total_written < count) {
        ssize_t len = write(fd, data.data() + total_written, count - total_written);

        if (len < 0) {
            response.error = 1; 
            return;
        }

        total_written += len;
    }

}

void mylseek(int fd, off_t offset, int whence, ServerMessage& response) {
    off_t result = lseek(fd, offset, whence);
    if (result < 0) {
        response.error = 1;
        return;
    }
    response.ret_long = result;
}


void mychmod(std::string path, mode_t mode, ServerMessage& response) {
    int result = chmod(path.c_str(), mode);
    if (result < 0) {
        response.error = 1;
        return;
    }
    response.ret_int = result;
}


void myunlink(std::string path, ServerMessage& response) {
    int result = unlink(path.c_str());
    if (result < 0) {
        response.error = 1;
        return;
    }
    response.ret_int = result;
}
void myrename(std::string oldpath, std::string newpath, ServerMessage& response) {
    int result = rename(oldpath.c_str(), newpath.c_str());
    if (result < 0) {
        response.error = 1;
        return;
    }
    response.ret_int = result;
}


ServerMessage parse_message(ClientMessage request){
    std::cout << "Received message!: " << request.toString() << std::endl;
    ServerMessage response;
    response.ticket = request.ticket;
    response.error = 0;
    response.data.clear();
    response.info = "";
    response.ret_auth = 0;
    response.ret_int = 0;
    response.ret_long = 0;
    
    try{
        if(request.func_name == "auth") {
            response.info = "auth";
            uint64_t new_auth = dist(engine);
            auths.push_back(new_auth);
            response.ret_auth = new_auth;
        } else if (std::find(auths.begin(), auths.end(), request.auth) == auths.end()){
            response.info = "bad auth";
            response.error = 1;
        } else if (request.func_name == "open") {
            myopen(request.pathname, request.mode, response);
            response.info = "open";
        } else if (request.func_name == "read") {
            myread(request.fd, request.count, response);
            response.info = "read";
        } else if (request.func_name == "write") {
            mywrite(request.fd, request.data, response);
            response.info = "write";
        } else if (request.func_name == "lseek") {
            mylseek(request.fd, request.offset, request.whence, response);
            response.info = "lseek";
        } else if (request.func_name == "chmod") {
            mychmod(request.pathname, request.mode, response);
            response.info = "chmod";
        } else if (request.func_name == "unlink") {
            myunlink(request.pathname, response);
            response.info = "unlink";
        } else if (request.func_name == "rename") {
            myrename(request.pathname, request.new_pathname, response);
            response.info = "rename";
        } else {
            response.info = "Message received: " + request.toString() + ". Not Implemented Error.";
        }
    } catch (std::exception e){
        response.error = 1;
    }
    return response;
}

void start_server(int port) {
    server_endpoint = boost::asio::ip::udp::endpoint(boost::asio::ip::udp::v4(), port);
    server_socket.open(boost::asio::ip::udp::v4());
    server_socket.bind(server_endpoint);

    std::cout << "Server is listening on port " << port << std::endl;
    ClientMessage msg;
    json j;

    while (true) {
        boost::asio::ip::udp::endpoint client_endpoint;
        size_t len = server_socket.receive_from(boost::asio::buffer(recv_buffer), client_endpoint);
        std::string raw_msg = std::string(recv_buffer.data(), len);

        from_json(json::parse(raw_msg), msg);
        
        auto response = parse_message(msg);
        std::cout << "Sending response: " << response.toString() << std::endl;
        to_json(j, response);
        server_socket.send_to(boost::asio::buffer(j.dump()), client_endpoint);
    }
}

int main() {
    start_server(8080);  // Start server on port 8080
    return 0;
}