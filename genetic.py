from random import choices, randint, randrange, random
from typing import List, Optional, Callable, Tuple
from functools import partial


Genome = List[int]
Population = List[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]


def fitness(genome: Genome) -> int:
    sumG = sum(genome)
    totalProfit =0
    pq =1023-sumG
    for i in range(10):
        totalProfit=totalProfit + (pq*genome[i])    
    return totalProfit
   



    
def generate_genome(length: int) -> Genome:
    total =1023
    choices = []
    for i in range(10):
        index=randrange(1023)
        if total-index <0:
            choices.append(0)
        else:
            choices.append(index)
            total =total-index
    return choices



def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


genome1 = generate_genome(10)
print(sum(genome1))
print(genome1)
print(fitness(genome1))
population1= generate_population(10,10)
print(population1)



def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")

    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length - 1)
    new1=a[0:p] + b[p:]
    new2=b[0:p] + a[p:]
    if sum(new1)>1023 or sum(new2)>1023:
        return a,b
    else:
        return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(genome: Genome, num: int = 1, probability: float = 0.074) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        b=1023-(sum(genome)-genome[index])
        genome[index] = genome[index] if random() > probability else randint(0,b)
    return genome


def population_fitness(population: Population, fitness_func: FitnessFunc) -> int:
    return sum([fitness_func(genome) for genome in population])


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(gene) for gene in population],
        k=2
    )
print("demnn")
print(selection_pair(population1,fitness))


def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    return sorted(population, key=fitness_func, reverse=True)


def genome_to_string(genome: Genome) -> str:
    return "".join(map(str, genome))



def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100,
        printer: Optional[PrinterFunc] = None) \
        -> Tuple[Population, int]:
    population = populate_func()
    

    for i in range(generation_limit):
        print(i)
        print(population)
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if printer is not None:
            printer(population, i, fitness_func)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    return population, i

print("=====================")
population, generations = run_evolution(
    populate_func = partial(generate_population,size =10,genome_length =10),
    fitness_func= partial(fitness),
    fitness_limit=10000000,
    generation_limit=1000,
)
print("========================")
print()
print("last poplation :")
print(population)
print("number of generations :")
print(generations+1)
print("winning child :" )
print(population[0])
print("winning childrens fitness value (each value is q value of 10 firms):" )
print(fitness(population[0]))
