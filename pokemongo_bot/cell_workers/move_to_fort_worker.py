from utils import distance, format_dist
from pokemongo_bot.human_behaviour import sleep
from pokemongo_bot import logger

class MoveToFortWorker(object):
    FLY_DIST = 150
    def __init__(self, fort, bot):
        self.fort = fort
        self.api = bot.api
        self.config = bot.config
        self.stepper = bot.stepper
        self.position = bot.position
        self.FLY_DIST = bot.config.fly_distance

    def work(self):
        lat = self.fort['latitude']
        lng = self.fort['longitude']
        fortID = self.fort['id']
        unit = self.config.distance_unit  # Unit to use when printing formatted distance

        dist = distance(self.position[0], self.position[1], lat, lng)

        # print('[#] Found fort {} at distance {}m'.format(fortID, dist))
        logger.log('[#] Found fort {} at distance {}'.format(
            fortID, format_dist(dist, unit)))

        if dist > self.FLY_DIST:
            logger.log('[#] Need to move closer to Pokestop (' + str(int(dist)) + 'm away)')
            position = (lat, lng, 0.0)

            if self.config.walk > 0:
                self.stepper._walk_to(self.config.walk, *position)
            else:
                self.api.set_position(*position)

            self.api.player_update(latitude=lat, longitude=lng)
            response_dict = self.api.call()
            logger.log('[#] Arrived at Pokestop')
            # sleep(0.5)
            return response_dict
        elif dist <= self.FLY_DIST and dist > 10:
            # fly to the fort
            position = (lat, lng, 0.0)
            self.api.set_position(*position)
            self.api.player_update(latitude=lat, longitude=lng)
            response_dict = self.api.call()
            logger.log('[#] Flew to Pokestop (dist within ' + str(self.FLY_DIST) + 'm)')
            # sleep(0.5)
            return response_dict
        else:
            logger.log('[#] Arrived at Pokestop (within in 10m)')

        return None
