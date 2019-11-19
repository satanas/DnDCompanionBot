import math

CURRENCY_CHART = {
    'pp': {
        'cp': {
            'rate': 1e3,
            'label': "1000"
        },
        'sp': {
            'rate': 100,
            'label': "100"
        },
        'ep': {
            'rate': 20,
            'label': "20"
        },
        'gp': {
            'rate': 10,
            'label': "10"
        },
        'pp': {
            'rate': 1,
            'label': "1"
        }
    },
    'gp': {
        'cp': {
            'rate': 100,
            'label': "100"
        },
        'sp': {
            'rate': 10,
            'label': "10"
        },
        'ep': {
            'rate': 2,
            'label': "2"
        },
        'gp': {
            'rate': 1,
            'label': "1"
        },
        'pp': {
            'rate': .1,
            'label': "1/10"
        }
    },
    'ep': {
        'cp': {
            'rate': 50,
            'label': "50"
        },
        'sp': {
            'rate': 5,
            'label': "5"
        },
        'ep': {
            'rate': 1,
            'label': "1"
        },
        'gp': {
            'rate': .5,
            'label': "1/2"
        },
        'pp': {
            'rate': .05,
            'label': "1/20"
        }
    },
    'sp': {
        'cp': {
            'rate': 10,
            'label': "10"
        },
        'sp': {
            'rate': 1,
            'label': "1"
        },
        'ep': {
            'rate': .2,
            'label': "1/5"
        },
        'gp': {
            'rate': .1,
            'label': "1/10"
        },
        'pp': {
            'rate': .01,
            'label': "1/100"
        }
    },
    'cp': {
        'cp': {
            'rate': 1,
            'label': "1"
        },
        'sp': {
            'rate': .1,
            'label': "1/10"
        },
        'ep': {
            'rate': .02,
            'label': "1/50"
        },
        'gp': {
            'rate': .01,
            'label': "1/100"
        },
        'pp': {
            'rate': .001,
            'label': "1/1000"
        }
    }
}

REVERSED_CHART = ['cp', 'sp', 'ep', 'gp', 'pp']

def decimal_validate(value):
    return not math.isnan(int(value))

def format_coins(r):
    t = {};
    for coin in CURRENCY_CHART:
        t[coin] = int(r[coin]) if decimal_validate(r[coin]) else 0
    return t

def rate(rate):
    return int(rate.split('/')[1]) if '/' in rate else 1

def exchange(target_currency, amount, currency):
    return amount * CURRENCY_CHART[currency][target_currency]['rate']

def modulus(target_currency, amount, currency):
    return amount % rate(CURRENCY_CHART[currency][target_currency]['label'])

def positive_calc(amount, currency, currency_obj):
    for  coin in CURRENCY_CHART:
        if currency == coin:
            currency_obj[currency] = currency_obj[currency] + amount
            return currency_obj[currency]

        exchanged = math.floor(exchange(coin, amount, currency))
        amount = modulus(coin, amount, currency)
        currency_obj[coin] += exchanged

def negative_calc(amount, currency, currency_obj):
    for  coin in REVERSED_CHART:
        if currency == coin:
            currency_obj[currency] = currency_obj[currency] + amount
            if currency_obj[currency] > 0:
                return currency_obj[currency]

        exchanged = math.floor(exchange(coin, amount, currency))
        amount = modulus(coin, amount, currency)

        #currency_obj[coin] += exchanged

def optimal_exchange(coin_args):
    pouch = {}
    for coin in CURRENCY_CHART:
        pouch[coin] = 0;

    formated = format_coins(coin_args);
    for f in formated:
        if formated[f] > 0:
            positive_calc(formated[f], f, pouch);

    for f in formated:
        if formated[f] < 0:
            negative_calc(formated[f], f, pouch);

    return pouch