import re
from config import Configuration
from app.cidr import Cidr
import redis


class BotHandler:

    def __init__(self):
        self.config = Configuration()
        self.token = self.config.read_param('telegram', 'token')
        self.help_message = self.config.read_param('telegram', 'help_message')
        self.cache = redis.StrictRedis(host=self.config.read_param('redis', 'host'),
                                       port=self.config.read_param('redis', 'port'),
                                       db=0)

    # общий обработчик поступающего текста
    def text_handler(self, message):
        # если получил подсеть в cidr
        if re.search(r'((\d){1,3}\.){3}((\d){1,3})\/(\d{1,2})', message):
            try:
                return self.cidr_handler(message)
            except ValueError as e:
                return e
        elif re.search(r'((\d){1,3}\.){3}((\d){1,3})(\s)?-(\s)?((\d){1,3}\.){3}((\d){1,3})', message):
            return self.range_handler(message)
        else:
            return('я умею только подсети считать.')

    # обработчик cidr нотации
    def cidr_handler(self, message):
        net, mask = message.split('/')[0], message.split('/')[1]
        if int(mask) not in range(0, 32):
            raise ValueError('маска не входит допустимый диапазон')
        response = self.cache.get(message)
        if response is None:
            cidr = Cidr()
            binary_subnet = cidr.get_subnet(cidr.net_to_bin(net), cidr.mask_to_bin(int(mask)))
            subnet = cidr.binary_to_ip(binary_subnet)
            binary_broadcast = cidr.get_broadcast(cidr.net_to_bin(net), cidr.mask_to_bin(int(mask)))
            broadcast = cidr.binary_to_ip(binary_broadcast)
            host_min  = cidr.binary_to_ip(cidr.get_host_min(binary_subnet))
            host_max = cidr.binary_to_ip(cidr.get_host_max(binary_broadcast))
            host_count = cidr.get_host_count(int(mask))
            response = "network - {0} \r\n " \
                       "broadcast - {1} \r\n " \
                       "hostmin - {2} \r\n " \
                       "hostmax - {3} \r\n " \
                       "hosts - {4} \r\n".format(subnet,
                                                 broadcast,
                                                 host_min,
                                                 host_max,
                                                 host_count)
            self.cache.set(message, response)
        return response

    # обработчик диапазона
    def range_handler(self, message):
        hostmin, hostmax = message.split('-')[0].strip(), message.split('-')[1].strip()
        response = self.cache.get(message)
        if response is None:
            cidr = Cidr()
            binary_hostmin = cidr.get_host_min(cidr.net_to_bin(hostmin))
            binary_hostmax = cidr.get_host_max(cidr.net_to_bin(hostmax))
            mask = cidr.get_mask_by_range(binary_hostmin, binary_hostmax)
            network = cidr.binary_to_ip(cidr.get_network_by_range(binary_hostmin, binary_hostmax))
            response = "{0}/{1}".format(network, mask)
            self.cache.set(message, response)
        return response
