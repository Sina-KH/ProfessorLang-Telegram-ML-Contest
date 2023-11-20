const axios = require('axios');
const { writeFile } = require('fs/promises');

const NUMBER_OF_PAGES_FOR_EACH_LANG = 100
const GITHUB_TOKEN = 'GITHUB_TOKEN_HERE'

let languages = [
    'CPP',
    'CPP', // 'CPLUSPLUS'
    'CSHARP',
    'CSS',
    'DART',
    //'DOCKER', // not a github language, requires manual insertion in additional sources (and repositories may contain its files, also)
    //'FUNC',   // not a github language, requires manual insertion in additional sources
    'GO',
    'HTML',
    'JAVA',
    'JAVASCRIPT',
    'JSON',
    'KOTLIN',
    'LUA',
    'NGINX',
    'OBJC', // 'OBJECTIVE_C'
    'PHP',
    'POWERSHELL',
    'PYTHON',
    'RUBY',
    'RUST',
    'SHELL',
    'SOLIDITY',
    'SQL',
    'SWIFT',
    //'TL',     // not a github language, requires manual insertion in additional sources
    'TYPESCRIPT',
    'XML',
]

let foundRepositories = []

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function loadPage(lang, i) {
    try {
        await sleep(500) // to prevent rate limit issue
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: 'https://api.github.com/search/repositories?q=language:' + lang + '&sort=stars&order=desc&page=' + i,
            headers: {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'Bearer ' + GITHUB_TOKEN
            }
        };
        const response = await axios.request(config)
        const data = response.data
        for (const item of data.items) {
            if (foundRepositories.findIndex((it) => {
                return it.full_name === item.full_name
            }) < 0)
                foundRepositories.push({
                    full_name: item.full_name,
                    lang: lang
                })
        }
        console.log('Lang: ' + lang + ', Page: ' + i)
        if (data.items.length < 1)
            return true
    } catch (e) {
        if (e.response?.status === 403) {
            console.log('failed with 403, lets wait...')
            await sleep(5000)
            return loadPage(lang, i)
        }
        console.log(e)
        return true
    }
    return false
}

async function loadRepos() {
    for (const lang of languages) {
        for (let i = 1; i <= NUMBER_OF_PAGES_FOR_EACH_LANG; i++) {
            const finished = await loadPage(lang, i)
            if (finished)
                break
        }
    }
    try {
        await writeResultFile()
        console.log('DONE!')
    } catch (e) {
    }
}

async function writeResultFile() {
    try {
        const fileName = '../3.repositories.csv'
        await writeFile(fileName, foundRepositories.reduce((prev, cur) => {
            return prev + cur.full_name + ',' + cur.lang + '\n'
        }, 'repo,lang\n'));
        console.log(`Wrote data to ${fileName}`);
    } catch (error) {
        console.error(`Got an error trying to write the file: ${error.message}`);
        throw error
    }
}

loadRepos().then()