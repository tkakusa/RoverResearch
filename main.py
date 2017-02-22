import functions

functions.Initialize()

bearing = functions.GetBearing()
functions.MoveForward(bearing, 5)
functions.Stop()

functions.Cleanup()

