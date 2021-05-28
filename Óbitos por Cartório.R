library(googlesheets4)
library(dplyr)
library(googledrive)

drive_auth()
1
temp <- tempfile()
download.file('https://data.brasil.io/dataset/covid19/obito_cartorio.csv.gz', temp)
cartorios <- read.table(temp, sep = ',', quote = '"', header = TRUE)
write.csv(cartorios,"cartorios.csv", row.names = FALSE)
td <- drive_get("https://drive.google.com/drive/u/2/folders/1T9O0Z6fG4TGZF2G3enOqJ5aH3in3HC_R")
drive_put("cartorios.csv", name="cartorios", type="spreadsheet", path = as_id(td))

