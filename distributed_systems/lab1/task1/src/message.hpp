#pragma once
#include<string>
#include <cstdint>
#include"json.hpp"
#include <sstream>

using json = nlohmann::json;

struct ClientMessage {
    uint64_t auth;
    uint64_t ticket;
    std::string info;
    std::string func_name;
    std::string pathname;
    mode_t mode;
    int fd;
    size_t count;
    off_t offset;
    int whence;
    std::string new_pathname;
    std::vector<uint8_t> data; 

    ClientMessage() = default;

    std::string toString() const {
        std::ostringstream oss;
        oss << "ClientMessage { "
            << "auth: " << auth << ", "
            << "ticket: " << ticket << ", "
            << "info: \"" << info << "\", "
            << "func_name: \"" << func_name << "\", "
            << "pathname: \"" << pathname << "\", "
            << "mode: " << mode << ", "
            << "fd: " << fd << ", "
            << "count: " << count << ", "
            << "offset: " << offset << ", "
            << "whence: " << whence << ", "
            << "data_size: " << data.size() << ", "
            << "new_pathname: \"" << new_pathname << "\" }";
        return oss.str();
    }
};

struct ServerMessage {
    uint64_t ticket;
    std::string info;
    uint64_t ret_auth;
    int ret_int;
    long ret_long;
    std::vector<uint8_t> data; 
    int error;

    std::string toString() const {
        std::ostringstream oss;
        oss << "ServerMessage { "
            << "ticket: " << ticket << ", "
            << "info: \"" << info << "\", "
            << "ret_auth: " << ret_auth << ", "
            << "ret_int: " << ret_int << ", "
            << "ret_long: " << ret_long << ", "
            << "error: " << error << ", "
            << "data_size: " << data.size() << " }"; 
        return oss.str();
    }
};

void to_json(json& j, const ClientMessage& p);
void from_json(const json& j, ClientMessage& p);
void to_json(json& j, const ServerMessage& p);
void from_json(const json& j, ServerMessage& p);