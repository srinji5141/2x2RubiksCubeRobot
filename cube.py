
# A cube state is represented as an array of 16 integers.
# the first 8 integers represent the permutation of the 8 pieces,
# and the last 8 integers represent the permutation.
# The permutation of a piece is either 0, 1, or 2, and is defined as: 
#       the number of clockwise twists necessary to get the white/yellow sticker to face up/down.





# There are 18 possible moves that can be applied: they are:
# 0: U
# 1: U'
# 2: U2
# 3: L
# 4: L'
# 5: L2
# 6: F
# 7: F'
# 8: F2
# 9: R
# 10: R'
# 11: R2
# 12: B
# 13: B'
# 14: B2
# 15: D
# 16: D'
# 17: D2

NUM_MOVES = 18
CUBE_SOLVED_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0]
STATE_PERM_OFFSET = 8
MOVES = ["U", "U'", "U2", "L", "L'", "L2", "F", "F'", "F2", "R", "R'", "R2", "B", "B'", "B2", "D", "D'", "D2"]
assert len(MOVES) == NUM_MOVES


PARTIAL_CUBE_ROTATION_SEQUENCES = (
    (),
    ("z'"),
    ("y", "z'"),
    ("y2", "z'"),
    ("y'", "z'"),
    ("z'", "z'"),
)

COMPLETE_CUBE_ROTATION_SEQUENCES = (
    (),
    ("y",),
    ("y2",),
    ("y'",),

    ("z'",),
    ("z'", "y"),
    ("z'", "y2"),
    ("z'", "y'"),

    ("y", "z'"),
    ("y", "z'", "y"),
    ("y", "z'", "y2"),
    ("y", "z'", "y'"),

    ("y2", "z'"),
    ("y2", "z'", "y"),
    ("y2", "z'", "y2"),
    ("y2", "z'", "y'"),

    ("y'", "z'"),
    ("y'", "z'", "y"),
    ("y'", "z'", "y2"),
    ("y'", "z'", "y'"),

    ("z'", "z'"),
    ("z'", "z'", "y"),
    ("z'", "z'", "y2"),
    ("z'", "z'", "y'"),
)

MOVES_AFTER_ROTATION = {
    "z'": {"U": "L", "F": "F", "R": "U", "B": "B", "L": "D", "D": "R"},
    "z": {"U": "R", "F": "F", "R": "D", "B": "B", "L": "U", "D": "L"},
    "y": {"U": "U", "F": "L", "R": "F", "B": "R", "L": "B", "D": "D"},
    "y2": {"U": "U", "F": "B", "R": "L", "B": "F", "L": "R", "D": "D"},
    "y'": {"U": "U", "F": "R", "R": "B", "B": "L", "L": "F", "D": "D"},
}

def apply_rotation_to_move(move, rotation):
    move_face = move[0]
    move_modifier = move[1:]
    new_move_face = MOVES_AFTER_ROTATION[rotation][move_face]
    return new_move_face + move_modifier

def apply_rotations_to_move(move, rotations):
    m = move
    for rotation in rotations:
        m = apply_rotation_to_move(m, rotation)
    return m

def apply_rotation_to_moves(moves, rotation):
    return [apply_rotation_to_move(move, rotation) for move in moves]

def apply_rotations_to_moves(moves, rotations):
    return [apply_rotations_to_move(move, rotations) for move in moves]

def invert_rotation(rotation):
    rotation_axis = rotation[0]
    rotation_modifier = rotation[1:]
    if rotation_modifier == "":
        rotation_modifier = "'"
    elif rotation_modifier == "2":
        rotation_modifier = "2"
    elif rotation_modifier == "'":
        rotation_modifier = ""
    else:
        raise Exception("Invalid rotation modifier in invert_rotation()")
    return rotation_axis + rotation_modifier

def invert_rotations(rotations):
    return [invert_rotation(i) for i in rotations][::-1]


def apply_cube_rotation(s, rotation):
    if rotation == "z'":
        apply_move(s, encode_move("F'"))
        apply_move(s, encode_move("B"))
    elif rotation == "y":
        apply_move(s, encode_move("U"))
        apply_move(s, encode_move("D'"))
    elif rotation == "y2":
        apply_move(s, encode_move("U2"))
        apply_move(s, encode_move("D2"))
    elif rotation == "y'":
        apply_move(s, encode_move("U'"))
        apply_move(s, encode_move("D"))
    else:
        raise Exception("Invalid rotation: " + rotation)

def apply_cube_rotations(s, rotations):
    for rotation in rotations:
        apply_cube_rotation(s, rotation)

def maybe_convert_16_state_to_14_state(s):
    # returns None if the 16-state cannot be converted to a 14-state without cube rotations,
    # otherwise returns the corresponding 14-state.
    if s[7] != 7 or s[15] != 0:
        return None
    return s[0:7] + s[8:15]

def convert_16_state_to_14_state(s):
    # returns the rotations needed to get to the new 14-state,
    # as well as the new 14-state.
    for rot_seq in COMPLETE_CUBE_ROTATION_SEQUENCES:
        s_new = s[:]
        apply_cube_rotations(s_new, rot_seq)
        new_14_state = maybe_convert_16_state_to_14_state(s_new)
        if new_14_state != None:
            return (rot_seq, new_14_state)

    raise Exception("Reached unreachable code in convert_16_state_to_14_state.")

