# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

import datetime
import time, threading
import logger


def email(sender, recipient, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    me = sender
    you = recipient
    msg['From'] = sender
    msg['To'] = recipient

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(me, 'Darcy0217')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
    logger.log('[#] Status email sent.')

def email_status(bot):

    # build body
    bot.api.get_player()

    response_dict = bot.api.call()
    # print('Response dictionary: \n\r{}'.format(json.dumps(response_dict, indent=2)))
    currency_1 = "0"
    currency_2 = "0"

    player = response_dict['responses']['GET_PLAYER']['player_data']

    # @@@ TODO: Convert this to d/m/Y H:M:S
    creation_date = datetime.datetime.fromtimestamp(
        player['creation_timestamp_ms'] / 1e3)

    pokecoins = '0'
    stardust = '0'
    balls_stock = bot.pokeball_inventory()

    if 'amount' in player['currencies'][0]:
        pokecoins = player['currencies'][0]['amount']
    if 'amount' in player['currencies'][1]:
        stardust = player['currencies'][1]['amount']

    body = ''
    body = body + '[#] Username: {username}\n'.format(**player)
    body = body + '[#] Acccount Creation: {}\n'.format(creation_date)
    body = body + '[#] Bag Storage: {}/{}\n'.format(bot.get_inventory_count('item'), player['max_item_storage'])
    body = body + '[#] Pokemon Storage: {}/{}\n'.format(
        bot.get_inventory_count('pokemon'), player[
            'max_pokemon_storage'])
    body = body + '[#] Stardust: {}\n'.format(stardust)
    body = body + '[#] Pokecoins: {}\n'.format(pokecoins)
    body = body + '[#] PokeBalls: ' + str(balls_stock[1]) + '\n'
    body = body + '[#] GreatBalls: ' + str(balls_stock[2]) + '\n'
    body = body + '[#] UltraBalls: ' + str(balls_stock[3]) + '\n'

    bot.api.get_inventory()
    response_dict = bot.api.call()
    if 'responses' in response_dict:
        if 'GET_INVENTORY' in response_dict['responses']:
            if 'inventory_delta' in response_dict['responses'][
                    'GET_INVENTORY']:
                if 'inventory_items' in response_dict['responses'][
                        'GET_INVENTORY']['inventory_delta']:
                    pokecount = 0
                    itemcount = 1
                    for item in response_dict['responses'][
                            'GET_INVENTORY']['inventory_delta'][
                                'inventory_items']:
                        # print('item {}'.format(item))
                        if 'inventory_item_data' in item:
                            if 'player_stats' in item[
                                    'inventory_item_data']:
                                playerdata = item['inventory_item_data'][
                                    'player_stats']

                                nextlvlxp = (
                                    int(playerdata.get('next_level_xp', 0)) -
                                    int(playerdata.get('experience', 0)))

                                if 'level' in playerdata:
                                    body = body + '[#] -- Level: {level}\n'.format(
                                            **playerdata)

                                if 'experience' in playerdata:
                                    body = body + '[#] -- Experience: {experience}\n'.format(
                                            **playerdata)
                                    body = body + '[#] -- Experience until next level: {}\n'.format(
                                            nextlvlxp)

                                if 'pokemons_captured' in playerdata:
                                    body = body + '[#] -- Pokemon Captured: {pokemons_captured}\n'.format(
                                            **playerdata)

                                if 'poke_stop_visits' in playerdata:
                                    body = body + '[#] -- Pokestops Visited: {poke_stop_visits}\n'.format(
                                            **playerdata)

    msg = MIMEText(body)
    msg['Subject'] = 'Pokemon Bot Status'
    me = 'pokemongobotdev@gmail.com'
    you = 'darcy.qiu@gmail.com'
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(me, 'Darcy0217')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
    logger.log('[#] Status email sent.')


def periodic_email_status(bot):
    email_status(bot)
    EMAIL_THREAD = threading.Timer(3600, periodic_email_status).start()
    logger.log('[#] Will send status again in 1 hour...')


EMAIL_THREAD = threading.Timer(3600, periodic_email_status)