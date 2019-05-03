{-
Daniel Quiroga 
April 24th, 2019
knightPlace.hs 
Takes in a list containing positions of queens in a column and returns a list of lists that contain which position in each column 
would be safe to put a knight where:
	1) it will not be caught by a queen when placed 
	2) it will not be in a position to capture a queen when placed

the input -> output looks like so: 
[Int] -> [[Int]] as declared 4 lines below
-}

--setting what the input of knighPlace will be and what should be returned when finished, used this to make sure that my algorithm was returning as expected 
knightPlace :: [Int] -> [[Int]]
--use what is returned from solve n to addZeros wherever there is an empty list use length n - 1 in order to maintain proper indexing of the list more info about addZeros in the comments above that funciton**
knightPlace n = addZeros (length n - 1) (solve n) 
	where
	solve [] = []
	--this is where the recursive calls begin - obtained from the pseudo code given in the powerpoint
	solve (x:xs) = [ [ a | a <- [1..length n], safe x xs a ] ] ++ solve xs


	--if any of the arguments below return true than the position is not valid meaning that we would not consider it for a knight placement
	--used the same beginning as queens.hs to call the recursion
	--this will return the points that survive and a empty [] for the columns that do not have any safe positions i.e. the empty lists'
	safe x xs a = and [ not (checkPlace x xs a i) | i <- [0..(length n - 1)]]

	--this is the function that checks all the positions to make sure it is a valid position, if any of the conditions are met than the position is not safe
	--conditions checking are the following: 
	--if the absolute value of the difference between row and column of the position and the position of the queen is 3 than the knight can be placed to capture
		--the queen therefore the position is not safe
	--else if the queen is in that row or column than the position is not safe
	checkPlace x xs a i --right now it does as expected and when False prints all positions and when true prints no positions
		| x /= 0 = True
		--this condition is checking if the position is in the same column as a queen, if so the position is not safe
		| (a == n!!i) && (n!!i /= 0) = True 
		--this condidiont is taking out the position of the queen from all the lists, meaning if the position is in the same row as a queen it is unsafe
		| abs(a - n!!i) == abs((length n) - i - 1) && xs == [] && n!!i /= 0 = True 
		-- this and the following line take the difference in positon of the x and y axis of the position and the queen and if the absolute value addition of the two is equal to 3 than that is a posision that a knight can be placed to capture a queen and hence is a not a safe position 
		| abs(a - n!!i) + abs(length n - (i+1)) == 3 && n!!i /= 0 && xs == [] = True 
		| abs(a - n!!i) + abs(length n - (i+1) - length xs ) == 3 && xs /= [] && n!!i /= 0 = True
		--this is the condition that takes into account all the diagonal paths that the queen may move and if the position is in the diagonal of the queen than the position is unsafe
		| abs(a - n!!i) == abs(length n - (i+1) - length xs) && n!!i /= 0 && xs /= [] = True
		--if it gets through all the condions and does not pass any of them then the position is safe and will be added to the list
		| otherwise = False 

--this adds zeros whenever there is a position with an empty list meaning that there is no safe position in that entire column for example if an empty list is in the 
-- output "[ [] ]" then this function will return that list with a zero like so: [ [0] ]
addZeros index final
	| index == -1 = [] --takes into account whenever the index becomes negative because of the recursion occuring
	| [final!!index] == [[]] = addZeros(index - 1) final ++ [[0]] --finds an index that is empty and essentially replaces it with a a list of 0
	| otherwise = addZeros(index - 1) final ++ [final!!index] --if the list has something inside it meaning that column has a safe postion than essentially ignore



--TODO: 

	--get the 0 for all the vertical columns 

	--take out all the ones in the same row as a queen 

	--take out all the points in the diagonal 

	--take out all the points that are combinations of [2,1] [1,2] [-2,1] [-1,2] [1,-2] [2,-1] from the queen positions in other words absolute of the difference of x and y
	-- is 3

	--return the points that survive

	--put a 0 into the empty list



