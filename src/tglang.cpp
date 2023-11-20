#include "tglang.h"
#include "RandomForestRegressor.h"
#include <iostream>
#include "utils.h"

enum TglangLanguage tglang_detect_programming_language(const char *text) {
    std::vector<float> tokenizedData = tglang_tokenize(text);
    float X[TGLANG_FEATURE_COUNT];
    std::copy(tokenizedData.begin(), tokenizedData.end(), X);

    Eloquent::ML::Port::RandomForest regressor;
    int result = regressor.predict(X);

    switch (result) {
        case 0: return TGLANG_LANGUAGE_OTHER;
        case 1: return TGLANG_LANGUAGE_C;
        case 2: return TGLANG_LANGUAGE_CPLUSPLUS;
        case 3: return TGLANG_LANGUAGE_CSHARP;
        case 4: return TGLANG_LANGUAGE_CSS;
        case 5: return TGLANG_LANGUAGE_DART;
        case 6: return TGLANG_LANGUAGE_DOCKER;
        case 7: return TGLANG_LANGUAGE_FUNC;
        case 8: return TGLANG_LANGUAGE_GO;
        case 9: return TGLANG_LANGUAGE_HTML;
        case 10: return TGLANG_LANGUAGE_JAVA;
        case 11: return TGLANG_LANGUAGE_JAVASCRIPT;
        case 12: return TGLANG_LANGUAGE_JSON;
        case 13: return TGLANG_LANGUAGE_KOTLIN;
        case 14: return TGLANG_LANGUAGE_LUA;
        case 15: return TGLANG_LANGUAGE_NGINX;
        case 16: return TGLANG_LANGUAGE_OBJECTIVE_C;
        case 17: return TGLANG_LANGUAGE_PHP;
        case 18: return TGLANG_LANGUAGE_POWERSHELL;
        case 19: return TGLANG_LANGUAGE_PYTHON;
        case 20: return TGLANG_LANGUAGE_RUBY;
        case 21: return TGLANG_LANGUAGE_RUST;
        case 22: return TGLANG_LANGUAGE_SHELL;
        case 23: return TGLANG_LANGUAGE_SOLIDITY;
        case 24: return TGLANG_LANGUAGE_SQL;
        case 25: return TGLANG_LANGUAGE_SWIFT;
        case 26: return TGLANG_LANGUAGE_TL;
        case 27: return TGLANG_LANGUAGE_TYPESCRIPT;
        case 28: return TGLANG_LANGUAGE_XML;
        default:
            return TGLANG_LANGUAGE_OTHER;
    }
}
