#!/usr/bin/env Rscript

Sys.setenv(TAR = "/bin/tar")

Sys.unsetenv("GITHUB_PAT")

if(!require("siftr", character.only = TRUE)){
  suppressPackageStartupMessages(library("devtools"))
  install_github("omarwagih/siftr")
}
