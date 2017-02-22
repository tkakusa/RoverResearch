forward_directions = set(['onward', 'ahead', 'forward', 'towards'])
reverse_directions = set(['backward', 'around', 'back'])
turning_directions = set(['left', 'right']) | reverse_directions

turning_actions = set(['turn','pivot', 'transition'])
movement_actions = set(['move', 'moving', 'go', 'going', 'drive', 'driving', 'proceed', 'accelerate', 'accelerating'])
stopping_actions = set(['stop', 'halt'])

time_units = set(['seconds'])
distance_units = set(['centimeters', 'units'])

larger_magnitude = set(['greater', 'more'])
smaller_magnitude = set(['less', 'fewer'])
equivalent_magnitude = set(['same', 'equal', 'is'])

inverted_conditionals = set(['until', 'once'])
normal_conditionals = set(['while', 'continuouly'])

check_statements = set(['if'])

negations = set(["not", "isn't"])

directions = forward_directions | turning_directions
actions = turning_actions | movement_actions | stopping_actions
units = time_units | distance_units
magnitudes = larger_magnitude | smaller_magnitude | equivalent_magnitude
conditionals = inverted_conditionals | normal_conditionals


file = open('textFile', 'r+')
fileout = open('main.py', 'w')

action = ' '
direction = ' '
value = ' '
condition = ' '
unit = ' '
magnitude = ' '
negation = ' '
check = ' '

tab_val = '    '
tab_count = 0
negated = 0

distanceRecheck = 0

fileout.write("import functions\n\n")
fileout.write("functions.Initialize()\n")

for line in file:
    for word in line.split():
        if word == 'end':
            if distanceRecheck:
                fileout.write(tab_val*tab_count + "x = functions.GetDistance()\n")
                print (tab_val*tab_count + "x = GetDistance()")
                distanceRecheck = distanceRecheck - 1
            tab_count = tab_count - 1
            pass
        elif word in actions:
            action = word
            print("Action:         %s" % word)
        elif word in directions:
            direction = word
            print("Direction:      %s" % word)
        elif word.isdigit():
            value = word
            print("Value:          %s" % word)
        elif word in conditionals:
            condition = word
            print("Condition:      %s" % word)
        elif word in units:
            unit = word
            print("Units:          %s" % word)
        elif word in magnitudes:
            magnitude = word
            print("Magnitude:      %s" % word)
        elif word in negations:
            negation = word
            print("Negation:       %s" % word)
        elif word in check_statements:
            check = word
            print("Check:          %s" % word)
    if condition in conditionals:
        if unit in distance_units:
            fileout.write(tab_val*tab_count + "x = functions.GetDistance()\n")
            print(tab_val*tab_count + "x = GetDistance()")
            fileout.write(tab_val*tab_count + "curr_bearing = functions.GetBearing()\n")
            print (tab_val*tab_count + "curr_bearing = GetBearing( )")
            if negation in negations or condition in inverted_conditionals:
                negated = 1
            if ((magnitude in larger_magnitude) or (magnitude in smaller_magnitude and negated)):
                fileout.write(tab_val*tab_count + "while ( x > %s ):\n" % value)
                print(tab_val*tab_count + "while ( x > %s ):" % value)
            elif ((magnitude in smaller_magnitude) or (magnitude in larger_magnitude and negated)):
                fileout.write(tab_val*tab_count + "while ( x < %s ):\n" % value)
                print(tab_val*tab_count + "while ( x < %s ):" % value)
            elif magnitude in equivalent_magnitude or negated:
                fileout.write(tab_val*tab_count + "while ( x != %s ):\n" % value)
                print(tab_val*tab_count + "while ( x != %s ):" % value)
            else:
                fileout.write(tab_val*tab_count + "while ( x == %s ):\n" % value)
                print(tab_val*tab_count + "while ( x == %s ):" % value)
            value = ''
            negated = 0
            distanceRecheck = distanceRecheck + 1
            tab_count = tab_count + 1
    elif check in check_statements:
        if unit in distance_units:
            fileout.write(tab_val*tab_count + "x = functions.GetDistance()\n")
            print(tab_val*tab_count + "x = GetDistance()")
            if negation in negations:
                negated = 1
            if ((magnitude in larger_magnitude) or (magnitude in smaller_magnitude and negated)):
                fileout.write(tab_val*tab_count + "if ( x > %s ):\n" % value)
                print(tab_val*tab_count + "if ( x > %s ):" % value)
            elif ((magnitude in smaller_magnitude) or (magnitude in larger_magnitude and negated)):
                fileout.write(tab_val*tab_count + "if ( x < %s ):\n" % value)
                print(tab_val*tab_count + "if ( x < %s ):" % value)
            elif magnitude in equivalent_magnitude and negated:
                fileout.write(tab_val*tab_count + "if ( x != %s ):\n" % value)
                print(tab_val*tab_count + "if ( x != %s ):" % value)
            else:
                fileout.write(tab_val*tab_count + "if ( x == %s ):\n" % value)
                print(tab_val*tab_count + "if ( x == %s ):" % value)
            negated = 0
            tab_count = tab_count + 1
    if action in turning_actions:
        if direction in reverse_directions:
            fileout.write(tab_val*tab_count + "functions.Turn ( \"around\" )\n" )
            print (tab_val*tab_count + "Turn ( \"around\" )" )
        else:
            fileout.write(tab_val*tab_count + "functions.Turn ( \"%s\" )\n" % direction )
            print (tab_val*tab_count + "Turn ( \"%s\" )" % direction )
    elif action in movement_actions:
        if direction in turning_directions:
            fileout.write(tab_val*tab_count + "functions.Turn ( \"%s\" )\n" % direction )
            print (tab_val*tab_count + "Turn ( \"%s\" )" % direction )
        if unit in time_units:
            fileout.write(tab_val*tab_count + "curr_bearing = functions.GetBearing( )\n")
            print (tab_val*tab_count + "curr_bearing = GetBearing( )")
            fileout.write(tab_val*tab_count + "functions.MoveForward(curr_bearing, %s )\n" % value)
            print (tab_val*tab_count + "MoveForward(curr_bearing, %s )" % value)
        else:
            fileout.write(tab_val*tab_count + "functions.MoveForward( curr_bearing )\n")
            print (tab_val*tab_count + "MoveForward( curr_bearing )")
    elif action in stopping_actions:
        fileout.write(tab_val*tab_count + "functions.Stop ()\n")
        print (tab_val*tab_count + "Stop ()")
    action = ' '
    direction = ' '
    value = ' '
    condition = ' '
    unit = ' '
    magnitude = ' '
    negation = ' '
    check = ' '

fileout.close()
file.close()
        

