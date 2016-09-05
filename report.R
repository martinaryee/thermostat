#install.packages(c("foreach", "jsonlite", "ggplot2", "scales"))
library(foreach)
library(jsonlite)
library(ggplot2)
library(scales)

jsons <- list(temp = c("sparkfun/keys_0lg42LbMzwCy953NOxJn.json",
                       "sparkfun/keys_8djvJjbo2ESL5wm2p6yY.json",
                       "sparkfun/keys_AJ57EDv0W8t1lMjKLJE5.json",
                       "sparkfun/keys_v0b32LwOJ3fEZKOQ25pw.json"),
              humidity = c("sparkfun/keys_AJ5KnxyZJ1InXpdJdjV3.json",
                           "sparkfun/keys_jqyJ09QJvYtvVgKGWMW9.json"),
              nest_mode = c("sparkfun/keys_q5wNxKdgvbuxrXlo4pAd.json"))

temp_df <- foreach(json = jsons[["temp"]], .combine="rbind") %do% {
  conf = fromJSON(json)
    message(conf$title, " - ", json)
    x = fromJSON(paste0("http://data.sparkfun.com/output/", conf$publicKey, ".json"))
  data.frame(title=conf$title, value=x[,1], time=x[,2], stringsAsFactors = FALSE)
}
temp_df$time <- strptime(temp_df$time, "%Y-%m-%dT%H:%M:%OS", tz="UTC")
temp_df$value <- as.numeric(temp_df$value)
temp_df$value_f <- temp_df$value * 9/5 + 32
date_fmt <- "%a %I%p"

temp_df <- subset(temp_df, time > "2016-08-09")
svg("temperature.svg", width=10, height=6)
ggplot(temp_df, aes(time, value_f, color=title)) + geom_line() + scale_x_datetime(labels = date_format(date_fmt, tz = "America/New_York"), date_breaks="1 day") + xlab("Time") + scale_y_continuous(breaks = seq(-100,100,1)) + ylab("Temperature (F)") + theme_bw()
dev.off()