def apply_move(s, move):
    if move == 0:  # U
        (s[0], s[1], s[2], s[3]) = (s[3], s[0], s[1], s[2])
        (s[8], s[9], s[10], s[11]) = (s[11], s[8], s[9], s[10])
    elif move == 1:  # U'
        (s[0], s[1], s[2], s[3]) = (s[1], s[2], s[3], s[0])
        (s[8], s[9], s[10], s[11]) = (s[9], s[10], s[11], s[8])
    elif move == 2:  # U2
        (s[0], s[1], s[2], s[3]) = (s[2], s[3], s[0], s[1])
        (s[8], s[9], s[10], s[11]) = (s[10], s[11], s[8], s[9])
    elif move == 3:  # L
        (s[0], s[3], s[4], s[7]) = (s[7], s[0], s[3], s[4])
        (s[8], s[11], s[12], s[15]) = ((s[15]+1)%3, (s[8]+2)%3, (s[11]+1)%3, (s[12]+2)%3)
    elif move == 4:  # L'
        (s[0], s[3], s[4], s[7]) = (s[3], s[4], s[7], s[0])
        (s[8], s[11], s[12], s[15]) = ((s[11]+1)%3, (s[12]+2)%3, (s[15]+1)%3, (s[8]+2)%3)
    elif move == 5:  # L2
        (s[0], s[3], s[4], s[7]) = (s[4], s[7], s[0], s[3])
        (s[8], s[11], s[12], s[15]) = (s[12], s[15], s[8], s[11])
    elif move == 6:  # F
        (s[3], s[2], s[5], s[4]) = (s[4], s[3], s[2], s[5])
        (s[11], s[10], s[13], s[12]) = ((s[12]+1)%3, (s[11]+2)%3, (s[10]+1)%3, (s[13]+2)%3)
    elif move == 7:  # F'
        (s[3], s[2], s[5], s[4]) = (s[2], s[5], s[4], s[3])
        (s[11], s[10], s[13], s[12]) = ((s[10]+1)%3, (s[13]+2)%3, (s[12]+1)%3, (s[11]+2)%3)
    elif move == 8:  # F2
        (s[3], s[2], s[5], s[4]) = (s[5], s[4], s[3], s[2])
        (s[11], s[10], s[13], s[12]) = (s[13], s[12], s[11], s[10])
    elif move == 9:  # R
        (s[2], s[1], s[6], s[5]) = (s[5], s[2], s[1], s[6])
        (s[10], s[9], s[14], s[13]) = ((s[13]+1)%3, (s[10]+2)%3, (s[9]+1)%3, (s[14]+2)%3)
    elif move == 10:  # R'
        (s[2], s[1], s[6], s[5]) = (s[1], s[6], s[5], s[2])
        (s[10], s[9], s[14], s[13]) = ((s[9]+1)%3, (s[14]+2)%3, (s[13]+1)%3, (s[10]+2)%3)
    elif move == 11:  # R2
        (s[2], s[1], s[6], s[5]) = (s[6], s[5], s[2], s[1])
        (s[10], s[9], s[14], s[13]) = (s[14], s[13], s[10], s[9])
    elif move == 12:  # B
        (s[1], s[0], s[7], s[6]) = (s[6], s[1], s[0], s[7])
        (s[9], s[8], s[15], s[14]) = ((s[14]+1)%3, (s[9]+2)%3, (s[8]+1)%3, (s[15]+2)%3)
    elif move == 13:  # B'
        (s[1], s[0], s[7], s[6]) = (s[0], s[7], s[6], s[1])
        (s[9], s[8], s[15], s[14]) = ((s[8]+1)%3, (s[15]+2)%3, (s[14]+1)%3, (s[9]+2)%3)
    elif move == 14:  # B2
        (s[1], s[0], s[7], s[6]) = (s[7], s[6], s[1], s[0])
        (s[9], s[8], s[15], s[14]) = (s[15], s[14], s[9], s[8])
    elif move == 15:  # D
        (s[4], s[5], s[6], s[7]) = (s[7], s[4], s[5], s[6])
        (s[12], s[13], s[14], s[15]) = (s[15], s[12], s[13], s[14])
    elif move == 16:  # D'
        (s[4], s[5], s[6], s[7]) = (s[5], s[6], s[7], s[4])
        (s[12], s[13], s[14], s[15]) = (s[13], s[14], s[15], s[12])
    elif move == 17:  # D2
        (s[4], s[5], s[6], s[7]) = (s[6], s[7], s[4], s[5])
        (s[12], s[13], s[14], s[15]) = (s[14], s[15], s[12], s[13])
    else:
        raise Exception("Invalid move!")

def encode_move(s):
    return MOVES.index(s)

def decode_move(i):
    return MOVES[i]

def new_cube():
    return CUBE_SOLVED_STATE[:]

def pretty_print_moves(seq):
    return " ".join([decode_move(i) for i in seq])

