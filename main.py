import pygame
import numpy as np
import pygame.color as Color
import utils.matrixs as matrixs
from utils.camera import Camera
from utils.reader import RenderBuffer, ObjReader

def main():

    objreader = ObjReader("./models/cube.obj")
    renderBuffer = objreader.parse()

    print(renderBuffer)

    pygame.init()

    # Set up the display
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    camera = Camera(
        fov=90, 
        zfar=1000, 
        znear= 1, 
        width= screen_width, 
        height=screen_height
    )
    
    pygame.display.set_caption("Pygame Draw Point")

    angle = 0



    WHITE:Color = (255, 255, 255)
    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
  
        angle += 0.001

        screen.fill(WHITE)
        #dt = clock.tick(60) / 1000.0
        projMat = matrixs.projection(camera)
        render(
            screen= screen, 
            rotation_angle=angle, 
            renderBuffer=renderBuffer, 
            projMat=projMat, 
            camera=camera
        )
        # Get delta time in milliseconds and convert to seconds (float)
        
        #updates the next frame
        pygame.display.flip()

    pygame.quit()


def draw_triangle(screen, projected_points, color=(255,255,255)):
    width, height = screen.get_size()
    screen_points = []

    for p in projected_points:
        # p is gonna be of the form [x, y, z, w]
        # We then normalize x and y with z to fit it onto R^2
        if p[3] != 0:
            x_ndc = p[0] / p[3]  # Normalize x via x' = x/z
            y_ndc = p[1] / p[3]  # Normalize y via y' = y/z
        else:
            x_ndc, y_ndc = 0, 0
        

        # convert from normalized device coords (-1..1) to screen coordinates
        x_screen = int((x_ndc + 1) * 0.5 * width)
        y_screen = int((1 - (y_ndc + 1) * 0.5) * height)  # flip y-axis
        screen_points.append((x_screen, y_screen))

    # draw triangle lines
    print(f"-----------\n{screen_points}")
    pygame.draw.line(screen, color, screen_points[0], screen_points[1])
    pygame.draw.line(screen, color, screen_points[1], screen_points[2])
    pygame.draw.line(screen, color, screen_points[2], screen_points[0])

def render(screen, renderBuffer:RenderBuffer, rotation_angle: float, projMat: np.matrix , camera: Camera):
    for tris in renderBuffer.tris:
        p1 = renderBuffer.verts[tris[0]]
        p2 = renderBuffer.verts[tris[1]]
        p3 = renderBuffer.verts[tris[2]]

        # This takes our non projected points 
        
        tri:list[np.ndarray] = [p1.copy(), p2.copy(), p3.copy()]

        rotate_z_mat = matrixs.rotate_z(rotation_angle)
        rotate_x_mat = matrixs.rotate_x(rotation_angle)
        rotate_y_mat = matrixs.rotate_y(rotation_angle)
        
        #rotate 
        for (i, p) in enumerate(tri):
            tri[i] = rotate_y_mat @ rotate_x_mat @ rotate_z_mat @ p    
        
        # translate
        for (i, _) in enumerate(tri): 
            tri[i] = tri[i] - np.array([0, 0, 2, 0]) 

        #points for rendering
        projected_points = np.stack([
            projMat @ tri[0],
            projMat @ tri[1],
            projMat @ tri[2]
        ])

        #draw the projected points on the screen
        draw_triangle(screen, projected_points, color=(255,0,0))

if __name__ == "__main__":
    main()
