FROM ubuntu

RUN apt-get update && apt-get install -y r-base r-cran-ggplot2 libcurl4-openssl-dev groff python-pip

RUN Rscript -e 'r <- getOption("repos"); r["CRAN"] <- "http://cran.cnr.berkeley.edu/"; options(repos = r); install.packages(c("curl", "jsonlite", "ggplot2", "scales"))'

RUN pip install python-nest phant awscli

COPY . /thermostat

CMD while true; do echo "`date`: Running update.sh"; cd /thermostat; ./update.sh; sleep 300; done
