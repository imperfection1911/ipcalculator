from app.binary import Binary


class Cidr(Binary):

    # перевод сети в двоичный вид
    def net_to_bin(self, net):
        binary = []
        octets = net.split('.')
        for octet in octets:
            binary_octet = self.dec_to_bin(int(octet))
            for bit in binary_octet:
                binary.append(bit)
        return binary

    # получение subnet
    @staticmethod
    def get_subnet(net, mask):
        network = []
        for i in range(0, len(net)):
            network.append(net[i] and mask[i])
        return network

    #  получение broadcast
    @ staticmethod
    def get_broadcast(net, mask):
        broadcast = []
        for i in range(0, len(net)):
            if mask[i] == 0:
                mask[i], net[i] = 1, 1
            broadcast.append(net[i] and mask[i])
        return broadcast

    # получение hostmin
    @staticmethod
    def get_host_min(net):
        host_min = net
        host_min[len(host_min) - 1] += 1
        return host_min

    # получение hostmax
    @staticmethod
    def get_host_max(broadcast):
        host_max = broadcast
        host_max[len(host_max) - 1] -= 1
        return host_max

    # получение кол-ва хостов
    @staticmethod
    def get_host_count(mask):
        return (2 ** (32 - int(mask))) - 2

    # получение маски по диапазону
    @staticmethod
    def get_mask_by_range(host_min, host_max):
        mask = 0
        for i in range(0, 32):
            if host_min[i] == host_max[i]:
                mask += 1
        return mask

    # получение адреса сети по диапазону
    @staticmethod
    def get_network_by_range(host_min, host_max):
        network = []
        i = 0
        while i < 32:
            if host_min[i] == host_max[i]:
                network.append(host_min[i])
            else:
                network.append(0)
            i += 1
        return network
