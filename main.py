import numpy
import image_convert

table = image_convert.output

SOURCE_POS = numpy.array([0.0, 0.0, 0.0]) # change this
CANVAS_POS = numpy.array([0.0, 0.0, 0.0])

PIXEL_DIFF = 0.1 # distance between arrows
LIMIT = 20 # number of commands per mcfunction

ACCEL = 0.05
DRAG = 0.01

def ypos_to_motion(y_pos:float, time:int) -> float:
    return (DRAG*y_pos + ACCEL*time)/(1 - (1 - DRAG)**time) - ACCEL/DRAG

def xzpos_to_motion(xz_pos:float, time:int) -> float:
    return xz_pos*(DRAG)/(1 - (1 - DRAG)**time)

def target_to_motion(target:list, time:int) -> list:
    relative = target - SOURCE_POS
    
    motion = numpy.array([
        xzpos_to_motion(relative[0], time),
        ypos_to_motion(relative[1], time),
        xzpos_to_motion(relative[2], time)
    ])
    return motion

def command(target:list, time:int) -> str:

    motion = target_to_motion(target, time)

    return (
        'summon minecraft:falling_block ' 
        + str(SOURCE_POS[0]) + ' ' + str(SOURCE_POS[1]) + ' ' + str(SOURCE_POS[2]) + ' '
        + '{Time:1, BlockState:{Name:"minecraft:lantern"}, Motion:['
        + str(motion[0]) + 'd, ' + str(motion[1]) + 'd, ' + str(motion[2]) + 'd'
        + ']}'
    )

for row_index, row in enumerate(table):
    for col_index, cell in enumerate(table):
        if not cell: continue
        print((row_index, col_index))