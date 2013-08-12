# -*- coding:utf-8 -*-

class TetrisGenomeExample:
    ## https://github.com/ielashi/eltetris/blob/master/src/eltetris.js
    Eltetris_ID = "Eltetris"
    Eltetris = {"PileHeight"        : -0.0,
                "LandingHeight"     : -4.500158825082766,
                "ErodedRows"        : +3.4181268101392694,
                "RowTransitions"    : -3.2178882868487753,
                "ColumnTransitions" : -9.348695305445199,
                "ColumnBuriedHoles" : -7.899265427351652,
                "ColumnWells"       : -3.3855972247263626}
    
    ## http://www.colinfahey.com/tetris/tetris_en.html
    PD_ID = "Pierre Dellacherie"      
    PD = {"PileHeight"        : -0.0,
          "LandingHeight"     : -1.0,
          "ErodedMetric"      : +1.0,
          "RowTransitions"    : -1.0,
          "ColumnTransitions" : -1.0,
          "ColumnBuriedHoles" : -4.0,
          "ColumnWells"       : -1.0}
    
    ## http://hal.inria.fr/docs/00/41/89/30/PDF/article.pdf
    '''
    Feature Symbol Weight
    Landing height      l  -12.63
    Eroded Piece Cells  e  6.60
    Row transitions     ∆r -9.22
    Column transitions  ∆c -19.77
    Holes               L  -13.08
    Board wells         W  -10.49
    Hole depth          D  -1.61
    Rows with holes     R  -24.04
    '''      
    ThieryScherrer_ID  = "ThieryScherrer"
    ThieryScherrer    = {"PileHeight"        : -00.00,
                         "LandingHeight"     : -12.60,
                         "ErodedMetric"      : +06.60,
                         "RowTransitions"    : -09.22,
                         "ColumnTransitions" : -19.77,
                         "ColumnBuriedHoles" : -13.08,
                         "ColumnWells"       : -10.49}
    
    
    PyEvolve1_ID = "PyEvolve1"
    PyEvolve1 = {"PileHeight"        : -0.6903200846016033,
                 "LandingHeight"     : -48.397173471721274,
                 "ErodedPieces"      : 29.57801575198271,
                 "ErodedRows"        : 4.947969428674859,
                 "ErodedMetric"      : 0.9258831965633374,
                 "RowTransitions"    : -24.337463194268338,
                 "ColumnTransitions" : -72.90931022325682,
                 "ColumnBuriedHoles" : -93.26927285333721,
                 "ColumnWells"       : -38.827245269520624 }

    SZ_ID = "SZ"
    SZ = {"PileHeight"        : 99.68460465396407,
          "LandingHeight"     : -45.73430286504265,
          "ErodedPieces"      : 31.79062306116279,
          "ErodedRows"        : 98.20340577309378,
          "ErodedMetric"      : -9.285784921471944,
          "RowTransitions"    : 13.506876614498339,
          "ColumnTransitions" : -93.51310760128506,
          "ColumnBuriedHoles" : -54.45437830207589,
          "ColumnWells"       : -88.03546571266037}
    
    PyEvolve9_ID = "PyEvolve9"
    PyEvolve9 = {"PileHeight"        : 5.671504912205824,
                 "LandingHeight"     : -9.49592892788563,
                 "ErodedPieces"      : 2.01539413359251,
                 "ErodedRows"        : -8.37674001734818,
                 "ErodedMetric"      : 2.9089163698839204,
                 "RowTransitions"    : -2.3118950065170125,
                 "ColumnTransitions" : -8.932548918392895,
                 "ColumnBuriedHoles" : -8.247085669016204,
                 "ColumnWells"       : -2.8006237653192523}

