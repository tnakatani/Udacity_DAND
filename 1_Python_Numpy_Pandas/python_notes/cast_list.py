def create_cast_list(filename):
    cast_list = []
    #use with to open the file filename
    with open("flying_circus_cast.txt") as f:
        #use the for loop syntax to process each line
        #and add the actor name to cast_list
        for line in f:
            dp = line.split(',')
            cast_list.append(dp[0])

    return cast_list

cast_list = create_cast_list('flying_circus_cast.txt')
for actor in cast_list:
    print(actor)
