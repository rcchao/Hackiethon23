import numpy as np

#define constants
PROB_INCR_1 = 15 
PROB_INCR_2 = 1

# Step 1
def storage_handling(successful_bombed, failed_bombed, all_bombed, p1ShotSeq, p1PrevHit, storage):
    # Update success status of previous hit
    if p1PrevHit:
        storage.append((1, (p1ShotSeq[-1][0]-1, p1ShotSeq[-1][1]-1)))
    else:
        storage.append((0, (p1ShotSeq[-1][0]-1, p1ShotSeq[-1][1]-1)))
    
    # Create lists for successful bombs and all prev bombs
    for i in range(len(storage)):
        all_bombed.append(storage[i][1])
        if storage[i][0] != 0:
            successful_bombed.append(storage[i][1])
        else:
            failed_bombed.append(storage[i][1])
    return

# Step 2
def increase_surrounding_correct_bombs(game_board, successful_bombed, failed_bombed, all_bombed):
    for successful_bomb in successful_bombed:
        
        # Some spaces should have a higher probability, like if a successful hit  
        # has surrounding 3 of 4 spaces being either walls or failed bombs.
        # The remaining space HAS to have another ship
        walled = 1
        # Horizontal left
        if (successful_bomb[1]-1) < 0 or \
        (successful_bomb[0], successful_bomb[1]-1) in failed_bombed:
            walled += 1
        
        # Horizontal right
        if (successful_bomb[1]+1) > 10 or \
        (successful_bomb[0], successful_bomb[1]+1) in failed_bombed:
            walled += 1
        
        # Vertical up
        if (successful_bomb[0]-1) < 0 or \
        (successful_bomb[0]-1, successful_bomb[1]) in failed_bombed:
            walled += 1
        
        # Vertical down
        if (successful_bomb[0]+1) > 10 or \
        (successful_bomb[0]+1, successful_bomb[1]) in failed_bombed:
            walled += 1
        
        if walled == 4:
            walled = 99
        
        # Now implement the probability increments, factoring in `walled`
        # Horizontal left
        if (successful_bomb[1]-1) >= 0 and \
        (successful_bomb[0], successful_bomb[1]-1) not in all_bombed:
            game_board[successful_bomb[0]][successful_bomb[1]-1] += walled*PROB_INCR_1

        # Horizontal right
        if (successful_bomb[1]+1) < 10 and \
        (successful_bomb[0], successful_bomb[1]+1) not in all_bombed:
            game_board[successful_bomb[0]][successful_bomb[1]+1] += walled*PROB_INCR_1
        
        # Vertical up
        if (successful_bomb[0]-1) >= 0 and \
        (successful_bomb[0]-1, successful_bomb[1]) not in all_bombed:
            game_board[successful_bomb[0]-1][successful_bomb[1]] += walled*PROB_INCR_1
        
        # Vertical down
        if (successful_bomb[0]+1) < 10 and \
        (successful_bomb[0]+1, successful_bomb[1]) not in all_bombed:
            game_board[successful_bomb[0]+1][successful_bomb[1]] += walled*PROB_INCR_1
    
    return game_board

# Step 3
def update_probabilities(game_board, ships, all_bombed):
    for i in range(10):
        for j in range(10):
            # For each ship, check all possible positions for the ship
            for ship in ships:
               
                # For each direction:
                # Check that we are within the bounds of the board and
                # Check that no part of a potential ship placement overlaps with
                # a bombed position
                
                # Horizontal left
                if j - ship >= -1 and \
                not any((i,y) in all_bombed for y in range(j-ship+1,j+1)):
                    game_board[i, j-ship+1:j+1] += PROB_INCR_2
                
                # Horizontal right
                if j + ship <= 10 and \
                not any((i,y) in all_bombed for y in range(j,j+ship)):
                    game_board[i, j:j+ship] += PROB_INCR_2
                
                # Vertical up
                if i - ship >= -1 and \
                not any((x,j) in all_bombed for x in range(i-ship+1,i+1)):
                    game_board[i-ship+1:i+1, j] += PROB_INCR_2
                
                # Vertical down
                if i + ship <= 10 and \
                not any ((x,j) in all_bombed for x in range(i,i+ship)): 
                    game_board[i:i+ship, j] += PROB_INCR_2
                
    return game_board

def ShipLogic(round, yourMap, yourHp, enemyHp, p1ShotSeq, p1PrevHit, storage):
   
    # Step 1: storage handling
    successful_bombed = []
    failed_bombed = []
    all_bombed = []
    if p1ShotSeq:
        storage_handling(successful_bombed, failed_bombed, all_bombed, p1ShotSeq, p1PrevHit, storage)
    
    # Step 2: Increase the probabilities of squares surrounding hits
    # Initialize an all-zero game board
    game_board = np.zeros((10,10))
    updated_board1 = increase_surrounding_correct_bombs(game_board, successful_bombed, failed_bombed, all_bombed)
    
    #Step 3: update probability
    # Initialize the ships
    ships = [5, 3, 3, 2, 2]
    prob_board = update_probabilities(updated_board1, ships, all_bombed)

    #Step 4: find highest probability
    max_coord = np.unravel_index(np.argmax(prob_board), prob_board.shape)
    #return coord [1-10] (default status is miss) & append to storage [0-9]
    y = max_coord[1] + 1
    x = max_coord[0] + 1
    
    return [x,y], storage
