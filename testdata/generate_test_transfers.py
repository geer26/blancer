import csv
import random
from random import randint
from random import randrange
from datetime import timedelta, datetime



def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    start = datetime(start[0], start[1], start[2], 0, 0, 0)
    end = datetime(end[0], end[1], end[2], 0, 0, 0 )
    
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return (start + timedelta(seconds=random_second))


def generate(r_id = 1, t = 1, amount = [1000, 15000], pocket = 1, category =1):

    r = []
    types = [-1, 1]

    r.append(r_id)
    r.append( random.choice(types) )
    r.append(randrange(amount[0], amount[1]+1))
    r.append(str(random_date( [2015, 2, 3], [2020, 10, 24] )) )
    r.append(pocket)
    r.append(category)
    

    return r


with open('innovators.csv', 'w', newline="") as file:
    writer = csv.writer(file, delimiter=',')
    
    writer.writerow([ "id", "type", "amount", "timestamp",  "pocket",  "category" ])

    for i in range(100):
        writer.writerow(generate())

    file.close()





