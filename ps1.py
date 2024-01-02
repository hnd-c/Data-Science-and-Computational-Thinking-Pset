################################################################################
# 6.0002 Fall 2020
# Problem Set 1
# Name:Hem N Chaudhary
# Collaborators:None
# Time:a couple of days

from state import *

##########################################################################################################
## Problem 1
##########################################################################################################

def generate_election(filename):
    """
    Reads the contents of a file, with data given in the following tab-delimited format,
    State   Democrat_votes    Republican_votes    EC_votes 
 
    Please ignore the first line of the file, which are the column headers.
    
    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    # TODO
    file_handle=open(filename,'r')  #open the file
    #print(file_handle.readlines())
    file_list=[]
    for line in file_handle:
        file_list.append(line)    #converted into list
    list_state=[]
    for i in range(1,len(file_list)): # for each element into file_list add add it to state class
        temp_line=file_list[i]
        temp_line=temp_line.strip('\n')
        temp=temp_line.split("\t")
        i=State(temp[0],int(temp[1]),int(temp[2]),int(temp[3]))
        list_state.append(i)
    
    return list_state
        
   
        
    

##########################################################################################################
## Problem 2: Helper functions 
##########################################################################################################

def election_result(election):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    Note: In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election - a list of State instances 

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'gop') if Democrats won, else ('gop', 'dem')
    """
    # TODO 
    dem_ec=0
    gop_ec=0
    for item in election:
        if item.get_winner()=='dem':   # check if winner is dem
            dem_ec+=item.get_ecvotes()
            
        else:
            gop_ec+=item.get_ecvotes()
            
    if dem_ec>gop_ec:             #check who has more ec votes
        return ('dem','gop')        
            
    else:
        return ('gop','dem')
            
            


def winner_states(election):
    """
    Finds the list of States that were won by the winning candidate (lost by the losing candidate).

    Parameters:
    election - a list of State instances 

    Returns:
    A list of State instances won by the winning candidate
    """
    # TODO
    list_inst=[]
    result=election_result(election)
    for item in election:
        if item.get_winner()==result[0]: #check if the state instances in election was won by winner
            list_inst.append(item)
    
    return list_inst
        
        
        
    


