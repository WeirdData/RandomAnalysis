# Copyright (c) 2020
# Author: Rohit Suratekar
#
# Lyrics Analaysis

suppressPackageStartupMessages(library(circlize))
data <- read.csv("/mnt/windows/Enigma/Rohit/PythonProjects/RandomAnalysis/r_df.csv")

horizontal = c("Alka Yagnik")

isHorizontal <- function(name){
  if (is.element(name, horizontal)){
    return("bending.inside")
  }else{
    return("clockwise")
  }
}

circos.clear()
circos.par(gap.after = 5)
chordDiagram(data, annotationTrack = "grid", 
             preAllocateTracks = 1, 
             annotationTrackHeight = mm_h(2))
circos.trackPlotRegion(track.index = 1, panel.fun = function(x, y) {
  xlim = get.cell.meta.data("xlim")
  ylim = get.cell.meta.data("ylim")
  sector.name = get.cell.meta.data("sector.index")
  circos.text(mean(xlim), 0.5, sector.name, 
              facing = "clockwise", 
              niceFacing = TRUE, 
              adj = c(0, 0.5))
  circos.axis(h = "top", labels.cex = 0.5, sector.index = sector.name, track.index = 2)
}, bg.border = NA)
