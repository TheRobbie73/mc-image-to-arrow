import numpy
import image_convert
import os, pathlib

table = image_convert.output
dump_path = pathlib.Path(__file__).parent.absolute()/'dump'
if not dump_path.exists(): dump_path.mkdir()

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

def command(target, time):

    motion = target_to_motion(target, time)

    return (
        'summon minecraft:falling_block ' 
        + str(SOURCE_POS[0]) + ' ' + str(SOURCE_POS[1]) + ' ' + str(SOURCE_POS[2]) + ' '
        + '{Time:1, BlockState:{Name:"minecraft:lantern"}, Motion:['
        + str(motion[0]) + 'd, ' + str(motion[1]) + 'd, ' + str(motion[2]) + 'd'
        + ']}'
    )

def components():
    source_to_target = CANVAS_POS - SOURCE_POS
    mag = numpy.linalg.norm(source_to_target)
    if mag == 0:
        delta_y = numpy.array([0.0, 0.0, 1.0])
    else:
        delta_y = numpy.array([source_to_target[0], 0.0, source_to_target[2]]) / mag * -1
    delta_x = numpy.array([delta_y[2] * -1, 0.0, delta_y[0]])
    offset = (delta_y * (len(table) - 1) + delta_x * (len(table[0]) - 1)) * -1 / 2
    return offset, delta_x, delta_y

def iterate(offset, delta_x, delta_y, main_path, folder_path):
    time = 20
    main_script = open(main_path, 'a')

    for row_index, row in enumerate(table):
        for col_index, cell in enumerate(row):
            if not cell: continue
            pos = (offset + delta_y * row_index + delta_x * col_index) * PIXEL_DIFF
            text = command(pos, time)
            main_script.write(text + "\n")
    
    main_script.close()

def make_folder(version:int = 0):
    mainfolder_name = 'foo' + str(version)
    mainfolder_path = dump_path/mainfolder_name

    if not mainfolder_path.exists(): 
        mainfolder_path.mkdir()
        main_path = mainfolder_path/'main.mcfunction'
        folder_path = mainfolder_path/'arrow_commands'
        folder_path.mkdir()
        
        return main_path, folder_path
    else:
        return make_folder(version + 1)


def main():
    offset, delta_x, delta_y = components()
    main_path, folder_path = make_folder()
    iterate(offset, delta_x, delta_y, main_path, folder_path)

main()