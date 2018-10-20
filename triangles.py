def get_length(side):
    x = side[0][0] - side[1][0]
    y = side[0][1] - side[1][1]
    return x*x + y*y


def get_hashs(dots):
    checking_array = list()
    array = list()

    for i, dot_first in enumerate(dots):
        for j, dot_second in enumerate(dots):
            for k, dot_third in enumerate(dots):
                dot = (dot_first, dot_second, dot_third)
                sorted_dot = sorted(dot)
                if dot_first != dot_second and dot_first != dot_third and dot_second != dot_third and sorted_dot not in checking_array:
                    checking_array.append(sorted_dot)
                    array.append(dot)
    del checking_array

    triangle_arr = list()
    for i in array:
        sides = [get_length((i[0], i[1])), get_length((i[1], i[2])), get_length((i[0], i[2]))]
        triangle_arr.append(sorted(sides, reverse=True))

    return triangle_arr