const SAMPLE_FOR_EACH_LANGUAGE = 15000
const RATES_PERCENT = {
    test: 0,
    valid: 0,
    train: 100 // we will separate in python trainer script
}

const languageExtensions = require('../1.languageExtensions.json')
let languages = languageExtensions.map(it => it.lang)

// file count for each language
let languageFileCount = {}

const fs = require('fs')
const fsPromises = require('fs').promises
const csv = require('csv-parser')
const iconv = require('iconv-lite');
const chardet = require('chardet');

// Function to check if a file is UTF-8 encoded
function detectEncoding(filePath) {
    const content = fs.readFileSync(filePath);
    const detectedEncoding = chardet.detect(content);
    console.log(detectedEncoding)
    return detectedEncoding;
}

// Function to convert a file to UTF-8
function convertToEncoding(filePath, detectedEncoding, targetEncoding) {
    const content = fs.readFileSync(filePath);
    const utf8Content = iconv.decode(content, detectedEncoding); // Convert from the detected encoding to UTF-8

    // Write the converted content back to the file
    fs.writeFileSync(filePath, utf8Content, targetEncoding);
}

function shuffle(array) {
    let currentIndex = array.length, randomIndex;

    while (currentIndex > 0) {

        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;

        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]];
    }

    return array;
}

let rows = []

async function generateSamples() {
    const prefix = "../10.sampleFiles/"
    if (fs.existsSync(`${prefix}train`))
        fs.rmdirSync(`${prefix}train`, {recursive: true})
    if (fs.existsSync(`${prefix}valid`))
        fs.rmdirSync(`${prefix}valid`, {recursive: true})
    if (fs.existsSync(`${prefix}test`))
        fs.rmdirSync(`${prefix}test`, {recursive: true})
    fs.mkdirSync(`${prefix}train`);
    fs.mkdirSync(`${prefix}valid`);
    fs.mkdirSync(`${prefix}test`);
    for (const language of languages) {
        console.log('creating empty dir for ' + language)
        fs.mkdirSync(`${prefix}train/` + language);
        fs.mkdirSync(`${prefix}test/` + language);
        fs.mkdirSync(`${prefix}valid/` + language);
    }
    return new Promise((resolve, reject) => {
        const writableStream = fs.createWriteStream(`${prefix}list.csv`, {flags: 'w'});
        writableStream.write('path,lang,use\n')

        fs.createReadStream('../8.sourceFiles.csv')
            .pipe(csv())
            .on('data', async function (row) {
                rows.push(row)
            })
            .on('end', function () {
                async function doNow() {
                    rows = shuffle(rows)
                    console.log(rows.length + ' files found.')
                    for (const row of rows) {
                        if (!row.language?.length)
                            continue
                        if (!languageFileCount[row.language])
                            languageFileCount[row.language] = 0
                        if (languageFileCount[row.language] >= SAMPLE_FOR_EACH_LANGUAGE)
                            continue
                        languageFileCount[row.language]++

                        let use = 'train'
                        if (languageFileCount[row.language] % 100 < RATES_PERCENT.test)
                            use = 'test'
                        else if (languageFileCount[row.language] % 100 < RATES_PERCENT.test + RATES_PERCENT.valid) {
                            use = 'valid'
                        }

                        try {
                            const sourcePath = '../5.sources/' + row.path
                            const newPath = prefix + use + "/" + row.language + "/" + row.path.replace(/\//g, '___')
                            await fsPromises.copyFile(sourcePath, newPath)

                            const encoding = chardet.detectFileSync(newPath)
                            if (encoding !== 'ISO-8859-1') {
                                // console.log(`Converting ${newPath} from ${encoding} to ISO-8859-1...`);
                                //convertToEncoding(newPath, encoding, 'latin1');
                            } else {
                                //console.log(`${newPath} is already in ISO-8859-1 format. Skipping...`);
                            }

                            writableStream.write(newPath.substring(prefix.length) + ',' + row.language + ',' + use + '\n')
                        } catch (e) {
                            console.log(e)
                            languageFileCount[row.language]--
                        }
                    }
                    console.log(`Data loaded, languages with less than ${SAMPLE_FOR_EACH_LANGUAGE} files:`)
                    console.log(JSON.stringify(
                        languages.filter(it => languageFileCount[it] < SAMPLE_FOR_EACH_LANGUAGE).map(it => {
                            return {
                                lang: it,
                                count: languageFileCount[it]
                            }
                        }))
                    )
                    writableStream.close()
                    resolve()
                }
                doNow()
            })
    })
}

generateSamples().then(() => {
    console.log('DONE')
})

function report() {
    console.log(languageFileCount)
    setTimeout(() => {
        report()
    }, 10000)
}
report()