def ec_votes_needed(election, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election - a list of State instances 
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    # TODO
    t_ec_loser=0
    result=election_result(election)
    for item in election:
        if item.get_winner()==result[1]:
            t_ec_loser+=item.get_ecvotes() #add ecvotes won by loser
    
    return (1+total/2)-t_ec_loser  #additin ec votes number
    
    
    

##########################################################################################################
## Problem 3: Brute Force approach
##########################################################################################################

def get_binary_representation(n, num_digits):
    """
    Helper function to get a binary representation of items to add to a subset,
    which combinations() uses to construct and append another item to the powerset.
    
    Parameters:
    n and num_digits are non-negative ints
    
    Returns: 
        a num_digits str that is a binary representation of n
    """
    result = ''
    while n > 0:
        result = str(n%2) + result
        n = n//2
    if len(result) > num_digits:
        raise ValueError('not enough digits')
    for i in range(num_digits - len(result)):
        result = '0' + result
    return result

def combinations(L):
    """
    Helper function to generate powerset of all possible combinations
    of items in input list L. E.g., if
    L is [1, 2] it will return a list with elements
    [], [1], [2], and [1,2].

    Parameters:
    L - list of items

    Returns:
    a list of lists that contains all possible
    combinations of the elements of L
    """
    powerset = []
    for i in range(0, 2**len(L)):
        binStr = get_binary_representation(i, len(L))
        subset = []
        for j in range(len(L)):
            if binStr[j] == '1':
                subset.append(L[j])
        powerset.append(subset)
    return powerset

def brute_force_swing_states(winner_states, ec_votes):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states, these are our swing states. Iterate over
    all possible move combinations using the helper function combinations(L).
    Return the move combination that minimises the number of voters moved. If
    there exists more than one combination that minimises this, return any one of them.

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states 
    The empty list, if no possible swing states
    """
    # TODO
    best_combo=[]
    minimum_so_far=0
    for stat in winner_states:
        minimum_so_far+=stat.get_margin()+1 #min voters need to move
    possible_move_combinations=combinations(winner_states) #all the combination
    for combo in possible_move_combinations:
        new_ecvotes=0
        num_voters_moved=0
        if len(combo)!=0:
            for elm in combo: #ecvotes and margin in each states in combo
                new_ecvotes+=elm.get_ecvotes()
                num_voters_moved+=(1+elm.get_margin())
                
            if new_ecvotes>int(ec_votes) and num_voters_moved<= minimum_so_far: #check for requirement
                best_combo=combo
                minimum_so_far=num_voters_moved

    
    if len(best_combo)!=0:
        return best_combo
    else:
        return []
    
##########################################################################################################
## Problem 4: Dynamic Programming
## In this section we will define two functions, max_voters_move and min_voters_move, that
## together will provide a dynamic programming approach to find swing states. This problem
## is analagous to the complementary knapsack problem, you might find Lecture 1 of 6.0002 useful 
## for this section of the pset. 
##########################################################################################################

def fastMaxVal(winner_states, ec_votes, memo):   #copy paste from lecture
    """Assumes toConsider a list of subjects, avail a weight
         memo supplied by recursive calls
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the subjects of that solution"""
    if memo == None:
        memo = {}
    if (len(winner_states), ec_votes) in memo:
        result = memo[(len(winner_states), ec_votes)]
    elif winner_states == [] or ec_votes == 0:
        result =(0, tuple())
    elif winner_states[0].get_ecvotes() > ec_votes:
        #Explore right branch only
        result = fastMaxVal(winner_states[1:], ec_votes, memo)
    else:
        nextItem = winner_states[0]
        #Explore left branch
        withVal, withToTake =\
                 fastMaxVal(winner_states[1:],
                            ec_votes - nextItem.get_ecvotes(), memo)
        withVal += nextItem.get_margin()+1
        #Explore right branch
        withoutVal, withoutToTake = fastMaxVal(winner_states[1:],
                                                ec_votes, memo)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(winner_states), ec_votes)] = result

    return result
         



def max_voters_move(winner_states, ec_votes, memo=None):
    """
    Finds the largest number of voters needed to relocate to get at most ec_votes
    for the election loser. 

    Analogy to the knapsack problem:
    Given a list of states each with a weight(#ec_votes) and value(#margin+1),
    determine the states to include in a collection so the total weight(#ec_votes)
    is less than or equal to the given limit(ec_votes) and the total value(#voters displaced)
    is as large as possible.

    Hint: If using a top-down implementation, it may be helpful to create a helper function

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes - int, the maximum number of EC votes 
    memo - dictionary, an OPTIONAL parameter for memoization (don't delete!).
    Note: If you decide to use the memo make sure to override the default value when it's first called.

    Returns:
    A list of State instances such that the maximum number of voters need to be relocated
    to these states in order to get at most ec_votes 
    The empty list, if every state has a # EC votes greater than ec_votes
    """
    # TODO
    
    value=fastMaxVal(winner_states, ec_votes, memo) 
    
    return list(value[1]) # returning second element of value which returns states 
    

def min_voters_move(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated. 
    Only return states that were originally won by the winner (lost by the loser)
    of the election.

    Hint: This problem is simply the complement of max_voters_move. You should call 
    max_voters_move with ec_votes set to (#ec votes won by original winner - ec_votes_needed)

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    # TODO
    ecvotes_winner=0
    for states in winner_states:
        ecvotes_winner+=states.get_ecvotes()   
    
    lowbound_ecvotes=ecvotes_winner-ec_votes_needed     #lower bound 
    non_swingstates=max_voters_move(winner_states,lowbound_ecvotes) #find all the non swing states 
    swingstates=[]
    for states in winner_states:  #all the states that are not swing states 
        if states not in non_swingstates:
            swingstates.append(states)
    
    
    
    return swingstates
    
    
    

##########################################################################################################
## Problem 5
##########################################################################################################

def relocate_voters(election, swing_states):
    """
    Finds a way to shuffle voters in order to flip an election outcome. Moves voters 
    from states that were won by the losing candidate (states not in winner_states), to 
    each of the states in swing_states. To win a swing state, you must move (margin + 1) 
    new voters into that state. Any state that voters are moved from should still be won 
    by the loser even after voters are moved. Also finds the number of EC votes gained by 
    this rearrangement, as well as the minimum number of voters that need to be moved.
    Note: You cannot move voters out of New York, Washington, Massachusetts, or California. 

    Parameters:
    election - a list of State instances representing the election 
    swing_states - a list of State instances where people need to move to flip the election outcome 
                   (result of min_voters_move or greedy_swing_states)

    Return:
    A tuple that has 3 elements in the following order:
        - a dictionary with the following (key, value) mapping: 
            - Key: a 2 element tuple of str, (from_state, to_state), the 2 letter State names
            - Value: int, number of people that are being moved 
        - an int, the total number of EC votes gained by moving the voters 
        - an int, the total number of voters moved 
    None, if it is not possible to sway the election
    """
    # TODO
    forbiden_states=['MA','NY','WA','CA']  
    
    states_loser=[]
    result=election_result(election)
    for item in election:
        if item.get_winner()==result[1]: #collect all the loser's state
            states_loser.append(item)
    
    ec_needed=ec_votes_needed(election, total=538) #ec vote needed 
    total_ec=0
    total_moved=0
    dic={}
    for item in swing_states:
        for state in states_loser:
            if item.get_margin()+1<state.get_margin() and state.get_name() not in forbiden_states: # if swing states has enough vote to flip 
                dic[state.get_name(),item.get_name()]=item.get_margin()+1
                total_ec+=item.get_ecvotes()
                total_moved+=item.get_margin()+1
                state.subtract_winning_candidate_voters(item.get_margin()+1)
                item.add_losing_candidate_voters(item.get_margin()+1)
                break
           
            elif state.get_margin()>1 and state.get_name() not in forbiden_states: #if swing states doesn has enough votes, just reduce the margin
                dic[state.get_name(),item.get_name()]=state.get_margin()-1
                state.subtract_winning_candidate_voters(state.get_margin()-1)
                item.add_losing_candidate_voters(state.get_margin()-1)
                total_moved+=state.get_margin()-1
                
                
                
                
                
    
    
    if ec_needed<=total_ec:
        return (dic,total_ec,total_moved)
    else:
        return None
                
                
        
    
    
    


if __name__ == "__main__":
    pass
    # Uncomment the following lines to test each of the problems

    # tests Problem 1
    year = 2012
    election = generate_election("%s_results.txt" % year)
    # print(len(election))
    # print(election[0])

    # tests Problem 2
    winner, loser = election_result(election)
    won_states = winner_states(election)
    names_won_states = [state.get_name() for state in won_states]
    reqd_ec_votes = ec_votes_needed(election)
    # print("Winner:", winner, "\nLoser:", loser)
    # print("States won by the winner: ", names_won_states)
    # print("EC votes needed:",reqd_ec_votes, "\n")

    # tests Problem 3
    brute_election = generate_election("60002_results.txt")
    brute_won_states = winner_states(brute_election)
    brute_ec_votes_needed = ec_votes_needed(brute_election, total=14)
    brute_swing = brute_force_swing_states(brute_won_states, brute_ec_votes_needed)
    names_brute_swing = [state.get_name() for state in brute_swing]
    voters_brute = sum([state.get_margin()+1 for state in brute_swing])
    ecvotes_brute = sum([state.get_ecvotes() for state in brute_swing])
    # print("Brute force swing states results:", names_brute_swing)
    # print("Brute force voters displaced:", voters_brute, "for a total of", ecvotes_brute, "Electoral College votes.\n")

    # tests Problem 4: max_voters_move
    # print("max_voters_move")
    # total_lost = sum(state.get_ecvotes() for state in won_states)
    # non_swing_states = max_voters_move(won_states, total_lost-reqd_ec_votes)
    # #print('non_swing_states',non_swing_states)
    # non_swing_states_names = [state.get_name() for state in non_swing_states]
    # max_voters_displaced = sum([state.get_margin()+1 for state in non_swing_states])
    # max_ec_votes = sum([state.get_ecvotes() for state in non_swing_states])
    # print("States with the largest margins (non-swing states):", non_swing_states_names)
    # print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")

    # tests Problem 4: min_voters_move
    print("min_voters_move")
    swing_states = min_voters_move(won_states, reqd_ec_votes)
    swing_state_names = [state.get_name() for state in swing_states]
    min_voters_displaced = sum([state.get_margin()+1 for state in swing_states])
    swing_ec_votes = sum([state.get_ecvotes() for state in swing_states])
    print("Complementary knapsack swing states results:", swing_state_names)
    print("Min voters displaced:", min_voters_displaced, "for a total of", swing_ec_votes, "Electoral College votes. \n")

    # tests Problem 5: relocate_voters
    print("relocate_voters")
    flipped_election = relocate_voters(election, swing_states)
    print("Flip election mapping:", flipped_election)