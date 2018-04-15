import data
import math
import MySQLdb
import random

# Set up database connection
connection = MySQLdb.connect (host = "localhost",
                              user = "pybull",
                              passwd = "theword",
                              db = "parts")

cursor = connection.cursor()
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone()
print("server version:", row[0])
cursor.close()
connection.close()

data = data.loadData()
print(data)

# Time to run simulation
daysInYear = 360
years = float(input("How many years to simulate?: "))
T = daysInYear * years

# List of available items (internal ID)
itemsAvailable = [100, 101, 102, 103]

# Expected life for each item
expectedLife = [10, 3, 6, 4]

# Number of items in use
noInUse = [1, 1, 2, 1]

# Time since last change
timeSince = [1, 1, 1, 1]

# Start inventory
startInventory = [1, 1, 1, 1]

# Dictionaries
itemLife = dict(zip(itemsAvailable, expectedLife))
itemClock = dict(zip(itemsAvailable, timeSince))
itemInventory = dict(zip(itemsAvailable, startInventory))

# Function to calculate conditional probability of defective item
# Using Weibull distribution with shape parameter 5
def weibull(item, time):
	alpha = itemLife.get(item) * 360 # the scale parameter (in this case equal to expected life) (in days)
	beta = 5 # the shape parameter
	pdf = beta/alpha * (time/alpha) ** (beta - 1) * math.exp(-time/730) # probability density function
	cdf = 1 - math.exp(-(time/alpha) ** beta) # cumulative probability
	prob = pdf / (1-cdf)
	return(prob) # return the conditional probabilty of defective item

# Function to 
def defective(prob):
	return random.random() < prob

# Start simulation
t = 1

while t <= T:
	for item in itemsAvailable:
		timeIn = itemClock.get(item)
		probability = weibull(item, timeIn)
		isDefective = defective(probability)
		if isDefective:
			# Check inventory
			# If in inventory, change item, reset clock for that item
			# If not in inventory, make order, wait, change item
			print("Item " + str(item) + " is defective.")
			if itemInventory.get(item) > 0:
				itemInventory[item] -= 1
				itemClock[item] = 0
	itemClock[item] += 1
	t += 1
