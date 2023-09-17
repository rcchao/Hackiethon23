def getShipPos():
    '''
    THIS IS THE LIST OF SHIPS
    [5,3,3,2,2] 
    That is: 
    1x 5 long
    2x 3 long
    2x 2 long

    Your ships must satisfy this 
    '''

    # due to a bug we have the indexing of ships are 0-9
    
    shipPos = [[(2,8), (3,8),(4,8)], 
                [(3,0),(4,0),(5,0),(6,0),(7,0)], 
                [(1,1),(2,1)] , 
                [(8,2), (8,3), (8,4)], 
                [(7,9), (8,9)]]
    return shipPos
