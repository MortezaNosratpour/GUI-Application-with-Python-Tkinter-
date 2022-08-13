# All methods that use for processing the paramerers of CAN protocol:
# "EGR position sensor voltage", "Intake manifold absolute pressure sensor voltage",
# "Accelerator pedal position 1 voltage", "Accelerator pedal position 1 voltage",
# "Throttle position 1 voltage", "Throttle position 2 voltage"

def unsigned_hex_string_to_decimal(response):
    dictionary_hexa_to_decimal = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10,
                                  'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    decimal = 0
    length = len(response)-1

    for digit in response:
        decimal += dictionary_hexa_to_decimal[digit] * 16 ** length
        length -= 1

    return decimal


def signed_hex_string_to_decimal(response):
    if response[0]!="8" and response[0]!="9" and response[0]!="A" and response[0]!="B" and response[0]!="C" and response[0]!="D" and response[0]!="E" and response[0]!="F":
        return unsigned_hex_string_to_decimal(response)
    else:
        length = len(response)
        oor=2**((length*4))
        remain=oor-unsigned_hex_string_to_decimal(response)
        decimal=-1*remain
        return decimal


def times_divided(decimal, time, divided):
    phy = (decimal * time)/divided
    return phy


def subtract_value(decimal, value):
    return decimal-value



def params_times5_dividedby255(response):
    decimal=unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 5., 255.)
    return phy



def params_030A_032F(response):
    decimal=unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 1., 10.)
    return phy


def params_030B_to_030C(response):
    decimal=unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 1110., 255.)
    return phy


def params_0316_0319_0331_to_0335_0338_033A_to_033B_033F(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy = times_divided(decimal, 1., 2.55)
    return phy


def params_0317(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy = times_divided((decimal+28), 1., 2.71)
    return phy


def params_0318_031D_0329_032C_0343_0344(response):
    decimal = unsigned_hex_string_to_decimal(response)
    return decimal


def params_0318_031A(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy = times_divided(decimal, 1., 512.)
    return phy


def params_031B(response):
    decimal = signed_hex_string_to_decimal(response)
    phy=times_divided(decimal, 1., 4096.)
    return phy


def params_031C(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 100., 32768.)
    return phy


def params_031F_to_0322(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=subtract_value(decimal, 40.)
    return phy


def params_0327_to_0328(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=subtract_value(decimal, 127.)
    return phy


def params_032A(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 0.25, 1.)
    return phy


def params_032B_032D(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 1., 128.)
    return phy


def params_032E(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 1., 65.535)
    return phy


def params_0336(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 0.5, 1)
    phy=subtract_value(phy, 64)
    return phy


def params_0337(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 100., 4096.)
    return phy


def params_0339(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 1., 2.)
    return phy


def params_033D(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 3., 1.)
    phy = subtract_value(phy, -300)
    return phy


def params_033E(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 3200., 255.)
    return phy


def params_0340(response):
    decimal = unsigned_hex_string_to_decimal(response)
    phy=times_divided(decimal, 1., 64.)
    return phy


