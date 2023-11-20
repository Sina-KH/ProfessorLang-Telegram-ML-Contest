//
// Created by Sina on 11/18/23.
//
#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include <regex>
#include <vector>
#include <algorithm>
#include "features.h"

std::string tglang_remove_comments(const std::string &source_code);

std::vector<std::string> tokenize_to_text(const std::string &source_code);

std::vector<int> tglang_tokenize_to_keywords(const std::string &text,
                                             std::size_t keyword_count);

std::vector<float> normalize_to_100(const std::vector<int> &arr);

std::vector<float> tglang_tokenize(const std::string &source_code);

#endif