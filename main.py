import functions

functions.Initialize()
x = functions.GetDistance()
curr_bearing = functions.GetBearing()
while ( x != 20 ):
    functions.MoveForward( curr_bearing )
    functions.Turn ( "left" )
    x = functions.GetDistance()
