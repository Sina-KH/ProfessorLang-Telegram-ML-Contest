//
// Created by Sina on 11/18/23.
//

#include "utils.h"

std::string tglang_remove_comments(const std::string &source_code) {
    // Remove single-line comments
    std::string code_without_comments = std::regex_replace(source_code, std::regex("//.*"), "");

    // Remove multi-line comments
    code_without_comments = std::regex_replace(code_without_comments, std::regex("/\\*(.*?)\\*/"), "");

    // Remove single-line comments
    code_without_comments = std::regex_replace(code_without_comments, std::regex("#.*"), "");

    // Remove multi-line comments using triple-quoted strings
    code_without_comments = std::regex_replace(code_without_comments, std::regex("'''(.*?)'''"), "");
    code_without_comments = std::regex_replace(code_without_comments, std::regex("\"\"\"(.*?)\"\"\""), "");

    code_without_comments = std::regex_replace(code_without_comments, std::regex("\"[^\"]*\""), "\"\"");
    code_without_comments = std::regex_replace(code_without_comments, std::regex("'[^']*'"), "''");

    //std::cout << "CODE:\n" << code_without_comments << "\n";

    return code_without_comments;
}

std::vector<std::string> tokenize_to_text(const std::string &source_code) {
    // Define a regular expression pattern to match words and symbols
    std::regex pattern("\\b\\w+\\b|[^\\w\\s]");

    // Use std::sregex_token_iterator to find all matches of the pattern in the source code
    std::sregex_token_iterator iterator(source_code.begin(), source_code.end(), pattern);
    std::sregex_token_iterator end;

    // Store the tokens in a vector
    std::vector<std::string> tokens(iterator, end);

    /*std::cout << "Tokens:\n";
    for (const std::string &token: tokens) {
        std::cout << token << "\n";
    }*/

    return tokens;
}

std::vector<int> tglang_tokenize_to_keywords(const std::string &text,
                                             std::size_t keyword_count) {
    std::vector<std::string> text_tokens = tokenize_to_text(text);

    // Replace keywords in the text
    std::vector<int> indexes;
    //std::vector<std::string> debug;
    for (const auto &token: text_tokens) {
        auto keyword_iter = std::find(ready_keywords, ready_keywords + keyword_count, token);
        if (keyword_iter != ready_keywords + keyword_count) {
            if (!indexes.empty()) {
                int last_item = indexes.back();
                if (last_item != std::distance(ready_keywords, keyword_iter) + 1) {
                    indexes.push_back(std::distance(ready_keywords, keyword_iter) + 1);
                    //debug.push_back(token);
                }
            } else {
                indexes.push_back(std::distance(ready_keywords, keyword_iter) + 1);
                //debug.push_back(token);
            }
        }

        if (indexes.size() == 200) {
            break;
        }
    }

    /*std::cout << "Indexes:\n";
    for (const int &index: indexes) {
        std::cout << index << "\n";
    }*/

    return indexes;
}

std::vector<float> normalize_to_100(const std::vector<int> &arr) {
    // Calculate the sum of the array
    int total = 0;
    for (int element: arr) {
        total += element;
    }
    if (total == 0)
        total = 1;

    // Normalize each element
    std::vector<float> normalized_arr;
    for (int element: arr) {
        normalized_arr.push_back(static_cast<float>(element) / total * 100);
    }

    return normalized_arr;
}

std::vector<float> tglang_tokenize(const std::string &source_code) {
    std::string code_without_comments = tglang_remove_comments(source_code);
    std::vector<int> tokens = tglang_tokenize_to_keywords(code_without_comments, TGLANG_FEATURE_COUNT);

    std::vector<int> x_data(TGLANG_FEATURE_COUNT, 0.0);
    // Assuming tokenized_to_keywords function is defined appropriately
    for (auto i : tokens) {
        x_data[i] = x_data[i] + 1;
    }
    return normalize_to_100(x_data);
}
