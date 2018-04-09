import unittest

from app.binary import Binary
from app.cidr import Cidr


class Test(unittest.TestCase):

    # тест метода dec_to_bin из Binary
    def test_binary_dec_to_bin(self):
        binary = Binary()
        call_result = binary.dec_to_bin(192)
        result = int(''.join(map(str, call_result)))
        self.assertEqual(result, 11000000)

    # тест метода bin_to_dec Binary
    def test_binary_bin_to_dec(self):
        binary = Binary()
        call_result = binary.bin_to_dec([1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        result = '.'.join(map(str, call_result))
        self.assertEqual(result, '192.168.0.1')

    # тест метода mask_to_bin Binary
    def test_mask_to_bin(self):
        binary = Binary()
        call_result = binary.mask_to_bin(24)
        result = int(''.join(map(str, call_result)))
        self.assertEqual(result, 11111111111111111111111100000000)

    # тест метода net_to_bin Cidr
    def test_net_to_bin(self):
        cidr = Cidr()
        binary_net = cidr.net_to_bin('192.168.16.100')
        result = int(''.join(map(str, binary_net)))
        self.assertEqual(result, 11000000101010000001000001100100)

    # тест метода get_subnet Cidr
    def test_get_subnet(self):
        cidr = Cidr()
        network = cidr.get_subnet(cidr.net_to_bin('192.168.16.100'), cidr.mask_to_bin(22))
        result = int(''.join(map(str, network)))
        self.assertEqual(result, 11000000101010000001000000000000)

    # тест метода get_broadcast Cidr
    def test_get_broadcast(self):
        cidr = Cidr()
        broadcast = cidr.get_broadcast(cidr.net_to_bin('192.168.16.100'), cidr.mask_to_bin(22))
        result = int(''.join(map(str, broadcast)))
        self.assertEqual(result, 11000000101010000001001111111111)

    # тест метода get_host_min Cidr
    def test_get_host_min(self):
        cidr = Cidr()
        hostmin = cidr.get_host_min(cidr.get_subnet(cidr.net_to_bin('192.168.16.100'), cidr.mask_to_bin(22)))
        ip = cidr.binary_to_ip(hostmin)
        self.assertEqual(ip, '192.168.16.1')

    # тест метода get_host_max Cidr
    def test_get_host_max(self):
        cidr = Cidr()
        hostmax = cidr.get_host_max(cidr.get_broadcast(cidr.net_to_bin('192.168.16.100'), cidr.mask_to_bin(22)))
        ip = cidr.binary_to_ip(hostmax)
        self.assertEqual(ip, '192.168.19.254')

    # тест метода get_host_count
    def test_get_host_count(self):
        cidr = Cidr()
        host_count = cidr.get_host_count(22)
        self.assertEqual(host_count, 1022)

    # тест метода get_mask_by_range
    def test_get_mask_by_range(self):
        cidr = Cidr()
        hostmin = cidr.get_host_min(cidr.get_subnet(cidr.net_to_bin('192.168.16.100'), cidr.mask_to_bin(22)))
        hostmax = cidr.get_host_max(cidr.get_broadcast(cidr.net_to_bin('192.168.16.100'), cidr.mask_to_bin(22)))
        mask = cidr.get_mask_by_range(hostmin, hostmax)
        self.assertEqual(mask, 22)

    # тест метода get_network_by_range
    def test_get_network_by_range(self):
        cidr = Cidr()
        hostmin = cidr.get_host_min(cidr.get_subnet(cidr.net_to_bin('192.168.16.100'), cidr.mask_to_bin(22)))
        hostmax = cidr.get_host_max(cidr.get_broadcast(cidr.net_to_bin('192.168.16.100'), cidr.mask_to_bin(22)))
        network = cidr.get_network_by_range(hostmin, hostmax)
        result = int(''.join(map(str, network)))
        self.assertEqual(result, 11000000101010000001000000000000)

if __name__ == '__main__':
    unittest.main()
