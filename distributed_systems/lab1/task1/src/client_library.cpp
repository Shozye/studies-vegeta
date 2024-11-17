#include <fcntl.h>
#include<unistd.h>
#include<iostream>
#include<boost/asio.hpp>
#include<boost/array.hpp>
#include"json.hpp"
#include<random>
#include <chrono>
#include"message.hpp"

using json = nlohmann::json;

std::string last_command = "nothing";
boost::asio::io_context io_context;
boost::asio::ip::udp::socket client_socket(io_context);
boost::asio::ip::udp::endpoint server_endpoint;
boost::array<char, 1024> recv_buffer;
boost::array<char, 1024> send_buffer;

std::random_device dev;
std::mt19937 engine(dev());
std::uniform_int_distribution<uint64_t> dist(0, UINT64_MAX);

bool network_initiated = false;
uint64_t auth_token = 0;

void send_to_server(ClientMessage msg){
    json j;
    to_json(j, msg);
    std::string raw_msg = j.dump();
    auto buf = boost::asio::buffer(raw_msg);
    client_socket.send_to(buf, server_endpoint);
    std::cout << "Message " << raw_msg << " sent to server!\n";
}

ServerMessage recv_from_server(int timeout_milliseconds){
    std::cout << "receiving from server with " << timeout_milliseconds << "ms" << std::endl; 
    boost::asio::ip::udp::endpoint sender_endpoint;

    boost::asio::steady_timer timer(client_socket.get_executor());

    bool receive_completed = false;
    boost::system::error_code ec;

    timer.expires_after(std::chrono::milliseconds(timeout_milliseconds));
    timer.async_wait([&](const std::error_code& error) {
        if (!error && !receive_completed) {
            client_socket.cancel();
        }
    });

    ServerMessage returnMessage;
    bool returned = false;

        // Start async receive
    client_socket.async_receive_from(
        boost::asio::buffer(recv_buffer), sender_endpoint,
        [&](const boost::system::error_code& error, std::size_t bytes_transferred) {
            if (!error) {
                receive_completed = true;
                timer.cancel(); 
                ec = error;

                std::string received_message(recv_buffer.data(), bytes_transferred);
                std::cout << "Raw Message from Server: " << received_message << std::endl;

                json j = json::parse(received_message);
                from_json(j, returnMessage);
                returned = true;
                return;
            } else if (error != boost::asio::error::operation_aborted) {
                ec = error;
            }
        }
    );

    io_context.reset();
    io_context.run();

    if(!returned){
        throw 1001;
    }

    return returnMessage; 
}

ServerMessage send_and_receive(ClientMessage msg){
    msg.auth = auth_token;
    uint64_t ticket = dist(engine);
    msg.ticket = ticket;

    ServerMessage response;
    auto start = std::chrono::high_resolution_clock::now();
    send_to_server(msg);
    auto now = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(now - start);
    while(elapsed.count() < 20000){
        response = recv_from_server(20000-elapsed.count());
        if (response.ticket == ticket){
            return response;
        }
        now = std::chrono::high_resolution_clock::now();
        elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(now - start);
        break;
    }
    return response;
}


void get_auth_token(){
    ClientMessage msg;
    msg.info = "Authorize me please!";
    msg.func_name = "auth";
    auto response = send_and_receive(msg);
    auth_token = response.ret_auth;
}

void starting_setup(std::string last_cmd){
    
    if (!network_initiated) {
        network_initiated = true;
        std::string ip = "127.0.0.1";
        int port = 8080;

        auto address = boost::asio::ip::address::from_string(ip);
        boost::asio::ip::udp::endpoint created_server_endpoint(address, port);
        server_endpoint = created_server_endpoint;
        client_socket.open(boost::asio::ip::udp::v4());
        std::cout << "Setup complete" << std::endl;
    }
    if (auth_token == 0){
        get_auth_token();
    }
}


int nopen(const char *pathname, mode_t mode){
    starting_setup("nopen");
    ClientMessage request;
    request.info = "";
    request.func_name = "open";
    request.pathname = pathname;
    request.mode = mode;
    try {
        auto response = send_and_receive(request);
        std::cout << "Message received in nopen: " << response.toString() << std::endl;
        if (response.error == 1){
            return -1;
        }
        return response.ret_int;
    } catch(int error_code){
        std::cout << error_code << std::endl;
        return -1;
    }
    return 0;
}

ssize_t nread(int fd, void* buf, size_t count){
    starting_setup("nread");
    ClientMessage request;
    request.info = "";
    request.func_name = "read";
    request.fd = fd;
    request.count = count;
    try {
        auto response = send_and_receive(request);
        std::cout << "Message received in nread: " << response.toString() << std::endl;
        if (response.error == 1){
            return -1;
        }
        for(int i = 0; i < response.data.size(); i++){
            ((uint8_t*)buf)[i] = response.data[i];
        }
        return response.data.size();
    } catch(int error_code){
        return -1;
    }
}
ssize_t nwrite(int fd, const void* buf, size_t count){
    starting_setup("nwrite");
    ClientMessage request;
    request.info = "";
    request.func_name = "write";
    request.fd = fd;
    request.count = count;
    for(int i = 0; i < count; i++){
        request.data.push_back(((uint8_t*)buf)[i]);
    }
    try {
        auto response = send_and_receive(request);
        std::cout << "Message received in nwrite: " << response.toString() << std::endl;
        if (response.error == 1){
            return -1;
        }
        return response.ret_long;
    } catch(int error_code){
        return -1;
    }
}
off_t nlseek(int fd, off_t offset, int whence){
    starting_setup("nlseek");
    ClientMessage request;
    request.info = "";
    request.func_name = "lseek";
    request.fd = fd;
    request.offset = offset;
    request.whence = whence;
    try {
        auto response = send_and_receive(request);
        std::cout << "Message received in nlseek: " << response.toString() << std::endl;
        if (response.error == 1){
            return -1;
        }
        return response.ret_long;
    } catch(int error_code){
        return -1;
    }
}
int nchmod(const char *pathname, mode_t mode){
    starting_setup("nchmod");
    ClientMessage request;
    request.info = "";
    request.func_name = "chmod";
    request.pathname = pathname;
    request.mode = mode;
    try {
        auto response = send_and_receive(request);
        std::cout << "Message received in nchmod: " << response.toString() << std::endl;
        if (response.error == 1){
            return -1;
        }
        return response.ret_int;
    } catch(int error_code){
        return -1;
    }
}
int nunlink(const char *pathname){
    starting_setup("nunlink"); 
    ClientMessage request;
    request.info = "";
    request.func_name = "unlink";  
    request.pathname = pathname;
    try {
        auto response = send_and_receive(request);
        std::cout << "Message received in nunlink: " << response.toString() << std::endl;
        if (response.error == 1){
            return -1;
        }
        return response.ret_int;
    } catch(int error_code){
        return -1;
    }
}
int nrename(const char *oldpath, const char *newpath){
    starting_setup("nrename");   
    ClientMessage request;
    request.info = "";
    request.func_name = "rename";
    request.pathname = oldpath;
    request.new_pathname = newpath;
    try {
        auto response = send_and_receive(request);
        std::cout << "Message received in nrename: " << response.toString() << std::endl;
        if (response.error == 1){
            return -1;
        }
        return response.ret_int;
    } catch(int error_code){
        return -1;
    }
}
