
class DiffableObject:
    def __init__(self, diffable_information, **options):
        super(DiffableObject, self).__init__(**options)
        self.diffable_information = diffable_information
        self.is_identical = False
    __slots__ = ['is_identical', 'diffable_information']

    def __setstate__(self, state):
        return

    def __getstate__(self):
        return None

    def set_identical(self, identical):
        self.is_identical = identical

def format_diff_text(old_message, new_message):
    old_lines = []
    new_lines = []
    for character in old_message.split():
        old_lines.append(DiffableObject(character))
    for character in new_message.split():
        new_lines.append(DiffableObject(character))
    fill_diffable_objects(old_lines, new_lines)
    return create_paragraph(old_lines, new_lines)

def create_paragraph(old_lines, new_lines):
    word_map = {}

    index = 0
    old_index = 0
    new_index = 0
    empty_object = DiffableObject("")
    empty_object.set_identical(True)
    old_object = retrieve_object(old_lines, old_index, empty_object)
    old_index += 1
    new_object = retrieve_object(new_lines, new_index, empty_object)
    new_index += 1
    while old_index <= len(old_lines) or new_index <= len(new_lines):
        if old_object.is_identical == new_object.is_identical:
            word_map[index] = [old_object.is_identical, new_object.is_identical, old_object.diffable_information, new_object.diffable_information]
            old_object = retrieve_object(old_lines, old_index, empty_object)
            old_index += 1
            new_object = retrieve_object(new_lines, new_index, empty_object)
            new_index += 1
        else:
            if not old_object.is_identical:
                word_map[index] = [old_object.is_identical, new_object.is_identical, old_object.diffable_information, None]
                old_object = retrieve_object(old_lines, old_index, empty_object)
                old_index += 1
            else:
                word_map[index] = [old_object.is_identical, new_object.is_identical, None, new_object.diffable_information]
                new_object = retrieve_object(new_lines, new_index, empty_object)
                new_index += 1

        index += 1
    equal_list = []
    old_list = []
    new_list = []
    last_old_identic = False
    last_new_identic = False
    formatted_text = ""
    for index in word_map:
        values = word_map[index]

        if values[0] != last_old_identic or values[1] != last_new_identic:
            if len(equal_list) > 0:
                formatted_text = "{}={}\n".format(formatted_text, " ".join(equal_list))
            if len(old_list) > 0:
                formatted_text = "{}-{}\n".format(formatted_text, " ".join(old_list))
            if len(new_list) > 0:
                formatted_text = "{}+{}\n".format(formatted_text, " ".join(new_list))
            equal_list = []
            old_list = []
            new_list = []

        if values[0] == values[1]:
            if values[0] == True:
                equal_list.append(values[2])
            else:
                old_list.append(values[2])
                new_list.append(values[3])
        else:
            if values[0] == False:
                old_list.append(values[2])
            else:
                new_list.append(values[3])

        last_old_identic = values[0]
        last_new_identic = values[1]

    if len(equal_list) > 0:
        formatted_text = "{}={}\n".format(formatted_text, " ".join(equal_list))
    if len(old_list) > 0:
        formatted_text = "{}-{}\n".format(formatted_text, " ".join(old_list))
    if len(new_list) > 0:
        formatted_text = "{}+{}\n".format(formatted_text, " ".join(new_list))
    return "```diff\n{}\n```".format(formatted_text)


def retrieve_object(lines, index, default_object):
    if index < len(lines):
        return lines[index]
    else:
        return default_object

def fill_diffable_objects(old_lines, new_lines):
    match_matrix = {}
    equal_occurences_map = {}
    init_match_matrix(match_matrix, len(old_lines), len(new_lines))
    fill_match_matrix_and_equal_occurences_map(old_lines, new_lines, match_matrix, equal_occurences_map)
    find_closest_occurences_and_set_diffable_bool(old_lines, new_lines, match_matrix, equal_occurences_map)

def init_match_matrix(match_matrix, maximal_x_matrix_size, maximal_y_matrix_size):
    for y in range(-1, maximal_y_matrix_size):
        match_matrix[(-1,y)] = 0
    for x in range(0, maximal_x_matrix_size):
        match_matrix[(x,-1)] = 0

def fill_match_matrix_and_equal_occurences_map(old_lines, new_lines, match_matrix, equal_occurences_map):
    maximal_x_matrix_size = len(old_lines)
    maximal_y_matrix_size = len(new_lines)
    for x in range(0,maximal_x_matrix_size):
        first_found_in_array = False
        really_added = 0
        for y in range(0, maximal_y_matrix_size):
            #Okay ich habe einen Treffer gefunden
            #Wenn es der Erste Treffer in derReihe ist, dann füge ich eine 1 hinzu, WENN (x-1,y-1) == (x+0,y-1) ist, ansonsten wird die Zahl nur Positiv
            #Die 1 wird dem wert von (x,y-1) hinzugefügt
            if old_lines[x].diffable_information == new_lines[y].diffable_information:
                if (not first_found_in_array) and abs(match_matrix[(x-1, y-1)]) == abs(match_matrix[(x-1, y)]):
                    really_added = 1
                    first_found_in_array = True
                match_matrix[(x,y)] = abs(match_matrix[(x-1,y)])+really_added
                #Hier positive EqualZahl auslesen und als index für den List eintrag der Position benutzen.
                fill_map_at_index(equal_occurences_map, match_matrix[(x,y)] , (x,y))
            else:
                # Man muss die inneren Ecken von 2 aufeinander Treffenden gleich hohen ParallelWerten auf den Wert setzen von den anderen paralellwerten
                if first_found_in_array and abs(match_matrix[(x-1, y)]) == abs(match_matrix[(x, y-1)]):
                    first_found_in_array = False
                    really_added = 0
                match_matrix[(x,y)] = (abs(match_matrix[(x-1,y)])+really_added)*-1


