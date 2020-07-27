const path = require('path');

const core = require('@actions/core');
const exec = require('@actions/exec');
const io = require('@actions/io');
const tc = require('@actions/tool-cache');

async function installSingularityVersion(versionSpec) {
    let downloadUrl = `https://github.com/hpcng/singularity/releases/download/v${versionSpec}/singularity-${versionSpec}.tar.gz`;
    const archivePath = await tc.downloadTool(downloadUrl, undefined);

    const extractDir = path.join(process.env.GOPATH, 'src', 'github.com', 'hpcng')
    await tc.extractTar(archivePath, extractDir)
    const extPath = path.join(extractDir, 'singularity');
    core.info('Extracting singularity...');
    core.info(`Successfully extracted singularity to ${extPath}`);

    core.info('Configuring');
    exec.exec('./mconfig', { cwd: extPath });
    const buildDir = path.join(extPath, 'builddir');
    core.info('Compiling');
    await io.execSync('make', { cwd: buildDir });

    core.info(`Installing to ${binDir}`);
    const binDir = path.join(extPath, 'bin');
    await io.cp(path.join(buildDir, 'singularity'), binDir);

    core.info('Adding to the cache ...');

    const cachedDir = await tc.cacheDir(
        binDir,
        'singularity',
        versionSpec
    );
    core.info(`Successfully cached singularity to ${cachedDir}`);
    return cachedDir;
}

async function main() {
    const versionSpec = core.getInput('singularity-version');
    core.info(`Setup singularity version spec ${versionSpec}`);
    // TODO check if already installed

    let binDir = tc.find('singularity', versionSpec);
    if (binDir) {
        core.info(`Found in cache @ ${binDir}`);
    } else {
        binDir = await installSingularityVersion(versionSpec);
    }
    core.addPath(binDir);
    core.info('Added singularity to the path');
    core.info(`Successfully setup singularity version ${versionSpec}`);
}

main()
    .then((msg) => {
        console.log(msg);
    })
    .catch((err) => {
        core.setFailed(err.message);
    });
