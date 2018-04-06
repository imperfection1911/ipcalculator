class Binary:

    # перевод из десятично в двоичную
    @staticmethod
    def dec_to_bin(dec):
        binary = []
        while dec > 0:
            # добавить остаток от деления на 2
            binary.append(dec % 2)
            dec //= 2
        # добавить нулей, если результат "короче" 8
        while len(binary) < 8:
            binary.append(0)
        # перевернуть список. получаем октет в двоичном виде
        binary.reverse()
        return binary

    # перевод из двоичной в десятичную
    @staticmethod
    def bin_to_dec(binary):
        result = []
        counter = 0
        while counter < len(binary):
            octet = []
            # считаем до 8
            while len(octet) < 8:
                octet.append(binary[counter])
                counter += 1
            grade = 7
            octet_dec = 0
            # переводим октет в десятичную
            for i in octet:
                octet_dec += i * (2 ** grade)
                grade -= 1
            result.append(octet_dec)
        return result

    # перевод маски в двоичный вид
    @staticmethod
    def mask_to_bin(mask):
        binary_mask = []
        counter = 0
        while counter < int(mask):
            binary_mask.append(1)
            counter += 1
        while len(binary_mask) < 32:
            binary_mask.append(0)
        return binary_mask

    # перевод bin ip в десятичный вид
    def binary_to_ip(self, binary_ip):
        # ip в десятичном виде
        dec_ip = []
        # октет для перевода в десятичный вид
        octet = []
        # счетчик октета
        octet_counter = 0
        i = 0
        while i < len(binary_ip) - 1:
            while octet_counter < 8:
                octet.append(binary_ip[i + octet_counter])
                octet_counter += 1
            i += octet_counter
            dec_ip.append(self.bin_to_dec(octet)[0])
            octet_counter = 0
            octet = []
        ip = ('.'.join(map(str, dec_ip)))
        return ip
