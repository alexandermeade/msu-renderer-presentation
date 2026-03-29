# The Goal of this Repo
This repo is to give a nice tour of how 3d rendering works. 

# What is a cpu renderer 
A CPU renderer is a primitive style of renderer mostly used to show off how a renderer works without having to worry about implementing the techniques for a GPU. 

There are heavy limitations put ontop of a CPU renderer and I would highly advise against using one for making anything serious. However most of these techniques should carry over if you were to use a tool like [Vulkan](https://www.vulkan.org/) or [OpenGL](https://www.opengl.org/) for GPU rendering. 

# Software Prequisites 
This tutorial was written using the [Python](https://www.python.org/) programming language with the [UV](https://docs.astral.sh/uv/guides/install-python/) package and project manager. 

> You do not need [UV](https://docs.astral.sh/uv/guides/install-python/) to complete this tutorial however python is essential. 


## What is a `.obj` file? 
An `.obj` file is a file type used for 3D models and is an export option in most modern 3D modeling software. For our purposes we'll be using [Blender](https://www.blender.org/) as that software.

In the example of the `cube.obj` file found in the [models](https://github.com/alexandermeade/msu-renderer-presentation/tree/main/models) subdirectory, we can open in it blender and it should look like this

<p align = "center">
  <img width="307" height="276" alt="image" src="https://github.com/user-attachments/assets/4c19b759-5f56-43dd-9ffb-38622da0183c" />
</p>

But we can export this using these settings. 
<p align = "center">
  <img width="262" height="400" alt="image" src="https://github.com/user-attachments/assets/f4a31ea5-342e-4ad0-a8d8-30b43a3c014e" />
</p>

> [!WARNING]
> Make sure to triangulate, if not the faces will generate in different pairings than what we would want.

When done correctly we should get to a result like
```
# Blender 3.6.5
# www.blender.org
o Cube
v 1.000000 1.000000 -1.000000
v 1.000000 -1.000000 -1.000000
v 1.000000 1.000000 1.000000
v 1.000000 -1.000000 1.000000
v -1.000000 1.000000 -1.000000
v -1.000000 -1.000000 -1.000000
v -1.000000 1.000000 1.000000
v -1.000000 -1.000000 1.000000
s 0
f 5 3 1
f 3 8 4
f 7 6 8
f 2 8 6
f 1 4 2
f 5 2 6
f 5 7 3
f 3 7 8
f 7 5 6
f 2 4 8
f 1 3 4
f 5 1 2
```

Looking at this we can pretty quickly see that each line starting with a `v` is gonna be some point in 3D space. Where as every `f` is gonna be some pairings of points to form a triangle. 

The way this cube gets subsected and rerendered back out in triangles looks like this with each triangle highlighted. 

<p align = "center">
  <img width="294" height="285" alt="image" src="https://github.com/user-attachments/assets/e27a2945-ff26-448c-961f-c15807859688" />
</p>

# Math Prerequisites 
As you have probably noticed when building a 3D renderer there is a pretty clear and hard issue that gets presented almost immeditatly.
How do we go from a set of vertexs $\mathbb{R^3}$ into a set of points on a screen $\mathbb{R^2}$. 

To do this we are going to utalize Linear Algebra which is a set of mathematics created for dealing with problems in $n$-th dimensional space via matrixs.

A few things to know about matrixs are the following. 

Matrixs are notated as a set of values within a number of rows and colmns
A $2\times 2$ example of a matrix would look like

$$
  M = \begin{bmatrix}
    1 & 2 \\
    3 & 4 
  \end{bmatrix}
$$

Matrix multiplication has an algoirthm to it and is preformed the way listed in the diagram below
<p align = "center">
  <img width="800" height="400" alt="Multiplication-of-3-by-3-Matrices-01" src="https://github.com/user-attachments/assets/0a96ca9c-3274-4d1d-815f-fb6a00c311dd" />
</p>
Matrix multiplication is not commutative meaning if A and B are matrixs and

$$A \not = B$$ $$ B \not = A^{-1}$$

then

$$
  AB \not = BA 
$$

Vectors are a special case of matrixs where there is a $1 \times n$ matrix.

$$
  \vec{v} = \begin{bmatrix} 
    x \\ 
    y \\ 
    \vdots \\
    n
    \end{bmatrix} 
$$


# Space

In 3D rendering we have two spaces we worry about and that is world space (Where our objects live) and screen space (Where we want them to be)

<p align = "center">
  <img width="526" height="571" alt="image"  src="https://github.com/user-attachments/assets/94ad4396-96a9-4901-95b7-9b660e4ed31b" />
</p>


# Object Files
An object file identitfied by the `.obj` extension on files. 
Is a file format used for 3D objects. 



# The Projection Matrix

The projection matrix is a transformation matrix that 
<p align = "center">
  <img width="722" height="522" alt="image" src="https://github.com/user-attachments/assets/62c58ecd-8b50-45c1-8945-48648f8ac34b" />
</p>
Let $\theta = \text{Field of View}$

Let $a = \text{aspect ratio} = width / height$

Let $f = tan^{-1}(\theta / 2)$ 

$$ 
\begin{bmatrix} 
  \frac{f}{a} & 0 & 0 & 0\\
  0 & f & 0 & 0 \\
  0 & 0 & -\frac{-z_{far} - z_{near}}{z_{far} - z_{near}} & -1 \\
  0 & 0 & -2\cdot \frac{z_{near} \cdot z_{far}}{z_{far} - z_{near}} & 0 \\
\end{bmatrix}
$$

Using the `cube.obj` file we should be able to produce the front of a cube through using the projected points of each vertex and then drawing it in order of the faces for each triangle (This is also known as the winding order)
<p align = "center">
  <img width="796" height="632" alt="image" src="https://github.com/user-attachments/assets/5e651f9a-77ba-4e46-b323-838e3b3217dd" />
</p>
