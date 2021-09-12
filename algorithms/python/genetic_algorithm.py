"""
Infinite monkey theorem / Shakespeare monkey problem
"""
import random


class GeneticAlgorithm:
    def __init__(self, elitism=True, roulette_wheel=False):
        # Instance variables
        self.population = []
        self.population_max = 0
        self.target = ""
        self.target_length = -1
        self.mutation_rate = -1
        self.run_status = False

        # GA Statistics
        self.generations = 0
        self.average_fitness = -1
        self.total_fitness = -1

        # Exploitative or exploratory
        self.elitism = elitism
        self.roulette_wheel = roulette_wheel

    def run_ga(self, target_gene, mutation_rate=1, population_max=100):
        # New target
        self.target = target_gene
        self.target_length = len(target_gene)
        self.mutation_rate = mutation_rate
        self.population_max = population_max

        # Reset GA statistics
        self.generations = 1    # Population is the first generation
        self.average_fitness = -1
        self.total_fitness = 0

        # Population generation
        self.generation_function()

        # Start the GA cycle
        self.run_status = True
        while self.run_status:
            # Fitness of the population
            self.total_fitness = 0
            best_fitness = -1
            chromosome_with_best_fitness = -1
            for individual in self.population:
                individual.fitness_function(self.target, self.target_length)
                self.total_fitness += individual.fitness
                if individual.fitness > best_fitness:
                    best_fitness = individual.fitness
                    chromosome_with_best_fitness = individual

                # Showcase each chromosome in the generation
                print("Chromosome:", individual.chromosome_string, "Fitness:", individual.fitness)
            
            self.average_fitness = self.total_fitness/self.population_max

            # Termination check
            if chromosome_with_best_fitness.chromosome_string == self.target:
                self.run_status = False
                self.print_generation_statistics()
                print("Best Chromosome:", chromosome_with_best_fitness.chromosome_string, "Best Fitness:", chromosome_with_best_fitness.fitness)
                break

            # Selection phase
            parent_a, parent_b = self.parent_selection()

            # Offspring
            self.offspring(parent_a, parent_b)

            # Survivor phase
            self.survivor_selection()

            # End of generation
            self.print_generation_statistics()
            self.generations += 1

    def generation_function(self):
        """
        Generate the initial population.
        """
        for i in range(self.population_max):
            self.population.append(Chromosome(self.target_length, mutation_rate=self.mutation_rate))
            print(self.population[i].chromosome_string)

    def parent_selection(self):
        """
        Parent selection. Terminate here if answer found
        """
        # Elitism method (exploitative)
        if self.elitism:
            return self.selection_elitism()

        # Roulette wheel method (exploitative and exploratory)
        elif self.roulette_wheel:
            return self.selection_roulette_wheel()

    def selection_elitism(self):
        """
        Implementing Elitism. Terminate here if answer found
        """
        def get_chromosome_with_best_fitness(p_population):
            p_best_fitness = -1
            p_chromosome = -1
            for individual in p_population:
                if individual.fitness > p_best_fitness:
                    p_best_fitness = individual.fitness
                    p_chromosome = individual
            return p_chromosome

        # Find chromosome with the best fitness
        chromosome_with_best_fitness = get_chromosome_with_best_fitness(self.population)

        # Avoid editing original list and remove the best fitness
        t_population = self.population.copy()
        t_population.remove(chromosome_with_best_fitness)

        # Find chromosome with the second best fitness
        chromosome_with_second_best_fitness = get_chromosome_with_best_fitness(t_population)
        
        return chromosome_with_best_fitness, chromosome_with_second_best_fitness

    def selection_roulette_wheel(self):
        """
        Implementing roulette wheel method. Higher fitness value given a larger proportion of the wheel.
        """
        roulette_wheel = []  # selection pool

        # How much each chromosome object counts towards the total wheel value
        for individual in self.population:
            total_wheel_percentage = (individual.fitness / self.total_fitness) * 100
            for _ in range(int(total_wheel_percentage)):
                roulette_wheel.append(individual)

        parent_a = roulette_wheel[random.randint(0, len(roulette_wheel) - 1)]
        parent_b = roulette_wheel[random.randint(0, len(roulette_wheel) - 1)]

        return parent_a, parent_b

    def offspring(self, parent_a, parent_b):
        def crossover_mutation():
            # Crossover and vice versa
            child_a = parent_a.crossover(parent_b)
            child_b = parent_b.crossover(parent_a)

            # Mutate both
            child_a.mutation()
            child_b.mutation()

            # Re-do fitness
            child_a.fitness_function(self.target, self.target_length)
            child_b.fitness_function(self.target, self.target_length)

            # Add to population
            self.population.append(child_a)
            self.population.append(child_b)

        if self.elitism:
            # Crossover with two parents, generate new population (new population size => 2x previous)
            for _ in range(int(self.population_max / 2)):
                crossover_mutation()
        elif self.roulette_wheel:
            crossover_mutation()

    def survivor_selection(self):
        """
        Replacement rule here.
        """
        # Elitism method (exploitative)
        if self.elitism:
            self.surivor_elitism()

        # Roulette wheel method (exploitative and exploratory)
        elif self.roulette_wheel:
            self.survivor_roulette_wheel()

    def surivor_elitism(self):
        """
        Replacement rule using elitism.
        """
        # Prune the population by removing the lowest fitness chromosome
        while len(self.population) > self.population_max:
            lowest_fitness = self.target_length + 1
            lowest_fitness_chromosome = -1
            for individual in self.population:
                if individual.fitness < lowest_fitness:
                    lowest_fitness = individual.fitness
                    lowest_fitness_chromosome = individual
            self.population.remove(lowest_fitness_chromosome)
    
    def survivor_roulette_wheel(self):
        """
        Replacement rule using roulette wheel. Lower fitness value given a larger proportion of the wheel.
        """
        while len(self.population) > self.population_max:
            roulette_wheel = []  # selection pool

            # How much each chromosome object counts towards the total wheel value
            for individual in self.population:
                total_wheel_percentage = 100 - (individual.fitness / self.total_fitness) * 100
                for _ in range(int(total_wheel_percentage)):
                    roulette_wheel.append(individual)
            self.population.remove(roulette_wheel[random.randint(0, len(roulette_wheel) - 1)])

    def print_generation_statistics(self):
        """
        Prints the statistics of the current generation
        """
        print("Generation:", self.generations, "Average Fitness:", self.average_fitness)


