## 🤓 ProfessorLang!

`ProfessorLang` is my new solution to detect languages, in `Telegram-ML-Contest` ROUND II.

My previous solution was not good enough, so I decided to implement a new solution from the ground up, to be fast and accurate enough.

🔥 It's now super-fast (response in a few mili-seconds) and up to 99% accurate based on the language.

---

### Steps

- I. Prepare dataset
- II. Pre-process the sample data
- III. Tokenize
- IV. Detect important features
- V. ReTokenize based on important features
- VI. Train the model
- VII. Make it a `.so` library
- ENJOY!

---

### i.Dataset

To prepare dataset, I've used GitHub public repositories.

Also, to detect normal chats (containing no codes), I've used:

All the steps to prepare dataset can be found in i.dataset directory:

The file `i.languageExtensions.csv` is the list of languages and their related extensions.

`2.repositoryFinder` mini-project is used to find repositories for each language. To use it, put a GitHub token is the js file and specify the number of pages you want the crawler, crawl from git for each language.

`3.repositories.csv` is the output of running the previous js script.

`4.repoDownloader` mini-project downloads the source codes into `5.sources` directory. This directory will be processed in next steps.

⚠️ After this step, rename `CPP` to `CPLUSPLUS` and `OBJC` to `OBJECTIVE_C` in sources directory.

`5.sources` are the source-codes created from previous downloader script.

`6.additionalSources` are the source files should be copied into `5.sources` to support all languages.

`7.listSources` lists the source codes and their related language.

`8.sourceFiles.csv` is the output of `7.listSources` script.

`9.samplesGenerator` creates `10.sampleFiles` to be used in the trainer! For now we use this script to create train and valid directories seaparately with different configs in .js file. and finally move valid files into `v.test` directory of the project to validate final outputs.

`11.keywords` contains keywords dictionary for languages to be used in our tokenizer during the training phase. We create a words keyword to merge using keywordExtractor.py.

### ii.dataset_other_code

I've stored all the non-source-code files here and finally after processing, copied them to source codes in the project as OTHER dir. (i.dataset/sources/OTHER/*.txt)

### iii.Trainer

`1.preprocess` creates a merged version of keywords sorted by length to preprocess all the sample codes and tokenize them. Then tokenizes all the sample source codes.

`2.preprocessedData` is the directory containing these preprocessed data.

⚠️ ***Please make sure you empty prev directory on re-creating this directory!***

`3.importantFeatures` is used to determine what features are more important.

`4.importantFeatures` is the output of script 3. We can optionally edit and only save most important ones with score more than 0 from script #3 outputs. (I did that)

`5.reprocessor` is used to tokenize source code based on important features. ALSO It considers other tokens as token `0` to determine non-source codes better.

`6.reprocessedData` is the output of previous script.

⚠️ ***Please make sure you empty prev directory on re-creating this directory!***

`7.train` is the trainer using `6.reproccessedData`. It finally creates a `RandomForestRegressor.h` file to be used in our cpp project.

You should add `#include <stdint.h>` top of the `RandomForestRegressor.h` file.

### iv.tglib

Just copy `RandomForestRegressor.h` here and replace features in `features.cpp` file with `FINAL_KEYWORDS.json` result. Then:

```
mkdir build
cd build
cmake ..
cmake --build .
```

### v.test

To test the project, you should **put .so file here**, and just follow these instructions:

```
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```

To test the library output, launch the resulting binary file tglang-tester with the following parameters:

`tglang-tester <input_file>`