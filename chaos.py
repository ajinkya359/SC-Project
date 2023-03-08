import math
from fuzzywuzzy import fuzz
import random
import string
from difflib import *

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class Agent:

    def __init__(self, length):

        self.params = [random.uniform(1,4),random.uniform(0.1,4)] #(a,d) 
        self.fitness = -1

    def __str__(self):

        return 'Params: ' + str(self.params) + ' Fitness: ' + str(self.fitness)

def init_agents(population, length):
    return [Agent(length) for _ in range(population)]

def ga():

    agents = init_agents(population, in_str_len)

    for generation in range(generations):

        print('Generation: ' + str(generation))

        temp_fitness = []
        
        #calculate the fitness of all agents.
        agents = fitness(agents)

        for agent in agents:
            #storing the correct fitness
            temp_fitness.append(agent.fitness)

        # print(temp_fitness)

        current_max_fitness = max(temp_fitness)
        
        #count the number of agents with max fitness.
        count = temp_fitness.count(current_max_fitness)

        
        print('Current_max_fitness',current_max_fitness)
        print('Count: ',count)

        #if more than 50% of the population has the max fitness which is above the threshold then stop the procedure or 
        #else repeat .
        if count/len(agents) >= 0.5 and current_max_fitness >= 90:
            print('Bazinga!')
            break

        agents = rank_selection(agents)
        agents = crossover(agents)
        agents = mutation(agents)
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    return agents[0]



def ani_jackard(s1,s2):
    str1 = [ord(i) for i in s1]
    str2 = [ord(i) for i in s2]

    str1 = set(str1)
    str2 = set(str2)

    score = (str1 & str2)
    score_u = str1|str2

    return 100-(len(score)/len(score_u))*100


def fitness(agents):
    print("a=",agents[0])
    for agent in agents:

        a = agent.params[0]
        d = agent.params[1]
        
        #every agent has Params: [1.4282256077720765, 3.487416630353859] Fitness: 99.84939759036145
        cipher = encrypt(plaintext,a,d)

        # agent.fitness = 100-fuzz.ratio(plaintext,cipher)
        agent.fitness = ani_jackard(plaintext,cipher)

    return agents

#TODO: I need to make the ranking based selection, 

def rank_selection(agents,selection_pressure=1.5):
    #s=[1,2]
    s=selection_pressure
    current_rank=0
    agents = sorted(agents, key=lambda agent: agent.fitness)
    print('\n'.join(map(str, agents)))
    print("-------------")
    ranks=[]
    ranks.append(current_rank)
    for i in range(1,len(agents)):
        if(agents[i-1].fitness<agents[i].fitness):
            current_rank+=1
        ranks.append(current_rank)
    prob=[]

    n=len(agents)

    # print('\n'.join(map(str, ranks)))
    # print("----------")
    
    for rank in ranks:
        temp=((2-selection_pressure)/n)+(2*rank*(selection_pressure-1))/(n*(n-1))
        prob.append(temp)
    for i in range(1,n):
        prob[i]=prob[i-1]+prob[i]

    # print('\n'.join(map(str, prob)))
    # print("---------------")
    
    next_gen_size=int(0.2*(n))
    
    next_gen=[]
    for i in range(0,next_gen_size):
        r=random.uniform(0,1)
        k=0
        for j in range(n):
            if(prob[j]<r):
                k+=1
        if(k>=n):
            k=n-1
        next_gen.append(agents[k])
    
    print('\n'.join(map(str, next_gen)))
    print("-----------------")
    return next_gen

def selection(agents):
    #we are getting the individuals with best fitness, can be multiple of them here. We are getting the 
    #ones with the best fitness.
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    print('\n'.join(map(str, agents)))
    #leading the the decrease in the diversity.
    agents = agents[:int(0.2 * len(agents))]
    print("------------")
    print('\n'.join(map(str, agents)))
    return agents

def crossover(agents):

    offspring = []

    for _ in range((population - len(agents)) // 2):

        parent1 = random.choice(agents)
        parent2 = random.choice(agents)
        child1 = Agent(2)
        child2 = Agent(2)
        # split = random.randint(0, in_str_len)
        child1.params = [parent1.params[0],parent2.params[1]]
        child2.params = [parent2.params[0],parent1.params[1]]

        offspring.append(child1)
        offspring.append(child2)

    agents.extend(offspring)

    return agents

def mutation(agents):
        
    for agent in agents:

        step_a = random.uniform(-0.2,0.2)
        step_d = random.uniform(-0.2,0.2)
        
        if random.uniform(0.0, 1.0) <= 0.1:

            agent.params[0] += step_a
            agent.params[1] += step_d

    return agents

def chaotic_map(n,x_0,y_0,a,d):
    # d = 0.3
    # a = 2.5 
    x=[]
    x.append(x_0)
    y = []
    y.append(y_0)

    for i in range(n-1):
        x.append((x[i]+d+(a*math.sin(2*math.pi*y[i])))%1)
        y.append(1 - a*pow(x[i],2) + y[i])

    return (x,y)

def float_to_shuffled_ints(x,y):
    x_sorted = sorted(x, reverse=True)
    y_sorted = sorted(y, reverse=True)

    shuffled_x = []
    for x_val in x:
        if x_val in x_sorted:
            i = x_sorted.index(x_val)
            shuffled_x.append(i)

    shuffled_y = []
    for y_val in y:
        if y_val in y_sorted:
            i = y_sorted.index(y_val)
            shuffled_y.append(i)


    # print('shuffled_x = ',shuffled_x)
    # print('shuffled_y = ',shuffled_y)

    key = []
    for i in shuffled_x:
        key.append(shuffled_y[i])

    return key



def encrypt(plaintext,a,d):
    ascii_lst = [ord(i) for i in plaintext]
    n = len(ascii_lst)

    ascii_avg = sum(ascii_lst)/n

    x_0 = ascii_avg/max(ascii_lst)
    y_0 = 0.2
    (x,y) = chaotic_map(n,x_0,y_0,a,d)

    private_key = float_to_shuffled_ints(x,y)
    # print('Private Key = ',private_key)

    ciphertext = []
    for i in range(len(ascii_lst)):
        ciphertext.append(chr(ascii_lst[i]+private_key[i]))

    # print('CipherText = ',ciphertext)
    return ''.join(ciphertext)

in_str = None
in_str_len = None
population = 20
generations = 100000

# plaintext = input('Enter Message: ')
plaintext = 'abcdefghij'*100
best_found=ga()
print(encrypt(plaintext,best_found.params[0],best_found.params[1]))