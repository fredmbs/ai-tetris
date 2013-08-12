# -*- coding:utf-8 -*-

import cPickle

class Tetromino:
    """ Class that handles the game current tetromino 
    
        Tetromino : 
        
                A tetromino is a geometric shape composed of four squares, 
            connected orthogonally. This, like dominoes and pentominoes, is a 
            particular type of polyomino. The corresponding polycube, called a 
            tetrocube, is a geometric shape composed of four cubes connected 
            orthogonally.
            
            A popular use of tetrominos is in the video game Tetris, where 
            they are often called Tetriminos.
            
        Reference : 
        
            http://en.wikipedia.org/wiki/Tetromino
            
        In the Tetris software modelation, each of the five Tetrominos have a
        symbol and name like described below:
        
        symbol         name
        --------- | --------------
        I        ->    stick
        O        ->    square
        T        ->    T
        J        ->    J
        L        ->    gun
        S        ->    inverted N
        Z        ->    snake
    """
    
    # Private Attribute that represents the shape of the Tetrominos
    SHAPE = [ 
                [ # Shape NONE
                  [ # Default Rotation 
                    [0,0],[0,0],[0,0],[0,0]     #,0 
                  ] 
                ],
                [ # Shape 0 
                  [ # Default Rotation 
                    [-1,-1],[-1,0],[0,-1],[0,0] #,2 
                  ] 
                ],
                [ # Shape I
                  [ # Default Rotation 
                    [0,-2],[0,-1],[0,0],[0,1]   #,4
                  ],
                  [ # 90 degrees Rotation 
                    [-2,0],[-1,0],[0,0],[1,0]   #,1
                  ]
                ],
                [ # Shape S
                  [ # Default Rotation 
                    [-1,-1],[-1,0],[0,1],[0,0]  #,3
                  ],
                  [ # 90 degrees Rotation 
                    [-1,1],[0,0],[0,1],[1,0]    #,2
                  ]
                ],
                [ # Shape Z
                  [ # Default Rotation 
                    [-1,1],[-1,0],[0,-1],[0,0] #,3
                  ],
                  [ # 90 degrees Rotation 
                    [-1,0],[0,1],[0,0],[1,1]    #,2
                  ]
                ],
                [ # Shape L
                  [ # Default Rotation 
                    [-1,-1],[0,0],[0,1],[0,-1]  #,3
                  ],
                  [ # 90 degrees Rotation 
                    [-1,1],[-1,0],[0,0],[1,0]   #,2
                  ],
                  [ # 180 degrees Rotation 
                    [0,-1],[0,0],[0,1],[1,1]    #,3
                  ],
                  [ # 270 degrees Rotation 
                    [-1,0],[1,-1],[0,0],[1,0]   #,2
                  ]
                ],
                [ # Shape J
                  [ # Default Rotation 
                    [-1,1],[0,-1],[0,0],[0,1]   #,3
                  ],
                  [ # 90 degrees Rotation 
                    [-1,0],[1,1],[0,0],[1,0]    #,2
                  ],
                  [ # 180 degrees Rotation 
                    [0,1],[0,0],[0,-1],[1,-1]   #,3
                  ],
                  [ # 270 degrees Rotation 
                    [-1,-1],[-1,0],[0,0],[1,0]  #,2
                  ]
                ],
                [ # Shape T
                  [ # Default Rotation 
                    [-1,0],[0,-1],[0,1],[0,0]   #,3
                  ],
                  [ # 90 degrees Rotation 
                    [-1,0],[0,1],[0,0],[1,0]    #,2
                  ],
                  [ # 180 degrees Rotation 
                    [0,-1],[0,0],[0,1],[1,0]    #,3
                  ],
                  [ # 270 degrees Rotation 
                    [-1,0],[0,-1],[0,0],[1,0]   #,2
                  ]
                ]
              ]

    FACE = [ 
                [ 
                  0 
                ],
                [ # Shape 0 
                  2 
                ],
                [ # Shape I
                  4,1
                ],
                [ # Shape S
                  3,2
                ],
                [ # Shape Z
                  3,2
                ],
                [ # Shape L
                  3,2,3,2
                ],
                [ # Shape J
                  3,2,3,2
                ],
                [ # Shape T
                  3,2,3,2
                ]
              ]
    
    HEIGHT = [ 
                [ 
                  0 
                ],
                [ # Shape 0 
                  2 
                ],
                [ # Shape I
                  1,4
                ],
                [ # Shape S
                  2,3
                ],
                [ # Shape Z
                  2,3
                ],
                [ # Shape L
                  2,3,2,3
                ],
                [ # Shape J
                  2,3,2,3
                ],
                [ # Shape T
                  2,3,2,3
                ]
              ]

    ROTATIONS = [ 
                  [], 
                  [0], 
                  [0,1], 
                  [0,1], 
                  [0,1], 
                  [0,1,-1,2],
                  [0,1,-1,2],
                  [0,1,-1,2]
                ]
    
    
    def __init__(self, tretroType = 0, row = 2, col = 2):
        self.changeTetromino(tretroType, row, col)
        
    def getType(self):
        return self.__type
    
    def getRotation(self):
        """ Getter method that returns the current shape rotation """
        return self.__rotation

    def getPosition(self):
        """ Getter method that returns the current position """
        return self.__row, self.__col
    
    def setPosition(self, row, col):
        self.__row = row
        self.__col = col
        
    def getShape(self):
        """ Getter method that returns the shape reference """
        return self.__shape[:]
    
    def getShapeRotation(self, rotation):
        r = rotation%len(Tetromino.SHAPE[self.__type])
        return Tetromino.SHAPE[self.__type][r]

    def getInfo(self, r):
        return self.__type, self.__row, self.__col, \
               Tetromino.SHAPE[self.__type][r]
    
    def getCopy(self):
        return cPickle.loads(cPickle.dumps(self, -1))
    
    def getRotations(self):
        return len(Tetromino.SHAPE[self.__type])
    
    def getHeight(self):
        return Tetromino.HEIGHT[self.__type][self.__rotation]

    def getHeightRotation(self, rotation):
        r = rotation%len(Tetromino.SHAPE[self.__type])
        return Tetromino.HEIGHT[self.__type][r]
    
    def changeTetromino(self, tetroType, row, col):
        """ Sets the type of the shape  
        
            Parameters:
                tetroType : An integer value to define the shape type
        """
        self.__row = row
        self.__col = col
        self.__type = tetroType
        self.__shape = Tetromino.SHAPE[self.__type][0]
        self.__rotation = 0
        return [[i[0] + self.__row, i[1] + self.__col] 
                          for i in self.__shape]
    
    def changeRotation(self, rotation):
        """ Method that changes the shape rotation values on the
            private variables
        
            Parameters:
                rotation : especify the relative position of shape based
                           on it's rotation restrictions
        """
        r = rotation%len(Tetromino.SHAPE[self.__type])
        self.__shape = Tetromino.SHAPE[self.__type][r]
        self.__rotation = r
        return r

    def addRotation(self, plus):
        """ Make the shape rotation
        
            Parameters:
                plus : An integer that defines the shape rotation based
                       on the shape rotation position
        """
        return self.changeRotation(self.__rotation + plus)

    def getShapeAt(self):
        return [[i[0] + self.__row, i[1] + self.__col] for i in self.__shape]

    def getShapeAtPosition(self, row, col):
        """ Getter method that returns the shape in position x, y """
        shape = self.__shape[:]
        return [[i[0] + row, i[1] + col] for i in shape]

    def getShapeAtRotation(self, row, col, rotation):
        """ Getter that returns the shape of rotation in position x, y """
        r = rotation%len(Tetromino.SHAPE[self.__type])
        shape = Tetromino.SHAPE[self.__type][r][:]
        return [[i[0] + row, i[1] + col] for i in shape]

    @staticmethod
    def getBoundingRectangle(shape):
        maxRow = minRow = shape[0][0]
        maxCol = minCol = shape[0][1]
        for i in shape:
            row = i[0]
            col = i[1]
            if (col < minCol): minCol = col
            if (row < minRow): minRow = row
            if (col > maxCol): maxCol = col
            if (row > maxRow): maxRow = row
        return minRow, minCol, maxRow, maxCol
    