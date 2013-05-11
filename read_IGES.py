#!/usr/bin/env python
from iges.curves_surfaces import RationalBSplineCurve, Line 
from iges.annotations import GeneralNote
from iges.entity import Entity, process_global_section

# http://ts.nist.gov/Standards/IGES/specfigures/index.cfm

def load_iges(iges_file):
    """Load IGES file.
    
    Args:
        iges_file: Name of IGES file to load.
        
    Returns:
        A dict containing the Start and Global sections of the IGES file
        and a list of entities with parameters."""
    param_string = ''
    entity_index = 0
    first_dict_line = True
    first_global_line = True
    first_param_line = True
    global_string = ""
    pointer_dict = {}
    product = {'start': '',
               'global': '',
               'entity_list': []}

    with open(iges_file, 'r') as f:
        for line in f.readlines():
            data = line[:80]
            id_code = line[72]

            if id_code == 'S':     # Start
                product['start'] += data[:72]
            elif id_code == 'G':   # Global
                # TODO: The global section should be parsed into individual
                #       fields.
                product['global'] += data[:72].strip()

                global_string += data   # Consolidate all global lines
                if first_global_line:
                    param_sep = data[2]
                    record_sep = data[6]
                    first_global_line = False

                # Record separator denotes end of global section
                if global_string.strip()[-1] == record_sep:
                    process_global_section(global_string)
            elif id_code == 'D':   # Directory entry
                if first_dict_line:
                    entity_type_number = int(data[0:8].strip())
                    # Curve and surface entities.
                    # See IGES spec v5.3, p. 38, Table 3
                    if entity_type_number == 100:   # Circular arc
                        e = Entity()
                    elif entity_type_number == 102: # Composite curve
                        e = Entity()
                    elif entity_type_number == 104: # Conic arc
                        e = Entity()
                    elif entity_type_number == 108: # Plane
                        e = Entity()
                    elif entity_type_number == 110: # Line
                        e = Line()
                    elif entity_type_number == 112: # Parametric spline curve
                        e = Entity()
                    elif entity_type_number == 114: # Parametric spline surface
                        e = Entity()
                    elif entity_type_number == 116: # Point
                        e = Entity()
                    elif entity_type_number == 118: # Ruled surface
                        e = Entity()
                    elif entity_type_number == 120: # Surface of revolution
                        e = Entity()
                    elif entity_type_number == 122: # Tabulated cylinder
                        e = Entity()
                    elif entity_type_number == 124: # Transformation matrix
                        e = Entity()
                    elif entity_type_number == 126: # Rational B-spline curve
                        e = RationalBSplineCurve()
                    elif entity_type_number == 128: # Rational B-spline surface
                        e = Entity()
                    # Need to add more ...
                    
                    # CSG Entities. See IGES spec v5.3, p. 42, Section 3.3
                    elif entity_type_number == 150: # Block
                        e = Entity()

                    # B-Rep entities.  See IGES spec v5.3, p. 43, Section 3.4
                    elif  entity_type_number == 186:
                        e = Entity()

                    # Annotation entities. 
                    # See IGES spec v5.3, p. 46, Section 3.5
                    elif entity_type_number == 202:
                        e = Entity()
                    elif entity_type_number == 212:
                        e = GeneralNote()

                    # Structural entities.
                    # See IGES spec v5.3, p. 50, Section 3.6
                    elif  entity_type_number == 132:
                        e = Entity()

                    else:
                        e = Entity()

                    e.add_section(data[0:8], 'entity_type_number')
                    e.add_section(data[8:16], 'parameter_pointer')
                    e.add_section(data[16:24], 'structure')
                    e.add_section(data[24:32], 'line_font_pattern')
                    e.add_section(data[32:40], 'level')
                    e.add_section(data[40:48], 'view')
                    e.add_section(data[48:56], 'transform')
                    e.add_section(data[56:65], 'label_assoc')
                    e.add_section(data[65:72], 'status_number')
                    e.sequence_number = int(data[73:].strip())

                    first_dict_line = False
                else:
                    e.add_section(data[8:16], 'line_weight_number')
                    e.add_section(data[16:24], 'color_number')
                    e.add_section(data[24:32], 'param_line_count')
                    e.add_section(data[32:40], 'form_number')
                    e.add_section(data[56:64], 'entity_label', type='string')
                    e.add_section(data[64:72], 'entity_subs_num')

                    first_dict_line = True
                    product['entity_list'].append(e)
                    pointer_dict.update({e.sequence_number : entity_index})
                    entity_index += 1

            elif id_code == 'P':   # Parameter data
                # Concatenate multiple lines into one string
                if first_param_line:
                    param_string = data[:64]
                    directory_pointer = int(data[64:72].strip())
                    first_param_line = False
                else:
                    param_string += data[:64]

                if param_string.strip()[-1] == record_sep:
                    first_param_line = True
                    param_string = param_string.strip()[:-1]
                    parameters = param_string.split(param_sep)
                    product['entity_list'][pointer_dict[directory_pointer]].add_parameters(parameters)

            elif id_code == 'T':   # Terminate
                pass
    return product

if __name__ == '__main__':
    # Setup
    #fileName = 'revB_alveolus_v5a_export.igs'
    #fileName = 'F126x.igs'
    FILENAME = 'f212x.igs'

    PRODUCT = load_iges(FILENAME)
    for entity in PRODUCT['entity_list']:
        if entity.d['entity_type_number'] == 212:
            print entity
    print(PRODUCT['start'])
    print(PRODUCT['global'])
