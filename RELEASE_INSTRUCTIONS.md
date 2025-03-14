# How to publish a new release

When a sufficient number of changes have been accumulated, a new release
can be made. Which will be accessible [in GitHub's releases page](https://github.com/microbial-pangenomes-lab/microGWAS/releases)

**Note:** `microGWAS` follow's the [semantic versioning](https://semver.org/) convention.

## 1) Run the test dataset to make sure there are no bugs

This is a very important step to avoid releasing a bugged version of the pipeline.

## 2) Add the release version to the repository

In the `main` branch, 
edit the `VERSION` file to indicate the target release version (e.g. `X.X.X`).
Also edit the `docs/source/conf.py` file so that the `release` and `version`
variables are up to date.

Then do `git add VERSION docs/source/conf.py` followed by `git commit -m "Version bump"`,
then by `git push`.

## 3) Make a github release

Apply a tag to identify the release in the git history by doing: `git tag X.X.X`
(where `X.X.X` is the target version), followed by `git push --tags`.

Prepare (in an empty folder) a clean tarball of the new version:

    git clone --recursive --branch X.X.X git@github.com:microbial-pangenomes-lab/microGWAS.git
    cd microGWAS
    mkdir ../temp_archive
    git archive --format=tar --prefix=microGWAS/ X.X.X | tar -xf - -C ../temp_archive
    git submodule foreach --recursive 'git archive --prefix=microGWAS/$path/ HEAD | tar -xf - -C ../../temp_archive'
    tar -czf ../microGWAS.tar.gz -C ../temp_archive .
    rm -rf ../temp_archive
    cd ..
    rm -rf microGWAS

Go to [microGWAS's release page](https://github.com/microbial-pangenomes-lab/microGWAS/releases)
, then click on "tags", click on the tag you just pushed, and finally click on
"Make new release from tag".
Fill the various fields following what has been done for previous releases
(e.g. [this one](https://github.com/microbial-pangenomes-lab/microGWAS/releases/tag/0.1.1)),
and add the `microGWAS.tar.gz` file generated by the previous step, then publish the new release.

## 4) Bump microGWAS's repository

On `microGWAS`'s `main` branch, edit the `VERSION` file so that it's clear the next version
is a draft (e.g. if latest release is `1.5.0` you could do `1.5.1-dev`), followed by
`git add VERSION`, `git commit -m "Development bump"` and `git push`.
