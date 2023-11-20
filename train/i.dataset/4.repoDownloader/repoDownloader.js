const fs = require('fs');
const csv = require('csv-parser');
const simpleGit = require('simple-git');

function shuffle(array) {
    let currentIndex = array.length,  randomIndex;

    // While there remain elements to shuffle.
    while (currentIndex > 0) {

        // Pick a remaining element.
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;

        // And swap it with the current element.
        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]];
    }

    return array;
}

// Read repositories from the CSV file
function readRepositoriesFromCSV(filePath) {
    return new Promise((resolve, reject) => {
        const repositories = [];
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (row) => {
                repositories.push(row);
            })
            .on('end', () => {
                resolve(repositories);
            })
            .on('error', (error) => {
                reject(error);
            });
    });
}

let repositories = []
let concurrents = 16
let doneCount = 0

async function downloadRepo(index) {
    if (index >= repositories.length) {
        console.log('finished one of parallels')
        return
    }
    const repo = repositories[index]
    try {
        const repoUrl = 'https://github.com/' + repo['repo'];
        const language = repo['lang'];

        if (!fs.existsSync(`../5.sources/${language}`)) {
            fs.mkdirSync(`../5.sources/${language}`, {recursive: true});
        }
        const targetDir = `../5.sources/${language}/${repoUrl.split('/').pop().replace('.git', '')}`

        if (fs.existsSync(targetDir)) {
            console.log(`${repoUrl} already cloned.`)
        } else {
            // Clone the repository
            let tm = new Date().getTime()
            await simpleGit().clone(repoUrl, {'--depth': 1, '--filter': 'blob:none'});
            let sec = (new Date().getTime() - tm) / 1000

            // Move the cloned repository to the corresponding language directory
            fs.renameSync(`./${repoUrl.split('/').pop().replace('.git', '')}`, targetDir);

            console.log(`${++doneCount}/${repositories.length}  | Cloned ${repoUrl} and moved to ${language} directory successfully (${sec} seconds)`);
        }
    } catch (error) {
        console.error(`Error cloning repository: ${error}`);
    }
    downloadRepo(index + concurrents)
}

// Clone repositories based on the CSV data
async function cloneRepositories() {
    console.log('Started on ' + new Date().toLocaleString() + ' using ' + concurrents + ' parallel downloads.')
    repositories = shuffle(await readRepositoriesFromCSV('../3.repositories.csv'))
    newRepositories = []

    for (const repo of repositories) {
        const repoUrl = 'https://github.com/' + repo['repo'];
        const language = repo['lang'];
        const targetDir = `../5.sources/${language}/${repoUrl.split('/').pop().replace('.git', '')}`
        if (fs.existsSync(targetDir)) {
            doneCount++
            console.log(`${repoUrl} already cloned.`)
        } else {
            newRepositories.push(repo)
        }
    }
    console.log(`${newRepositories.length} repositories left! (total: ${repositories.length})`)
    repositories = newRepositories
    doneCount = 0
    for (let i = 0; i < concurrents; i++) {
        downloadRepo(i)
    }
}

cloneRepositories().then()
