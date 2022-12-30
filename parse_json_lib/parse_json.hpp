#ifndef JSON_H
#define JSON_H

#include <map>
#include <memory>
#include <optional>
#include <string>
#include <vector>

namespace json {
enum class JSONValueType { String, Number, Object, Array, Boolean, Null };
struct JSONValue {
  std::optional<std::string> string;
  std::optional<double> number;
  std::optional<bool> boolean;
  std::optional<std::vector<JSONValue>> array;
  std::optional<std::map<std::string, JSONValue>> object;
  JSONValueType type;
};
enum class JSONTokenType { String, Number, Syntax, Boolean, Null };
struct JSONToken {
  std::string value;
  JSONTokenType type;
  int location;
  std::shared_ptr<std::string> full_source;
};

std::tuple<std::vector<JSONToken>, std::string> lex(const std::string&);
std::tuple<JSONValue, int, std::string> parse(std::vector<JSONToken>,
                                              int index = 0);
std::tuple<JSONValue, std::string> parse(const std::string&);
std::string deparse(JSONValue, const std::string& whitespace = "");
} // namespace json

#endif
