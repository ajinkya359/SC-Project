import random,math
import matplotlib.pyplot as plt

def ani_jackard(s1, s2):
    str1 = [ord(i) for i in s1]
    str2 = [ord(i) for i in s2]

    str1 = set(str1)
    str2 = set(str2)

    score = (str1 & str2)
    score_u = str1 | str2

    return 100-(len(score)/len(score_u))*100
def fitness(agents):
    # print("a=", agents[0])
    for agent in agents:

        a = agent.params[0]
        d = agent.params[1]

        # every agent has Params: [1.4282256077720765, 3.487416630353859] Fitness: 99.84939759036145
        cipher = encrypt(plaintext, a, d)

        # agent.fitness = 100-fuzz.ratio(plaintext,cipher)
        agent.fitness = ani_jackard(plaintext, cipher)

    return agents


def chaotic_map(n, x_0, y_0, a, d):
    # d = 0.3
    # a = 2.5
    x = []
    x.append(x_0)
    y = []
    y.append(y_0)

    for i in range(n-1):
        x.append((x[i]+d+(a*math.sin(2*math.pi*y[i]))) % 1)
        y.append(1 - a*pow(x[i], 2) + y[i])

    return (x, y)

def encrypt(plaintext, a, d):
    ascii_lst = [ord(i) for i in plaintext]
    n = len(ascii_lst)

    ascii_avg = sum(ascii_lst)/n

    x_0 = ascii_avg/max(ascii_lst)
    y_0 = 0.2
    (x, y) = chaotic_map(n, x_0, y_0, a, d)

    private_key = float_to_shuffled_ints(x, y)
    # print('Private Key = ',private_key)

    ciphertext = []
    for i in range(len(ascii_lst)):
        ciphertext.append(chr(ascii_lst[i]+private_key[i]))

    # print('CipherText = ',ciphertext)
    return ''.join(ciphertext)


def float_to_shuffled_ints(x, y):
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

def init_agents(population, length):
    return [Agent(length) for _ in range(population)]

class Agent:

    def __init__(self, length):

        self.params = [random.uniform(1,4),random.uniform(0.1,4)] #(a,d)
        self.pbest=[self.params[0],self.params[1]] 
        self.fitness = ind_fitness(self.pbest[0],self.pbest[1])
        self.velocity=[0,0]

    def __str__(self):

        return 'Params: ' + str(self.params) + ' Fitness: ' + str(self.fitness)

def ind_fitness(a,d):
    cipher = encrypt(plaintext, a, d)
    fitness = ani_jackard(plaintext, cipher)
    return fitness


def pso(agents,generations,c1,c2,bounds):
    agent=fitness(agents)
    gbest = [0, 0]
    gbest_fitness = -100000000

    for generation in range(generations):
        #calculate the fitness of agents
        agents=fitness(agents)
        #finding the gbest will change only if the 
        for agent in agents:
            #updated the gbest
            pbest_fitness=ind_fitness(agent.pbest[0],agent.pbest[1])
            if agent.fitness>gbest_fitness:
                # print("Updated the global best")
                gbest[0]=agent.params[0]
                gbest[1]=agent.params[1]
                gbest_fitness=agent.fitness
            #updated the pbest of the agent
            if agent.fitness>pbest_fitness:
                print("Updated the personal best")
                agent.pbest[0]=agent.params[0]
                agent.pbest[1]=agent.params[1]
        
        #now finding the velocities and position of each particle.
        for agent in agents:
            #updating velocities
            # print("velocity ",agent.velocity)
            agent.velocity[0]=agent.velocity[0]+c1*random.uniform(-1,1)*(agent.pbest[0]-agent.params[0])+c2*random.uniform(-1,1)*(gbest[0]-agent.params[0])
            agent.velocity[1]=agent.velocity[1]+c1*random.uniform(-1,1)*(agent.pbest[1]-agent.params[1])+c2*random.uniform(-1,1)*(gbest[1]-agent.params[1])
            #updating position
            agent.params[0]=agent.params[0]+agent.velocity[0]
            if agent.params[0]<bounds[0][0]:
                agent.params[0]=bounds[0][0]
            if agent.params[0]>bounds[0][1]:
                agent.params[0]=bounds[0][1]
    
            agent.params[1] = agent.params[1]+agent.velocity[1]
            if agent.params[1]<bounds[1][0]:
                agent.params[1]=bounds[1][0]
            if agent.params[1]>bounds[1][1]:
                agent.params[1]=bounds[1][1]
        if gbest_fitness>99:
            print("Done")
            break
        print('\n'.join(map(str, agents)))
        x=[]
        y=[]
        for agent in agents:
            x.append(agent.params[0])
            y.append(agent.params[1])
        plt.scatter(x,y)
        x_temp=[gbest[0]]
        y_temp=[gbest[1]]
        plt.scatter(x_temp,y_temp)
        # plt.show()
       
        print("----------------------")
    for agent in agents:
        if agent.fitness>gbest_fitness:
            gbest[0]=agent.params[0]
            gbest[1]=agent.params[1]
    return agents,gbest   




in_str = None
in_str_len = None
population = 100
generations = 100

plaintext = input('Enter Message: ')
agents = init_agents(population, in_str_len)
bounds=[[1,4],[0.1,4]]

agents,gbest=pso(agents,generations,0,10,bounds)

print(encrypt(plaintext,gbest[0],gbest[1]))
print(ind_fitness(gbest[0],gbest[1]))