class Chromosome:
    def __init__(self, chromosome_length, chromosome_string="", mutation_rate=1):
        # Instance variables
        self.chromosome_string = ""
        self.chromosome_length = chromosome_length
        self.fitness = -1
        self.mutation_rate = mutation_rate
        self.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. "

        # Check if chromosome string has been given
        if len(chromosome_string) == 0:
            for i in range(self.chromosome_length):
                self.chromosome_string += "".join(random.choice(self.characters))
        else:
            self.chromosome_string = chromosome_string

    def fitness_function(self, target_chromosome_string, target_chromosome_length):
        """
        Calculate the fitness of a Chromosome.
        """
        # Normalised fraction of correct letters used
        # Count the number of correct characters at the correct index
        correct_characters = 0 
        for i in range(target_chromosome_length):
            if self.chromosome_string[i] == target_chromosome_string[i]:
                correct_characters += 1
        self.fitness = correct_characters

    def crossover(self, second_chromosome):
        """
        Crossover the genes.
        """
        # Choose a random crossover index
        crossover_point = random.randint(0, self.chromosome_length - 1)

        # Take first part from this chromosome and second part from the alternate chromosome
        first_part = self.chromosome_string[:crossover_point]
        second_part = second_chromosome.chromosome_string[crossover_point:]
        
        # Return child chromosome
        return Chromosome(
            self.chromosome_length,
            first_part + second_part,
            self.mutation_rate
        )

    def mutation(self):
        """
        Mutate the chromosome string.
        """
        # Randomly choose to mutate characters in the chromosome
        for i in range(self.chromosome_length):
            probability = random.randint(0, 99)
            if probability <= self.mutation_rate:
                self.chromosome_string = (
                    self.chromosome_string[:i]
                    + random.choice(self.characters)
                    + self.chromosome_string[i + 1:]
                )


if __name__ == "__main__":
    # Test chromosome (1% mutation rate)
    a = Chromosome(6, "Hello.")
    print("A chromosome:", a.chromosome_string)
    b = Chromosome(6, "Prize.")
    print("B chromosome:", b.chromosome_string)
    c = a.crossover(b)
    print("C chromosome:", c.chromosome_string)
    c.mutation()
    print("C Mutation:", c.chromosome_string)

    # Pause until next section
    while input("Run exploitative GA (1% mutation rate). Continue? y/n: ") != "y":
        pass

    # Run exploitative GA (1% mutation rate)
    ga = GeneticAlgorithm(elitism=True)
    ga.run_ga("Swammar")

    # Pause until next section
    while input("Run exploratory GA (1% mutation rate). Continue? y/n: ") != "y":
        pass

    # Run exploratory GA (1% mutation rate)
    ga = GeneticAlgorithm(elitism=False, roulette_wheel=True)
    ga.run_ga("Swammar")
