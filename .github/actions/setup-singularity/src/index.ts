import path from 'path';

import {info, getInput, addPath, setFailed } from '@actions/core';
import exec from '@actions/exec';
import io from '@actions/io';
import tc from '@actions/tool-cache';

async function installSingularityVersion(versionSpec) {
    let downloadUrl = `https://github.com/hpcng/singularity/releases/download/v${versionSpec}/singularity-${versionSpec}.tar.gz`;
    const archivePath = await tc.downloadTool(downloadUrl, undefined);

    const extractDir = path.join(process.env.GOPATH, 'src', 'github.com', 'hpcng')
    await tc.extractTar(archivePath, extractDir)
    const extPath = path.join(extractDir, 'singularity');
    info('Extracting singularity...');
    info(`Successfully extracted singularity to ${extPath}`);

    info('Configuring');
    await exec.exec('./mconfig', [], { cwd: extPath });
    const buildDir = path.join(extPath, 'builddir');
    info('Compiling');
    await exec.exec('make', [], { cwd: buildDir });

    const binDir = path.join(extPath, 'bin');
    info(`Installing to ${binDir}`);
    await io.cp(path.join(buildDir, 'singularity'), binDir);

    info('Adding to the cache ...');

    const cachedDir = await tc.cacheDir(
        binDir,
        'singularity',
        versionSpec
    );
    info(`Successfully cached singularity to ${cachedDir}`);
    return cachedDir;
}

async function main() {
    const versionSpec = getInput('singularity-version');
    info(`Setup singularity version spec ${versionSpec}`);
    // TODO check if already installed

    let binDir = tc.find('singularity', versionSpec);
    if (binDir) {
        info(`Found in cache @ ${binDir}`);
    } else {
        binDir = await installSingularityVersion(versionSpec);
    }
    addPath(binDir);
    info('Added singularity to the path');
    info(`Successfully setup singularity version ${versionSpec}`);
}

main()
    .then((msg) => {
        console.log(msg);
    })
    .catch((err) => {
        setFailed(err.message);
    });
