#!/usr/bin/env Rscript

Sys.setenv(TAR = "/bin/tar")

if(!require("siftr", character.only = TRUE)){
  suppressPackageStartupMessages(library("devtools"))
  install_github("omarwagih/siftr")
}