def fill_map_at_index(equal_occurences_map, diff_index, point):
    if diff_index not in equal_occurences_map:
        equal_occurences_map[diff_index] = []
    equal_occurences_map.get(diff_index).append(point)
    
def find_closest_occurences_and_set_diffable_bool(old_lines, new_lines, match_matrix, equal_occurences_map):
    # Die Matrix koordinate der letzten festgelegten �bereinstimmung.
    last_matrix_coordinate=(-1,-1)
    # counter geht von 1 bis zur Zahl die als Maximale übereinstimmung gelistet wurde
    # dient als index f�r equalOccurencesMap
    for counter in range(1, len(equal_occurences_map.keys()) + 1):
        nth_occurenceList = equal_occurences_map[counter]
    
        # wenn der erste wert nicht geeignet ist dann darf er nicht gesetzt werden.
        # wenn es keinen geeigneten wert gibt, muss das nth überprungen werden und last_matrix_coordinategesetzt bleiben wie es war.

        current_best_matrix_coordinate = None
        current_best_diagonal_length = 0
        current_best_coordinate_difference = 0
        current_best_difference = 0
        # Hier werden alle Treffer der nächsten möglichen Gleichen Zeile durchgegangen.
        for index in range(0, len(nth_occurenceList)):
            # Die Koordinate, die gerade auf ihre Tauglichkeit geprüft wird.
            actual_matrix_coordinate = nth_occurenceList[index]
        
            # Notiz an mich. Beim nächsten Treffer muss überprüft werden, dass er höhergelegene x und y koordinaten hat als der letzte Wert.
            
            # Break wenn nebeneinanderreihung den Verlauf  stören würde
            # muss für alle Längen an aneinanderreihungen Sein.
            
    
            if actual_matrix_coordinate[0] <= last_matrix_coordinate[0] or actual_matrix_coordinate[1] <= last_matrix_coordinate[1]:
                continue
            
            if current_best_matrix_coordinate is None:
                current_best_matrix_coordinate = actual_matrix_coordinate
                current_best_diagonal_length = count_diagonal_length(match_matrix, old_lines, new_lines, current_best_matrix_coordinate[0], current_best_matrix_coordinate[1])
                current_best_coordinate_difference = (current_best_matrix_coordinate[0] - last_matrix_coordinate[0]) + (current_best_matrix_coordinate[1] - last_matrix_coordinate[1])
                current_best_difference = current_best_diagonal_length - current_best_coordinate_difference
                continue
            
            
            # Bei jedem durchgang wird geschaut, ob l�nge - koordinatenabstand >= dem vorherigen ist, Wenn == dann wo länge > ist
            # wird als neuer referencewert gespeichert
                                                                                                                                                      
            actualDiagonalLength = count_diagonal_length(match_matrix, old_lines, new_lines, actual_matrix_coordinate[0], actual_matrix_coordinate[1])
            coordinatesDifference = (actual_matrix_coordinate[0] - last_matrix_coordinate[0]) + (actual_matrix_coordinate[1] - last_matrix_coordinate[1])
            actualDifference = actualDiagonalLength - coordinatesDifference
            
            if actualDifference>=current_best_difference:
                if actualDifference == current_best_difference:
                    if actualDiagonalLength > current_best_diagonal_length:
                        current_best_matrix_coordinate = actual_matrix_coordinate
                        current_best_diagonal_length = actualDiagonalLength
                        current_best_difference = actualDifference
                else:
                    current_best_matrix_coordinate = actual_matrix_coordinate
                    current_best_diagonal_length = actualDiagonalLength
                    current_best_difference = actualDifference
    

        # Falls es keinen geeigneten Teffer f�r den index gab, wird dieser Komplett �berprungen und die Reference bleibt
        # auf den letzten g�ltigen Wert
        
        if current_best_matrix_coordinate is None:
            continue
        

        # Wenn ein geeigneter Kandidat gefunden wurde, wird er die neue Reference.
        
        
        last_matrix_coordinate = current_best_matrix_coordinate
        
        # Trefferkoordinate den Textlisten zuordnen und true einspeichern.
        # Dabei den counter um die länge erhöhen, damit diese indizes übersprungen werden können.
        
        for i in range(0, current_best_diagonal_length):
            old_lines[current_best_matrix_coordinate[0]+i].set_identical(True)
            new_lines[current_best_matrix_coordinate[1]+i].set_identical(True)
        last_matrix_coordinate = (last_matrix_coordinate[0] + current_best_diagonal_length-1, last_matrix_coordinate[1] + current_best_diagonal_length-1)
        counter += current_best_diagonal_length-1

def count_diagonal_length(match_matrix, old_lines, new_lines, x, y):
    maximal_x_matrix_size = len(old_lines)
    maximal_y_matrix_size = len(new_lines)
    counter = 1
    x += 1
    y += 1
    while x < maximal_x_matrix_size and y < maximal_y_matrix_size:
        if not (match_matrix[(x-1,y-1)] >0 and match_matrix[(x,y)]>0):
            break

        x += 1
        y += 1
        counter += 1

    return counter