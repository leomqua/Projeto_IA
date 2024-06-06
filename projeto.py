locations = ["apartment", "kitchen", "office", "trash bin", "exit", "kitchen table", "bookshelf"]
objects = ["Fanta", "Beer can", "Coke", "Milk", "Apple juice"]
people = ["Michael", "Christopher", "Matthew", "Joshua", "Daniel", "David"]

graph = {
    "apartment": ["kitchen", "office", "exit"],
    "kitchen": ["apartment","kitchen table", "trash bin"],
    "office": ["apartment","bookshelf"],
    "kitchen table": ["kitchen"],
    "bookshelf": ["office"],
    "trash bin": ["kitchen"],
    "exit": ["apartment"],
}

object_locations = {
    "Fanta": "kitchen table",
    "Beer can": "bookshelf",
    "Coke": "trash bin",
    "Milk": "kitchen table",
    "Apple juice": "kitchen table",
}

person_locations = {
    "Michael": "apartment",
    "Christopher": "office",
    "Matthew": "kitchen",
    "Joshua": "office",
    "Daniel": "kitchen",
    "David": "office",
}

phrases = [
  "Hello! I am a robot.\n",
  "\nPlease, follow me.\n",
  "\nPlease, take this object.\n",
  "\nHello!\n",
]
current_location = "apartment"
held_object = None


def find_object_location(obj):

    visited = set()
    queue = [current_location]

    while queue:
        current = queue.pop(0)
        visited.add(current)
        neighbors = graph[current]
        for neighbor in neighbors:
            if neighbor not in visited:
               queue.append(neighbor)

        if obj in object_locations and object_locations[obj] == current:
           return current

    return None

def find_person_location(person):

    visited = set()
    queue = [current_location]

    while queue:
        current = queue.pop(0)
        visited.add(current)
        neighbors = graph[current]
        for neighbor in neighbors:
            if neighbor not in visited:
               queue.append(neighbor)

        if person in person_locations and person_locations[person] == current:
            return current


def find_shortest_path(graph, current_location, end):
  visited = set()
  queue = [[current_location]]

  if end in object_locations:
      end = find_object_location(end)

  if end in person_locations:
      end = find_person_location(end)

  if current_location == end:
      return [current_location]

  while queue:
      path = queue.pop(0)
      node = path[-1]

      if node not in visited:
          neighbors = graph[node]
          for neighbor in neighbors:
              if neighbor not in path:  # Evita ciclos no grafo
                  new_path = list(path)
                  new_path.append(neighbor)
                  queue.append(new_path)

                  if neighbor == end:
                      return new_path

          visited.add(node)

def execute_command(command):
  parts = command.split(", ")

  for part in parts:
      action, argument = part.split(" ", 1)
      if '.' in argument:
          argument = argument.rstrip('.')
      if action == "and": 
          action, argument = argument.split(" ", 1)
      if action == "then":
          action, argument = argument.split(" ", 1)
      if action == "Move" or action == "move":
          argument = argument[3:]
          move(argument)
      elif action == "grasp":
          location = find_object_location(argument)
          if location:
              grasp(argument)
          else:
              print(f"Cannot grasp {argument}. Object not found.")
      elif action == "bring":
          argument = argument[6:]
          bring(argument)
      elif action == "put":
          put()
      elif action == "introduce":  
            introduce()
      elif action == "guide":
          argument = argument[11:]
          guide(argument)
      elif action == "leave":
          leave()


def move(destination):
  global current_location 
  path = find_shortest_path(graph,current_location, destination)
  if destination in locations or destination in objects:
    if path:
      for location in path[1:]:
          print(f"Going to {location}")
          current_location = location
          print(f"Arrived at {location}")
  
  elif destination in people:
      print(f"Going to {destination}")
      for location in path[1:]:
          print(f"Going to {location}")
          current_location = location
          print(f"Arrived at {location}")

def grasp(obj):
    global held_object
    if obj in object_locations and object_locations[obj] == current_location:
        print(f"Grasping {obj}")
        held_object = obj
        object_locations.pop(obj)
    else:
        print(f"Cannot grasp {obj}. Not found in the current location.")

def bring(end):
    global held_object
    if end in people:
        if person_locations[end] == current_location:
            print(phrases[2])
            print(f"Brought {held_object} to {end}")
        else:
            print(f"Bringing {held_object} to {end}")
            move(end)
            print(phrases[2])
            print(f"Brought {held_object} to {end}")
    if end in locations:
        if end == current_location:
            print(f"Brought {held_object} to {end}")
        else:
            print(f"Bringing {held_object} to {end}")
            move(end)
            print(f"Brought {held_object} to {end}")
    held_object = None

def put():
    global held_object
    move("trash bin")
    print(f"Putting {held_object} in the trash bin")
    held_object = None

def leave():
    move("exit")
    print("Leaving the Apartment")

def introduce():
        print(phrases[3])

def guide(destination):
        print(phrases[1])
        move(destination)
        print(f"Finished guiding to {destination}")

# Exemplos:
commands = [
    #"Move to kitchen, then move to exit, and leave the apartment.",
    #"Move to Coke, grasp Coke, and bring it to Daniel.",
    #"Move to Beer can, grasp Beer can, and bring it to kitchen table.",
    #"Move to Fanta, grasp Fanta, and put it in the trash bin.",
    #"Move to Matthew, and introduce yourself.",
    #"Move to Joshua, and guide him to the exit.",
    #"Move to Milk, grasp Milk, and bring it to bookshelf.",
]

# for command in commands:
#     print(phrases[0])
#     execute_command(command)

input_command = input("Command: ")
print("\n" + phrases[0] + "\n", end ="")  
execute_command(input_command)
