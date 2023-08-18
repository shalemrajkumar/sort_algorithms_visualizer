#!/usr/bin/env python
# coding: utf-8

# ### imports

# In[34]:


import numpy as np
import math
get_ipython().system('pip install pygame')
import pygame

pygame.init()
np.random.seed(seed=10)


# ## Drawing using pygame

# In[35]:


class draw_information:
    black = 0, 0, 0
    white = 255, 255, 255
    green = 0, 255, 0
    red = 255, 0, 0
    bg = white
    
    font = pygame.font.SysFont('comicsans', 30)
    large_font = pygame.font.SysFont('comicsans', 40)

    side_pad = 100
    top_pad = 150
    
    gradients = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)]
    
    def __init__(self, width, height, lst):
        self.width = width
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))    # window setup
        pygame.display.set_caption("Sorting_Algorithm_Visualization")
        self.set_list(lst)
        
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.side_pad) / len(lst))  #Block width
        self.block_height = math.floor((self.height - self.top_pad) / (self.max_val - self.min_val))  #Block width
        self.start_x = self.side_pad // 2        #start drawing


# ### Imp_fun

# ### generate_list

# In[36]:


def generate_starting_list(n, min_val, max_val):
#     lst = []
    lst = list(np.random.randint(min_val, high = max_val, size=n))
#     for _ in range(n):
#         val = random.randint(min_val, max_val)
#         lst.append(val)

    return lst


# ### Drawing_pygame_functions

# In[37]:


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.bg)

    title = draw_info.large_font.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.green)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2.5 , 5))

    controls = draw_info.font.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.black)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/3 , 45))

    sorting = draw_info.font.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.black)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2.5 , 75))

    draw_list(draw_info)
    pygame.display.update()
    
    
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.side_pad//2, draw_info.top_pad, 
                        draw_info.width - draw_info.side_pad, draw_info.height - draw_info.top_pad)
        pygame.draw.rect(draw_info.window, draw_info.bg, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.gradients[i % 3]

        if i in color_positions:
            color = color_positions[i] 

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


# ### Sorting_Algorithms

# #### Bubble_Sort

# In[38]:


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.green, j + 1: draw_info.red}, True)
                yield True


# #### Insersection_sort

# In[39]:


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst


# ### Main()

# In[40]:


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = draw_information(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"


    pygame.quit()


# ### Run

# In[41]:


if __name__ == "__main__":
    main()


# In[ ]:




