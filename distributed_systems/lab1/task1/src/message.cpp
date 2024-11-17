#include "message.hpp"

void to_json(json& j, const ClientMessage& p) {
    j = json{
        {"auth", p.auth},
        {"ticket", p.ticket},
        {"info", p.info},
        {"func_name", p.func_name},
        {"pathname", p.pathname},
        {"mode", p.mode},
        {"fd", p.fd},
        {"count", p.count},
        {"offset", p.offset},
        {"whence", p.whence},
        {"data", p.data},
        {"new_pathname", p.new_pathname}
    };
}

void from_json(const json& j, ClientMessage& p) {
    j.at("auth").get_to(p.auth);
    j.at("ticket").get_to(p.ticket);
    j.at("info").get_to(p.info);
    j.at("func_name").get_to(p.func_name);
    j.at("pathname").get_to(p.pathname);
    j.at("mode").get_to(p.mode);
    j.at("fd").get_to(p.fd);
    j.at("count").get_to(p.count);
    j.at("offset").get_to(p.offset);
    j.at("whence").get_to(p.whence);
    j.at("new_pathname").get_to(p.new_pathname);
    j.at("data").get_to(p.data);
}

void to_json(json& j, const ServerMessage& p) {
    j = json{
        {"ticket", p.ticket},
        {"info", p.info},
        {"ret_auth", p.ret_auth},
        {"ret_int", p.ret_int},
        {"ret_long", p.ret_long},
        {"data", p.data},
        {"error", p.error}
    };
}

void from_json(const json& j, ServerMessage& p) {
    j.at("ticket").get_to(p.ticket);
    j.at("info").get_to(p.info);
    j.at("ret_auth").get_to(p.ret_auth);
    j.at("ret_int").get_to(p.ret_int);
    j.at("ret_long").get_to(p.ret_long);
    j.at("data").get_to(p.data);
    j.at("error").get_to(p.error);
}
