import cleaner
import random

class Population():
    def __init__(self):
        self.groups = list()
                
    def __len__(self):
        total_pop = int()
        for group in self.groups:
            total_pop += len(group)   
        return total_pop
    
    def __str__(self):
        if self.qt_groups() > 0:
            group_str = 'GROUPS IN POPULATION:'
        else:
            group_str = str()
            
        for group in self.groups:
            group_str += '\n' + str(group)
        
        if self.qt_groups() > 0:
            group_str += f'\n\nTotal: {len(self)} \n'
            
        return group_str
    
    def add_group(self,group_name,qt_members_group):
        group = Group(group_name,len(self) + 1,qt_members_group)
        self.groups.append(group)
        
    def qt_groups(self):
        return len(self.groups)
    
    def add_sampled_member(self,drawn_nr):
        for group in self.groups:
            if group.count_start <= drawn_nr <= group.count_end:
                group.increase_sample()
                break
            
            
    def return_sampled(self,tot_sample):
        sample_str = '\nSAMPLE:'
            
        for group in self.groups:
            sample_str += '\n' + group.return_sampled(tot_sample)
        sample_str += f'\n\nTotal: {tot_sample} ({tot_sample / len(self) * 100:0.2f}% of population) \n'
            
        return sample_str
                 
            
class Group():
    global population
    
    def __init__(self,name,count_start,qt_members):
        self.count_start = count_start
        self.count_end = count_start + qt_members - 1
        self.name = name
        self.sampled = int()
        
    def __len__(self):
        return self.count_end - self.count_start + 1
    
    def __str__(self):
        return f'{self.name}: {len(self)} ({len(self) / len(population) * 100:0.2f}%)'
    
    def increase_sample(self):
        self.sampled += 1
        
    def return_sampled(self,tot_sample):
        return f'{self.name}: {self.sampled} ({self.sampled / tot_sample * 100:0.2f}%)'
    
    def calc_sample_precision(self,tot_sample):
        sample_percent = self.sampled / tot_sample
        pop_percent = len(self) / len(population)
        precision = (1 - abs(sample_percent - pop_percent)) * 100
        return precision
        
    
    
def read_groups_screen(population):
    add_group = 'y'
    while add_group == 'y':
        cleaner.clear_screen()
        print(population)
        
        #Asking for the name of the group
        while True:
            group_name = input(f'Name of group {population.qt_groups() + 1}: ')
            if not group_name.strip():
                continue
            else:
                break
        
        #Asking for the quantity of members in the group
        while True:
            try:
                group_qt = int(input(f'Quantity of members in {group_name}: '))
            except:
                continue
            else:
                if group_qt < 1:
                    continue
                else:
                    break
        
        #Creating the group in the population
        population.add_group(group_name,group_qt)
        
        #Ask if user wants to input one more group
        add_group = str()
        while add_group not in ['y','n']:
            add_group = input('Add one more group (y/n)? ').lower()

            
def read_groups_file(population):
    error_msg = str()
    while True:
        try:
            cleaner.clear_screen()
            file_name = input(f'{error_msg}Inform valid file name: ')
            with open(file_name) as file:
                content = file.read()
            lines = content.split('\n')
        except:
            error_msg = 'File not found. '
            continue
        else:
            if lines[0] != 'SQT':
                error_msg = 'File informed has invalid data. '
            else:
                break
                
    for line in lines:
        if line == 'SQT' or not line.strip():
            pass
        else:
            try:
                broken_line = line.split(';')
                group_name = broken_line[0]
                group_qt = broken_line[1]
                population.add_group(group_name,int(group_qt))
            except:
                return False
            
    if len(population) == 0:
        return False
    else:
        return True
                
    
if __name__ == '__main__':
    population = Population()
    
    while True:
        cleaner.clear_screen()
        opt = input('Read information about the population in a file or input it manually (f/m)? ').lower()
        if opt not in ('f','m'):
            continue
        else:
            break
    
    if opt == 'm':
        read_groups_screen(population)
    else:
        if not read_groups_file(population):
            print('Broken file!')
            import sys
            sys.exit(0)

    
    #Asking the size of the sample
    #cleaner.clear_screen()
    print(population)
    
    while True:
        try:
            qt_sample = int(input("What's the size of the sample? "))
        except:
            continue
        else:
            if (qt_sample < 1) or (qt_sample > len(population)):
                continue
            else:
                print(f'Selecting {qt_sample} members in the population. Please wait...')
                break
            
    #Selecting who is part of the sample in the population
    sampled_members = random.sample(list(range(1,len(population)+1)),qt_sample)
    for i in sampled_members:
        population.add_sampled_member(i)
        
    #Comparing the population to the sample
    cleaner.clear_screen()
    print(population)
    print(population.return_sampled(qt_sample))
    
    #Calculation the precision of the sample
    sum_precisions = float()
    for group in population.groups:
        sum_precisions += group.calc_sample_precision(qt_sample)
       
    avg_precision = sum_precisions / len(population.groups)
    print(f'Precision of the sample: {avg_precision:0.2f}')