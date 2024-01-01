from OpenGL.GL import *
import pygame as pg
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr, math

class MeshColored: 
    def __init__(self, filename):
        verticies = self.loadMesh(filename)
        self.vertexCount = len(verticies)//8
        verticies = np.arra(verticies,dtype = np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, verticies.nbytes, verticies, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))
    
    def loadMesh(self, filename):
        self.objectList= self.getObjects(filename)
        
        self.materialData = self.getMaterial(filename)
        self.objectsWithMaterialUsed = self.matchMaterial(filename)

        objInMesh = []

        for obj in self.objectList:
            objV= self.getVertexData(filename, obj)
            objVn = self.getVN(filename,obj)
    
    def matchMaterial(self, filename):
        with open(filename, "r") as file:
            line = file.readline()
            word = line.split(" ")
            objectSighted = False
            matched = {}
            while line:
                if word[0] == "o":
                    objectSighted = True
                    currObj = word[1]
                if word[0] == "usemtl" and objectSighted:
                    matched[currObj] = word[1]
                    objectSighted = False
            return matched

    def getVertexData(self, filename, obj):
        verticies = []
        v = []
        vn = []
        with open(filename, "r") as file:
            line = file.readline()
            words = line.split(" ")

            while line:
                if words[0] == "o" and readV:
                    return verticies
                if words[1] == obj:
                    readV = True
                if words[0] == "v":
                    v.append(self.read3Data(words))
                if words[0] == "vn":
                    vn.append(self.read3Data(words))
                if words[0] == "f":
                    self.readFaceData(words,v, vn, verticies)
                
    def readFaceData(self, words: list[str], v:list[list[float]],
                     vn:list[list[float]], verticies:list[float]) -> None:
        
        triangleCount = len(words)-3
        
        for i in range(triangleCount):
            self.makeCorner(words[1],v,vt,vn,verticies)
            self.makeCorner(words[2+i],v,vt,vn,verticies)
            self.makeCorner(words[3+i],v,vt,vn,verticies) #we have been here

    def read3Data(self, words: list[str]) -> list[float]:
        return [
            float(words[1]),
            float(words[2]),
            float(words[3])
        ]                
                

    
    def getMaterial(self, filename):
        mtlFilename = self.getMTLFilename(filename)
        materialData = self.getMTLData(mtlFilename)
        return materialData
    
    def getMTLData(self, mtlFilename):
        with open(mtlFilename, "r") as file:
            line = file.readline()
            word = line.split(" ")
            emptyColorFlag = False
            materials = {}
            while line:
                if word[0] == "newmtl" and emptyColorFlag: # If previosu do not provided Kd
                    materials.keys()[-1] = [0,0,0]
                    currentMaterial = word[1]
                    materials[word[1]] = []
                elif word[0] == "newmtl" and not emptyColorFlag: # New material spotted
                    materials[word[1]] = []
                    currentMaterial = word[1]
                    emptyColorFlag = True
                if word[0] == "Kd": # Get data from that and apply to current key

                    materials[currentMaterial] = [word[1],word[2],word[3]]
                    emptyColorFlag = False
            return materials
                

    def getMTLFilename(self,filename):
        with open(filename, "r") as file:
            line = file.readline()
            word = line.split(" ")

            while line:
                if word[0] == "mtllib":
                    return word[1]
    
    def getObjects(self, filename):
        with open(filename, "r") as file:
            line = file.readline()
            objects = []

            words = line.split(" ")
            while line:
                if words[0] == "o":
                    objects.append(words[1])
            return objects
                

class MeshTextured:
    def __init__(self, filename):
        verticies = self.loadMesh(filename)
        self.vertex_count = len(verticies)//8
        verticies = np.array(verticies, dtype=np.float32)
        
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER, verticies.nbytes, verticies, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    
    def loadMesh(self, filename: str) -> list[float]:
        verticies = []
        v = []
        vt = []
        vn = []
        with open(filename, "r") as file:
            line = file.readline()

            while line:
                words = line.split(" ")
                if words[0] == "v":
                    v.append(self.readVertexData(words))
                elif words[0] == "vt":
                    vt.append(self.readTexCoordData(words))
                elif words[0] == "vn":
                    vn.append(self.readNormalData(words))
                elif words[0] == "f":
                    self.readFaceData(words,v,vt, vn, verticies)
                else:
                    pass
                line = file.readline()

        return verticies

    def readVertexData(self, words: list[str]) -> list[float]:
        return [
            float(words[1]),
            float(words[2]),
            float(words[3])
        ]
    def readTexCoordData(self, words: list[str]) -> list[float]:
        return [
            float(words[1]),
            float(words[2])
        ]
    def readNormalData(self, words: list[str]) -> list[float]:
        return [
            float(words[1]),
            float(words[2]),
            float(words[3])
        ]
    def readFaceData(self, words: list[str], v:list[list[float]], vt:list[list[float]], 
                     vn:list[list[float]], verticies:list[float]) -> None:
        triangleCount = len(words)-3
        
        for i in range(triangleCount):
            self.makeCorner(words[1],v,vt,vn,verticies)
            self.makeCorner(words[2+i],v,vt,vn,verticies)
            self.makeCorner(words[3+i],v,vt,vn,verticies)

    def makeCorner(self, cornerDescription: str, v:list[list[float]], vt:list[list[float]], 
        vn:list[list[float]], verticies:list[float]) -> None:
        """
        Data of the faces is collection of relevant information about verticy
        Later before putting it in buffer (vbo), we can address which data to use by defining adequate 
        vertexAttribPointers in positions that will relate to object data that we will use

        so 
        v is the position
        vt is texture coordinate on face
        vn is normals for lighting 

        and color is processed serparetly, and joined in data just before dumping in the buffer
        """
        v_vt_vn = cornerDescription.split("/")
        for i, space in enumerate(v_vt_vn):
            if space == '':
                v_vt_vn[i] = '0'
        for element in v[int(v_vt_vn[0])-1]: 
            verticies.append(element)
        try:
            for element in vt[int(v_vt_vn[1])-1]:
                verticies.append(element)
        except Exception:
            pass
        for element in vn[int(v_vt_vn[2])-1]:
            verticies.append(element)
        

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1,(self.vbo,))

        
class Cube:

    def __init__(self, position, eulers):

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)


