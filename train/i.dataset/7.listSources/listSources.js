const fs = require('fs');
const path = require('path');
const glob = require('fast-glob');
const through2 = require('through2')

const languageExtensions = require('../1.languageExtensions.json')

let languages = []
let extensionsToLanguageMap = {}
let filenamesToLanguageMap = {}
let allowedOtherDirForLanguages = ['NGINX', 'DOCKER', 'SQL', 'CSS']

async function readLanguages() {
    try {
        // Read the entire file
        languages = languageExtensions.map(it => it.lang)
        for (const lang of languageExtensions) {
            for (const ext of lang.extensions || []) {
                if (!extensionsToLanguageMap[ext])
                    extensionsToLanguageMap[ext] = [lang.lang]
                else
                    extensionsToLanguageMap[ext].push(lang.lang)
            }
            for (const filename of lang.filenames || []) {
                if (!filenamesToLanguageMap[filename])
                    filenamesToLanguageMap[filename] = [lang.lang]
                else
                    filenamesToLanguageMap[filename].push(lang.lang)
            }
        }
        console.log(extensionsToLanguageMap)
        console.log(filenamesToLanguageMap)
    } catch (error) {
        console.error('Error reading the file:', error);
        throw error;
    }
}

// helper to get a file extension
function getFileExtension(filePath) {
    return path.extname(filePath).toLowerCase();
}

const filesBasedOnLanguage = {}

function processLanguageFiles(language, finalWritableStream) {
    return new Promise((resolve, reject) => {
        finalWritableStream.write(`path,extension,language\n`)

        const prefix = '../5.sources/'
        const fileStream = glob.stream(`${prefix}${language}/**/*`, { onlyFiles: true, followSymbolicLinks: false });

        fileStream.pipe(through2.obj((filePath, enc, next) => {
            // Process each file here
            // You can perform operations on the file without loading all files into memory
            if (filePath.indexOf('minif') > -1) {
                // ignore minified files
                next()
                return
            }
            let ext = getFileExtension(filePath)
            if (!ext) {
                next()
                return
            }
            ext = ext.substring(1)
            let relatedLanguages = extensionsToLanguageMap[ext]
            if (!relatedLanguages?.length)
                relatedLanguages = filenamesToLanguageMap[path.basename(filePath)]
            if (!relatedLanguages?.length) {
                next()
                return
            }
            let relatedLanguage = null
            if (relatedLanguages.length > 1) {
                relatedLanguage = relatedLanguages.filter(it => it.toLowerCase() === language.toLowerCase())
            } else {
                relatedLanguage = relatedLanguages[0]
            }
            if (!relatedLanguage) {
                next()
                return
            }
            if (relatedLanguage !== language && allowedOtherDirForLanguages .indexOf(language) < 0) {
                // get text files as other only in other folder!
                next()
                return
            }
            if (!filesBasedOnLanguage[relatedLanguage])
                filesBasedOnLanguage[relatedLanguage] = 0
            filesBasedOnLanguage[relatedLanguage]++
            finalWritableStream.write(`${filePath.substring(prefix.length)},${ext},${relatedLanguage}\n`)

            // Call the callback to indicate that processing for this file is complete
            next();
        }))

        fileStream.on('error', err => {
            reject(err);
        });

        fileStream.on('end', () => {
            fileStream.end();
        });

        fileStream.on('finish', () => {
            resolve();
        });
    })
}

async function listSources() {
    // open stream to write
    const writableStream = fs.createWriteStream("../8.sourceFiles.csv", { flags: 'w' });

    // read languages
    await readLanguages()
    for (const language of languages) {

        // extract files
        console.log('Working on ' + language + ' directory')

        // process language
        await processLanguageFiles(language, writableStream)
    }

    writableStream.end();

    for (const lang of languages) {
        console.log(`${filesBasedOnLanguage[lang]} files found for ${lang} language.`)
    }
}

listSources().then()