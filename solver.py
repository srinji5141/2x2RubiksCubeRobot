from cube import apply_rotations_to_moves, convert_16_state_to_14_state, invert_rotations

SEVEN_FACTORIAL = 5040
SOLUTION_LENGTH_BYTES = 6

def encode_perm(perm):
    # https://antoinecomeau.blogspot.com/2014/07/mapping-between-permutations-and.html
    n = 7

    pos = [0,1,2,3,4,5,6]
    elems = [0,1,2,3,4,5,6]

    k = 0
    m = 1

    for i in range(n-1):
        k += m * pos[perm[i]]
        m = m * (n - i)
        pos[elems[n - i - 1]] = pos[perm[i]]
        elems[pos[perm[i]]] = elems[n - i - 1]
    
    return k

def encode_14_state_as_int(s):
    orientation_number = 0

    for i in (0, 1, 2, 3, 4, 5):
        orientation_number += 3**i * s[7 + i]

    permutation_number = encode_perm(s[0:7])

    return permutation_number + orientation_number * SEVEN_FACTORIAL

def decode_bytes_to_moves(byte_arr):
    nums = []
    for b in byte_arr:
        lower = b & 0xf
        upper = b >> 4
        nums.append(lower)
        nums.append(upper)
    assert len(nums) == 2 * SOLUTION_LENGTH_BYTES
    MOVES = ["U", "U'", "U2", "F", "F'", "F2", "R", "R'", "R2"]
    result = []
    for num in nums:
        if num < len(MOVES):
            result.append(MOVES[num])
        else:
            assert(num == 15)
    return result


def translate_general_solution_to_solution_with_only_executable_moves(sol):
    # we assume that sol consists of only moves (no cube rotations)
    # we output a solution consisting only of:
        # rotations will only consist of ("z'", "y", "y2", "y'")
        # and moves will only consist of ("D", "D2", "D'")
    if len(sol) == 0:
        return []
    
    first_move = sol[0]
    first_move_modifier = first_move[1:]
    first_move_face = first_move[0]
    remaining_sol = sol[1:]

    initial_rotations = ()
    final_rotations = ()
    if first_move_face == "D":
        initial_rotations = ()
    elif first_move_face == "F":
        initial_rotations = ("y", "z'")
    elif first_move_face == "L":
        initial_rotations = ("z'",)
    elif first_move_face == "R":
        initial_rotations = ("z'",)
        if first_move_modifier == "'":
            final_rotations = ("y",)
        elif first_move_modifier == "":
            final_rotations = ("y'",)
        elif first_move_modifier == "2":
            final_rotations = ("y2",)
    elif first_move_face == "B":
        initial_rotations = ("y'", "z'")
    elif first_move_face == "U":
        initial_rotations = ()
        if first_move_modifier == "'":
            final_rotations = ("y",)
        elif first_move_modifier == "":
            final_rotations = ("y'",)
        elif first_move_modifier == "2":
            final_rotations = ("y2",)
    else:
        raise Exception("Error in translate_general_solution_to_solution_with_only_executable_moves")

    # TODO: use recursion here, and apply the initial and final rotations appropriately...
    remaining_sol = apply_rotations_to_moves(remaining_sol, initial_rotations)
    remaining_sol = apply_rotations_to_moves(remaining_sol, final_rotations)
    first_move = "D" + first_move_modifier
    return list(initial_rotations) + [first_move] + translate_general_solution_to_solution_with_only_executable_moves(remaining_sol)
    

def get_solution_for_state(s):
    # s is assumed to be a 16-state.
    # we will output a sequence of rotations and moves that will solve s
    # rotations will only consist of ("z'", "y", "y2", "y'")
    # and moves will only consist of ("D", "D2", "D'")
    initial_rotations, new_14_state = convert_16_state_to_14_state(s)

    state_int_repr = encode_14_state_as_int(new_14_state)
    file_byte_offset = state_int_repr * SOLUTION_LENGTH_BYTES
    with open("massive_table.bin", "rb") as f:
        f.seek(file_byte_offset)
        solution_bytes = f.read(SOLUTION_LENGTH_BYTES)
    solution_urf = decode_bytes_to_moves(solution_bytes)
    solution = apply_rotations_to_moves(solution_urf, invert_rotations(initial_rotations))

    return translate_general_solution_to_solution_with_only_executable_moves(solution)


