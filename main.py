import matplotlib.pyplot as plt

# Predefined variables used in the functions, modifiable
fireDelay = 0.7 #delay between weapon fires (in seconds)
reloadTime = 0.5 #time per reload (in seconds)
damagePerShot = 56000 #damage per shot
magCap = 7 #shots per magazine
ammoReserve = 20 #total reserve ammo
shotsFired = 0
nextFire = fireDelay
totalDamage = 0
dataPoints = 4500 #pls make datapoints and xScale in multiples of 10
xScale = 45 #scale of the X axis
yScale = 300000 #scale of the Y axis
xIncrements = xScale/dataPoints
timeElapsed = 0
shotsFiredTotal = 0

#graph limits
plt.xlim(0, xScale)
plt.ylim(0, 150000)

x = [] #establish x array
for i in range(dataPoints): #fills the x axis with standard units based on increments
  x.append(round(i*xIncrements, 5))

tDMG = [] #establish tDMG array and fill it
for i in range(dataPoints):
  if(shotsFiredTotal == ammoReserve): #checking for whether the entire reserve is emptied
      totalDamage = totalDamage
  else: #if reserve is not emptied, continues to check for next shot
    if (shotsFired == magCap): #checking for reload
      nextFire += reloadTime
      shotsFired = 0
    elif timeElapsed == nextFire: #checking whether or not it is time to fire
      totalDamage += damagePerShot
      nextFire += fireDelay
      nextFire = round(nextFire, 5)
      shotsFired += 1
      shotsFiredTotal += 1
    else: #if neither a reload or shot fires, keep value as is
      totalDamage = totalDamage
  timeElapsed += xIncrements
  timeElapsed = round(timeElapsed, 8) #this round CHANGES the graph so careful with it
  tDMG.append(totalDamage)
  
dps = [0]
for z in range(dataPoints):
  if not z==0:
    dps.append(tDMG[z]/x[z])

# Plot x axis, dps point on Y
plt.plot(x,dps)
# Add a legend and labels
plt.legend(['dps'])
plt.xlabel('x')
plt.ylabel('value')

# Show the plot
plt.show()
