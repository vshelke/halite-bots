import hlt
import logging

game = hlt.Game("legend")
logging.info("Starting my bot!")

def dna(ship, entity):
    if isinstance(entity, hlt.entity.Planet) and ship.can_dock(entity):
        command_queue.append(ship.dock(entity))
        return True
    else:
        navigate_command = ship.navigate(
            ship.closest_point_to(entity),
            game_map,
            speed=int(hlt.constants.MAX_SPEED),
            max_corrections=18,
            angular_step=5)
        if navigate_command:
            command_queue.append(navigate_command)
            return True
    return False

def get_nearest_entities(ship):
    entities_by_distance = game_map.nearby_entities_by_distance(ship)
    ships = []
    planets = []
    for distance in sorted(entities_by_distance):
        for nearest_entity in entities_by_distance[distance]:
            if isinstance(nearest_entity, hlt.entity.Planet):
                planets.append(nearest_entity)
            elif isinstance(nearest_entity, hlt.entity.Ship):
                ships.append(nearest_entity)
    return ships, planets

def my_ratio(nos):
    total = 0
    for player in game_map.all_players():
        total += len(player.all_ships())
    return int((nos/total)*100)

def attack(ship, ships):
    for target in ships:
        if target in my_ships:
            continue
        return dna(ship, target)

while True:
    game_map = game.update_map()
    command_queue = []
    my_ships = game_map.get_me().all_ships()
    for ship in my_ships:
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue
        ships, planets = get_nearest_entities(ship)
        if my_ratio(len(my_ships)) > 43:
            # attack
            _ = attack(ship, ships)
        else:
            for planet in planets:
                if planet.is_full():
                    continue
                elif dna(ship, planet):
                    break
                else:
                    _ = attack(ship, planet.all_docked_ships())
                    break
    game.send_command_queue(command_queue)
