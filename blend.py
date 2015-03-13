bnone = [(9 * 18, 3 * 18), (10 * 18, 3 * 18), (11 * 18, 3 * 18)]
bleft = [(0, 0), (0, 18), (0, 2 * 18)]
bright = [(72, 0), (72, 18), (72, 18 * 2)]
bup = [(18, 0), (18 * 2, 0), (18 * 3, 0)]
bdown = [(18, 2 * 18), (18 * 2, 2 * 18), (18 * 3, 2 * 18)]
bcenter = [(18, 18), (2 * 18, 18), (3 * 18, 18)]
bleftstick = [(9 * 18, 0), (9 * 18, 18), (9 * 18, 2 * 18)]
brightstick = [(12 * 18, 0), (12 * 18, 18), (12 * 18, 2 * 18)]
bupstick = [(6 * 18, 0), (7 * 18, 0), (8 * 18, 0)]
bdownstick = [(6 * 18, 3 * 18), (7 * 18, 3 * 18), (8 * 18, 3 * 18)]
bvertical = [(5 * 18, 0), (5 * 18, 18), (5 * 18, 2 * 18)]
bhorizontal = [(6 * 18, 4 * 18), (7 * 18, 4 * 18), (8 * 18, 4 * 18)]
bdr = [(0, 3 * 18), (2 * 18, 3 * 18), (4 * 18, 3 * 18)]
bdl = [(18, 3 * 18), (3 * 18, 3 * 18), (5 * 18, 3 * 18)]
bul = [(18, 4 * 18), (3 * 18, 4 * 18), (5 * 18, 4 * 18)]
bur = [(0, 4 * 18), (2 * 18, 4 * 18), (4 * 18, 4 * 18)]

BNONE = 0
BLEFT = 1
BRIGHT = 2
BUP = 3
BDOWN = 4
BCENTER = 5
BLEFTSTICK = 6
BRIGHTSTICK = 7
BUPSTICK = 8
BDOWNSTICK = 9
BVERTICAL = 10
BHORIZONTAL = 11
BDR = 12
BDL = 13
BUL = 14
BUR = 15

assign = {
    (1, 1, 1, 1): BCENTER,
    (0, 1, 0, 0): BLEFTSTICK,
    (1, 0, 0, 0): BRIGHTSTICK,
    (0, 0, 0, 1): BUPSTICK,
    (0, 0, 1, 0): BDOWNSTICK,
    (0, 0, 0, 0): BNONE,
    (0, 1, 1, 1): BLEFT,
    (1, 0, 1, 1): BRIGHT,
    (1, 1, 0, 1): BUP,
    (1, 1, 1, 0): BDOWN,
    (0, 0, 1, 1): BVERTICAL,
    (1, 1, 0, 0): BHORIZONTAL,
    (0, 1, 0, 1): BDR,
    (1, 0, 0, 1): BDL,
    (1, 0, 1, 0): BUL,
    (0, 1, 1, 0): BUR,
}

result = {BCENTER: bcenter,
          BLEFT: bleft,
          BRIGHT: bright,
          BUP: bup,
          BDOWN: bdown,
          BNONE: bnone,
          BLEFTSTICK: bleftstick,
          BRIGHTSTICK: brightstick,
          BUPSTICK: bupstick,
          BDOWNSTICK: bdownstick,
          BVERTICAL: bvertical,
          BHORIZONTAL: bhorizontal,
          BDR: bdr,
          BDL: bdl,
          BUL: bul,
          BUR: bur,


          }
mix = {}
for key in assign:
    mix[key] = result[assign[key]]
wmix = {}
for key in assign:
    x, y, z = result[assign[key]]
    # for s in (x,y,z):
    #    for t in s:
    #        print (t%18)
    wmix[key] = [(x[0] * 2, x[1] * 2),
                 (y[0] * 2, y[1] * 2),
                 (z[0] * 2, z[1] * 2)]
del (result, assign)
