#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
Created on Fri May  1 18:38:03 2020

@author: of

The object of this project is to find out which specific hands, and under 
what circumstances it is ok to bet 'all-in' in a Tempest hold'em game.

The project starts by simulating different scenarios and finding out what 
hands are the most powerfull ones.  
"""

import time
import json

import numpy as np

from holdem.deck import Deck
from holdem.card import Card
from holdem.evaluator import Evaluator
from init_rank import init_rank

initial_ranking = init_rank.initial_ranking
evaluator = Evaluator()

def game(nplayers, pretty_print = False):
    """
    
    
    Parameters
    ----------
    nplayers : int
        number of players in the simulated game.
    pretty_print : Boolean, optional
        It prints the game simulation. The default is False.

    Returns
    -------
    initial_rank : list
        initial ranking positions of the drawn hands    
    ranking : list
        global result ranking of each of the drawn hands. lower ranking means
        higher global hand (lowest rank is an imperial flush)
    """

    deck = Deck()
    # Repartimos 2 cartas a cada jugador
    hands = [deck.draw(2) for _ in range(nplayers)]

    # Cada jugador decide si apuesta o no apuesta en base a su posicion y su mano inicial.
    initial_rank = [initial_ranking(hand) for hand in hands] # ranking inicial p/2 jugadores, seg�n Michael Shackleford.

    # Se reparte las 5 cartas comunes.
    board = deck.draw(5)


    if pretty_print:
        [Card.print_pretty_cards(i) for i in hands] # imprime la mano de cada jugador
        Card.print_pretty_cards(board) # imprime tablero
        evaluator.hand_summary(board, hands) # imprime ganador

    # Se calcula el ranking de cadfloat64a mano.
    ranking = [evaluator.evaluate(hand, board) for hand in hands]
    return([initial_rank, ranking])

def simulate_games(nplayers, simulations, print_simulations = False, save_file = ""):
    """
    
    
    Parameters
    ----------
    nplayers : int
        number of players per game simulation.
    simulations : int
        number of games simulated. 
    print_simulations : Boolean, optional
        Prints every simulated game. The default is False.
    save_file : str, optional
        If not-null, it saves the results in a .json
        Note: the format would be "filename.json". 
    The default is "" (null).

    Returns
    -------
    results : list
        list of games played. Each game has inside of it the initial hand
        ranking and the final global rank.

    """                 

    results = [game(nplayers, print_simulations) for _ in range(simulations)]

    if save_file:
        with open(save_file, "w") as write_file:
            json.dump(results, write_file)
            
    return results

def load_sim_json(filename, print_json = False):
    """
    
    
    Parameters
    ----------
    filename : str
        name of the file where results where previously storaged.
    print_json : Bool, optional
        prints what was storaged in the .json. The default is False.

    Returns
    -------
    data : list
        returns the results previously storaged in the json.

    """

    try:
        with open(filename,) as f:
            data = json.load(f)
        if print_json:
            print(data)
        return (data)
    except:
        pass
    
    print('no file with the specified name')

def linear(results):
    """
    

    Parameters
    ----------
    results : list
        A list with the simulated  and storaged games.

    Returns
    -------
    mat : np.array
        With al the results distributed in onle 2 columns. They are no longer
        separated games, it only matters the initial hand and the final rank. 

    """
    nplayers = len(results[0][0])
    simulations = len(results)
    
    mat = np.zeros((nplayers*simulations, 2))
    cont = 0
    for i in results:
        mat[(cont)*nplayers : (cont+1)*nplayers, 0] = i[0][:]
        mat[(cont)*nplayers : (cont+1)*nplayers, 1] = i[1][:]
        cont += 1
    
    return mat




nplayers = 9
simulations = 10
filename = "simulations.json"

# results = simulate_games(9, 10, save_file=filename)
results = load_sim_json("simulations.json")




    
