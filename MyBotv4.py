import hlt
import logging
# import time

game = hlt.Game("legend")
logging.info("Starting my bot!")
THRESH = 45

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
    nearest_entities = []
    for distance in sorted(entities_by_distance):
        for nearest_entity in entities_by_distance[distance]:
            nearest_entities.append(nearest_entity)
    return nearest_entities

while True:
    # start_time = time.time()
    game_map = game.update_map()
    command_queue = []
    my_ships = game_map.get_me().all_ships()
    for ship in my_ships:
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue
        n_entities = get_nearest_entities(ship)
        for ent in n_entities:
            if isinstance(ent, hlt.entity.Planet):
                if ent.is_full():
                    continue
                elif dna(ship, ent):
                    break
                elif ent.is_owned() and ent.owner.id != game_map.my_id:
                    dna(ship, ent.all_docked_ships()[0])
                    break
                continue
            if isinstance(ent, hlt.entity.Ship):
                if ent in my_ships:
                    continue
                dna(ship, ent)
                break
    game.send_command_queue(command_queue)
    # logging.info(' delay ' + str(int(1000 * (time.time() - start_time))))
