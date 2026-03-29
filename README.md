# What is a cpu renderer 
A CPU renderer is a primitive style of renderer mostly used to show off how a renderer works.

# Pre requisites 
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

Matrix multiplication is not commutative meaning if A and B are matrixs and $A \not = B$ and $B \not = A^{-1}$ then

$$
  AB \not = BA 
$$

Vectors are a special case of matrixs where there is one colomn and $n$ many rows.

$$
  \vec{v} = \begin{bmatrix} 
    a \\ 
    b \\ 
    \vdots
    \end{bmatrix} 
$$


# Space

In 3D rendering we have two spaces we worry about and that is world space (Where our objects live) and screen space (Where we want them to be)

<p align = "center">
  <img width="526" height="571" alt="image"  src="https://github.com/user-attachments/assets/94ad4396-96a9-4901-95b7-9b660e4ed31b" />
</p>




# The Projection Matrix

The projection matrix is a transformation matrix that 
<p align = "center">
  <img width="361" height="261" alt="image" src="https://github.com/user-attachments/assets/62c58ecd-8b50-45c1-8945-48648f8ac34b" />
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