class App:
    def __init__(self):
        pg.init()
        pg.display.set_mode((640,480),pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.tickCount = 0
        glClearColor(0, 0, 0, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        self.shader = self.createShader("shaders/vertex","shaders/fragment")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"),0) # 1 intiger to uniform location and throwing 0 to sampler (you are sampling texture 0 in case if we have more textures here)
        self.cube = Cube(
            position=[0,0,-4],
            eulers= [0,45,0]
        )
        if self.material == 1:
            self.cube_mesh = MeshTextured("objects/stitch.obj")
        elif self.material == 0:
            self.cube_mesh = MeshColored("objects/stitch.obj")

        self.texture = MaterialTex("textures/tex1.jpg")

        self.color = MaterialColor("objects/stitcth.mtl")

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 640/480,
            near = 0.1, far = 10, dtype = np.float32
        )

        glUniformMatrix4fv(
            glGetUniformLocation(self.shader,"projection"), #location of projection uniform
            1,GL_FALSE,projection_transform
        ) #send matrix to uniform

        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model") #save model location to use every frame

        self.mainloop()

    def createShader(self, vertexFilePath, fragmentFilePath):

        with open(vertexFilePath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilePath, 'r') as f:
            fragment_sec = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_sec, GL_FRAGMENT_SHADER)
        )

        return shader
    
    def mainloop(self):

        running = True
        translation_vectors = [0,0,0,1,1,1] #X,Y,Z,Pitch,Yaw,Roll
        translate = [False, False] # flag, done
        circular_translate = [0, 0.01, 1.1] #initial angle, angular speed, radius
        while(running):
            self.tickCount += 1
            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        running = False
                    case pg.KEYDOWN:
                        if translate[0]:
                            translate = [False, True]
                        
                        elif not translate[0]:
                            translate[0] = True
                        
                    case _:
                        pass
            
            if circular_translate[0] >= 360:
               circular_translate[0] -= 360
            if translate[0]:
                self.cube.position[0] = 1 // 2 + circular_translate[2] * math.cos(circular_translate[0])
                self.cube.position[1] = 1 // 2 + circular_translate[2] * math.sin(circular_translate[0])
                circular_translate[0] += circular_translate[1]
                
            


            
            self.cube.eulers[2] += translation_vectors[5]
            if (self.cube.eulers[2] > 360):
                self.cube.eulers[2] -=360
            self.cube.eulers[1] += translation_vectors[4]
            if (self.cube.eulers[1] > 360):
                self.cube.eulers[1] -=360
            self.cube.eulers[0] += translation_vectors[3]
            if (self.cube.eulers[0] > 360):
                self.cube.eulers[0] -=360
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glUseProgram(self.shader)
            self.texture.use()

            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1 = model_transform,
                m2 = pyrr.matrix44.create_from_eulers(
                    eulers = np.radians(self.cube.eulers),
                    dtype = np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1 = model_transform,
                m2 = pyrr.matrix44.create_from_translation(
                    vec = self.cube.position,
                    dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)
            pg.display.flip()

            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.cube_mesh.destroy()
        self.texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class MaterialTex:


    def __init__(self,filepath):
        self.texture = glGenTextures(1) # Num Of textures needed
        glBindTexture(GL_TEXTURE_2D, self.texture) # Binding now with gpu package
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # Positions of 2D Textures, with repeat if we get bigger thingy
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST) # Smaller texture needed? Downsapmple it
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # We need bigger texture ? Linearly scale it

        image = pg.image.load(filepath).convert() #load image and convert to "device friendly pixel format"
        image_width, image_height = image.get_rect().size # get_rectangle
        image_data = pg.image.tostring(image, "RGBA") #make image data to string nice and simple

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0,GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        #           (texturelocation, mipmap level, internal format, width,height, border color?, format of data, data format, actual data of image)
        glGenerateMipmap(GL_TEXTURE_2D)
        # generate image

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        #we can load multiple textures or maps like lightmap
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1,(self.texture,))

class MaterialMtl:
    def __init__(self) -> None:
        
if __name__ == "__main__":
    myApp = App()