


points=[]
series.exposure_points=[]
s=1000000
x=-35
y=-16
while y<=5:
	while x<=-7:
		points.append([x*s,y*s])
		x+=7
	y+=7
	x=-35

series.appendCustom(points)
#print series.exposure_points
#series.preview()
series.dosage=[10,11,13,15,17,20,23,26,30,34,40,45,52,60,69,79,90,105,121,139]
print len(series.dosage)
#stage.printSeries(series.exposure_points,series.dosage)

