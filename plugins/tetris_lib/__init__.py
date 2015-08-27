import os
import json

class TetrisConfig():
    def __init__(self, path):
        self.path = path
        if not os.path.isfile(self.path):
            self.config = self.check({})
            self.save()
        else:
            self.config = self.check(self.load())
            
    def check(self, config):
        """makes sure all used values are in the dict, otherwise sets defaults"""
        default = {"fallspeed" : 1000,
                   "fallspeed_increment" : 2000,
                   "height" : 40,
                   "width" : 10,
                   "squaresize" : 21,
                   "colors" : [(255 ,255, 0), (255,255,255), (255,0,0), (0,255,0), (0,0,255), (255 ,0, 255), (0 ,255, 255)],
                   "pieces" : [
                             [
                              [1],
                              [1],
                              [1],
                              [1]
                             ],
                             [
                              [1, 1],
                              [1],
                              [1],
                              #[1]
                             ],
                             [
                              [1, 1],
                              [0, 1],
                              [0, 1],
                              #[0, 1]
                             ],
                             [
                              [1, 1],
                              [1, 1]
                             ],
                             [
                              [0, 1],
                              [1, 1],
                              [1, 0]
                             ],
                             [
                              [1, 0],
                              [1, 1],
                              [1, 0]
                             ],
                             [
                              [1, 0],
                              [1, 1],
                              [0, 1]
                             ]
                              ]}
        
        for k,v in default.items():
            if not (k in config):
                config[k] = v
        
        return config
                
    def save(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.config, indent=4, sort_keys=True))
    
    def load(self):
        with open(self.path, "r") as f:
            return json.loads(f.read())