def convert_colors_to_piece(c1, c2, c3):
    colors = {c1, c2, c3}
    if colors == {"WHITE", "ORANGE", "BLUE"}:
        return 0
    if colors == {"WHITE", "RED", "BLUE"}:
        return 1
    if colors == {"WHITE", "RED", "GREEN"}:
        return 2
    if colors == {"WHITE", "ORANGE", "GREEN"}:
        return 3
    if colors == {"YELLOW", "ORANGE", "GREEN"}:
        return 4
    if colors == {"YELLOW", "RED", "GREEN"}:
        return 5
    if colors == {"YELLOW", "RED", "BLUE"}:
        return 6
    if colors == {"YELLOW", "ORANGE", "BLUE"}:
        return 7
    return None

def get_orientation(c1, c2, c3):
    if c1 == "YELLOW" or c1 == "WHITE":
        return 0
    if c2 == "YELLOW" or c2 == "WHITE":
        return 1
    if c3 == "YELLOW" or c3 == "WHITE":
        return 2
    return None

def convert_color_arr_to_16_state(arr):
    # Note; color array of 24 colors follows the speffz letter scheme for corners
    # https://cuberoot.me/wp-content/uploads/2019/02/501-Speffz-Lettering-Scheme-1.pdf

    for i in range(len(arr)):
        if arr[i] == "BLACK":
            arr[i] = "YELLOW"

    pieces = [-1, -1, -1, -1, -1, -1, -1, -1]
    orientations = [-1, -1, -1, -1, -1, -1, -1, -1]

    piece_indices = (
        (0, 17, 4),    # UBL
        (1, 13, 16),   # UBR
        (2, 9, 12),    # UFR
        (3, 5, 8),     # UFL
        (20, 11, 6),   # DFL
        (21, 15, 10),  # DFR
        (22, 19, 14),  # DBR
        (23, 7, 18)    # DBL
    )

    for position in range(8):
        i1, i2, i3 = piece_indices[position]
        (c1, c2, c3) = arr[i1], arr[i2], arr[i3]
        piece = convert_colors_to_piece(c1, c2, c3)
        orientation = get_orientation(c1, c2, c3)
        pieces[position], orientations[position] = piece, orientation

    for i in range(8):
        if pieces[i] is None or orientations[i] is None:
            return None
        if pieces[i] == -1 or orientations[i] == -1:
            return None
    
    for i in range(8):
        for j in range(8):
            if i != j and pieces[i] == pieces[j]:
                return None
    orientation_sum = sum(orientations)
    if orientation_sum % 3 != 0:
        return None
    
    return pieces + orientations


def convert_char_to_color(c):
    if c == 'W':
        return "WHITE"
    if c == 'O':
        return "ORANGE"
    if c == 'G':
        return "GREEN"
    if c == 'R':
        return "RED"
    if c == 'B':
        return "BLUE"
    if c == 'Y':
        return "YELLOW"

    return None

def convert_color_string_to_color_arr(s):
    return [convert_char_to_color(c) for c in s]

if __name__ == "__main__":
    # color_arr = [
    #     "ORANGE", "ORANGE", "WHITE", "BLUE",
    #     "WHITE", "RED", "RED", "BLUE",
    #     "YELLOW", "GREEN", "ORANGE", "YELLOW",
    #     "RED", "WHITE", "ORANGE", "GREEN",
    #     "BLUE", "GREEN", "WHITE", "YELLOW",
    #     "GREEN", "YELLOW", "BLUE", "RED",
    # ]

    #color_str = "GRWORBYBYGBORBOWWYRWGOGY"    # D F2 R F2 D2 B2 L2 B' D2
    # color_str = "BRRWYROOBGGWYWBYGRWOGOYB"   # B' U D L2 U' B R' D' L'
    # color_str = "WORRRGYYYBYRWWWBBGGGBOOO"   # D2 R' F2 R2 L' F L B' L'
    color_str = "WRRYROGBBBWYWYGGBGOROOYW" # R2 F U' R2 B2 R2 U2 F2 B2

    color_arr = convert_color_string_to_color_arr(color_str)

    state = convert_color_arr_to_16_state(color_arr)
    if state is None:
        print("Scan error!")
        exit(0)
    print("got state: ", state)

    sol = get_solution_for_state(state)
    print(" ".join(sol))